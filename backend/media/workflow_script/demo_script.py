from apps.ticket.models import TicketRecord
from service.ticket.ticket_base_service import ticket_base_service_ins

"""
1.因为使用execfile/exec执行脚本，脚本中会跟随celery的执行环境
2.ticket_id和action_from参数会通过调用的时候传递过来，可以直接使用.可以使用ticket_id获取ticket相关的信息
3.因为使用execfile/exec执行脚本, 不得使用if __name__ == '__main__'
4.本脚本场景为服务器权限申请，工单中有自定义字段:host_ip
"""


def demo_script_call():
    # 获取工单信息ip地址信息
    username, msg = ticket_base_service_ins.get_ticket_field_value(ticket_id, 'creator')  # ticket_id会通过exec传过来
    # 你也可以获取工单的其他字段信息，包括自定义字段的值。根据获取的值做后续处理
    print(username)
    return True, ''


demo_script_call()