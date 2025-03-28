import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import WordCloud
import jieba

def build_wordcloud():
    # 读取电商产品推荐数据，假设数据存储在Products.csv文件中，包含电商产品名称和推荐标签两列
    df = pd.read_csv('csv_data/product.csv')

    # 提取电商产品名称
    names = df['name']

    # 将电商产品名称拼接为字符串
    text = ' '.join(names)

    # 使用jieba进行中文分词
    seg_list = jieba.cut(text)
    seg_text = ' '.join(seg_list)

    # 统计词频
    words = seg_text.split()
    word_counts = {}
    for word in words:
        if word not in word_counts:
            word_counts[word] = 0
        word_counts[word] += 1

    # 创建词云图
    wordcloud = (
        WordCloud()
            .add("", list(word_counts.items()), word_size_range=[20, 150])
            .set_global_opts(title_opts=opts.TitleOpts(title="电商产品名称词云图"))
    )

    # 生成词云图并保存
    wordcloud.render("static/product_wordcloud.html")
