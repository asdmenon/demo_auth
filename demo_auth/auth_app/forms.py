from django import forms


class AuthForm(forms.Form):
    civ_id = forms.CharField(
        label="Civil ID", max_length=100, help_text="Enter Civil ID"
    )
