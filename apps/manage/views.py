from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """
    总览
    :param request:
    :return:
    """
    return HttpResponse("This is loonflow's api server, please view frontend page, reference: http://loonflow.readthedocs.io/")



