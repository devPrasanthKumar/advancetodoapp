from django import forms
from .models import ListDetails, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class FormForListDetails(forms.ModelForm):

    due_date = forms.DateField(required=False,
                               widget=forms.TextInput(attrs={"type": "date"}))
    fileUpload = forms.FileField(required=False)
    desc = forms.CharField(label="Enter :")

    class Meta:
        model = ListDetails
        fields = "__all__"
        exclude = ("slug", "owner", "updateDate",)

    def __init__(self, *args, **kwargs):
        super(FormForListDetails, self).__init__(*args, **kwargs)

        # Define common widget attributes for all fields
        common_widget_attrs = {"class": "form-control"}

        # Loop through fields and assign common attributes to widgets
        for field_name, field in self.fields.items():
            print(field_name)
            if field_name:
                self.fields[field_name].widget.attrs.update(
                    common_widget_attrs)


class SignInForm(UserCreationForm):

    userIMG = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ["userIMG", "username", "email", "password1", "password2"]

    common_attrs = {"class": "form-control"}

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name:
                self.fields[field_name].widget.attrs.update(self.common_attrs)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username'}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'})
    )


class UserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ["username", "email", "userIMG"]

    common_attrs = {"class": "form-control"}

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name:
                self.fields[field_name].widget.attrs.update(self.common_attrs)
