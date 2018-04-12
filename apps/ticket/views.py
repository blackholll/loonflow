from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class TicketListView(View):
    def get(self, request, *args, **kwargs):

        return HttpResponse('haahha')

    def post(self, request, *args, **kwargs):
        return HttpResponse('post')

def ticketlist(response):
    if response.method == 'POST':
        return HttpResponse('postssss')