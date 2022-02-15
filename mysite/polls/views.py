from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # dic
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    return HttpResponse(render(request, "polls/index.html", context))

def detail(request, question_id):
    # No encouraged
    # try:
    #     question = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist.")
    question = get_object_or_404(Question, pk = question_id)
    # template = loader.get_template('polls/detail.html')
    context = {
        'question': question,
    }
    # return HttpResponse(template.render(context, request))
    return HttpResponse(render(request, "polls/detail.html", context))
    # return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return HttpResponse(render(request, "polls/results.html", {'question': question}))
    # return HttpResponse("You're looking at the results of question %s." % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return HttpResponse(render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice"}))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = (question.id, )))
    # return HttpResponse("You're voting on question %s." % question_id)