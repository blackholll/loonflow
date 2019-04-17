"""
loonflow在调用通知脚本时会将工单一些属性通过全局变量的方式传进来，所以在此脚本中可以直接使用。变量如下
globals = {'title_result': title_result, 'content_result': content_result,
                   'participant': ticket_obj.participant, 'participant_type_id': ticket_obj.participant_type_id,
                   'multi_all_person': ticket_obj.multi_all_person, 'ticket_value_info': ticket_value_info,
                   'last_flow_log': last_flow_log, 'participant_info_list': participant_info_list}

"""
import requests


def demo_notice_script_call():
    phone_list = []
    email_list = []
    for participant_info in participant_info_list:
        phone_list.append(participant_info['phone'])
        email_list.append(participant_info['email'])
    # 此处为了演示，同时发送了短信和邮件，实际使用建议分开在不同脚本中发送不同类型的消息
    sms_result = requests.post('http://xxxxx.com/sendsms', {'phone': phone_list, 'context': content_result}) #发送短信，需要你的企业内有提供发送短信的接口，当然你也可以自己实现这个接口的逻辑
    mail_result = requests.post('http://xxxxx.com/sendemail', {'phone': email_list, 'context': content_result,'title': title_result}) #发送邮件，需要你的企业内有提供发送邮件的接口，当然你也可以自己实现这个接口的逻辑
    if sms_result.json().get('code') == 0 and mail_result.json().get('code') == 0:
        return True, ''
    else:
        return False, 'send_sms_result:{}, send_email_result:{}'.format(sms_result.json().get('msg'), mail_result.json().get('msg'))


demo_notice_script_call()
