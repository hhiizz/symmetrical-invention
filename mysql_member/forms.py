from django import forms
class NameForm(forms.Form):
    user_name= forms.CharField(label='floatingInput', max_length=100)
    user_password= forms.CharField(label='floatingPassword', max_length=100)
    class Meta:
        fields = ('user_name','user_password')
class LongForm(forms.Form):
    user_name= forms.CharField(label='floatingInput', max_length=100)
    user_password= forms.CharField(label='floatingPassword', max_length=100)
    class Meta:
        fields = ('user_name','user_password')