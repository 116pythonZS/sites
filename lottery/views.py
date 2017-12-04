from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import Http404,HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic

# Create your views here.
from . import tiantian


def index(request):
	datas_numcounter = tiantian.statisticsresult3()
	return render(request, template_name="lottery/index.html", context={"datas_numcounter": datas_numcounter})

