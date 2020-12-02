from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
    return render(request, 'log_keepers/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'log_keepers/topics.html', context)


@login_required
def topic(request, topic_id=1):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, "log_keepers/topic.html", context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('log_keepers:topics'))
    context = {'form': form}
    return render(request, "log_keepers/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('log_keepers:topic', args=[topic_id]))
    context = {'form': form, 'topic': topic}
    return render(request, 'log_keepers/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('log_keepers:topic', args=[topic.id]))
    context = {'form': form, 'entry': entry, 'topic': topic}
    return render(request, 'log_keepers/edit_entry.html', context)


@login_required
def delete_topic(request, topic_id):
    if check_topic(topic_id):
        topic = Topic.objects.filter(id=topic_id)[0]
        if request.user != topic.owner:
            raise Http404
        else:
            topic.delete()
    else:
        return HttpResponseRedirect(reverse('log_keepers:topics'))
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {"topics":topics}
    return render(request, "log_keepers/topics.html",context)


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    else:
        entry.delete()
    return HttpResponseRedirect(reverse("log_keepers:topic",args=[topic.id]))


def check_topic(topic_id):
    topics = Topic.objects.all()
    for topic in topics:
        if topic.id == topic_id:
            return True
    return False
