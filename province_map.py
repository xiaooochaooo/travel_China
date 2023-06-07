import pandas as pd
from pyecharts.charts import Map, Pie, Tab, WordCloud
from pyecharts import options as opts
import os
import re
import get_tfidf


def draw_province_map(province, city):
    return (
        Map()
        .add(
            series_name='旅游指数',
            maptype=province,
            data_pair=city
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=province + '地图'),
            visualmap_opts=opts.VisualMapOpts(max_=9, min_=3, is_piecewise=False)
        )
    )


def draw_province_pie(province, city):
    return (
        Pie(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(animation=True, animation_easing='elasticOut', animation_delay=1000))
        )
        .add(
            '旅游指数',
            city,
            rosetype="radius",
            center=['50%', '60%'],
            label_opts=opts.LabelOpts(formatter="{b}: {d}%")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=province + '旅游指数饼图', pos_left='center', pos_top='50'),
        )
    )


# 1. 加载停用词：读取停用词文件

def load_stops(file_path):
    """
        1. 打开文件，需要指定文件的编码格式（utf-8）
        2. 按行读取文件中的每隔单词：readlines
        3. 遍历文件中的每个单词：把单词存放到一个新建的列表中
        4. 返回停用词列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    words = []
    # 3.  遍历文件中的每个单词
    for line in lines:
        line = line.strip('\n')
        words.append(line)
    return words


def draw_province_wordcloud(province, word):
    return (
        WordCloud()
        .add(series_name=province + "热点分析", data_pair=word, word_size_range=[50, 100], shape='circle')
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )


def draw(province, city, word):
    tab = Tab()
    tab.add(draw_province_map(province, city), '城市图')
    tab.add(draw_province_pie(province, city), '饼图')
    tab.add(draw_province_wordcloud(province, word), '词云图')
    tab.render(province + "可视化.html")


if __name__ == '__main__':
    word_stop = load_stops('./stop_words.utf8')
    dir_list = os.listdir('E:\\travel_China\\Data')
    for province in dir_list:
        subdir = os.listdir(r'E:\travel_China\Data' + '\\' + province)
        citys = []
        dic = {}
        for city in subdir:
            if re.match(r'.+景点信息.csv$', city):
                data = pd.read_csv(r'E:\travel_China\Data' + '\\' + province + '\\' + city)
                citys.append([city[:-8], max(data['hot'])])
            else:
                words = get_tfidf.get_res(r'E:\travel_China\Data' + '\\' + province + '\\' + city)
        if province in ['黑龙江省', '内蒙古自治区']:
            province = province[:3]
        else:
            province = province[:2]
        print(citys)
        draw(province, citys, words)
