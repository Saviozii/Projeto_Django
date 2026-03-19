from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='Car_brand')
    factory_year = models.IntegerField(blank=True, null=True)
    model_year = models.IntegerField(blank=True, null=True)
    plate = models.CharField(max_length=10, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='cars/', blank=True, null=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    # versão grande — para hero e car_infor (1280x720)
    photo_large = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(1280, 720)],
        format='JPEG',
        options={'quality': 88}
    )

    # versão card — para grids e listagens (640x360)
    photo_card = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(640, 360)],
        format='JPEG',
        options={'quality': 82}
    )

    # versão thumb — para miniaturas (200x130)
    photo_thumb = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(200, 130)],
        format='JPEG',
        options={'quality': 75}
    )

    def __str__(self):
        return self.model

class inventory(models.Model):
    car_total = models.IntegerField()
    car_valor = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.car_total} - :{self.car_valor}'