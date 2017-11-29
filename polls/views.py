from django.shortcuts import render, get_object_or_404
from django.http import Http404,HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic


from django.http import HttpResponse

from polls.models import Question, Choice
# Create your views here.

class IndexView(generic.ListView):
	template_name = "polls/index.html"
	context_object_name = "latest_question_list"

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	template_name = "polls/detail.html"
	model = Question

class ResultsView(generic.DetailView):
	model = Question
	template_name = "polls/results.html"

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
