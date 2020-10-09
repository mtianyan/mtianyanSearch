from django import forms


class LoginForm(forms.Form):
    """登录表单验证"""
    # 用户名密码不能为空
    email = forms.CharField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """验证码form & 注册表单form"""
    # 此处email与前端name需保持一致。
    email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)
    re_password = forms.CharField(required=True, min_length=5)