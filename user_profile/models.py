from django.db import models
from djangoProject.settings import AUTH_USER_MODEL


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    about_me = models.TextField(max_length=4096, null= True, blank=True)
    facebook = models.CharField(max_length=64, null=True, blank=True)
    twitter = models.CharField(max_length=64, null=True, blank=True)
    instagram = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return str(self.user)
