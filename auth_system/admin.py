from django.contrib import admin

from .models import Accounts, MessageTo, Report

admin.site.register(Accounts)
admin.site.register(MessageTo)
admin.site.register(Report)