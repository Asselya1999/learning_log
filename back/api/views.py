from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    return render(request, 'api/index.html')


def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'api/topics.html', context)


def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'api/topic.html', context)



def new_topic(request):
    """определяем новый топик"""
    if request.method != 'POST':
        """данные не отпралялись. Создается пустая форма"""
        form = TopicForm()

    else:
        """отправленные данные POST, обработать данные"""
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('api:topics')

    #Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'api/new_topic.html', context)

def new_entry(request, topic_id):
    """добавим новую запись по определенному топику"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        """отправленные данные POST, обработать данные"""
        form = EntryForm(data=request.POST)
        if form.is_valid():
           new_entry = form.save(commit=False)
           new_entry.topic = topic
           new_entry.save()
           return redirect('api:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'api/new_entry.html', context)

def edit_entry(request, entry_id):
    """будем редактировать существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        """останется исходный запрос"""
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('api:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'api/edit_entry.html', context)








