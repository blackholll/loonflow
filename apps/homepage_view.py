from django.http import HttpResponse
from django.views import View


class HomepageView(View):
    def get(self, request, *args, **kwargs):
        """
        Front page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return HttpResponse('<div>Welcome to loonflow<br><a href="/manage">management background</a><br><a href="/admin">django management background</a><br><a href="https://github.com/blackholll/loonflow">Working with documentation</a></div>')