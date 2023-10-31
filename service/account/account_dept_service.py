import time

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, QuerySet

from apps.account.models import Dept, UserDept, User, DeptApprover, Tenant
from apps.loon_base_model import SnowflakeIDGenerator
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.util.archive_service import archive_service_ins
from service.util.tree_service import tree_service_ins


class AccountDeptService(BaseService):
    """
    account department related service
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_dept_sub_dept_id_list(cls, dept_id: int) -> tuple:
        """
        get department's all subordinate department
        :param dept_id:
        :return:
        """
        dept_id_list = []
        dept_obj = Dept.objects.filter(id=dept_id).first()
        if dept_obj:
            dept_id_list.append(dept_obj.id)
        else:
            return True, []

        def iter_dept_id_list(new_dept_id):
            new_dept_obj = Dept.objects.filter(id=new_dept_id).first()
            if new_dept_obj:
                sub_dept_queryset = Dept.objects.filter(parent_dept_id=new_dept_obj.id).all()
                for sub_dept in sub_dept_queryset:
                    if sub_dept:
                        dept_id_list.append(sub_dept.id)
                        iter_dept_id_list(sub_dept.id)

        iter_dept_id_list(dept_id)
        return True, dept_id_list

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
    @auto_log
    def get_dept_detail_by_id(cls, dept_id: int) -> tuple:
        """
        get dept detail for api
        :param dept_id:
        :return:
        """
        dept_obj = Dept.objects.get(id=dept_id)
        result = dept_obj.get_dict()
        return True, result






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
    @auto_log
    def add_dept(cls, name: str, parent_dept_id: int, leader_id: int, approver_id_list: list, label: str, creator_id: int, tenant_id:int) -> tuple:
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
        dept_obj = Dept(name=name, parent_dept_id=parent_dept_id, leader_id=leader_id, label=label,
                        creator_id=creator_id, tenant_id=tenant_id)
        dept_obj.save()
        dept_approver_list = []
        for approver_id in approver_id_list:
            time.sleep(0.01)  # SnowflakeIDGenerator has bug will, just workaround provisionally
            dept_approver_list.append(DeptApprover(dept_id=dept_obj.id, user_id=approver_id, id=SnowflakeIDGenerator()(), tenant_id=tenant_id))
            SnowflakeIDGenerator().__call__()

        if dept_approver_list:
            DeptApprover.objects.bulk_create(dept_approver_list)
        return True, dict(dept_id=dept_obj.id)

    @classmethod
    @auto_log
    def update_dept(cls, dept_id: int, name: str, parent_dept_id: int, leader_id: int, approver_id_list: list, label: str) -> tuple:
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
        dept_queryset = Dept.objects.filter(id=dept_id)
        if not dept_queryset:
            return False, 'dept is not existed or has been deleted'
        # todo: update dept basic info,update approver info
        dept_queryset.update(name=name, parent_dept_id=parent_dept_id, leader_id=leader_id, label=label)
        dept_approver_queryset = DeptApprover.objects.filter(dept_id=dept_id)
        existed_approver_id_list = [dept_approver.user_id for dept_approver in dept_approver_queryset]
        need_del_approver_id_list = [existed_approver_id for existed_approver_id in existed_approver_id_list if existed_approver_id not in approver_id_list]
        need_add_approver_id_list = [approver_id for approver_id in approver_id_list if approver_id not in existed_approver_id_list]
        add_record = []
        for need_add_approver_id in need_add_approver_id_list:
            add_record.append(DeptApprover(dept_id=dept_id, user_id=need_add_approver_id, id=SnowflakeIDGenerator()()))
            time.sleep(0.001)  # temporary action for  SnowflakeIDGenerator concurrence bug
        DeptApprover.objects.bulk_create(add_record)
        if need_del_approver_id_list:
            DeptApprover.objects.filter(dept_id=dept_id, user_id__in=need_del_approver_id_list).delete()
        return True, ''

    @classmethod
    @auto_log
    def delete_dept(cls, dept_id: int, operator_id: int) -> tuple:
        """
        delete department record
        :param dept_id:
        :param operator_id:
        :return:
        """
        dept_obj = Dept.objects.get(id=dept_id)
        if dept_obj:
            archive_service_ins.archive_record("Dept", dept_obj, operator_id)
            dept_approver_queryset = DeptApprover.objects.filter(dept_id=dept_id)
            if dept_approver_queryset:
                archive_service_ins.archive_record_list("DeptApprover", dept_approver_queryset, operator_id)
        return True, ""

    @classmethod
    @auto_log
    def batch_delete_dept(cls, dept_id_list: list, operator_id: int) -> tuple:
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
        return True, ""





    @classmethod
    @auto_log
    def get_dept_tree(cls, tenant_id: int, search_value: str, parent_dept_id: int, simple: bool) -> tuple:
        """
        get department tree
        :param tenant_id:
        :param search_value:
        :param parent_dept_id:
        :param simple:
        :return:
        """
        query_params = Q()
        query_params &= Q(tenant_id=tenant_id)
        if parent_dept_id:
            query_params &= Q(parent_dept_id=parent_dept_id)
        if search_value:
            query_params &= Q(name__contains=search_value)
        if not (parent_dept_id or search_value):
            # no parent_department_id and search_value ,only return root department
            query_params &= Q(parent_dept_id=0)

        raw_dept_queryset = Dept.objects.filter(query_params)

        flag, dept_link_list = cls.get_dept_link_list(raw_dept_queryset)
        flag, dept_id_tree = tree_service_ins.build_tree_from_lists(dept_link_list)
        flag, dept_id_list = tree_service_ins.get_value_list_from_tree(dept_id_tree)

        dept_leader_id_list = []
        dept_approver_id_list = []
        dept_approver_map = dict()
        dept_info_map = dict()
        related_dept_queryset = Dept.objects.filter(id__in=dept_id_list)

        for dept_obj in related_dept_queryset:
            dept_id_list.append(dept_obj.id)
            dept_leader_id_list.append(dept_obj.leader_id)
            dept_approver_queryset = DeptApprover.objects.filter(dept_id=dept_obj.id).all()
            approver_list = []
            for approver_obj in dept_approver_queryset:
                dept_approver_id_list.append(approver_obj.user_id)
                approver_list.append({"id": approver_obj.user_id})
            dept_approver_map[dept_obj.id] = approver_list

            dept_info = dict(id=dept_obj.id, name=dept_obj.name, leader_id=dept_obj.leader_id,
                             approver_info_list=dept_approver_map.get(dept_obj.id))  # 缺少审批人的详细信息
            dept_info_map[dept_obj.id] = dept_info

        related_user_id_list = dept_leader_id_list + dept_approver_id_list
        related_user_id_list = list(set(related_user_id_list))
        user_map = dict()
        related_user_queryset = User.objects.filter(id__in=related_user_id_list)
        for related_user in related_user_queryset:
            related_user_detail = related_user.get_dict()
            user_map[related_user.id] = dict(id=related_user_detail.get("id"), name=related_user_detail.get("name"),
                                             alias=related_user_detail.get("alias"))

        # related dept id which has children, 将所有parent_id不为0的找出来， 然后将这些数据的parent_id找出来。
        has_child_dept_id_list = []

        parent_query_params = ~Q(parent_dept_id=0) & Q(tenant_id=tenant_id) & Q(parent_dept_id__in=dept_id_list)
        parent_queryset = Dept.objects.filter(parent_query_params)
        for parent_obj in parent_queryset:
            has_child_dept_id_list.append(parent_obj.parent_dept_id)

        flag, all_leaf_node_value_list = tree_service_ins.get_leaf_value_list_from_tree(dept_id_tree)
        return cls.get_tree_list_from_tree_and_other(dept_id_tree, user_map, dept_info_map, has_child_dept_id_list, all_leaf_node_value_list, tenant_id, simple)

    @classmethod
    @auto_log
    def get_tree_list_from_tree_and_other(cls, tree_node, user_map: dict, dept_info_map: dict,
                                          has_child_dept_id_list: list, all_leaf_node_value_list: list, tenant_id:int, simple:bool) -> tuple:
        """
        get tree list from treenode, user info, approver info. if node has leaf node,  it should be expended
        :param tree_node:
        :param user_map:
        :param dept_info_map:
        :param has_child_dept_id_list:
        :param all_leaf_node_value_list:
        :param simple:
        :return:
        """

        result_list = []
        # if tree_node and tree_node.value:
        if tree_node:
            current_info = dict()
            if tree_node.value:
                current_info.update(dept_info_map.get(tree_node.value))
            else:
                #todo: get tenant name
                tenant_obj = Tenant.objects.get(id=tenant_id)

                current_info.update(dict(id=0, name=tenant_obj.name))
            if not simple:
                current_info["leader_info"] = user_map.get(dept_info_map.get(tree_node.value).get("leader_id")) if tree_node.value else {}
                approver_info_list = dept_info_map.get(tree_node.value).get("approver_info_list") if tree_node.value else []

                new_approver_info_list = []
                for approver_info in approver_info_list:
                    new_approver_info = user_map.get(approver_info.get("id"))
                    new_approver_info_list.append(new_approver_info)
                current_info["approver_info_list"] = new_approver_info_list
            else:
                if current_info.get("approver_info_list"):
                    current_info.pop('approver_info_list')
            current_info["need_expend"] = True if tree_node.value not in all_leaf_node_value_list else False
            current_info["has_children"] = True if tree_node.value not in has_child_dept_id_list else False
            current_info["children"] = []


            for child in tree_node.children:
                current_info["children"] = current_info["children"] + cls.get_tree_list_from_tree_and_other(child, user_map, dept_info_map,
                                                                                      has_child_dept_id_list,
                                                                                      all_leaf_node_value_list, tenant_id, simple)[1]

            result_list.append(current_info)
        return True, result_list

    @classmethod
    def get_dept_link_list(cls, department_queryset: QuerySet):
        """
        get department link list. [[1,2,3], [1,2,4], [1,4,7], [1,4,8]]
        :param department_queryset:
        :return:
        """
        result_list = []
        for department_obj in department_queryset:
            current_list = []
            current_list.append(department_obj.id)
            current_dept = department_obj
            while current_dept.parent_dept_id:
                current_list.append(current_dept.parent_dept_id)
                current_dept = Dept.objects.get(id=current_dept.parent_dept_id)
            current_list.reverse()
            result_list.append(current_list)

        return True, result_list



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
    def get_department_full_path(cls, department:Dept):
        pass


    def get_root_department(cls, department:Dept) -> tuple:
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
