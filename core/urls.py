# 在 core/urls.py 文件中
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # --- 新增的首页URL ---
    path('', views.homepage, name='homepage'),
    path('search/', views.search_results, name='search_results'),  # <-- 新增这一行
    path('contact/', views.contact_view, name='contact'), # <-- 新增这一行
    # --- 新闻模块 ---
    path('news/', views.post_list, name='post_list'),
    path('news/<int:pk>/', views.post_detail, name='post_detail'),

    # --- 项目模块 ---
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
]