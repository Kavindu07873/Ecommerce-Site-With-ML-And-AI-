# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils import timezone

# # Create your models here.


# class CoreModel(models.Model):
#     created = models.DateTimeField(
#         'Created',
#         null=False,
#         default=timezone.now,
#         editable=False,
#     )

#     updated = models.DateTimeField(
#         'Updated',
#         null=False,
#         auto_now=True,
#         editable=False,
#     )

#     class Meta:
#         abstract = True
#         ordering = ['-updated']




# class AbstractAccount(CoreModel):
#     about = models.TextField(
#         'About me',
#         blank=True,
#         null=True
#     )
#     age = models.SmallIntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(100)],
#         blank=True,
#         null=True
#     )
#     photo = models.ImageField(
#         upload_to=get_upload_to,
#         blank=True,
#         null=True
#     )
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#     )

