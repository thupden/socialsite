from django import forms

class CommentForm(forms.Form):
    body = forms.CharField(widget = forms.TextInput(
        attrs={
            "class" : "form-control",
            "placeholder" : 'Leave a comment !'
        }
    ))