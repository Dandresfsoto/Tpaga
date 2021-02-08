from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, ButtonHolder, Layout, Div


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control form-control-lg inverse-mode",
                "autocomplete": "off"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control form-control-lg inverse-mode",
                "autocomplete": "off"
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                "username",
                css_class="form-group m-b-20"
            ),
            Div(
                "password",
                css_class="form-group m-b-20"
            ),
            Div(
                ButtonHolder(
                    Submit("submit", "Ingresar", css_class="btn btn-primary btn-block btn-lg")
                ),
                css_class="login-buttons"
            )
        )
