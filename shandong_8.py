import os
import re
import pandas as pd
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

def get_excel():


    # 读取Excel文件
    df = pd.read_excel('超链接信息.xlsx')

    # 将每列数据存储在一个大列表中
    all_data = []
    for column in df.columns:
        all_data.extend(df[column].tolist())

    # 打印整个大列表
    # # 打印每列的前几个元素
    # for i, column in enumerate(column_names):
    #     print(f'列名: {column}')
    #     print(column_data[i])
    #     print('\n')
    return all_data
get_url=get_excel()
# get_url_2=get_url[2000:]

model = {

}
df=pd.DataFrame()
def get_page(get_url,driver,model,df):

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

    # print(content)
    # for url in get_url:
    for index, url in enumerate(get_url):
        print(f"Processing URL {index + 1}: {url}")
        # 在这里执行与 URL 相关的操作
        try:
            # driver.get(url)
            # content = driver.page_source
            response = requests.get(url=url, headers=headers)
            response.encoding = 'UTF-8'  # 将编码设置为 UTF-8，或者您需要的任何其他编码

            content = response.text
            soup=BeautifulSoup(content,'html.parser')

            try:
                h3=soup.find('h3',class_='text-center') #事项名称
                title=h3.text
                # print(title)
                # model['基本信息']['事项名称']=title
                model['问题1']=title
                model['表格:事项名称']=title
            except:
                model['问题1'] = ''
                model['表格:事项名称'] = ''
            try:
                th=soup.find('th',class_='text-center')#实施主体
                zhuti=th.text
                # print(zhuti)


                tr_tags=soup.find('table',class_='table table-bordered its-table-overview').find('tbody').find_all('tr')
                tr=tr_tags[0]
                second_td=tr.find_all('td')[0]
                text = second_td.get_text()
                # print(text)
                model['表格:实施主体'] = text
            except:
                model['表格:实施主体'] = ''
            try:
                tr_tags_2 = soup.find('table',class_='table table-bordered its-table-overview').find('tbody').find_all('tr')
                tr_2 = tr_tags_2[5]
                second_th=tr_2.find_all('th')[1]
                text_2 = second_th.get_text()
                # print(text_2)
                td_2 = tr_2.find_all('td')[1]
                str_td_2=td_2.text

                str_td_1 =soup.find('td',class_='办理形式').string

                model['表格:办理形式']=str_td_1
            except:
                model['表格:办理形式']=''
            try:
                #是否收费
                tr_12 = tr_tags_2[12]
                one_th = tr_12.find_all('th')[0].get_text()
                two_td = tr_12.find_all('td')[0].get_text()
                # if two_td=='1':
                #     two_td='是'
                # if two_td = '0':
                #     two_td='否'
                model['表格:是否收费']=two_td
                model['表格:查看详情(url)']=url
            except:
                model['表格:是否收费'] = ''
                model['表格:查看详情(url)'] = ''
            try:
                #咨询方式
                tr_17 = tr_tags_2[17]
                zixun_th = tr_17.find('th').get_text()
                td_phone = tr_17.find('td')

                # 提取包含<br>标签的内容
                content_with_br = td_phone.get_text("\n", strip=True)

                # 移除 "电话咨询："
                phone_info = content_with_br.replace("电话咨询：", "")

                model['表格:咨询方式'] = phone_info+"<br>"
            except:
                model['表格:咨询方式'] = ''
            try:
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

                model['表格:办理时间'] = clean_time+"<br>"
                model['表格:办理地点	'] = clean_location+"<br>"
                # print(location_td,time_br)
                # print(td_Text,one_th,two_td)
            except:
                model['表格:办理时间'] = ''
                model['表格:办理地点	'] = ''
            try:
                #办理材料
                all_tr=soup.find('div',id='sqcl').find('table',class_='table table-bordered').find('tbody').find_all('tr')
                # 遍历每个<tr>标签并获取其第一个<td>标签中的文本
                text_2 = ''

                for tr in all_tr:
                    first_td = tr.find('td')  # 找到第一个<td>标签
                    if first_td:
                        text = first_td.get_text()  # 获取文本内容

                        text_2+=text
                        # print(text_2)
                    else:
                        print("未找到<td>标签")
                model['表格:材料'] = text_2.replace('\n', '').replace('\t','').replace('已关联电子证照','').replace(' ','').replace('材料名称填写','').replace('材料名称','')
            except:
                model['表格:材料'] = '暂无'

            print(model)


            # # 将新的数据附加到现有DataFrame
            df = df.append(model, ignore_index=True)
            #
            # # 保存为Excel文件
            df.to_excel('my_url_data_20.xlsx', index=False)

        except:
            continue
if __name__ == '__main__':
    url = ['http://whzwfw.sd.gov.cn/wh/icity/proinfo/index?id=99bb4f9fed-da69-4f3b-8b09-569abf279d95',
           'http://whzwfw.sd.gov.cn/wh/icity/proinfo/index?id=05491f6f-9ef9-4339-b33d-cb0ba6305103']

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
    get_page(get_url,driver,model,df)


def get_main_page(driver,start_page,end_page):
    for page_number in range(start_page, end_page + 1):
        url = f"http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={page_number}&pg=20&cateid=1103&tpl=1361&checkError=1"
        driver.get(url)
        print(f'第{page_number}页')

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        print(content)
        a=soup.find('div',class_='jcse-news-title').find_all('a')[0]

        href=a.get('href')
        link='http://www.wendeng.gov.cn/jsearchfront/'+href
        print(link)
# get_main_page(driver,1,2)

def get_new_url():
    new_url='http://www.wendeng.gov.cn/jsearchfront/interfaces/cateSearch.do'
    data={
        'websiteid':'371081000500000',
        'q':'',
        'p':1,
        'pg':20,
        'cateid':'1103',
          'tpl':'1361',
        'checkError':'1'
    }
    r=requests.post(new_url,data=data)
    print(r.text)

