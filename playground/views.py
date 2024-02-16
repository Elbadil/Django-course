from django.shortcuts import render
from django.http import HttpResponse

# HTTPRespo
def say_hello_http(request):
    """"""
    return HttpResponse('Hello From Http Response')

# Rendering a template
def say_hello_html(request):
    """"""
    return render(request, 'hello.html', { 'name': 'Adel' })
