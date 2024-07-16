from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_viewer = models.BooleanField(default=True)

    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        return super().has_module_perms(app_label)