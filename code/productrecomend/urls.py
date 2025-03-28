"""productrecomend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from product import views
#用于前后端连接
urlpatterns = [
                  # path('admin/', views.admin_view, name='admin'),
                  # path("admin/", admin.site.urls, name='admin'),
                  path('admin/', admin.site.urls),
                  path("", views.index, name="index"),
                  path("login/", views.login, name="login"),
                  path("register/", views.register, name="register"),
                  path("logout/", views.logout, name="logout"),
                  path("all_product/", views.index, name="all_product"),
                  path("product/<int:product_id>/", views.product, name="product"),
                  path("score/<int:product_id>/", views.score, name="score"),
                  path("comment/<int:product_id>/", views.make_comment, name="comment"),
                  path("like_comment/<int:comment_id>/<int:product_id>/", views.like_comment, name="like_comment"),
                  path("unlike_comment/<int:comment_id>/<int:product_id>/", views.unlike_comment, name="unlike_comment"),
                  path("collect/<int:product_id>/", views.collect, name="collect"),
                  path("decollect/<int:product_id>/", views.decollect, name="decollect"),
                  path("personal/", views.personal, name="personal"),
                  path("mycollect/", views.mycollect, name="mycollect"),
                  path("my_comments/", views.my_comments, name="my_comments"),
                  path("my_rate/", views.my_rate, name="my_rate"),
                  path("delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
                  path("delete_rate/<int:rate_id>", views.delete_rate, name="delete_rate"),
                  path("hot_product/", views.hot_product, name="hot_product"), # 收藏最多
                  path("most_view/", views.most_view, name="most_view"),
                  path("most_mark/", views.most_mark, name="most_mark"),
                  path("latest_product/", views.latest_product, name="latest_product"),
                  # path("mark_sort/", views.mark_sort, name="mark_sort"),
                  path("search/", views.search, name="search"),
                  path("all_tags/", views.all_tags, name="all_tags"),
                  path("data_analysis/", views.data_analysis, name="data_analysis"),
                  path("one_tag/<int:one_tag_id>/", views.one_tag, name="one_tag"),
                  path("choose_tags/", views.choose_tags, name="choose_tags"),
                  path("user_recommend/", views.user_recommend, name="user_recommend"),#用户推荐
                  path("item_recommend/", views.item_recommend, name="item_recommend"),#物品推荐
                  path("comment_analysis/", views.comment_analysis, name="comment_analysis"),#评分分布统计
                  path("tags_analysis/", views.tags_analysis, name="tags_analysis"),#电商产品表统计
                  path("years_analysis/", views.years_analysis, name="years_analysis"),#电商产品上映年份及数量统计
                  path("years_analysis_dash/", views.years_analysis_dash, name="years_analysis_dash"),#电商产品上映年份及数量统计，大屏使用
                  path("word_analysis/", views.word_analysis, name="word_analysis"),#电商产品标签词云分析
                  path("dashboard/", views.dashboard, name="dashboard"),#大屏看板
                  path("total_data/", views.total_data, name="total_data"),#查看总量
                  path("country_analysis/", views.country_analysis, name="country_analysis"),#各国电商产品分布
                  path("percent_analysis/", views.percent_analysis, name="percent_analysis"),#各国电商产品分布
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

admin.site.site_header = '跨境电商产品推荐与展示系统'
admin.site.index_title = '首页-跨境电商产品推荐与展示系统'
admin.site.site_title = '跨境电商产品推荐与展示系统'
