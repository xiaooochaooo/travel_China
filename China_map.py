import pandas as pd
import numpy as np
from pyecharts.charts import Map, Page
from pyecharts import options as opts
import os
import re


def draw(province):
    return (
        Map()
        .add(
            series_name='旅游指数',
            data_pair=province,
            maptype='china'
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title='中国地图',subtitle='数据来自携程旅行，部分地区数据缺失'),
            visualmap_opts=opts.VisualMapOpts(max_=9, min_=3, is_piecewise=False)
        )
    )


def draww(city):
    (
        Page(layout=Page.DraggablePageLayout)
        .add(draw(city))
        .save_resize_html("中国地图.html", cfg_file="./chart_config.json", dest="中国地图.html")

    )


if __name__ == '__main__':
    province = []
    dir_list = os.listdir('E:\\travel_China\\Data')
    for i in dir_list:
        sub_dir = os.listdir(r'E:\travel_China\Data' + '\\' + i)
        sum_score = 0
        # print(i)
        for j in sub_dir:
            if re.match(r'.+景点信息.csv$', j):
                data = pd.read_csv(r'E:\travel_China\Data' + '\\' + i + '\\' + j)
                if sum_score == 0:
                    sum_score = data['hot'].mean(axis=0)
                else:
                    sum_score = (sum_score + data['hot'].mean(axis=0)) / 2
        province.append([i, round(sum_score, 1)])
    # print(province)
    draww(province)
