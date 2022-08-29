from attr import field
from django import forms
from idna import alabel
class GETSKILL(forms.Form):
    skill = forms.CharField(label='get_skill',max_length=1000)
    type_skill =forms.CharField(label='job',max_length=500)
    class Meta:
        fields = ('skill','type_skill')

