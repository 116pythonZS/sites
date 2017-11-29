from django.shortcuts import render, get_object_or_404
from django.http import Http404,HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse


from django.http import HttpResponse

from polls.models import Question, Choice
# Create your views here.

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	template = loader.get_template("polls/index.html")
# 	context = {
# 		"latest_question_list": latest_question_list, }
# 	return HttpResponse(template.render(context, request))
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		"latest_question_list": latest_question_list, }
	return render(request, 'polls/index.html', context)

# def detail(request, question_id):
# 	try:
# 		question = Question.objects.get(pk=question_id)
# 	except Question.DoesNotExist:
# 		raise Http404("Question does not exist")
# 	return render(request, 'polls/detail.html', {"question": question})
def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {"question": question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# 重新显示问题的投票表单
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# 成功处理之后 POST 数据之后，总是返回一个 HttpResponseRedirect 。防止因为用户点击了后退按钮而提交了两次。
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
