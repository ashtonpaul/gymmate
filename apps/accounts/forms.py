from django import forms


class PasswordResetForm(forms.Form):
    """
    Password Reset form
    """
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput()
    )

    def clean_confirm_password(self):
        """
        Validate form data
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        if len(confirm_password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")

        return confirm_password
