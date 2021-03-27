from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm


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


