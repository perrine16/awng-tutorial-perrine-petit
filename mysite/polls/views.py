from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import  reverse
from django.views import generic
from .models import Question, Choice
from django.utils import timezone

# Create your views here.

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """Return the last five published questions. (not including 
        those set to be published in the future)"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

#def index(request):
#    latest_question_list = Question.objects.order_by("-pub_date") [:5]
#    context = {
#        "latest_question_list": latest_question_list,
#    }
#    return render(request, "polls/index.html", context)

class DetailView(generic.DetailView):
    model = Question
    template_name ="polls/detail.html"
    def get_queryset(self):
        """ excludes question that are not published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())
    
#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/detail.html", {"question":question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

#def results(request, question_id):
#    response = "You're looking at the results of question %s."
#    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
