# 在 core/forms.py 文件中
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="您的姓名")
    email = forms.EmailField(label="您的邮箱")
    message = forms.CharField(widget=forms.Textarea, label="留言内容")