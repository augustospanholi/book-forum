from django import forms
from core.models import Post, Reply, Rules


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'field-input',
                'placeholder': 'Thread title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'field-input',
                'placeholder': 'Write your post...',
                'rows': 8,
            }),
            'category': forms.Select(attrs={
                'class': 'field-input',
            }),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'field-input',
                'placeholder': 'Write your reply...',
                'rows': 4,
            }),
        }


class RulesForm(forms.ModelForm):
    class Meta:
        model = Rules
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'field-input',
                'rows': 20,
            }),
        }
