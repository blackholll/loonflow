import logging
import time
import traceback

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, QuerySet

from apps.account.models import Dept, UserDept, User, DeptApprover, Tenant
from apps.loon_base_model import SnowflakeIDGenerator
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins
from service.util.tree_service import tree_service_ins

logger = logging.getLogger("django")

class AccountDeptService(BaseService):
    """
    account department related service
    """

    def __init__(self):
        pass

    @classmethod
    def get_dept_sub_dept_id_list(cls, dept_id: int) -> list:
        """
        get department's all subordinate department
        :param dept_id:
        :return:
        """
        dept_id_list = []
        dept_obj = Dept.objects.get(id=dept_id)
        dept_id_list.append(dept_obj.id)

        def iter_dept_id_list(new_dept_id):
            new_dept_obj = Dept.objects.filter(id=new_dept_id).first()
            if new_dept_obj:
                sub_dept_queryset = Dept.objects.filter(parent_dept_id=new_dept_obj.id).all()
                for sub_dept in sub_dept_queryset:
                    if sub_dept:
                        dept_id_list.append(sub_dept.id)
                        iter_dept_id_list(sub_dept.id)

        iter_dept_id_list(dept_id)
        return dept_id_list

    @classmethod
    def get_dept_user_id_list(cls, dept_id: int) -> list:
        """
        get dept's all user id list, include sub dept's user
        :param dept_id:
        :return:
        """
        all_dept_id_list = [dept_id] + cls.get_dept_sub_dept_id_list()
        from apps.account.models import UserDept
        user_dept_queryset = UserDept.objects.filter(dept_id__in=all_dept_id_list)
        user_id_list = list(set([user_dept.user_id for user_dept in user_dept_queryset]))
        return user_id_list


    @classmethod
    @auto_log
    def get_dept_username_list(cls, dept_id: object) -> tuple:
        """
        get department's all username list
        :param dept_id: int or str
        :return:
        """
        if type(dept_id) == str:
            dept_id_str_list = dept_id.split(',')  # 用于支持多部门
            dept_id_list = [int(dept_id_str) for dept_id_str in dept_id_str_list]
        else:
            dept_id_list = [dept_id]

        sub_dept_id_list_total = []

        for dept_id in dept_id_list:
            flag, sub_dept_id_list = cls.get_dept_sub_dept_id_list(dept_id)
            if flag is False:
                return False, sub_dept_id_list
            sub_dept_id_list_total = sub_dept_id_list_total + sub_dept_id_list

        user_dept_queryset = UserDept.objects.filter(dept_id__in=sub_dept_id_list_total).all()
        user_id_list = [user_dept.user_id for user_dept in user_dept_queryset]

        user_queryset = User.objects.filter(id__in=user_id_list).all()
        user_name_list = [user.username for user in user_queryset]

        return True, user_name_list

    @classmethod
    @auto_log
    def get_dept_by_id(cls, dept_id: int) -> tuple:
        """
        get department's info by dept_id
        :param dept_id:
        :return:
        """
        return True, Dept.objects.filter(id=dept_id).first()

    @classmethod
    def get_dept_detail_by_id(cls, dept_id: str) -> dict:
        """
        get dept detail for api
        :param dept_id:
        :return:
        """
        try:
            dept_obj = Dept.objects.get(id=dept_id)
        except Dept.DoesNotExist as e:
            raise CustomCommonException("dept is not exist")
        except Exception:
            raise
        result = dept_obj.get_dict()
        return result

    @classmethod
    @auto_log
    def get_dept_by_ids(cls, dept_ids: str) -> tuple:
        """
        get department's queryset by dept_ids
        :param dept_ids:
        :return:
        """
        if dept_ids:
            dept_id_list = dept_ids.split(',')
        return True, Dept.objects.filter(id__in=dept_id_list, is_deleted=False).all()

    @classmethod
    @auto_log
    def get_dept_list(cls, search_value: str, page: int = 1, per_page: int = 10, simple=False) -> tuple:
        """
        get dept restful list by search params
        :param search_value: department name or department description Support fuzzy queries
        :param page:
        :param per_page:
        :param simple: 只返回部分数据
        :return:
        """
        query_params = Q(is_deleted=False)
        if search_value:
            query_params &= Q(name__contains=search_value) | Q(label__contains=search_value)
        dept_objects = Dept.objects.filter(query_params)
        paginator = Paginator(dept_objects, per_page)
        try:
            dept_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            dept_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            dept_result_paginator = paginator.page(paginator.num_pages)
        dept_result_object_list = dept_result_paginator.object_list
        dept_result_object_format_list = []
        for dept_result_object in dept_result_object_list:
            result_dict = dept_result_object.get_dict()
            if simple:
                simple_result_dict = dict()
                simple_result_dict['id'] = result_dict['id']
                simple_result_dict['name'] = result_dict['name']
                simple_result_dict['parent_dept_info'] = result_dict['parent_dept_info']
            dept_result_object_format_list.append(result_dict)
        return True, dict(dept_result_object_format_list=dept_result_object_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    def add_dept(cls, name: str, parent_dept_id: str, leader_id: str, approver_id_list: list,
                 creator_id: str, tenant_id: str, label: dict={}) -> int:
        """
        add department record
        :param name:
        :param parent_dept_id:
        :param leader_id:
        :param approver_id_list:
        :param label:
        :param creator_id:
        :param tenant_id:
        :return:
        """
        if not parent_dept_id:
            parent_dept_id = '00000000-0000-0000-0000-000000000000'
        dept_obj = Dept(name=name, parent_dept_id=parent_dept_id, leader_id=leader_id, label=label,
                        creator_id=creator_id, tenant_id=tenant_id)
        dept_obj.save()
        dept_approver_list = []
        for approver_id in approver_id_list:
            dept_approver_list.append(
                DeptApprover(dept_id=dept_obj.id, user_id=approver_id,
                             tenant_id=tenant_id))

        if dept_approver_list:
            DeptApprover.objects.bulk_create(dept_approver_list)
        return str(dept_obj.id)

    @classmethod
    @auto_log
    def update_dept(cls, tenant_id:str, dept_id: str, name: str, parent_dept_id: str, leader_id: str, approver_id_list: list,
                    label: dict) -> bool:
        """
        update department record
        :param dept_id:
        :param name:
        :param parent_dept_id:
        :param leader_id:
        :param approver_id_list:
        :param label:
        :return:
        """
        dept_queryset = Dept.objects.filter(id=dept_id, tenant_id=tenant_id).all()
        if not dept_queryset:
            raise CustomCommonException("dept is not existed or has been deleted")

        dept_queryset.update(name=name, parent_dept_id=parent_dept_id, leader_id=leader_id, label=label)
        dept_approver_queryset = DeptApprover.objects.filter(dept_id=dept_id)
        existed_approver_id_list = [dept_approver.user_id for dept_approver in dept_approver_queryset]
        need_del_approver_id_list = [existed_approver_id for existed_approver_id in existed_approver_id_list if
                                     existed_approver_id not in approver_id_list]
        need_add_approver_id_list = [approver_id for approver_id in approver_id_list if
                                     approver_id not in existed_approver_id_list]
        add_record = []
        for need_add_approver_id in need_add_approver_id_list:
            add_record.append(DeptApprover(dept_id=dept_id, user_id=need_add_approver_id, id=SnowflakeIDGenerator()()))
            time.sleep(0.001)  # temporary action for  SnowflakeIDGenerator concurrence bug
        DeptApprover.objects.bulk_create(add_record)
        if need_del_approver_id_list:
            DeptApprover.objects.filter(dept_id=dept_id, user_id__in=need_del_approver_id_list).delete()
        return True


    @classmethod
    @auto_log
    def update_dept_parent_dept(cls, tenant_id:str, dept_id: str, parent_dept_id: str) -> bool:
        """
        update department's parent_dept_id
        :param tenant_id:
        :param dept_id:
        :param parent_dept_id:
        :return:
        """
        dept_queryset = Dept.objects.filter(id=dept_id, tenant_id=tenant_id).all()
        if not dept_queryset:
            raise CustomCommonException("dept is not existed or has been deleted")
        if not parent_dept_id:
            parent_dept_id = '00000000-0000-0000-0000-000000000000'
        dept_queryset.update(parent_dept_id=parent_dept_id)
        return True


    @classmethod
    @auto_log
    def delete_dept(cls, dept_id: int, operator_id: int) -> bool:
        """
        delete department record
        :param dept_id:
        :param operator_id:
        :return:
        """
        try:
            dept_obj = Dept.objects.get(id=dept_id)
        except Dept.DoesNotExist as e:
            raise CustomCommonException("dept is not exist")
        except Exception:
            raise
        if dept_obj:
            archive_service_ins.archive_record("Dept", dept_obj, operator_id)
            dept_approver_queryset = DeptApprover.objects.filter(dept_id=dept_id)
            if dept_approver_queryset:
                archive_service_ins.archive_record_list("DeptApprover", dept_approver_queryset, operator_id)
        return True

    @classmethod
    @auto_log
    def batch_delete_dept(cls, dept_id_list: list, operator_id: int) -> bool:
        """
        batch delete dept record
        :param dept_id_list:
        :param operator_id:
        :return:
        """
        dept_queryset = Dept.objects.filter(id__in=dept_id_list).all()
        if dept_queryset:
            archive_service_ins.archive_record_list("Dept", dept_queryset, operator_id)
            dept_approver_queryset = DeptApprover.objects.filter(dept_id__in=dept_id_list)
            if dept_approver_queryset:
                archive_service_ins.archive_record_list("DeptApprover", dept_approver_queryset, operator_id)
        return True

    @classmethod
    def get_dept_tree(cls, tenant_id: str) -> list:
        """
        get department tree, it's difficult to use mui tree view for lazy loading, so just return all dept info here
        :param tenant_id:
        :param is_simple:
        :return:
        """
        query_params = Q(tenant_id=tenant_id)
        raw_dept_queryset = Dept.objects.filter(query_params)

        dept_link_list = cls.get_dept_link_list(raw_dept_queryset)
        dept_id_tree = tree_service_ins.build_tree_from_lists(dept_link_list)
        dept_id_list = tree_service_ins.get_value_list_from_tree(dept_id_tree)

        dept_leader_id_list = []
        dept_approver_id_list = []
        dept_approver_map = dict()
        dept_info_map = dict()
        
        related_dept_queryset = Dept.objects.filter(id__in=dept_id_list)
        for dept_obj in related_dept_queryset:
            dept_id_list.append(dept_obj.id)
            dept_leader_id_list.append(dept_obj.leader_id)

            dept_info = dict(id=str(dept_obj.id), name=dept_obj.name)
            dept_info_map[str(dept_obj.id)] = dept_info

        related_user_id_list = dept_leader_id_list + dept_approver_id_list
        related_user_id_list = list(set(related_user_id_list))
        

        has_child_dept_id_list = []
        has_parent_query_params = ~Q(parent_dept_id='00000000-0000-0000-0000-000000000000') & Q(tenant_id=tenant_id) & Q(parent_dept_id__in=dept_id_list)
        parent_queryset = Dept.objects.filter(has_parent_query_params)
        for parent_obj in parent_queryset:
            has_child_dept_id_list.append(str(parent_obj.parent_dept_id))

        flag, all_leaf_node_value_list = tree_service_ins.get_leaf_value_list_from_tree(dept_id_tree)
        return cls.get_tree_list_from_tree_and_other(dept_id_tree, dept_info_map, has_child_dept_id_list,
                                                     all_leaf_node_value_list, tenant_id)

    @classmethod
    def get_tree_list_from_tree_and_other(cls, tree_node, dept_info_map: dict,
                                          has_child_dept_id_list: list, all_leaf_node_value_list: list, tenant_id: str) -> list:
        """
        get tree list from treenode
        :param tree_node:
        :param user_map:
        :param dept_info_map:
        :param has_child_dept_id_list:
        :param all_leaf_node_value_list:
        :return:
        """

        result_list = []
        # if tree_node and tree_node.value:
        if tree_node:
            # 跳过默认UUID值的节点
            if tree_node.value and str(tree_node.value) == '00000000-0000-0000-0000-000000000000':
                # 直接处理子节点
                for child in tree_node.children:
                    child_result = cls.get_tree_list_from_tree_and_other(child, dept_info_map,
                                                                      has_child_dept_id_list,
                                                                      all_leaf_node_value_list,
                                                                      tenant_id)
                    result_list.extend(child_result)
                return result_list
                
            current_info = dict()
            if tree_node.value:
                dept_info = dept_info_map.get(tree_node.value, {})
                if dept_info:
                    # 确保id是字符串类型
                    if 'id' in dept_info and dept_info['id'] is not None:
                        dept_info['id'] = str(dept_info['id'])
                    current_info.update(dept_info)
                else:
                    # 如果dept_info为空，设置默认值，确保id是字符串类型
                    current_info.update(dict(id=str(tree_node.value), name=""))
            else:
                tenant_obj = Tenant.objects.get(id=tenant_id)

                current_info.update(dict(id="00000000-0000-0000-0000-000000000000", name=tenant_obj.name))
            # 确保all_leaf_node_value_list和has_child_dept_id_list不为None
            leaf_node_list = all_leaf_node_value_list or []
            child_dept_list = has_child_dept_id_list or []
            current_info["children"] = []
            for child in tree_node.children:
                # 确保子节点的值是字符串类型，以便在dept_info_map中正确查找
                if child.value is not None:
                    if not isinstance(child.value, str):
                        child.value = str(child.value)
                    if child.value not in dept_info_map:
                        try:
                            dept_obj = Dept.objects.get(id=child.value)
                            if is_simple:
                                dept_info = dict(id=str(dept_obj.id), name=dept_obj.name)
                            else:
                                dept_info = dict(id=str(dept_obj.id), name=dept_obj.name, leader_id=str(dept_obj.leader_id) if dept_obj.leader_id else None)
                            dept_info_map[child.value] = dept_info
                        except Exception as e:
                            pass
                child_result = cls.get_tree_list_from_tree_and_other(child, dept_info_map,
                                                                   has_child_dept_id_list,
                                                                   all_leaf_node_value_list,
                                                                   tenant_id)
                current_info["children"] = current_info["children"] + child_result
            result_list.append(current_info)
        return result_list

    @classmethod
    def get_dept_link_list(cls, department_queryset: QuerySet):
        """
        get department link list. [['1','2','3'], ['1','2','4'], ['1','4','7'], ['1','4','8']]
        :param department_queryset:
        :return:
        """
        result_list = []
        for department_obj in department_queryset:
            current_list = []
            current_list.append(str(department_obj.id))
            current_dept = department_obj
            while current_dept.parent_dept_id and current_dept.parent_dept_id != '00000000-0000-0000-0000-000000000000':
                try:
                    current_list.append(str(current_dept.parent_dept_id))
                    current_dept = Dept.objects.get(id=current_dept.parent_dept_id)
                except Dept.DoesNotExist:
                    break
            # 过滤掉默认UUID值
            # current_list = [str(dept_id) for dept_id in current_list if str(dept_id) != '00000000-0000-0000-0000-000000000000']
            current_list.reverse()
            if current_list:
                result_list.append(current_list)

        return result_list

    @classmethod
    def get_dept_path_list(cls, tenant_id: str, search_value:str) -> list:
        """
        get department path list, eg. [{'id':1, 'path':'技术部-基础设施部'}]
        :param search_value: department name
        :return: list of dict with dept id and full path
        """
        result_list = []
        # 获取所有匹配的部门
        department_queryset = Dept.objects.filter(name__contains=search_value, tenant_id=tenant_id).all()
        
        # 收集所有需要查询的部门ID
        dept_ids = set()
        for dept in department_queryset:
            dept_ids.add(dept.id)
            current_dept = dept
            while current_dept and current_dept.parent_dept_id != '00000000-0000-0000-0000-000000000000':
                dept_ids.add(current_dept.parent_dept_id)
                current_dept = Dept.objects.filter(id=current_dept.parent_dept_id).first()
        
        # 一次性查询所有需要的部门信息
        dept_map = {str(dept.id): dept for dept in Dept.objects.filter(id__in=dept_ids).all()}
        
        for dept in department_queryset:
            path_list = []
            current_dept = dept
            
            # 获取所有父部门
            while current_dept:
                path_list.append(current_dept.name)
                if current_dept.parent_dept_id == '00000000-0000-0000-0000-000000000000':
                    break
                current_dept = dept_map.get(str(current_dept.parent_dept_id))
            
            # 反转路径顺序并构建字符串
            path_list.reverse()
            path_str = '-'.join(path_list)
            
            result_list.append({
                'id': str(dept.id),
                'path': path_str,
                'name': dept.name
            })
            
        return result_list
        

    @classmethod
    def get_dept_path(cls, tenant_id: str, dept_id:str)->dict:
        """
        get department path, eg. {'id':1, 'path':'技术部-基础设施部'}
        :param dept_id: department id
        """
        department_obj = Dept.objects.filter(id=dept_id, tenant_id=tenant_id).first()
        
        dept_ids = []
        current_dept = department_obj
        dept_ids.append(str(department_obj.id))
        while current_dept and current_dept.parent_dept_id != '00000000-0000-0000-0000-000000000000':
            dept_ids.append(str(current_dept.parent_dept_id))
            current_dept = Dept.objects.filter(id=current_dept.parent_dept_id).first()

        
        dept_map = {str(dept.id): dept for dept in Dept.objects.filter(id__in=dept_ids).all()}
        path_list = []
        for dept_id in dept_ids:
            if dept_id != '00000000-0000-0000-0000-000000000000':
                path_list.append(dept_map[dept_id].name)
        path_list.reverse()
        path_str = '-'.join(path_list)
        result = {
            'id': dept_id,
            'path': path_str,
            'name': department_obj.name
        }
        return result
        
    @classmethod
    def get_query_tree(cls, department_queryset: QuerySet):
        """
        get query result tree
        :param department_queryset:
        :return:
        """
        #
        # root = DepartmentTreeNode(0)
        # all_list = []
        # for department_obj in department_queryset:

    @classmethod
    def get_department_full_path(cls, department: Dept):
        pass

    def get_root_department(cls, department: Dept) -> tuple:
        """
        get root department
        :param department:
        :return:
        """
        if department.parent_dept_id != 0:
            return cls.get_root_department(department.parent_dept)
        else:
            return True, department


class DepartmentTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


class DepartmentLinkNode:
    def __init__(self, value):
        self.value = value
        self.next = None


account_dept_service_ins = AccountDeptService()
