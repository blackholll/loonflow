from django.urls import path
from apps.ticket.views import TicketListView, TicketView, TicketTransition, TicketFlowlog, TicketFlowStep, TicketState, \
    TicketsStates, TicketAccept, TicketDeliver, TicketAddNode, \
    TicketAddNodeEnd, TicketField, TicketScriptRetry, TicketComment, TicketHookCallBack, TicketParticipantInfo, \
    TicketClose, TicketsNumStatistics, TicketRetreat, UploadFile

urlpatterns = [
    path('', TicketListView.as_view()),
    path('/<int:ticket_id>', TicketView.as_view()),
    path('/<int:ticket_id>/transitions', TicketTransition.as_view()),
    path('/<int:ticket_id>/flowlogs', TicketFlowlog.as_view()),
    path('/<int:ticket_id>/flowsteps', TicketFlowStep.as_view()),
    path('/<int:ticket_id>/state', TicketState.as_view()),
    path('/<int:ticket_id>/fields', TicketField.as_view()),
    path('/<int:ticket_id>/accept', TicketAccept.as_view()),
    path('/<int:ticket_id>/deliver', TicketDeliver.as_view()),
    path('/<int:ticket_id>/add_node', TicketAddNode.as_view()),
    path('/<int:ticket_id>/add_node_end', TicketAddNodeEnd.as_view()),
    path('/<int:ticket_id>/retry_script', TicketScriptRetry.as_view()),
    path('/<int:ticket_id>/comments', TicketComment.as_view()),
    path('/<int:ticket_id>/hook_call_back', TicketHookCallBack.as_view()),
    path('/<int:ticket_id>/participant_info', TicketParticipantInfo.as_view()),
    path('/<int:ticket_id>/close', TicketClose.as_view()),
    path('/<int:ticket_id>/retreat', TicketRetreat.as_view()),
    path('/states', TicketsStates.as_view()),  # 批量获取工单状态
    path('/num_statistics', TicketsNumStatistics.as_view()),  # 批量获取工单状态
    path('/upload_file', UploadFile.as_view()),  # 批量获取工单状态

]
