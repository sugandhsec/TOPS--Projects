from import_export import resources

from django.contrib import admin

from myapp.resources import SignupResource , UserResource , logResource
from .models import User,Signup,log ,petty_amount
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class SignupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SignupResource


class userAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserResource

class logAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = logResource
    list_display=('fname','lname','email','emp_code','reason','amount','type','petty_amount','date')

admin.site.register(User , userAdmin)
admin.site.register(Signup , SignupAdmin)
admin.site.register(log , logAdmin)
admin.site.register(petty_amount)
