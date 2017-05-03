from django import forms
from Portfolio.models import Comment, AdminInfo, Context

class CommentForm(forms.ModelForm):
    commentor_email = forms.CharField(widget=forms.HiddenInput)
    comment = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Comment
        exclude = ('content', 'date', 'edit_date', 'commentor')


class AdminLoginForm(forms.ModelForm):
    admin_pw = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = AdminInfo
        exclude = ('admin_lv', 'fails', 'fail_time')


class ContextForm(forms.ModelForm):
    class Meta:
        model = Context
        exclude = ()