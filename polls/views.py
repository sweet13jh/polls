from django.views import generic
from django.template import loader
from .models import Question
###Generic View(class-based views)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    """Return the last five published questions."""
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Question
from django.http import Http404
from django.shortcuts import render, get_object_or_404

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')

    context = {'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'polls/result.html',{'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = HttpResponse("You're looking at the results of question %s." % question_id)
    return response

def vote(request, question_id):
    return HttpResponse("You're voting on question %s" % question_id)
