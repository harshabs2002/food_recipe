from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    MALE='M'
    FEMALE='F'
    OTHERS='O'
    GENDER_choices=[
        (MALE,'Male'),
        (FEMALE,'Female'),
        (OTHERS,'Others'),

    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_images',default='default_profile_image.jpg')
    gender=models.CharField(max_length=20,choices=GENDER_choices,default=OTHERS)

    def __str__(self):
        return self.user.username
    
