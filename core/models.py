# 这是 core/models.py 文件的完整内容（已修正）

from django.db import models
from django.utils import timezone

# ==============================================================================
# 模型一: Post (文章)
# ==============================================================================
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('NEWS', '新闻动态'),
        ('ANNOUNCEMENT', '官方公告'),
        ('REPORT', '透明度报告'),
    ]

    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='NEWS', verbose_name="分类")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="发布日期")
    author = models.CharField(max_length=100, default='ACC Foundation', verbose_name="作者")
    cover_image = models.ImageField(upload_to='post_covers/', blank=True, null=True, verbose_name="封面图片")

    # --- 确保 attachment 字段在这里 ---
    attachment = models.FileField(upload_to='post_attachments/', blank=True, null=True, verbose_name="附件下载")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章与公告"
        verbose_name_plural = verbose_name
        ordering = ['-published_date']


# ==============================================================================
# 模型二: Fund (公共基金池)
# ==============================================================================
class Fund(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="基金名称")
    description = models.TextField(verbose_name="基金用途描述")
    wallet_address = models.CharField(max_length=128, blank=True, null=True, verbose_name="关联钱包地址")
    FUND_TYPE_CHOICES = [
        ('REWARD', '奖励基金'),
        ('STABILITY', '稳定基金'),
        ('GRANT', '激励基金'),
        ('OTHER', '其他'),
    ]
    fund_type = models.CharField(max_length=20, choices=FUND_TYPE_CHOICES, default='OTHER', verbose_name="基金类型")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "公共基金池"
        verbose_name_plural = verbose_name


# ==============================================================================
# 模型三: Project (生态激励项目)
# ==============================================================================
class Project(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', '申请中'),
        ('REVIEWING', '审核中'),
        ('FUNDED', '已资助'),
        ('IN_PROGRESS', '进行中'),
        ('COMPLETED', '已完成'),
    ]

    name = models.CharField(max_length=200, verbose_name="项目名称")
    description = models.TextField(verbose_name="项目描述")
    developer_info = models.CharField(max_length=200, verbose_name="开发者/团队信息")
    grant_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="资助金额 (USD)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED', verbose_name="项目状态")
    start_date = models.DateField(blank=True, null=True, verbose_name="项目开始日期")
    cover_image = models.ImageField(upload_to='project_covers/', blank=True, null=True, verbose_name="封面图片")
    is_featured = models.BooleanField(default=False, verbose_name="设为精选项目")

    # --- 确保这里没有多余的 attachment 字段 ---

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "生态激励项目"
        verbose_name_plural = verbose_name
        ordering = ['-start_date']