from django import forms
from .models import Receta, Comment
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update({'class': 'd-none'})

        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('name', 'parent', 'email', 'content')

        widgets = {
            'name':
            forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email':
            forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content':
            forms.Textarea(
                attrs={
                    'class':
                    'ml-3 mb-3 form-control border-0 comment-add rounded-0',
                    'rows': '1',
                    'placeholder': 'Añade un comentario'
                }),
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)
