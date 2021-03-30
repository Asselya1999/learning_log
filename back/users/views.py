from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Регистрируем нового юзера"""
    if request.method != 'POST':
        """данные не отпралялись. Создается пустая форма"""
        form = UserCreationForm()

    else:
        """отправленные данные POST, обработать данные"""
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('api:index')

    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, r'C:\Users\леново\PycharmProjects\kbtu\back\users\templates\registration\register.html', context)