# 这是 core/views.py 文件的完整、正确版本

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import get_user_model # 确保这个导入存在

from .models import Post, Project # 确保这两个模型导入存在
from .forms import ContactForm    # 确保表单导入存在

def homepage(request):
    latest_posts = Post.objects.all().order_by('-published_date')[:3]
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    context = {
        'latest_posts': latest_posts,
        'featured_projects': featured_projects,
    }
    return render(request, 'core/homepage.html', context)
    latest_posts = Post.objects.all().order_by('-published_date')[:3]
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    context = {
        'latest_posts': latest_posts,
        'featured_projects': featured_projects,
    }
    return render(request, 'core/homepage.html', context)

def post_list(request):
    all_posts = Post.objects.all().order_by('-published_date')
    paginator = Paginator(all_posts, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'core/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'core/post_detail.html', context)

def project_list(request):
    all_projects = Project.objects.all().order_by('-start_date')
    paginator = Paginator(all_projects, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'projects': page_obj,
    }
    return render(request, 'core/project_list.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {
        'project': project,
    }
    return render(request, 'core/project_detail.html', context)

def search_results(request):
    query = request.GET.get('q')
    if query:
        post_results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        project_results = Project.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        query = ""
        post_results = []
        project_results = []
    context = {
        'query': query,
        'posts': post_results,
        'projects': project_results,
    }
    return render(request, 'core/search_results.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            print(f"--- 收到新的联系信息 ---")
            print(f"姓名: {name}")
            print(f"邮箱: {email}")
            print(f"内容: {message}")
            return HttpResponse("<h1>感谢您的留言！</h1><p>我们已收到您的信息。</p><a href='/'>返回首页</a>")
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})