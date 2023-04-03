
from import_export import resources
from .models import *

class SignupResource(resources.ModelResource):
    class Meta:
        model = Signup

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class logResource(resources.ModelResource):
    class Meta:
        model = log