from apps.ticket.models import CustomField as TicketCustomField
from service.account.account_base_service import account_base_service_ins
from service.account.account_user_service import account_user_service_ins
from service.workflow.workflow_base_service import workflow_base_service_ins
from service.base_service import BaseService
from service.workflow.workflow_component_service import workflow_component_service_ins
from apps.ticket.models import Record as TicketRecord


class TicketFieldService(BaseService):
    """
    ticket field service
    """
    @classmethod
    def get_field_value_column(cls, field_type: str) -> str:
        """
        get what the column about field's value should save to
        :param field_type:
        :return:
        """
        if field_type in ["text", "select", "cascade", "user", "department", "field", "radio", "checkbox"]:
            return "common_value"
        elif field_type == "number":
            return "number_value"
        elif field_type == "date":
            return "date_value"
        elif field_type == "datetime":
            return "datetime_value"
        elif field_type == "time":
            return "time_value"
        elif field_type in ["rich_text", "textarea"]:
            return "rich_text_value"
    
    @classmethod
    def get_ticket_all_field_value(cls, tenant_id: str, ticket_id: str) -> dict:
        """
        get ticket all field value
        :param tenant_id:
        :param ticket_id:
        :return:
        """
        ticket_obj_queryset = TicketCustomField.objects.filter(ticket_id=ticket_id, tenant_id=tenant_id).all()
        result_dict = {}
        for ticket_custom_field in ticket_obj_queryset:
            if ticket_custom_field.field_type in ("text", "select", "cascade", "user", "department", "file"):
                result_dict[ticket_custom_field.field_key] = ticket_custom_field.common_value
            elif ticket_custom_field.field_type == "number":
                result_dict[ticket_custom_field.field_key] = ticket_custom_field.number_value
            elif ticket_custom_field.field_type == "date":
                result_dict[ticket_custom_field.field_key] = ticket_custom_field.date_value
            elif ticket_custom_field.field_type == "datetime":
                result_dict[ticket_custom_field.field_key] = ticket_custom_field.datetime_value
            elif ticket_custom_field.field_type == "time":
                result_dict[ticket_custom_field.field_key] = ticket_custom_field.time_value
            elif ticket_custom_field.field_type in ["rich_text", "textarea"]:
                result_dict[ticket_custom_field.field_key] = ticket_custom_field.rich_text_value
            else:
                result_dict[ticket_custom_field.field_key] = ticket_custom_field.common_value
        basic_info_dict = cls.get_ticket_basic_field_value(tenant_id, ticket_id)
        result_dict.update(basic_info_dict)
        return result_dict


    @classmethod
    def get_ticket_basic_field_value(cls, tenant_id: str, ticket_id: str) -> dict:
        """
        get ticket basic field value
        :param tenant_id:
        :param ticket_id:
        :return:
        """
        result_dict = {}
        ticket_obj = TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)
        result_dict['title'] = ticket_obj.title
        result_dict['act_state'] = ticket_obj.act_state
        result_dict['parent_ticket_id'] = ticket_obj.parent_ticket_id
        result_dict['parent_ticket_node_id'] = ticket_obj.parent_ticket_node_id
        result_dict['workflow_id'] = str(ticket_obj.workflow_id)
        result_dict['workflow_version_id'] = str(ticket_obj.workflow_version_id)
        result_dict['creator_id'] = str(ticket_obj.creator_id)
        result_dict['created_at'] = ticket_obj.created_at
        # add creator_info
        creator_info = account_user_service_ins.get_user_by_user_id(tenant_id, ticket_obj.creator_id)
        result_dict['creator_info'] = dict(
            id = str(creator_info.id),
            name = creator_info.name,
            alias = creator_info.alias if creator_info.alias else '',
            email = creator_info.email if creator_info.email else '',
            phone = creator_info.phone if creator_info.phone else '',
        )
        #add workflow_info
        workflow_info =workflow_base_service_ins.get_workflow_info_by_id_and_version_id(tenant_id, ticket_obj.workflow_id, ticket_obj.workflow_version_id)
        result_dict['workflow_info'] = dict(
            id = workflow_info.get('workflow_id'),
            name = workflow_info.get('name'),
            description = workflow_info.get('description'),
        )
        
        return result_dict

    @classmethod
    def get_ticket_field_value(cls, tenant_id: str, ticket_id: str, field_key: str):
        """
        get ticket custom field queryset
        :param tenant_id:
        :param ticket_id:
        :return:
        """
        result_dict = {}
        ticket_custom_field_obj = TicketCustomField.objects.get(ticket_id=ticket_id, tenant_id=tenant_id, field_key=field_key)
        if ticket_custom_field_obj.field_type in ("text", "select", "cascade", "user", "file"):
                result_dict[ticket_custom_field_obj.field_key] = ticket_custom_field_obj.common_value
        elif ticket_custom_field_obj.field_type == "number":
            result_dict[ticket_custom_field_obj.field_key] = ticket_custom_field_obj.number_value
        elif ticket_custom_field_obj.field_type == "date":
            result_dict[ticket_custom_field_obj.field_key] = ticket_custom_field_obj.date_value
        elif ticket_custom_field_obj.field_type == "rich_text":
            result_dict[ticket_custom_field_obj.field_key] = ticket_custom_field_obj.rich_text_value
        else:
            result_dict[ticket_custom_field_obj.field_key] = ticket_custom_field_obj.common_value
            
        return result_dict[field_key]

    @classmethod
    def update_ticket_fields(cls, tenant_id: str, ticket_id:str, operator_id: str, workflow_id: str, version_id: str, field_info_dict: dict) -> bool:
        """
        add ticket custom field record
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param workflow_id:
        :param version_id:
        :param field_info_dict:
        :return:
        """
        for field_key, field_value in field_info_dict.items():
            if field_key == 'title':
                TicketRecord.objects.filter(id=ticket_id, tenant_id=tenant_id).update(title=field_value)


        workflow_custom_field_queryset = workflow_component_service_ins.get_workflow_custom_fields(tenant_id, workflow_id, version_id)
        field_key_type_dict = {}
        for workflow_custom_field in workflow_custom_field_queryset:
            field_key_type_dict[workflow_custom_field['component_key']] = workflow_custom_field['type']
        
        need_update_field_value_list, need_add_field_value_list = [], []
        ticket_custom_field_queryset = TicketCustomField.objects.filter(ticket_id=ticket_id, tenant_id=tenant_id).all()
        exist_field_key_list = [ticket_custom_field.field_key for ticket_custom_field in ticket_custom_field_queryset]
        for field_key in field_info_dict.keys():
            if field_key in exist_field_key_list:
                if type(field_info_dict.get(field_key)) == list:
                    need_update_field_value_list.append({field_key: ','.join(field_info_dict.get(field_key))})
                else:
                    need_update_field_value_list.append({field_key: field_info_dict.get(field_key)})
            else:
                if type(field_info_dict.get(field_key)) == list:
                    need_add_field_value_list.append({field_key: ','.join(field_info_dict.get(field_key))})
                else:
                    need_add_field_value_list.append({field_key: field_info_dict.get(field_key)})


        for need_update_field_value in need_update_field_value_list:
            field_key = list(need_update_field_value.keys())[0]
            field_value_column = cls.get_field_value_column(field_key_type_dict.get(field_key))
            TicketCustomField.objects.filter(ticket_id=ticket_id, tenant_id=tenant_id, field_key=field_key).update(**{field_value_column: need_update_field_value[field_key]})

        for need_add_field_value in need_add_field_value_list:
            field_key = list(need_add_field_value.keys())[0]
            field_value_column = cls.get_field_value_column(field_key_type_dict.get(field_key))
            if field_value_column:
                TicketCustomField.objects.create(ticket_id=ticket_id, tenant_id=tenant_id, field_key=field_key, 
                                                field_type=field_key_type_dict.get(field_key), **{field_value_column: need_add_field_value[field_key]})
        return True


ticket_field_service_ins = TicketFieldService()
