import email
from django import forms
class NameForm(forms.Form):
    # 只需要和前端name一樣不用綁lable，post可以不用表單POST['']，表單只是用來驗證資料的正確性，
    user_name= forms.CharField(label='floatingInput', max_length=100)
    user_password= forms.CharField(label='floatingPassword', max_length=100)
    email= forms.CharField(label='floatingPassword', max_length=100)
    class Meta:
        fields = ('user_name','user_password')
class LongForm(forms.Form):
    user_name= forms.CharField(label='floatingInput', max_length=100)
    user_password= forms.CharField(label='floatingPassword', max_length=100)
    class Meta:
        fields = ('user_name','user_password')


