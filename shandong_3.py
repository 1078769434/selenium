import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# # 提取代理API接口，获取1个代理IP
# api_url = "http://v2.api.juliangip.com/dynamic/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no=1625922143116609&sign=94bdeba08458b5dc5a6ac5fd35c78bfb"
#
# # 获取API接口返回的代理IP
# proxy_ip = requests.get(api_url).text
#
# # 用户名密码认证(动态代理/独享代理)
# username = "18595492501"
# password = "limao2.22"
# proxies = {
# "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
# }

# 白名单方式（需提前设置白名单）
# proxies = {
#     "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
# }
model = {
    '基本信息':{

    },
    '办理信息':{

    },
'办理材料':{}
}

def get_page(url,driver,model):
    # response=requests.get(url=url,headers=headers)
    # response.encoding = 'UTF-8'  # 将编码设置为 UTF-8，或者您需要的任何其他编码
    #
    # content=response.text
    # print(content)
    driver.get(url)
    content = driver.page_source
    soup=BeautifulSoup(content,'html.parser')

    h3=soup.find('h3',class_='text-center') #事项名称
    title=h3.text
    # print(title)
    model['基本信息']['事项名称']=title
    th=soup.find('th',class_='text-center')#实施主体
    zhuti=th.text
    # print(zhuti)


    tr_tags=soup.find('table',class_='table table-bordered its-table-overview').find('tbody').find_all('tr')
    tr=tr_tags[0]
    second_td=tr.find_all('td')[0]
    text = second_td.get_text()
    # print(text)
    model['基本信息']['实施主体'] = text

    tr_tags_2 = soup.find('table',class_='table table-bordered its-table-overview').find('tbody').find_all('tr')
    tr_2 = tr_tags_2[5]
    second_th=tr_2.find_all('th')[1]
    text_2 = second_th.get_text()
    # print(text_2)
    td_2 = tr_2.find_all('td')[1]
    str_td_2=td_2.text

    str_td_1 =soup.find('td',class_='办理形式').string

    model['基本信息']['办理形式']=str_td_1

    #是否收费
    tr_12 = tr_tags_2[12]
    one_th = tr_12.find_all('th')[0].get_text()
    two_td = tr_12.find_all('td')[0].get_text()
    model['基本信息']['是否收费']=two_td

    #咨询方式
    tr_17 = tr_tags_2[17]
    zixun_th = tr_17.find('th').get_text()
    td_phone = tr_17.find('td')

    # 提取包含<br>标签的内容
    content_with_br = td_phone.get_text("\n", strip=True)

    # 移除 "电话咨询："
    phone_info = content_with_br.replace("电话咨询：", "")

    model['办理信息']['咨询方式'] = phone_info+"<br>"

    td=soup.find('td',class_='办理形式')
    #办理形式
    td_Text=td.text

    #受理地点、时间
    tr_19 = tr_tags_2[19]
    location_td = tr_19.find('td').get_text().replace('\n', '').replace('\t','')
    # print(location_td)
    location_pattern = r'受理地点：(.*?)办理窗口名称'
    #
    #
    #
    match = re.search(location_pattern, location_td)
    #
    #
    clean_location = match.group(1)
    # print(clean_location)



    time_br = tr_19.find('td').get_text().replace('\n', '').replace('\t','')
    # 使用正则表达式匹配受理时间
    time_pattern = r'受理时间：(.*?)\u2003'
    time_match = re.search(time_pattern, time_br)
    clean_time = time_match.group(1)

    model['办理信息']['办理时间'] = clean_time+"<br>"
    model['办理信息']['办理地点'] = clean_location+"<br>"
    # print(location_td,time_br)
    # print(td_Text,one_th,two_td)

    #办理材料
    all_tr=soup.find('div',id='sqcl').find('table',class_='table table-bordered').find('tbody').find_all('tr')
    # 遍历每个<tr>标签并获取其第一个<td>标签中的文本
    text_2 = ''
    for tr in all_tr:
        first_td = tr.find('td')  # 找到第一个<td>标签
        if first_td:
            text = first_td.get_text().replace('\n', '').replace('\t','')  # 获取文本内容
            text_2+=text
        else:
            print("未找到<td>标签")
    model['办理材料']['content'] = text_2.replace('\n', '').replace('\t','').replace('已关联电子证照','')
# all_td_1=all_tr[1].find_all('td')
# td_text_1=all_td_1[0].get_text()
#
# all_td_2=all_tr[2].find_all('td')
# td_text_2=all_td_2[0].get_text()
#
# all_td_3=all_tr[3].find_all('td')
# td_text_3=all_td_3[0].get_text()
#
# all_td_4=all_tr[4].find_all('td')
# td_text_4=all_td_4[0].get_text()

# print(td_text_1,td_text_2)
    print(model)
if __name__ == '__main__':
    url = 'http://whzwfw.sd.gov.cn/wh/icity/proinfo/index?id=99bb4f9fed-da69-4f3b-8b09-569abf279d95'

    headers = {
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':
            'gzip, deflate',
        'Accept-Language':
            'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control':
            'max-age=0',
        'Cookie':
            'ICITYSession=e4508a530f8c4eeaa70e992964bebe86; wondersLog_sdywtb_sdk=%7B%22persistedTime%22%3A1695877730832%2C%22updatedTime%22%3A1696563997391%2C%22sessionStartTime%22%3A1696563788782%2C%22sessionReferrer%22%3A%22%22%2C%22deviceId%22%3A%22dab93d8b91f11106f0de882f67e142a5-2766%22%2C%22LASTEVENT%22%3A%7B%22eventId%22%3A%22wondersLog_pv%22%2C%22time%22%3A1696563997391%7D%2C%22sessionUuid%22%3A5493791481539976%2C%22costTime%22%3A%7B%7D%7D',
        'Host':
            'whzwfw.sd.gov.cn',
        'Proxy-Connection':
            'keep-alive',
        'Upgrade-Insecure-Requests':
            '1',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55'
    }
    proxy = {
        'http': '58.220.95.54:9400'
    }
    # 创建ChromeOptions对象，并配置为无头模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 启用无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速

    # 创建Chrome浏览器实例
    driver = webdriver.Chrome(options=chrome_options)
    get_page(url,driver,model)