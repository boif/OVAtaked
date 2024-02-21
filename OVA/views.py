from datetime import datetime
from django.shortcuts import render, redirect
from OVA.models import Image, Contact
from OVA.forms import RegisterForm, AddImage, ProfileForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import CreateView
from OVA.service import send



def home(request):
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home',
            'year': datetime.now().year,
        }
    )

def contact(request):
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'year': datetime.now().year,
        }
    )

def about(request):
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'year': datetime.now().year,
        }
    )

def images(request):
    images = Image.objects.filter()
    return render(
        request,
        'app/images.html',
        {
            'images': images,
            'year': datetime.now().year,
            'title': 'Images',
            'message': 'GPZ INDUSTRIEZZZ COLLECTION'
        }

    )

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/login/')
    else:
        form = RegisterForm()
    return render(
        request,
        'app/signup.html',
        {
            'form': form,
            'year': datetime.now().year,
        },
    )

@login_required
def addimage(request):
    if request.POST:
        form = AddImage(request.POST, request.FILES)
        if form.is_valid():
            addimg = form.save(commit=False)
            addimg.author = request.user
            addimg.save()
            return redirect('/images/')
    else:
        form = AddImage()
    return render(
        request,
        'app/addimage.html',
        {
            'form': form,
            'title': 'Add image',
        }
    )

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Image.objects.filter(author=user.id)
    profile = user.profile
    return render(
        request,
        "app/profile.html",
        {
            'username': user.username,
            'profile_pic': profile.profile_pic.url,
            'vk': profile.vk,
            'posts': posts
        }
    )
def profilesettings(request):
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(
        request,
        'app/profilesettings.html', {
            'form': form,
            'title': 'Profile settings'
        }
    )

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'app/subscribe.html'

    def form_valid(self, form):
        form.save()
        send(form.instance.email)
        return super().form_valid(form)