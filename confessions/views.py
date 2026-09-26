from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import CustomUserCreationForm
from .forms import ConfessionForm
from .models import Confession


def signup_view(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('wall')
  else:
    form = CustomUserCreationForm()
  return render(request, 'accounts/signup.html', {'form': form})


def wall_view(request):
  confessions = Confession.objects.filter(is_approved=True).order_by(
      '-created_at'
  )

  if request.method == 'POST':
    if not request.user.is_authenticated:
      return redirect('login')
    form = ConfessionForm(request.POST)
    if form.is_valid():
      confession = form.save(commit=False)
      confession.author = request.user
      confession.save()
      return redirect('wall')
  else:
    form = ConfessionForm()

  context = {'confessions': confessions, 'form': form}
  return render(request, 'confessions/wall.html', context)


@login_required
def upvote_confession(request, pk):
  confession = get_object_or_404(Confession, pk=pk)
  confession.upvotes += 1
  confession.save()
  return redirect('wall')