from django.forms import ModelForm, CharField
from .models import User, Profile

# class ProfileUpdateForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'

class ProfileUpdateForm(ModelForm):
    first_name = CharField(max_length=32)
    last_name = CharField(max_length=32)
    class Meta:
        model = Profile
        fields = ['bio']