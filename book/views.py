import os
# import pandas as pd
import json
from django import template
from django.db.models.functions import ExtractMonth, ExtractWeek, TruncMonth, TruncWeek
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, DeleteView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Book, Category, Publisher, UserActivity, Class, Teacher
from .models import Buybook, Reference_Book
# from .models import UserActivity,Profile,Member,BorrowRecord
from django.apps import apps
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Count
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.contrib import admin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import BookCreateEditForm, PubCreatedEditForm, MemberCreateEditForm, ProfileForm, BorrowRecordCreateForm

from util.useful import get_n_days_ago, create_clean_dir, change_col_format
# from .groups_permissions import check_user_group,user_groups,check_superuser,SuperUserRequiredMixin,allowed_groups
# from .custom_filter import get_item
from datetime import date, timedelta, datetime
#
# from django.forms.models import model_to_dict
# from django.core.paginator import Paginator
# from django.contrib.contenttypes.models import ContentType
# from comment.models import Comment
# from comment.forms import CommentForm
# from notifications.signals import notify
# from .notification import send_notification
import logging
from pyecharts.charts import Bar
from django_echarts.views.backend import EChartsBackendView


logger = logging.getLogger(__name__)

TODAY = get_n_days_ago(0, "%Y%m%d")
PAGINATOR_NUMBER = 5
allowed_models = ['Category', 'Publisher', 'Book', 'Member', 'UserActivity', 'BorrowRecord']


#
#

# ui
def uiView(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))
    context['segment'] = load_template
    html_template = loader.get_template('home/' + load_template)
    print('html_template=', html_template)
    return HttpResponse(html_template.render(context, request))

def echartview(request):
    context = {}
    return render(request,"Teacher/Class/ClassEchart.html")

# 404
def page_not_found(request, exception):
    return render(request, 'home/page-404.html')


# 500
def page_error(request):
    return render(request, 'home/page-500.html')


# HomePage
class HomeView( TemplateView):
    template_name = "index.html"
    context = {}

    def get(self, request, *args, **kwargs):
        book_count = Book.objects.aggregate(Sum('quantity'))['quantity__sum']

        data_count = {"book": book_count,
                      # "member": Member.objects.all().count(),
                      "category": Category.objects.all().count(),
                      "publisher": Publisher.objects.all().count(), }

        # user_activities = UserActivity.objects.order_by("-created_at")[:5]
        # user_avatar = {e.created_by: Profile.objects.get(user__username=e.created_by).profile_pic.url for e in
        #                user_activities}
        # short_inventory = Book.objects.order_by('quantity')[:5]
        #
        # current_week = date.today().isocalendar()[1]
        # new_members = Member.objects.order_by('-created_at')[:5]
        # new_members_thisweek = Member.objects.filter(created_at__week=current_week).count()
        # lent_books_thisweek = BorrowRecord.objects.filter(created_at__week=current_week).count()

        # books_return_thisweek = BorrowRecord.objects.filter(end_day__week=current_week)
        # number_books_return_thisweek = books_return_thisweek.count()
        # new_closed_records = BorrowRecord.objects.filter(open_or_close=1).order_by('-closed_at')[:5]

        self.context['data_count'] = data_count
        # self.context['recent_user_activities'] = user_activities
        # self.context['user_avatar'] = user_avatar
        # self.context['short_inventory'] = short_inventory
        # self.context['new_members'] = new_members
        # self.context['new_members_thisweek'] = new_members_thisweek
        # self.context['lent_books_thisweek'] = lent_books_thisweek
        # self.context['books_return_thisweek'] = books_return_thisweek
        # self.context['number_books_return_thisweek'] = number_books_return_thisweek
        # self.context['new_closed_records'] = new_closed_records

        return render(request, self.template_name, self.context)


# TeacherPage
class TeacherView(TemplateView):
    template_name = "Teacher/Teacher_Index.html"
    context = {}

    # users = User.objects.all()
    # for user in users:
    #     print(user.get_username(),user.is_superuser)
    def get(self, request, *args, **kwargs):
        book_count = Book.objects.aggregate(Sum('quantity'))['quantity__sum']
        class11 = Class.objects.filter(grade=1,semester=1).count()
        class12 = Class.objects.filter(grade=1,semester=2).count()
        class21 = Class.objects.filter(grade=2,semester=1).count()
        class22 = Class.objects.filter(grade=2,semester=2).count()
        class31 = Class.objects.filter(grade=3,semester=1).count()
        class32 = Class.objects.filter(grade=3,semester=2).count()
        class41 = Class.objects.filter(grade=4,semester=1).count()
        class42 = Class.objects.filter(grade=4,semester=2).count()

        data_count = {"book": book_count,
                      "class11": class11,
                      "class12": class12,
                      "class21": class21,
                      "class22": class22,
                      "class31": class31,
                      "class32": class32,
                      "class41": class41,
                      "class42": class42,
                      "referencebook":Reference_Book.objects.all().count() ,
                      "teacher":Teacher.objects.all().count(),
                      "user_total":User.objects.all().count(),
                      # "member": Member.objects.all().count(),
                      "category": Category.objects.all().count(),
                      "publisher": Publisher.objects.all().count(), }
        user = self.request.user.username
        group = None

        if user:
            user = User.objects.get(username=user)
            groups = user.groups.all()
            if groups:
                group = groups[0]
        # user_activities = UserActivity.objects.order_by("-created_at")[:5]
        # user_avatar = {e.created_by: Profile.objects.get(user__username=e.created_by).profile_pic.url for e in
        #                user_activities}
        # short_inventory = Book.objects.order_by('quantity')[:5]
        #
        # current_week = date.today().isocalendar()[1]
        # new_members = Member.objects.order_by('-created_at')[:5]
        # new_members_thisweek = Member.objects.filter(created_at__week=current_week).count()
        # lent_books_thisweek = BorrowRecord.objects.filter(created_at__week=current_week).count()

        # books_return_thisweek = BorrowRecord.objects.filter(end_day__week=current_week)
        # number_books_return_thisweek = books_return_thisweek.count()
        # new_closed_records = BorrowRecord.objects.filter(open_or_close=1).order_by('-closed_at')[:5]

        self.context['data_count'] = data_count
        self.context['group'] = group
        # self.context['user_total'] = self.
        # self.context['recent_user_activities'] = user_activities
        # self.context['user_avatar'] = user_avatar
        # self.context['short_inventory'] = short_inventory
        # self.context['new_members'] = new_members
        # self.context['new_members_thisweek'] = new_members_thisweek
        # self.context['lent_books_thisweek'] = lent_books_thisweek
        # self.context['books_return_thisweek'] = books_return_thisweek
        # self.context['number_books_return_thisweek'] = number_books_return_thisweek
        # self.context['new_closed_records'] = new_closed_records

        return render(request, self.template_name, self.context)


# ClassInfoPage
class ClassInfoView( TemplateView):
    model = Class
    context_object_name = 'classes'
    template_name = 'Teacher/Class/Class_info.html'
    # TO DO  使用教职工工号搜索相关课程
    # 目前先展示所有课程
    search_value = ""
    order_field = "classid"
    class_total = ""

    def get_queryset(self):
        search = self.request.GET.get("search")
        orderby = self.request.GET.get("orderby")
        user = self.request.user.username
        group = None
        if user:
            users = User.objects.get(username=user)
            groups = users.groups.all()
            if groups:
                group = groups[0]
        if orderby:
            all_class = Class.objects.all().order_by(orderby)
            self.order_field = orderby
        else:
            all_class = Class.objects.all().order_by(self.order_field)
        if search:
            all_class = all_class.filter(
                Q(classname__icontains=search) | Q(classid__icontains=search)
            )
            self.search_value = search
        self.class_total = all_class.count()
        paginator = Paginator(all_class, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        classes = paginator.get_page(page)
        return classes

    def get_context_data(self, *args, **kwargs):
        context = super(ClassInfoView, self).get_context_data(*args, **kwargs)
        context['class_total'] = self.class_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        # context['group'] = self.group
        return context

#MyClassView
class MyClassView(LoginRequiredMixin,TemplateView):
    login_url = 'login'
    model = Class
    context_object_name = 'classes'
    template_name = 'Teacher/Class/My_Class.html'
    search_value =""
    order_field = "classid"
    class_total =""

    def get_queryset(self):
        search = self.request.GET.get("search")
        orderby = self.request.GET.get("orderby")
        user = self.request.user.username
        group = None
        if user:
            users = User.objects.get(username=user)
            groups = users.groups.all()
            if groups:
                group = groups[0]
        if orderby:
            all_class = Class.objects.all().order_by(orderby)
            self.order_field = orderby
        else:
            all_class = Class.objects.all().order_by(self.order_field)
        all_class = all_class.filter(
            teacher_id=user)

        if search:
            all_class = all_class.filter(
                Q(classname__icontains=search) | Q(classid__icontains=search)
            )
            self.search_value = search
        self.class_total = all_class.count()
        paginator = Paginator(all_class, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        classes = paginator.get_page(page)
        return classes

    def get_context_data(self, *args, **kwargs):
        context = super(MyClassView, self).get_context_data(*args, **kwargs)
        context['class_total'] = self.class_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        # context['group'] = self.group
        return context



class BuybookView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    model = Buybook
    context_object_name = 'buybooks'
    template_name = 'Admin/BuyBook/buybook.html'
    # TO DO  使用教职工工号搜索相关课程
    # 目前先展示所有课程
    search_value = ""
    order_field = ""
    class_total = ""

    def get_queryset(self):
        search = self.request.GET.get("search")
        orderby = self.request.GET.get("orderby")
        if orderby:
            all_book = Buybook.objects.all().order_by(orderby)
            self.order_field = orderby
        else:
            # all_book = Buybook.objects.all().order_by(self.order_field)
            all_book = Buybook.objects.all()
        if search:
            all_book = all_book.filter(
                Q(bookname__icontains=search) | Q(author__icontains=search) | Q(coursename__icontains=search) |
                Q(teacher__teacher_name__icontains=search)
            )
            # mywhere = ""
            self.search_value = search
        self.class_total = all_book.count()
        paginator = Paginator(all_book, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        classes = paginator.get_page(page)
        return classes

    def get_context_data(self, *args, **kwargs):
        context = super(BuybookView, self).get_context_data(*args, **kwargs)
        context['class_total'] = self.class_total
        print(context['class_total'])
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


class BuyView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    model = Buybook
    context_object_name = 'buybooks'
    template_name = 'Admin/BuyBook/edit_buybook.html'
    # TO DO  使用教职工工号搜索相关课程
    # 目前先展示所有课程
    search_value = ""
    order_field = ""
    class_total = ""

    def get_queryset(self):
        search = self.request.GET.get("search")
        orderby = self.request.GET.get("orderby")
        bookid = self.request.GET['bookid']
        if orderby:
            all_book = Buybook.objects.all().order_by(orderby)
            self.order_field = orderby
        else:
            # all_book = Buybook.objects.all().order_by(self.order_field)
            all_book = Buybook.objects.all()
            book = Buybook.objects.get(id=bookid)
            book.status = '1'
            book.save()
        if search:
            all_book = all_book.filter(
                Q(bookname__icontains=search) | Q(author__icontains=search) | Q(coursename__icontains=search) |
                Q(teacher__teacher_name__icontains=search)
            )
            # mywhere = ""
            self.search_value = search
        self.class_total = all_book.count()
        paginator = Paginator(all_book, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        classes = paginator.get_page(page)
        return classes

    def get_context_data(self, *args, **kwargs):
        context = super(BuyView, self).get_context_data(*args, **kwargs)
        context['class_total'] = self.class_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


# APPLYBOOK
def Applybook(request):
    return render(request, 'Admin/BuyBook/apply_book.html')


def EditApplyBook(request):
    context = {}
    if request.method == 'GET':
        info = Buybook()
        info.isbn = request.GET.get('Inputisbn')
        if info.isbn != None:
            # info.teacher = request.GET.get('Inputteacherid')
            info.coursecode = request.GET.get('Inputcourseid')
            info.coursename = request.GET.get('Inputcoursename')
            info.bookname = request.GET.get('Inputbookname')
            info.author = request.GET.get('Inputauthor')
            info.save()

        context['info'] = '添加成功'
        context['teacher'] = info.teacher
        return render(request, 'Admin/BuyBook/edit_apply_book.html')


class EditcourseView(LoginRequiredMixin, DetailView):
    model = Class
    context_object_name = 'course'
    template_name = 'Admin/Course/edit_course.html'
    login_url = 'login'

    # comment_form = CommentForm()

    def get_object(self, queryset=None):
        obj = super(EditcourseView, self).get_object(queryset=queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_class_name = self.get_object().classname
        reference_book = Reference_Book.objects.all()
        context['reference'] = reference_book
        logger.info(f'Book  <<{current_class_name}>> retrieved from db')
        return context


def Updatecourse(request):
    # if request.user.is_authenticated():
    context = {}
    # admin.site.register([Class])
    courseid = request.POST['courseid']
    course = Class.objects.get(classid=courseid)
    course.classname = request.POST['coursename']
    course.semester = request.POST['semester']
    course.grade = request.POST['grade']
    course.description = request.POST['description']
    course.file = request.FILES.get('uploadfile')
    course.reference = request.POST['reference']
    # course.teacher_id = request.GET['teacher']
    # with open(course.file.name, 'wb') as f:
    #     for i in course.file:
    #         f.write(i)
    course.save()
    return render(request, 'Admin/Course/update_course.html')


class ReferenceListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    model = Buybook
    context_object_name = 'referencelist'
    template_name = 'Admin/reference/referencelist.html'
    # TO DO  使用教职工工号搜索相关课程
    # 目前先展示所有课程
    search_value = ""
    order_field = ""
    class_total = ""

    def get_queryset(self):
        search = self.request.GET.get("search")
        orderby = self.request.GET.get("orderby")
        if orderby:
            reference_book = Reference_Book.objects.all().order_by(orderby)
            self.order_field = orderby
        else:
            # all_book = Buybook.objects.all().order_by(self.order_field)
            reference_book = Reference_Book.objects.all()
        if search:
            reference_book = reference_book.filter(
                Q(ISBN__icontains=search) | Q(bookname__icontains=search) | Q(author__icontains=search)
                # Q(class_id__icontains=search)
            )
            # mywhere = ""
            self.search_value = search
        self.class_total = reference_book.count()
        paginator = Paginator(reference_book, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        classes = paginator.get_page(page)
        return classes

    def get_context_data(self, *args, **kwargs):
        context = super(ReferenceListView, self).get_context_data(*args, **kwargs)
        context['class_total'] = self.class_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


# ClassDetailPage
class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class
    context_object_name = 'clasz'
    template_name = 'Teacher/Class/class_detail.html'
    login_url = 'login'

    # comment_form = CommentForm()

    def get_object(self, queryset=None):
        obj = super(ClassDetailView, self).get_object(queryset=queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_class_name = self.get_object().classname
        logger.info(f'Book  <<{current_class_name}>> retrieved from db')
        return context

# Echarts
class EchartView(EChartsBackendView):
    template_name = 'Teacher/Class/ClassEchart.html'

    def get_echarts_instance(self, *args, **kwargs):
        bar = Bar("Chart","Vise Title")
        bar.add("课程",["Sememter 1","Semeter 2"],[20 , 10])
        return bar




#
# # Global Serch
# @login_required(login_url='login')
# def global_serach(request):
#     search_value = request.POST.get('global_search')
#     if search_value =='':
#         return HttpResponseRedirect("/")
#
#     r_category = Category.objects.filter(Q(name__icontains=search_value))
#     r_publisher = Publisher.objects.filter(Q(name__icontains=search_value)|Q(contact__icontains=search_value))
#     r_book = Book.objects.filter(Q(author__icontains=search_value)|Q(title__icontains=search_value))
#     r_member = Member.objects.filter(Q(name__icontains=search_value)|Q(card_number__icontains=search_value)|Q(phone_number__icontains=search_value))
#     r_borrow = BorrowRecord.objects.filter(Q(borrower__icontains=search_value)|Q(borrower_card__icontains=search_value)|Q(book__icontains=search_value))
#
#
#     context={
#         'categories':r_category,
#         'publishers':r_publisher,
#         'books':r_book,
#         'members':r_member,
#         'records':r_borrow,
#     }
#
#     return render(request, 'book/global_search.html',context=context)

#
# # Chart
# class ChartView(LoginRequiredMixin,TemplateView):
#     template_name = "book/charts.html"
#     login_url = 'login'
#     context={}
#
#     def get(self,request, *args, **kwargs):
#
#         top_5_book= Book.objects.order_by('-quantity')[:5].values_list('title','quantity')
#         top_5_book_titles = [b[0] for b in top_5_book ]
#         top_5_book__quantities = [b[1] for b in top_5_book ]
#         # print(top_5_book_titles,top_5_book__quantities)
#
#         top_borrow = Book.objects.order_by('-total_borrow_times')[:5].values_list('title','total_borrow_times')
#         top_borrow_titles = [b[0] for b in top_borrow ]
#         top_borrow_times = [b[1] for b in top_borrow ]
#
#         r_open = BorrowRecord.objects.filter(open_or_close=0).count()
#         r_close = BorrowRecord.objects.filter(open_or_close=1).count()
#
#         m = Member.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(c=Count('id'))
#         months_member = [e['month'].strftime("%m/%Y") for e  in m]
#         count_monthly_member= [e['c'] for e in m]
#
#
#         self.context['top_5_book_titles']=top_5_book_titles
#         self.context['top_5_book__quantities']=top_5_book__quantities
#         self.context['top_borrow_titles']=top_borrow_titles
#         self.context['top_borrow_times']=top_borrow_times
#         self.context['r_open']=r_open
#         self.context['r_close']=r_close
#         self.context['months_member']=months_member
#         self.context['count_monthly_member']=count_monthly_member
#
#
#         return render(request, self.template_name, self.context)

# Book
class BookListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Book
    context_object_name = 'books'
    template_name = 'book/book_list.html'
    search_value = ""
    order_field = "id"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        print("orderby=", order_by)
        if order_by:
            all_books = Book.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_books = Book.objects.all().order_by(self.order_field)
        if search:
            all_books = all_books.filter(
                Q(title__icontains=search) | Q(author__icontains=search)
            )
            # mywhere = ""
            self.search_value = search
        self.count_total = all_books.count()
        paginator = Paginator(all_books, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        books = paginator.get_page(page)
        return books

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book/book_detail.html'
    login_url = 'login'

    # comment_form = CommentForm()

    def get_object(self, queryset=None):
        obj = super(BookDetailView, self).get_object(queryset=queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_book_name = self.get_object().title
        logger.info(f'Book  <<{current_book_name}>> retrieved from db')
        # comments = Comment.objects.filter(book=self.get_object().id)
        # related_records = BorrowRecord.objects.filter(book=current_book_name)
        # context['related_records'] = related_records
        # context['comments'] = comments
        context['comment_form'] = self.comment_form
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    login_url = 'login'
    # form_class=BookCreateEditForm
    template_name = 'book/book_create.html'

    def post(self, request, *args, **kwargs):
        super(BookCreateView, self).post(request)
        new_book_name = request.POST['title']
        messages.success(request, f"New Book << {new_book_name} >> Added")
        # UserActivity.objects.create(created_by=self.request.user.username,target_model=self.model.__name__,detail =f"Create {self.model.__name__} << {new_book_name} >>")
        return redirect('book_list')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    login_url = 'login'
    form_class = BookCreateEditForm
    template_name = 'book/book_update.html'

    def post(self, request, *args, **kwargs):
        current_book = self.get_object()
        current_book.updated_by = self.request.user.username
        current_book.save(update_fields=['updated_by'])
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="warning",
                                    target_model=self.model.__name__,
                                    detail=f"Update {self.model.__name__} <<{current_book.title} >>")
        return super(BookUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        title = form.cleaned_data['title']
        messages.warning(self.request, f"Update << {title} >> success")
        return super().form_valid(form)


# class BookUpdateView(LoginRequiredMixin,UpdateView):
#     model = Book
#     login_url = 'login'
#     # form_class=BookCreateEditForm
#     template_name = 'book/book_update.html'
#
#     def post(self, request, *args, **kwargs):
#         current_book = self.get_object()
#         current_book.updated_by=self.request.user.username
#         current_book.save(update_fields=['updated_by'])
#         UserActivity.objects.create(created_by=self.request.user.username,
#             operation_type="warning",
#             target_model=self.model.__name__,
#             detail =f"Update {self.model.__name__} << {current_book.title} >>")
#         return super(BookUpdateView, self).post(request, *args, **kwargs)
#
#     def form_valid(self, form):
#       title=form.cleaned_data['title']
#       messages.warning(self.request, f"Update << {title} >> success")
#       return super().form_valid(form)

class BookDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        book_pk = kwargs["pk"]
        delete_book = Book.objects.get(pk=book_pk)
        model_name = delete_book.__class__.__name__
        messages.error(request, f"Book << {delete_book.title} >> Removed")
        delete_book.delete()
        # UserActivity.objects.create(created_by=self.request.user.username,
        #     operation_type="danger",
        #     target_model=model_name,
        #     detail =f"Delete {model_name} << {delete_book.title} >>")
        return HttpResponseRedirect(reverse("book_list"))



