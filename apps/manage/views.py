from django.http import HttpResponse


def index(request):
    """
    总览
    :param request:
    :return:
    """
    return HttpResponse("This is loonflow's api server, please view frontend page, reference: http://loonflow.readthedocs.io/")



