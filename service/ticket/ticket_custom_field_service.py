from apps.loon_base_model import SnowflakeIDGenerator
from apps.ticket.models import TicketCustomField
from service.base_service import BaseService
from service.workflow.workflow_custom_field_service import workflow_custom_field_service_ins


class TicketCustomFieldService(BaseService):
    """
    ticket custom field service
    """
    def get_field_value_column(self, field_type: str) -> str:
        """
        get what the column about field's value should save to
        :param field_type:
        :return:
        """
        if field_type in ["text", "select", "cascade", "user", "field"]:
            return "common_value"
        elif field_type == "number":
            return "number_value"
        elif field_type == "date":
            return "date_value"
        elif field_type == "datetime":
            return "datetime_value"
        elif field_type == "time":
            return "time_value"
        elif field_type == "rich_text":
            return "rich_text_value"

    @classmethod
    def add_record(cls, tenant_id: int, operator_id: int, workflow_id: int, field_info_dict: dict) -> bool:
        """
        add ticket custom field record
        :param tenant_id:
        :param operator_id:
        :param workflow_id:
        :param field_info_dict:
        :return:
        """
        workflow_custom_field_queryset = workflow_custom_field_service_ins.get_workflow_custom_field(workflow_id)
        custom_field_dict = {}
        for workflow_custom_field in workflow_custom_field_queryset:
            custom_field_dict[workflow_custom_field.field_key] = workflow_custom_field.field_type
        record_list = []
        for field_key, field_value in field_info_dict:
            field_value_column = cls.get_field_value_column(custom_field_dict.get(field_key))
            record_list.append(TicketCustomField(id=SnowflakeIDGenerator()(), tenant_id=tenant_id, creator_id=operator_id,
                                                 **{field_value_column: field_value}))
            import time
            time.sleep(0.001)  # SnowflakeIDGenerator has bug will, just workaround provisionally
        TicketCustomField.objects.bulk_create(record_list)
        return True


ticket_custom_field_service_ins = TicketCustomFieldService()
