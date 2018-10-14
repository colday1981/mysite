import markdown
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import Blog,BlogType


def blog_common_data(request, blogs_all_list):
    paginator=Paginator(blogs_all_list,settings.EACH_PAGE_NUM)            #每10页进行分页
    page_num=request.GET.get('page',1)                               #获取url页面参数(get请求)
    page_of_blogs=paginator.get_page(page_num)
    current_page_num=page_of_blogs.number             #获取当前页码
    #获取当前页码前后两页的页码范围
    page_range=list(range(max(current_page_num -2,1),current_page_num))+list(range(current_page_num, min(current_page_num+2,paginator.num_pages)+1))
    #加上省略标记
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1]>=2:
        page_range.append('...')

    #加上首页和尾页
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)
    #获取日期归档对应的博客数量
    blog_dates=Blog.objects.dates('created_time','month',order="DESC")
    blog_dates_dict={}
    for blog_date in blog_dates:
        blog_count=Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count

    context={}
    context['blogs']=page_of_blogs.object_list
    context['page_of_blogs']=page_of_blogs
    context['page_range']=page_range
    context['blog_types']=BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates']=blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list=Blog.objects.all()
    context = blog_common_data(request, blogs_all_list)
    return render_to_response('blog_list.html', context)


def blog_with_type(request, blog_type_pk):
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
    context=blog_common_data(request, blogs_all_list)
    context['blog_type']=blog_type
    return render_to_response('blog_with_type.html', context)

def blog_with_date(request, year, month):
    blogs_all_list=Blog.objects.filter(created_time__year=year, created_time__month=month)
    context=blog_common_data(request,blogs_all_list)
    context['blogs_with_date']='%s年%s月'% (year, month)
    return render_to_response('blog_with_date.html', context)

def blog_detail(request, blog_pk):
    context={}
    blog=get_object_or_404(Blog, pk=blog_pk)
    blog.content=markdown.markdown(blog.content,
                                   extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc',])
    context['blog']=blog
    context['previous_blog']=Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog']=Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog']=blog
    return render_to_response('blog_detail.html', context)


# Create your views here.
