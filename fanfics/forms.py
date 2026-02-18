from django import forms
from .models import Fanfic
from accounts.models import Profile


class FanficForm(forms.ModelForm):
    class Meta:
        model = Fanfic
        fields = ['titulo', 'descricao', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-text'}),
            'descricao': forms.Textarea(attrs={'class': 'input-area', 'rows': 3}),
            'conteudo': forms.Textarea(attrs={'class': 'input-area', 'rows': 10}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
