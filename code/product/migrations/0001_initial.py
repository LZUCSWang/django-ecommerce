# Generated by Django 2.2.10 on 2023-07-16 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='电商产品名称')),
                ('price', models.IntegerField(default=0, verbose_name='电商产品价格')),
                ('shop_name', models.CharField(max_length=200, verbose_name='店铺名称')),
                ('shop_type', models.CharField(max_length=200, verbose_name='店铺类型')),
                ('d_rate_nums', models.IntegerField(verbose_name='用户评价数')),
                ('origin_product_link', models.URLField(max_length=1000, null=True, verbose_name='产品链接')),
                ('origin_image_link', models.URLField(max_length=255, null=True, verbose_name='爬取原图地址')),
                ('image_link', models.FileField(max_length=255, upload_to='cover', verbose_name='封面图片')),
                ('imdb_link', models.URLField(null=True)),
            ],
            options={
                'verbose_name': '电商产品',
                'verbose_name_plural': '电商产品',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '前台用户',
                'verbose_name_plural': '前台用户',
            },
        ),
        migrations.CreateModel(
            name='UserTagPrefer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Tags', verbose_name='标签名')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='product.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '用户偏好',
                'verbose_name_plural': '偏好',
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.FloatField(verbose_name='评分')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('Product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='电商产品id')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '评分信息',
                'verbose_name_plural': '评分信息',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='collect',
            field=models.ManyToManyField(blank=True, to='product.User', verbose_name='收藏者'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='product.Tags', verbose_name='标签'),
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Comment', verbose_name='评论')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '评论点赞',
                'verbose_name_plural': '评论点赞',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='电商产品'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.User', verbose_name='用户'),
        ),
    ]
