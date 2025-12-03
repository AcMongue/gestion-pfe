from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """Formulaire pour envoyer un message"""
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content', 'attachment']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet du message'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Contenu du message...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'recipient': 'Destinataire',
            'subject': 'Objet',
            'content': 'Message',
            'attachment': 'Pièce jointe (optionnelle)',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # L'expéditeur ne peut pas s'envoyer de messages à lui-même
            from users.models import User
            self.fields['recipient'].queryset = User.objects.exclude(id=user.id).order_by('role', 'last_name', 'first_name')


class ReplyForm(forms.Form):
    """Formulaire pour répondre rapidement à un message"""
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Votre réponse...'
        }),
        label='Réponse'
    )
    attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Pièce jointe (optionnelle)'
    )
