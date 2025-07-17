
# 这是 core/admin.py 文件的完整内容

from django.contrib import admin
from .models import Post, Fund, Project # 从当前目录的 models.py 导入我们的三个模型

# 创建一个自定义的管理类，可以让列表页显示更多信息
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'author')
    list_filter = ('category', 'published_date')
    search_fields = ('title', 'content')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'developer_info', 'grant_amount')
    list_filter = ('status',)
    search_fields = ('name', 'description')

# 将模型和其自定义管理类注册到后台管理系统中
# Django会使用我们自定义的Admin类来展示模型
admin.site.register(Post, PostAdmin)
admin.site.register(Fund) # Fund模型比较简单，使用默认方式注册
admin.site.register(Project, ProjectAdmin)