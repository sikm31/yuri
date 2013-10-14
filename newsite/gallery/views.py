# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from gallery.models import Choice, Poll

class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by('-pub_date')[:5]


#def index(request):
#   return HttpResponse("Hello, world. You're at the poll index.")

#def detail(request, poll_id):
 #   return HttpResponse("You're looking at poll %s." % poll_id)

#def detail(request, poll_id):
 #   try:
 #       poll = Poll.objects.get(pk=poll_id)
 #   except Poll.DoesNotExist:
 #       raise Http404
 #   return render(request, 'gallery/detail.html', {'poll': poll})

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'gallery/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'gallery/results.html'

#def vote(request, poll_id):
#    return HttpResponse("You're voting on poll %s." % poll_id)
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'gallery/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('gallery:results', args=(p.id,)))
