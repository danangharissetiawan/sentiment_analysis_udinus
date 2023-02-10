from django import forms


class BroadcastForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BroadcastForm, self).__init__(*args, **kwargs)

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) > 200:
            raise forms.ValidationError('Message too long')
        return message



