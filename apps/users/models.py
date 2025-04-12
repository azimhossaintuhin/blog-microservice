from  tortoise.models import Model
from  tortoise import fields
import uuid
from  tortoise.signals import post_save


class User(Model):
    id = fields.UUIDField(pk=True , default=uuid.uuid4)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    is_verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.username
    
class  UserProfile(Model):
    id = fields.UUIDField(pk=True , default=uuid.uuid4)
    user = fields.ForeignKeyField("models.User", related_name="profile")
    first_name = fields.CharField(max_length=50,default="")
    last_name = fields.CharField(max_length=50 ,default="")
    phone = fields.CharField(max_length=15, default="")
    address = fields.TextField(default="")
    profile_picture = fields.CharField(max_length=255, default="")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


@post_save(User)
async def create_user_profile(sender, instance, created, update_fields, using_db):
    if created:
        # Check if a user profile already exists
        existing_profile = await UserProfile.filter(user=instance).first()
        if not existing_profile:
            await UserProfile.create(user=instance)
