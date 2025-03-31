import json
import random
import pandas as pd
import os
from functools import wraps
import logging

logger = logging.getLogger('django')

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.db.models.functions import ExtractYear
from django.contrib.staticfiles import finders

from product_it.cache_keys import USER_CACHE, ITEM_CACHE
from product_it.recommend_movies import recommend_by_user_id, recommend_by_item_id
from .forms import *
from product.word_cloud import build_wordcloud
from product.templatetags.grav_tag import gravatar

def Products_paginator(Products, page):
    paginator = Paginator(Products, 12)
    if page is None:
        page = 1
    Products = paginator.page(page)
    return Products


# from django.urls import HT
# json response
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json;"
        super(JSONResponse, self).__init__(content, **kwargs)


# 登录功能
def login(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            result = User.objects.filter(username=username)
            if result:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session["login_in"] = True
                    request.session["user_id"] = user.id
                    request.session["name"] = username
                    # 用户第一次注册，需要选标签
                    new = request.session.get('new')
                    if new:
                        tags = Tags.objects.all()
                        print('goto choose tag')
                        return render(request, 'choose_tag.html', {'tags': tags})
                    return redirect(reverse("index"))
                else:
                    return render(
                        request, "login.html", {"form": form, "message": "密码错误"}
                    )
            else:
                return render(
                    request, "login.html", {"form": form, "message": "账号不存在"}
                )
    else:
        form = Login()
        return render(request, "login.html", {"form": form})


# 注册功能
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        error = None
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password2"]
            email = form.cleaned_data["email"]
            User.objects.create(
                username=username,
                password=password,
                email=email,
            )
            request.session['new'] = 'true'
            # 根据表单数据创建一个新的用户
            return redirect(reverse("login"))  # 跳转到登录界面
        else:
            return render(
                request, "register.html", {"form": form, "error": error}
            )  # 表单验证失败返回一个空表单到注册页面
    form = RegisterForm()
    return render(request, "register.html", {"form": form})


def logout(request):
    if not request.session.get("login_in", None):  # 不在登录状态跳转回首页
        return redirect(reverse("index"))
    request.session.flush()  # 清除session信息
    print('注销')
    return redirect(reverse("index"))


def login_in(func):  # 验证用户是否登录
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        is_login = request.session.get("login_in")
        if is_login:
            return func(*args, **kwargs)
        else:
            return redirect(reverse("login"))

    return wrapper


# Create your views here.
def index(request):
    order = request.POST.get("order") or request.session.get('order')
    request.session['order'] = order
    if order == 'collect':
        products = Product.objects.annotate(collectors=Count('collect')).order_by('-collectors')
        print(products.query)
        title = '收藏排序'
    elif order == 'rate':
        products = Product.objects.all().annotate(marks=Avg('rate__mark')).order_by('-marks')
        title = '评分排序'
    else:
        products = Product.objects.order_by('-price')
        title = '价格排序'
    paginator = Paginator(products, 20)
    new_list = Product.objects.all()[:20]
    current_page = request.GET.get("page", 1)
    products = paginator.page(current_page)
    return render(request, 'items.html', {'products': products, 'new_list': new_list, 'title': title})


# 电商产品详情
def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.num += 1
    product.save()
    comments = product.comment_set.order_by("-create_time")
    user_id = request.session.get("user_id")
    product_rate = Rate.objects.filter(product=product).all().aggregate(Avg('mark'))  # 电商产品评分
    if product_rate:
        product_rate = product_rate['mark__avg']
    else:
        product_rate = 0
    if user_id is not None:
        user_rate = Rate.objects.filter(product=product, user_id=user_id).first()
        user = User.objects.get(pk=user_id)
        is_collect = product.collect.filter(id=user_id).first()
    for comment in comments:
        print(f"User email: {comment.user.email}")
        print(f"Gravatar URL: {gravatar(comment.user.email, size=48)}")
    return render(request, "product.html", locals())


def search(request):  # 搜索
    if request.method == "POST":  # 如果搜索界面
        key = request.POST["search"]
        request.session["search"] = key  # 记录搜索关键词解决跳页问题
    else:
        key = request.session.get("search")  # 得到关键词
    products = Product.objects.filter(
        Q(name__icontains=key)
    )  # 进行内容的模糊搜索
    page_num = request.GET.get("page", 1)
    products = Products_paginator(products, page_num)
    return render(request, "items.html", {"products": products, 'title': '搜索结果'})


# 所有标签
def all_tags(request):
    tags = Tags.objects.all()
    return render(request, "all_tags.html", {'all_tags': tags})


# 数据分析
def data_analysis(request):
    tags = Tags.objects.all()
    return render(request, "data_analysis.html", {'all_tags': tags})


# 一个标签
def one_tag(request, one_tag_id):
    tag = Tags.objects.get(id=one_tag_id)
    products = tag.product_set.all()
    page_num = request.GET.get("page", 1)
    products = Products_paginator(products, page_num)
    return render(request, "items.html", {"products": products, 'title': tag.name})


# 收藏最多
def hot_product(request):
    page_number = request.GET.get("page", 1)  # 分页
    Products = Product.objects.annotate(user_collector=Count('collect')).order_by('-user_collector')[:10]  # 查出所有电商产品，按收藏人数排序
    Products = Products_paginator(Products[:10], page_number)
    return render(request, "items.html", {"Products": Products, "title": "收藏最多"})  # 返回给items.html


# 评分最多
def most_mark(request):
    page_number = request.GET.get("page", 1)
    Products = Product.objects.all().annotate(num_mark=Count('rate')).order_by('-num_mark')
    Products = Products_paginator(Products, page_number)
    return render(request, "items.html", {"Products": Products, "title": "评分最多"})


# 浏览最多
def most_view(request):
    page_number = request.GET.get("page", 1)
    Products = Product.objects.annotate(user_collector=Count('num')).order_by('-num')
    Products = Products_paginator(Products, page_number)
    return render(request, "items.html", {"Products": Products, "title": "浏览最多"})


# 最新电商产品
def latest_product(request):
    product_list = Product.objects.order_by("-id")[:10]
    json_products = [product.to_dict(fields=['name', 'image_link', 'id', 'shop_name', 'd_rate_nums']) for product in product_list]
    return HttpResponse(json.dumps(json_products), content_type="application/json")


# 修改个人信息
@login_in
def personal(request):
    user = User.objects.get(id=request.session.get("user_id"))
    if request.method == "POST":
        form = Edit(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            request.session['name'] = user.username
            return render(
                request, "personal.html", {"message": "修改成功!", "form": form, 'title': '我的信息', 'user': user}
            )
        else:
            return render(
                request, "personal.html", {"message": "修改失败", "form": form, 'title': '我的信息', 'user': user}
            )
    form = Edit(instance=user)
    return render(request, "personal.html", {"user": user, 'form': form, 'title': '我的信息'})


@login_in
@csrf_exempt
def choose_tags(request):
    tags_name = json.loads(request.body)
    user_id = request.session.get('user_id')
    for tag_name in tags_name:
        tag = Tags.objects.filter(name=tag_name.strip()).first()
        UserTagPrefer.objects.create(tag_id=tag.id, user_id=user_id, score=5)
    request.session.pop('new')
    return redirect(reverse("index"))


@login_in
# 给电商产品进行评论
def make_comment(request, product_id):
    user = User.objects.get(id=request.session.get("user_id"))
    product = Product.objects.get(id=product_id)
    comment = request.POST.get("comment")
    Comment.objects.create(user=user, product=product, content=comment)
    return redirect(reverse("product", args=(product_id,)))


@login_in
# 展示我的评论的地方
def my_comments(request):
    user = User.objects.get(id=request.session.get("user_id"))
    comments = user.comment_set.all()
    print('comment:', comments)
    return render(request, "my_comment.html", {"item": comments})


# 给评论点赞
@login_in
def like_comment(request, comment_id, product_id):
    user_id = request.session.get("user_id")
    LikeComment.objects.get_or_create(user_id=user_id, comment_id=comment_id)
    return redirect(reverse("product", args=(product_id,)))


# 取消点赞
@login_in
def unlike_comment(request, comment_id, Product_id):
    user_id = request.session.get("user_id")
    LikeComment.objects.filter(user_id=user_id, comment_id=comment_id).delete()
    return redirect(reverse("product", args=(Product_id,)))


@login_in
def delete_comment(request, comment_id):
    Comment.objects.get(pk=comment_id).delete()
    return redirect(reverse("my_comments"))


@login_in
# 给电商产品打分 在打分的时候清除缓存
def score(request, product_id):
    user_id = request.session.get("user_id")
    # user = User.objects.get(id=user_id)
    product = Product.objects.get(id=product_id)
    score = float(request.POST.get("score"))
    get, created = Rate.objects.get_or_create(user_id=user_id, product=product, defaults={"mark": score})
    if created:
        for tag in product.tags.all():
            prefer, created = UserTagPrefer.objects.get_or_create(user_id=user_id, tag=tag, defaults={'score': score})
            if not created:
                # 更新分数
                prefer.score += (score - 3)
                prefer.save()
        print('create data')
        # 清理缓存
        user_cache = USER_CACHE.format(user_id=user_id)
        item_cache = ITEM_CACHE.format(user_id=user_id)
        cache.delete(user_cache)
        cache.delete(item_cache)
        print('cache deleted')
    return redirect(reverse("product", args=(product_id,)))


# 我的评分
@login_in
def my_rate(request):
    user = User.objects.get(id=request.session.get("user_id"))
    rate = user.rate_set.all()
    return render(request, "my_rate.html", {"item": rate})


def delete_rate(request, rate_id):
    Rate.objects.filter(pk=rate_id).delete()
    return redirect(reverse("my_rate"))


# 收藏电商产品
@login_in
def collect(request, product_id):
    user = User.objects.get(id=request.session.get("user_id"))
    product = Product.objects.get(id=product_id)
    product.collect.add(user)
    product.save()
    return redirect(reverse("product", args=(product_id,)))


# 取消收藏电商产品
@login_in
def decollect(request, Product_id):
    user = User.objects.get(id=request.session.get("user_id"))
    product = Product.objects.get(id=Product_id)
    product.collect.remove(user)
    # product.rate_set.count()
    product.save()
    return redirect(reverse("product", args=(Product_id,)))


# 我的收藏
@login_in
def mycollect(request):
    user = User.objects.get(id=request.session.get("user_id"))
    product = user.product_set.all()
    return render(request, "mycollect.html", {"item": product})


# 基于用户推荐
def user_recommend(request):
    user_id = request.session.get("user_id")
    print("用户推荐，user_id:", user_id)
    if user_id is None:
        # 未登录用户返回随机推荐
        product_list = Product.objects.order_by('?')[:3]
    else:
        # 获取用户标签偏好
        user_prefer = UserTagPrefer.objects.filter(user_id=user_id).order_by('-score')
        print(user_prefer)
        if user_prefer.exists():
            # 基于标签偏好推荐
            tag_weights = {p.tag_id: p.score for p in user_prefer}
            products = Product.objects.all()
            weighted_products = []
            
            for product in products:
                score = 0
                for tag in product.tags.all():
                    score += tag_weights.get(tag.id, 0)
                if score > 0:
                    weighted_products.append((score, product))
            
            weighted_products.sort(key=lambda x: (-x[0], -x[1].collect.count()))
            product_list = [p[1] for p in weighted_products[:15]]
        else:
            # 无标签偏好时返回热门商品
            product_list = Product.objects.annotate(
                weight=Count('collect') + Count('rate')
            ).order_by('-weight')[:15]

    json_products = [product.to_dict(fields=['name', 'image_link', 'id', 'shop_name', 'd_rate_nums']) 
                    for product in product_list]
    random.shuffle(json_products)
    return HttpResponse(json.dumps(json_products[:3]), content_type="application/json")


# 基于物品推荐
def item_recommend(request):
    """基于当前浏览商品的标签推荐相似商品"""
    current_product_id = request.GET.get('product_id')
    # print("当前浏览商品ID:", current_product_id)
    
    if not current_product_id:
        # 没有当前商品时返回随机商品
        product_list = Product.objects.order_by('?')[:3]
    else:
        # 使用缓存提高性能
        cache_key = f'item_similar_{current_product_id}'
        product_list = cache.get(cache_key)
        
        if product_list is None:
            # 调用推荐函数,只传入商品ID
            product_list = recommend_by_item_id(current_product_id=current_product_id)
            cache.set(cache_key, product_list, 60 * 5)  # 缓存5分钟
            # print('设置商品推荐缓存')
        # else:
        #     print('命中商品推荐缓存')

    # 转换为JSON格式并随机打乱顺序
    json_products = [product.to_dict(fields=['name', 'image_link', 'id', 'shop_name', 'd_rate_nums']) 
                    for product in product_list]
    random.shuffle(json_products)
    
    # 打印推荐结果
    # print('推荐商品:', [(p['name'], p['id']) for p in json_products[:3]])
    return HttpResponse(json.dumps(json_products[:3]), content_type="application/json")


# 数据分析

def read_csv_data():
    """读取产品CSV数据"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_data', 'product.csv')
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

# 电商产品表统计图
def tags_analysis(request): 
    """商品分类统计"""
    try:
        df = read_csv_data()
        if df is not None:
            # 统计各标签数量
            tag_counts = df['tag'].value_counts()
            
            data = [{'name': tag, 'value': int(count)}
                    for tag, count in tag_counts.items()]
            return JsonResponse(data, safe=False)
    except Exception as e:
        print(f"Error in tags_analysis: {e}")
        return JsonResponse([], safe=False)

# 电商产品不同标签及平均价格
def years_analysis(request):
    """返回各品类平均价格"""
    try:
        df = read_csv_data()
        if df is not None:
            # 计算各标签的平均价格
            avg_prices = df.groupby('tag')['price'].mean()
            
            data = [{
                'key': tag,
                'value': round(float(price), 2)
            } for tag, price in avg_prices.items()]
            return JsonResponse(data, safe=False)
    except Exception as e:
        print(f"Error in years_analysis: {e}")
        return JsonResponse([], safe=False)

# 词云分析
def word_analysis(request):
    # 生成词云
    build_wordcloud()
    context = {'wordcloud_file': 'product_wordcloud.html'}
    return render(request, 'wordcloud.html', context)