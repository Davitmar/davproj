from django.shortcuts import render
from django.http import HttpResponse
from main.models import University, Country

def index(request):
    s=''
    u=University.objects.all()
    for i in u:
        s+=f'<p>{str(i)}</p>'
    return HttpResponse(s)

def first(request):
    #try:
    if 'rank' in request.GET:
        r = request.GET['rank']
        u = University.objects.filter(rank=r)[0]
        return HttpResponse(f'<p>{str(u)}</p>')
#except:
    s=''
    u = University.objects.all()[:30]
    for i in u:
        s += f'<p>{str(i)}</p>'
    return HttpResponse(s)
