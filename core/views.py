# 在 core/views.py 文件中
from django.shortcuts import render, get_object_or_404 # 确保导入了 get_object_or_404
from django.core.paginator import Paginator  # <-- 新增这一行
from .models import Post, Project       

# 已有的列表视图
def post_list(request):
    # 1. 先获取所有文章的原始列表
    all_posts = Post.objects.all().order_by('-published_date')

    # 2. 创建一个 Paginator 对象，告诉它我们获取的所有文章，并且每页只显示 5 篇
    paginator = Paginator(all_posts, 5) 

    # 3. 从URL的GET请求中获取 'page' 参数，也就是用户想看的页码
    #    例如： /news/?page=2  ->  page_number 会是 '2'
    page_number = request.GET.get('page')

    # 4. 使用 paginator.get_page() 获取指定页码的页面对象(page_obj)
    #    这个方法很安全，即使用户提供一个无效的页码（比如字母或超范围的数字），也不会报错
    page_obj = paginator.get_page(page_number)

    # 5. 将这个包含当前页面文章信息和分页信息的 page_obj 对象传递给模板
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'core/post_list.html', context)
def post_detail(request, pk):
    # 使用 get_object_or_404 函数来获取一个对象。
    # 它的好处是，如果找不到对应pk的对象，它会自动返回一个 404 Not Found 页面，
    # 这比程序直接崩溃要友好得多。
    post = get_object_or_404(Post, pk=pk)

    context = {
        'post': post,
    }

    return render(request, 'core/post_detail.html', context)
    # --- 请将以下代码添加到 core/views.py 文件末尾 ---

# 别忘了从 models 导入 Project 模型
from .models import Project

# 项目列表视图
# 在 core/views.py 文件中，找到 project_list 函数并替换

def project_list(request):
    # 1. 获取所有项目的原始列表
    all_projects = Project.objects.all().order_by('-start_date')

    # 2. 创建 Paginator 对象，我们同样设置每页5个
    paginator = Paginator(all_projects, 5) 

    # 3. 从URL获取页码
    page_number = request.GET.get('page')

    # 4. 获取对应的页面对象
    page_obj = paginator.get_page(page_number)

    # 5. 将 page_obj 对象传递给模板。
    #    注意，我们这里用的键名是 'projects'，值为 page_obj
    #    这样做的好处是，模板里的 for 循环 `{% for project in projects %}` 不需要修改。
    context = {
        'projects': page_obj,
    }
    return render(request, 'core/project_list.html', context)

# 项目详情视图
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {
        'project': project,
    }
    return render(request, 'core/project_detail.html', context)
    # --- 请将以下代码添加到 core/views.py 文件末尾 ---

# 在 core/views.py 中，找到 homepage 函数并替换
def homepage(request):
    # 查询最新的3篇文章 (这部分逻辑不变)
    latest_posts = Post.objects.all().order_by('-published_date')[:3]

    # --- 修改这部分查询逻辑 ---
    # 我们不再是查询进行中的项目，而是只查询被设为精选的项目
    # filter(is_featured=True) 会精确地找出所有勾选了“设为精选”的项目
    featured_projects = Project.objects.filter(is_featured=True)[:3]

    # 将两份数据都打包到 context 中
    context = {
        'latest_posts': latest_posts,
        'featured_projects': featured_projects, # <-- 修改了键名，让它更清晰
    }

    return render(request, 'core/homepage.html', context)
    # 在 core/views.py 文件顶部，找到导入语句，新增 Q
from django.db.models import Q

# --- 请将以下函数代码添加到 core/views.py 文件末尾 ---

def search_results(request):
    # 1. 从 URL 的 GET 参数中获取用户输入的搜索关键词 (q)
    #    例如 /search/?q=基金会 -> query 的值会是 "基金会"
    query = request.GET.get('q')

    # 2. 如果用户提交了关键词
    if query:
        # 使用 Q 对象进行复杂的 OR 查询
        # __icontains 表示“不区分大小写的包含”
        # 我们希望找到标题(title)或内容(content)中包含关键词的文章
        post_results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

        # 同时，我们还希望找到名称(name)或描述(description)中包含关键词的项目
        project_results = Project.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        # 如果用户没有输入关键词就直接访问 /search/，则返回空列表
        query = "" # 传一个空字符串给模板，避免模板出错
        post_results = []
        project_results = []

    # 3. 将搜索词和两份结果都打包到 context 中
    context = {
        'query': query,
        'posts': post_results,
        'projects': project_results,
    }

    # 4. 渲染一个新的搜索结果模板
    return render(request, 'core/search_results.html', context)
    # 在 core/views.py 文件顶部，新增 ContactForm 的导入
from .forms import ContactForm

# --- 请将以下函数代码添加到 core/views.py 文件末尾 ---
def contact_view(request):
    if request.method == 'POST':
        # 如果是POST请求，说明用户提交了表单，我们用提交的数据来填充表单
        form = ContactForm(request.POST)
        if form.is_valid():
            # 如果表单数据有效（比如邮箱格式正确）
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # ** 临时操作 **：我们先在终端打印出信息，确认我们成功收到了数据
            print(f"--- 收到新的联系信息 ---")
            print(f"姓名: {name}")
            print(f"邮箱: {email}")
            print(f"内容: {message}")

            # TODO: 在下一步中，我们会在这里添加发送邮件的代码

            # 暂时先返回一个简单的成功信息
            from django.http import HttpResponse
            return HttpResponse("<h1>感谢您的留言！</h1><p>我们已收到您的信息。</p><a href='/'>返回首页</a>")
    else:
        # 如果是GET请求（用户刚打开这个页面），我们展示一个空的表单
        form = ContactForm()

    # 将表单对象传递给模板进行渲染
    return render(request, 'core/contact.html', {'form': form})