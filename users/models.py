from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image


class User(AbstractUser):
    email = models.EmailField(_("email address"))

    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    city = models.CharField(max_length=20, blank=True)
    url = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        def crop_center(pil_img, crop_width, crop_height):
            img_width, img_height = pil_img.size
            return pil_img.crop(
                (
                    (img_width - crop_width) // 2,
                    (img_height - crop_height) // 2,
                    (img_width + crop_width) // 2,
                    (img_height + crop_height) // 2,
                )
            )

        def crop_max_square(pil_img):
            return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

        im_thumb = crop_max_square(img).resize((300, 300), Image.LANCZOS)
        im_thumb.save(self.image.path, quality=95)

        # if img.height> 300 or img.width > 300:
        #     size = (300,300)
        #     img.thumbnail(size)
        #     img.save(self.image.path)