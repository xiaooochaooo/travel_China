from selenium import webdriver
from selenium.webdriver import ChromeOptions
import pandas as pd
from SaveToTxt import save_txt
import numpy as np

# 声明浏览器对象并定义URLURL包含一个page参数代表当前页面
option = ChromeOptions()
option.add_argument('--headless')  # 加上“headless”参数后运行时就不会跳出一个新的浏览器窗口
browser = webdriver.Chrome(options=option)
browser.implicitly_wait(5)  # implicitly_wait是设置隐式延时等待，防止出现找不到元素的错误


def crawlData(url):
    url_table = pd.DataFrame(columns=['city', 'url', 'province'])
    browser.get(url)
    province = browser.find_element_by_css_selector(
        '#__next > div > div > div > div.city-module > div.city-selector > div:nth-child(2) > div.city-selector-tab-main > div:nth-child(18) > div.city-selector-tab-main-city-title').get_attribute(
        'textContent')
    parents = browser.find_elements_by_css_selector(
        '#__next > div > div > div > div.city-module > div.city-selector > div:nth-child(2) > div.city-selector-tab-main > div:nth-child(18) > div.city-selector-tab-main-city-list > a')
    for parent in parents:
        new_list = pd.DataFrame(
            {'city': [parent.get_attribute('title')], 'url': [parent.get_attribute('href')], 'province': [province]})
        url_table = pd.concat([url_table, new_list])
    for i, data in url_table.iterrows():
        sight_table = pd.DataFrame(columns=['name', 'city', 'hot', 'score', 'address', 'url', 'image_url'])
        url = data['url'].replace('place', 'sight')
        browser.get(url)
        # print(url)
        parents = browser.find_elements_by_css_selector(
            '#content > div.ttd2_background > div > div.des_wide.f_right > div > div.list_wide_mod2 > div')
        for parent in parents:
            name = parent.find_elements_by_css_selector('div.rdetailbox > dl > dt > a:nth-child(2)')
            if len(name) != 0:
                sub_url = name[0].get_attribute('href')
                name = name[0].get_attribute('textContent')
                hot = parent.find_element_by_css_selector(
                    'div.rdetailbox > dl > dt > a.hot_score > b.hot_score_number').get_attribute('textContent')
                score = parent.find_elements_by_css_selector('div.rdetailbox > ul > li:nth-child(1) > a > strong')
                if len(score) != 0:
                    score = score[0].get_attribute('textContent')
                else:
                    score = 0
                address = parent.find_element_by_css_selector('div.rdetailbox > dl > dd.ellipsis').get_attribute(
                    'textContent')
                image = parent.find_element_by_css_selector('div.leftimg > a > img').get_attribute('src')
                new_list = pd.DataFrame({'name': [name],
                                        'city': [data['city']],
                                        'hot': [float(hot)],
                                        'score': [float(score)],
                                        'address': [address],
                                        'url': [sub_url],
                                        'image_url': [image]})
                sight_table = pd.concat([sight_table, new_list])
        sight_table.replace(0, np.NaN, inplace=True)
        sight_table.fillna(round(sight_table['score'].mean(), 1))
        sight_table.to_csv(f"{data['city']}景点信息.csv")
        for j, d in sight_table.iterrows():
            sub_url = d['url']
            browser.get(sub_url)
            print(sub_url)
            parents = browser.find_elements_by_css_selector(
                '#__next > div.poiDetailPageWrap > div > div.moduleWrap > div.mainModule > div.detailModuleRef > div > div:nth-child(2) > div > div > p')
            introduce = ['\n', '\n']
            for parent in parents:
                introduce.append(parent.get_attribute('textContent'))
            save_txt(r'E:\travel_China' + '\\' + data['province'] + '.txt', introduce)
        print(f"{data['city']}爬取完毕")


if __name__ == '__main__':
    root_url = 'https://you.ctrip.com/'
    crawlData(root_url)
