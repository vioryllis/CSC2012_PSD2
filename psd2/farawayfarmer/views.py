from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def plants(request):
    template = loader.get_template("selection.html")
    context = {
        "testList": ["test1", "test2", "test3"],
    }
    return HttpResponse(template.render(context, request))