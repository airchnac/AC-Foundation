"""
URL configuration for acc_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
# 在 acc_project/urls.py 文件中
from django.contrib import admin
# 确保从 django.urls 导入了 path 和 include
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 新增这一行，它将所有非 admin/ 的URL请求，都转交给 core.urls 去处理
    path('', include('core.urls')),
]
# 在 acc_project/urls.py 文件中
from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # <-- 新增导入
from django.conf.urls.static import static   # <-- 新增导入

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# --- 新增以下代码 ---
# 仅在DEBUG模式下（即我们的开发环境中），才让Django的开发服务器托管媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)