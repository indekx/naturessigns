from django import forms
from .models import Join

# Join newsletter form
class JoinNewsLetterForm(forms.ModelForm):

    class Meta:
        model = Join
        fields = ('email',)

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        q_set = Join.objects.filter(email__iexact=email)
        if q_set.exists():
            raise forms.ValidationError('This email already subscribed')
        return email
