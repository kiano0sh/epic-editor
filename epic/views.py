from django.shortcuts import render
from django.views.generic import TemplateView


class LoggedIn(TemplateView):
    template_name = 'accounts/logged_in.html'


class LoggedOut(TemplateView):
    template_name = 'accounts/logged_out.html'


def index(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'main/index.html', context=context)
