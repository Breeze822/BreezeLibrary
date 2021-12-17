# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from book.views import page_error,page_not_found
urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    # path("", include("apps.authentication.urls")), # Auth routes - login / register
    # path("", include("apps.home.urls"))             # UI Kits Html files
    path("", include("book.urls")),
    path("auth/", include("authentication.urls")),  # Auth routes - login / register
]
handler404= 'book.views.page_not_found'
handler500= 'book.views.page_error'