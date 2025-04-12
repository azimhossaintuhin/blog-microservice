from  tortoise.models import Model
from tortoise import fields
import uuid



class Category(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    image = fields.CharField(max_length=255 ,default="")
    name = fields.CharField(max_length=255 ,default="")
    slug  = fields.CharField(max_length=255 ,default="")
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    async def save(self, *args, **kwargs):
        self.slug = self.name.replace(" ", "-").lower()
        await super().save(*args, **kwargs)
        
    
        
class BlogReader(Model):
    blog_id = fields.CharField(max_length=255)
    user_id = fields.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.user_id} read {self.blog_id}"

class Blog(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    image = fields.CharField(max_length=255 ,default="")
    author = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255)
    category = fields.ForeignKeyField("models.Category", related_name="blogs")
    content = fields.TextField()
    read_count = fields.ManyToManyField("models.BlogReader")
    tags = fields.CharField(max_length=255 ,default="" ,help="comma separated tags")
    is_published = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def save(self, using_db = None, update_fields = None, force_create = False, force_update = False):
        self.slug = self.title.replace(" ", "-").lower()
        return super().save(using_db, update_fields, force_create, force_update)
    
    

    

    