from django.contrib import admin

from . import models as blog_models

admin.site.register(blog_models.Post)
admin.site.register(blog_models.Suggest) # Added new model
admin.site.register(blog_models.Issue)   # Added new model
admin.site.register(blog_models.Comment)
admin.site.register(blog_models.Category)
admin.site.register(blog_models.Tag)