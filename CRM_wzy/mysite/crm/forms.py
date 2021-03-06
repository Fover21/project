# __author: busensei
# data: 2018/10/29
from django import forms
from crm import models


# 给所有的字段加增加样式属性（Bootstrap的）
class BaseForm(forms.ModelForm):
    # 给所有的字段加属性
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


# 注册forms
class RegisterForms(BaseForm):
    # 再次确认密码的输入框
    re_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(attrs={'onblur': "v_repeat()", 'onkeyup': "v_repeat()"}),
        error_messages={
            'required': '密码不能为空'
        }
    )

    class Meta:
        # 注册这个models中的表
        model = models.UserProfile
        # fields = '__all__'  # 所有字段
        fields = ['username', 'name', 'password', 're_password', 'department']  # 选哪些字段
        # exclude = []  # 不包括那些字段
        widgets = {
            'name': forms.widgets.Input(attrs={'onblur': "v_name()", 'onkeyup': "v_name()"}),
            'department': forms.widgets.Select(attrs={'style': "width: 278px"}),
            'username': forms.widgets.EmailInput(attrs={'onblur': "v_name()", 'onkeyup': "v_name()"}),
            'password': forms.widgets.PasswordInput(attrs={'onblur': "v_password()", 'onkeyup': "v_password()"}),
        }

        labels = {
            'username': '用户名',
            'password': '密码',
            'name': '姓名',
            'department': '部门',
        }
        error_messages = {
            'username': {
                'required': '用户名不能为空',
            },
            'password': {
                'required': '密码不能为空',
            },
            'name': {
                'required': '姓名不能为空',
            },

        }

        # 给所有的字段加属性
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')


# 客户form
class CustomerForm(BaseForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        widgets = {
            'course': forms.widgets.SelectMultiple
        }