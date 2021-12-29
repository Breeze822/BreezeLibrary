# Author :Breeze_xylf
# Date :
from django.contrib import admin
from django.urls import path, include, re_path
from .views import TeacherView,ClassInfoView,ClassDetailView,MyClassView
from .views import HomeView,BookListView,BookCreateView,BookDeleteView,BookDetailView,BookUpdateView
from .views import uiView, BuybookView, ReferenceListView, Applybook, EditcourseView
from .views import BuyView
from .views import EchartView,echartview
from . import views
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

    #Teacher
    path('ClassInfo', ClassInfoView.as_view(), name="class_info"),
    path('class_detail/<str:pk>/', ClassDetailView.as_view(), name="class_detail"),
    path('my_class', MyClassView.as_view(),name='my_class'),

    #ul
    re_path(r'^ui\.*', uiView, name='ui'),
    #echarts
    # path('echarts/',EchartView,name='echart'),
    path('echart/',echartview),

    #Admin
    path('buybook/', BuybookView.as_view(), name='buybook'),
    path('buy/', BuyView.as_view(), name='buy'),
    path('edit_apply_book', views.EditApplyBook, name='edit_apply_book'),

    #Booklist
    path('booklist/', ReferenceListView.as_view(), name='referencelist'),

    #Apply
    path('apply_book/', Applybook, name='apply_book'),

    #Edit
    path('edit_course/<str:pk>/', EditcourseView.as_view(), name='edit_course'),
    #Update
    # path('update_course/<str:pk>/', UpdatecourseView.as_view(), name='update_course'),
    path('update_course/', views.Updatecourse, name='update_course'),

]

