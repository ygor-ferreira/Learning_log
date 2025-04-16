from django import forms
#aqui ele ta pegando o banco de dados chamado Topic
# que esta dentro de models
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        #aqui ta pegando o banco de dados Topic
        #e deixando ele como modelo para poder usar
        model = Topic
        fields = ['text']
        #para tirar os labels do formularios
        labels = {'text': ''}
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # widgets é o nome do retangulo que voce clica para poder cadastrar
        #nesse caso é para colocar o retangulo maior ja q é um textarea
        #attrs = São atributos referente a esse textarea, 
        #nesse caso quero um textarea de 80 colunas de largura
        widgets = {'text': forms.Textarea(attrs={'cols':80})}