# Author :Breeze_xylf
# Date :
from django.contrib import admin
from django.urls import path, include, re_path
from .views import TeacherView,ClassInfoView,ClassDetailView
from .views import HomeView,BookListView,BookCreateView,BookDeleteView,BookDetailView,BookUpdateView
from .views import CategoryListView,CategoryCreateView,CategoryDeleteView
from .views import PublisherListView,PublisherCreateView,PublisherDeleteView
from .views import uiView
urlpatterns = [

    #Teacher page
    path("",TeacherView.as_view(),name='teacher'),

    #home page
    # path("", HomeView.as_view(), name='home'),

    path('book_list.html',BookListView.as_view(), name = "book_list" ),
    path('book-create',BookCreateView.as_view(), name = "book_create" ),
    path('book-delete/<int:pk>/',BookDeleteView.as_view(), name = "book_delete" ),
    path('book-update/<int:pk>/',BookUpdateView.as_view(), name = "book_update"),
    path('book-detail/<int:pk>/',BookDetailView.as_view(), name = "book_detail" ),

    #Category
    path('category-list',CategoryListView.as_view(),name = "category_list"),
    path('category-create',CategoryCreateView.as_view(),name = "category_create"),
    path('category-delete/<int:pk>',CategoryDeleteView.as_view(),name = "category_delete"),

    #Publisher
    path('publisher-list',PublisherListView.as_view(),name = "publisher_list"),
    path('publisher-create',PublisherCreateView.as_view(),name = "publisher_create"),
    path('publisher-delete/<int:pk>',PublisherDeleteView.as_view(),name = "publisher_delete"),

    #Teacher
    path('ClassInfo',ClassInfoView.as_view(), name="class_info"),
    path('class-detial/<str:pk>/', ClassDetailView.as_view(), name="class_detail"),

    #ul
    re_path(r'^ui\.*', uiView, name='ui'),
]

