from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
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
    listed_jobs = Job.objects.filter(client=user)
    working_jobs = Job.objects.filter(freelancer=user)
    return render(request, 'profiles/detail.html', {
        'profile_user': user,
        'listed_jobs': listed_jobs,
        'working_jobs': working_jobs,
    })

@login_required
def edit_profile(request, user_id):
    if user_id != request.user.id:
        return redirect(reverse('home'))

@login_required
def edit_profile(request):
    if request.method == "POST":
        request_user = User.objects.get(id=request.user.id)

        request_user.first_name = request.POST["first_name"]
        request_user.last_name = request.POST["last_name"]
        request_user.profile.bio = request.POST["bio"]
        request_user.profile.save()
        request_user.save()
        return redirect(reverse('home'))

    user = request.user
    return render(request, 'profiles/edit.html', {
        'profile_user':user
    })


@login_required
def create_job(request):
    if request.method == "POST":
        # Obtain request's data
        user = request.user
        title = request.POST["title"]
        reward = request.POST["reward"]
        description = request.POST["description"]
        category_title = request.POST["category"]
        if category_title:
            category = Category.objects.get(title=category_title)
        else:
            category = None
        # Create job
        job = Job(job_title=title, client=user, reward=reward, category=category, description=description)
        job.save()
        return HttpResponseRedirect(reverse("home"))

    categories = Category.objects.all()
    return render(request, "jobs/job_create.html", {
        "categories":categories
    })

def jobs_list(request):
    jobs = Job.objects.filter(is_active=True, is_finished=False).order_by("id").reverse()
    return render(request, "jobs/index.html", {
        "jobs":jobs,
    })

def jobs_detail(request, pk):
    job = Job.objects.get(id=pk)
    work_requests = RequestToClient.objects.filter(job=job)
    requesting_freelancers = [work_request.freelancer.id for work_request in work_requests]
    print(requesting_freelancers)
    user_have_requested = request.user.id in requesting_freelancers
    

    return render(request, 'jobs/job_detail.html', {'job':job,
            'work_requests': work_requests,
            'user_have_requested':user_have_requested})

def jobs_delete(request, pk):
    if request.method == "POST":
        job = Job.objects.get(id=pk).delete()

    return redirect(reverse('jobs_list'))

@login_required
def send_request(request, pk):
    job = Job.objects.get(id=pk)
    # client = User.objects.get()
    work_request = RequestToClient(freelancer=request.user, client=job.client, job=job)
    work_request.save()
    notification = Notification(to=job.client, job=job, message=f"{request.user} requested to work on {job.job_title}")
    notification.save()
    return redirect(reverse('jobs_list'))

@login_required
def delete_request(request, pk):
    job = Job.objects.get(id=pk)
    found_request = RequestToClient.objects.get(job=job)
    found_request.delete()
    notification = Notification(to=job.client, job=job, message=f"{request.user} canceled the request to work on {job.job_title}")
    notification.save()
    return redirect(reverse('jobs_list'))

@login_required
def accept_request(request, pk):
    work_request = RequestToClient.objects.get(id=pk)
    job = work_request.job
    job.is_active = False
    job.freelancer = work_request.freelancer
    RequestToClient.objects.filter(job=job).delete()
    job.save()
    notification = Notification(to=job.freelancer, job=job, message=f"{request.user} have accepted your request to work on {job.job_title}")
    notification.save()
    return redirect(reverse('jobs_list'))

@login_required
def decline_request(request, pk):
    work_request = RequestToClient.objects.get(id=pk)
    
    notification = Notification(to=work_request.freelancer, job=work_request.job, message=f"{work_request.client} have declined your request to work on {work_request.job.job_title}")
    notification.save()
    work_request.delete()
    return redirect(reverse('jobs_list'))

@login_required
def upload(request, pk):
    if request.method != "POST":
        return redirect(reverse("home"))
    job = Job.objects.get(id=pk)
    job.file = request.FILES.get("file")
    job.is_finished = True
    job.save()
    notification = Notification(to=job.client,job=job, message=f"{job.freelancer} submitted the work on {job.job_title}")
    notification.save()
    return redirect(reverse("home"))

@login_required
def download(request, pk):
    if request.method != "POST":
        return redirect(reverse("home"))
    job = Job.objects.get(id=pk)
    file = job.file
    response = HttpResponse(file, content_type="application/adminupload")
    response['Content-Disposition'] = f'attachment; filename="{job.file.name}"'
    return response

@login_required
def notifications(request, pk):
    user = User.objects.get(id=pk)
    if request.user != user:
        return redirect(reverse("home"))
    notifications_data = Notification.objects.filter(to=user).order_by("id").reverse()
    return render(request, "notifications/notifications_page.html", {
        "notifications": notifications_data,
    })



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