from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from items.models import MediaForm


def media_create(request):
    if request.method == "POST":
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('photo-list'))
    else:
        form = MediaForm()
    return render_to_response('photos/create/html', {'form': form})