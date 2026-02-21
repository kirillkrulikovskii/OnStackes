from django.db import models
from django.contrib.auth import get_user_model; User = get_user_model()






class Blog(models.Model):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title  = models.CharField(max_length=255, verbose_name="Title", help_text="Enter the title of the post.")
    content= models.TextField(max_length=1024, blank=True, null=True, verbose_name="Content", help_text="Enter the content of the post, if you want anything to write")

    files  = models.FileField (upload_to="media/files" ,blank=True,null=True)
    images = models.ImageField(upload_to="media/images",blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish    = models.BooleanField (default=True)
    shares     = models.ManyToManyField(User,  related_name="post_shares", blank=True)

    category   = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)    
    tags       = models.ManyToManyField('Tag', related_name="post_tags"  , blank=True)

    def __str__(self): return f"{self.title} by {self.author}"
    def comments_count(self): self.comment_post.count() # type: ignore

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post   = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post")
    content= models.TextField(max_length=512)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"Comments by {self.author} at {self.created_at}"

class Category(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self): return self.title

class Tag(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self): return self.title