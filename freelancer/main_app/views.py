from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.dispatch import receiver
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Profile, Job, RequestToClient, Notification, Category
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models.signals import post_save
from .forms import ProfileUpdateForm
# Define the home view
def home(request):
    return render(request, 'main_app/index.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

def view_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profiles/detail.html', {
        'profile_user': user,
    })

@login_required
def edit_profile(request, user_id):
    if user_id != request.user.id:
        return redirect(reverse('home'))
    

class UserUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'auth/user_form.html'
    context_object_name = 'user'
    queryset = User.objects.all()
    print("queryset", queryset)
    form_class = ProfileUpdateForm


# class UserUpdate(LoginRequiredMixin, UpdateView):
    # template_name = 'auth/user_form.html'
    # context_object_name = 'user'
    # queryset = Profile.objects.all()
    # form_class = ProfileUpdateForm

    # def get_success_url(self):
    #     return reverse('profiles_details', kwargs={'user_id': self.get_object().user.id})

    # def get_context_data(self, **kwargs):
    #     context = super(UserUpdate, self).get_context_data(**kwargs)
    #     context['user_form'] = ProfileUpdateForm(instance=self.request.user)
    #     return context
    
    # def form_valid(self, form):
    #     user_form = form.save(commit=False)
    #     User.last_name = user_form.last_name
    #     User.first_name = user_form.first_name
    #     user_form.save()