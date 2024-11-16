from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login
from .models import BlogPost
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'Home.html')
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password= request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            username = user.username  # Extract the username from the user
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': ('Invalid email or password')}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid email or password'}, status=400)

    return render(request, 'Login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('password2')
        user = User.objects.filter(username=username)

        if user.exists():
            return JsonResponse({'success': False, 'message': 'Username Already Taken'})

        if password == confirmpassword:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            return JsonResponse({'success': True, 'message': 'Account Created Successfully'})

        return JsonResponse({'success': False, 'message': 'Passwords do not match'})

    return render(request, 'register.html')


def dashboard(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'Dashboard.html', {'posts': posts})

# Create a New Blog Post
@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        post = BlogPost.objects.create(
            title=title, content=content, image=image, author=request.user)
        return redirect('dashboard')
    return render(request, 'Create.html')

# Edit an Existing Post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.save()
        return redirect('dashboard')
    return render(request, 'Edit.html', {'post': post})

# Delete a Post
@login_required
def delete_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    post.delete()
    return redirect('dashboard')
# view blog details
@login_required
def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'BlogDetail.html', {'post': post})