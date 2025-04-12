from tortoise import models, fields

class Comment(models.Model):
    id = fields.UUIDField(pk=True)
    blog_id = fields.CharField(max_length=255)
    user_id = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} commented on {self.blog_id}"


class Reply(models.Model):
    id = fields.UUIDField(pk=True)
    comment = fields.ForeignKeyField("models.Comment", related_name="replies" ,on_delete="CASCADE")
    user_id = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} replied to {self.comment_id}"
