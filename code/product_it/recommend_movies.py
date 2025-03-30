# -*-coding:utf-8-*-
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "product.settings"
import django

django.setup()
from product.models import *
from math import sqrt, pow
import operator
from django.db.models import Subquery, Q, Count


# from django.shortcuts import render,render_to_response
class UserCf:

    # 获得初始化数据
    def __init__(self, all_user):
        self.all_user = all_user

    # 通过用户名获得列表，仅调试使用
    def getItems(self, username1, username2):
        return self.all_user[username1], self.all_user[username2]

    # 计算两个用户的皮尔逊相关系数
    def pearson(self, user1, user2):  # 数据格式为：物品id，浏览
        sum_xy = 0.0  # user1,user2 每项打分的的累加
        n = 0  # 公共浏览次数
        sum_x = 0.0  # user1 的打分总和
        sum_y = 0.0  # user2 的打分总和
        sumX2 = 0.0  # user1每项打分平方的累加
        sumY2 = 0.0  # user2每项打分平方的累加
        for movie1, score1 in user1.items():
            if movie1 in user2.keys():  # 计算公共的浏览次数
                n += 1
                sum_xy += score1 * user2[movie1]
                sum_x += score1
                sum_y += user2[movie1]
                sumX2 += pow(score1, 2)
                sumY2 += pow(user2[movie1], 2)
        if n == 0:
            # print("p氏距离为0")
            return 0
        molecule = sum_xy - (sum_x * sum_y) / n  # 分子
        denominator = sqrt((sumX2 - pow(sum_x, 2) / n) * (sumY2 - pow(sum_y, 2) / n))  # 分母
        if denominator == 0:
            return 0
        r = molecule / denominator
        return r

    # 计算与当前用户的距离，获得最临近的用户
    def nearest_user(self, current_user, n=1):
        distances = {}
        # 用户，相似度
        # 遍历整个数据集
        for user, rate_set in self.all_user.items():
            # 非当前的用户
            if user != current_user:
                distance = self.pearson(self.all_user[current_user], self.all_user[user])
                # 计算两个用户的相似度
                distances[user] = distance
        closest_distance = sorted(
            distances.items(), key=operator.itemgetter(1), reverse=True
        )
        # 最相似的N个用户
        print("closest user:", closest_distance[:n])
        return closest_distance[:n]

    # 给用户推荐电商产品
    def recommend(self, username, n=3):
        recommend = {}
        nearest_user = self.nearest_user(username, n)
        for user, score in dict(nearest_user).items():  # 最相近的n个用户
            for movies, scores in self.all_user[user].items():  # 推荐的用户的电商产品列表
                if movies not in self.all_user[username].keys():  # 当前username没有看过
                    if movies not in recommend.keys():  # 添加到推荐列表中
                        recommend[movies] = scores * score
        # 对推荐的结果按照电商产品
        # 浏览次数排序
        return sorted(recommend.items(), key=operator.itemgetter(1), reverse=True)


# 基于用户的推荐
def recommend_by_user_id(user_id):
    print("\n===== 基于用户的商品推荐 =====")
    print(f"为用户 {user_id} 推荐商品...")
    
    # 1. 获取用户偏好
    user_prefer = UserTagPrefer.objects.filter(user_id=user_id).order_by('-score')
    current_user = User.objects.get(id=user_id)
    
    # 2. 用户未评分情况处理 
    if current_user.rate_set.count() == 0:
        print("\n该用户暂无评分记录")
        if user_prefer.exists():
            print("基于用户标签偏好进行推荐:")
            # 基于用户标签偏好进行推荐
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
            recommended = [p[1] for p in weighted_products[:15]]
        else:
            print("无标签偏好,返回热门商品:")
            recommended = Product.objects.annotate(
                weight=Count('collect') + Count('rate')
            ).order_by('-weight')[:15]

        for i, product in enumerate(recommended, 1):
            print(f"\n{i}. {product.name}")
            print(f"   价格: ¥{product.price}")
            print(f"   店铺: {product.shop_name}")
            print(f"   评论数: {product.d_rate_nums}")
            print(f"   标签: {[t.name for t in product.tags.all()]}")
        return recommended

    # 3. 获取相似用户
    similar_users = User.objects.filter(
        rate__product__in=current_user.rate_set.values('product')
    ).annotate(
        common_count=Count('rate__product')
    ).filter(
        common_count__gte=2  # 至少有2个共同评分
    ).order_by('-common_count')[:10]

    # 4. 计算用户相似度并加权推荐
    user_cf = UserCf(all_user={})
    recommendations = {}
    
    for similar_user in similar_users:
        similarity = user_cf.pearson(
            dict(current_user.rate_set.values_list('product_id', 'mark')),
            dict(similar_user.rate_set.values_list('product_id', 'mark'))
        )
        
        if similarity <= 0:
            continue
            
        # 获取相似用户评分高的商品
        for rate in similar_user.rate_set.filter(mark__gte=4):
            if rate.product_id not in recommendations:
                recommendations[rate.product_id] = 0
            recommendations[rate.product_id] += similarity * rate.mark

    # 5. 结合商品属性进行最终排序
    recommended_products = Product.objects.filter(id__in=recommendations.keys())
    weighted_recommendations = []
    
    for product in recommended_products:
        base_score = recommendations[product.id]
        # 考虑商品的收藏数和评分
        final_score = base_score * (1 + 0.1 * product.collect.count() + 0.1 * product.rate_set.count())
        weighted_recommendations.append((final_score, product))

    weighted_recommendations.sort(key=lambda x: -x[0])
    
    print("\n为您推荐以下商品:")
    final_products = [item[1] for item in weighted_recommendations[:15]]
    for i, product in enumerate(final_products, 1):
        print(f"\n{i}. {product.name}")
        print(f"   价格: ¥{product.price}")
        print(f"   店铺: {product.shop_name}")
        print(f"   评论数: {product.d_rate_nums}")
        print(f"   标签: {[t.name for t in product.tags.all()]}")
        print("   " + "="*20)

    print("\n===== 推荐完成 =====\n")
    return final_products


def recommend_by_item_id(current_product_id=None, k=15):
    """基于当前浏览商品标签的推荐"""
    # print("\n===== 基于标签的商品推荐 =====")
    
    # 获取当前浏览的商品
    try:
        current_product = Product.objects.get(id=current_product_id) if current_product_id else None
    except Product.DoesNotExist:
        current_product = None
    
    if not current_product:
        print("\n无当前浏览商品,返回热门商品排行:")
        hot_products = Product.objects.annotate(
            popular=Count('collect') + Count('rate')
        ).order_by('-popular')[:k]
        return hot_products

    # 输出当前浏览商品信息  
    # print(f"\n当前浏览商品: {current_product.name}")
    # print(f"价格: ¥{current_product.price}")
    # print(f"店铺: {current_product.shop_name}")
    # print(f"评论数: {current_product.d_rate_nums}")
    # print(f"所属标签: {[t.name for t in current_product.tags.all()]}")

    # 基于当前商品标签推荐同类商品
    current_tags = current_product.tags.all()
    
    similar_products = Product.objects.filter(
        tags__in=current_tags
    ).exclude(
        id=current_product.id  # 排除当前商品
    ).annotate(
        tag_count=Count('tags', filter=Q(tags__in=current_tags)),
        popular=Count('collect') + Count('rate')
    ).filter(
        tag_count__gt=0  
    ).order_by(
        '-tag_count',
        '-popular'
    )[:k]

    # print("\n为您推荐以下同类商品:")
    # for i, p in enumerate(similar_products, 1):
    #     print(f"\n{i}. {p.name}")
    #     print(f"   价格: ¥{p.price}")
    #     print(f"   店铺: {p.shop_name}") 
    #     print(f"   评论数: {p.d_rate_nums}")
    #     print(f"   共同标签数: {p.tag_count}")
    #     print(f"   所属标签: {[t.name for t in p.tags.all()]}")
    #     print("   " + "="*20)

    # print("\n===== 推荐完成 =====\n")
    return similar_products


if __name__ == '__main__':
    # 测试用户id为1的推荐
    recommend_by_item_id(current_product_id=1)
