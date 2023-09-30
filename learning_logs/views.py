from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm , EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404 

def index(request):
    """ THE HOME PAGE FOR LEARNNING LOGS"""
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """show all topics"""
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context={'topics':topics}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    """Show a single topic and its all entry"""
    topic=Topic.objects.get(id=topic_id)
    # make sure the topic belong to the current user
    if topic.owner != request.user:
        raise Http404
    # below their is use of foreign key.
    entries=topic.entry_set.order_by('-date_added')
    context={'topics': topic, 'entries': entries, 'id':topic_id}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    """ADD A NEW TOPIC."""
    if request.method!= 'POST':
        # no data submitted; create a blank form.
        form = TopicForm()
    else:
        # post data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # display a blank and a invalid form   
    context = {'form': form}
    return render (request, 'learning_logs/new_topic.html',context)

@login_required
def new_entry(request, topic_id):
    """Adding new entry for a particular topic"""
    topic=Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # no data submitted; create a blank form.
        form = EntryForm()
    else:
        # post data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect ('learning_logs:topic',topic_id=topic_id)
        
    # Display a blank or invalid form
    context={'topic':topic , 'form':form }
    return render(request, 'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST' :
        # intial request; pre-fill form with the current entry,
        form = EntryForm(instance=entry)
    
    else:
        # post data submitted, process data.
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id= topic.id)
        
    context={'entry':entry, 'topic': topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html',context)
