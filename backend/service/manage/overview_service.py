from service.base_service import BaseService


class OverviewService(BaseService):
    """
    总览
    """
    def __init__(self):
        pass

    def get_new_ticket_type_count_statistics_info(self, start_time: str, end_time: str)->tuple:
        """
        获取每种类型工单创建数量统计数据
        :return:
        """
        return '', ''
