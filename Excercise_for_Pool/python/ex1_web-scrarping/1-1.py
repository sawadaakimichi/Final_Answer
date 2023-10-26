#使用するモジュール
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
# ユーザーエージェント文字列
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57"

#グルナビのurl
url="https://r.gnavi.co.jp/"
#リクエストを送信
headers = {'User-Agent': user_agent}

res = requests.get(url,headers=headers)
soup=BeautifulSoup(res.text,'html.parser')
url_list=[]
for x in range(1,4):
    url_list.append(f'https://r.gnavi.co.jp/area/jp/rs/?p={x}')
    
Big_list=[]
import time
 # 正規表現を使用して住所を分割する関数
def split_address(address):
           
            pattern = r'(.+?[都道府県|都|道|府|県])(.+?)([\d\-]+)'
            match = re.match(pattern, address)
            if match:
                prefecture = match.group(1).strip()
                city = match.group(2).strip()
                block = match.group(3).strip()
                return prefecture, city, block
            else:
                return None, None, None           
#1-3ページでURLを取得し、それぞれの店舗情報を取り出す、
for x in url_list:
    url=x
    time.sleep(3)
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    restaurant_list=soup.find('div',class_="style_resultRestaurant__WhVwP")
    a_tag2=restaurant_list.find_all('a',class_="style_titleLink__oiHVJ")
    restaurant_link_list=[x['href']for x in a_tag2]
#urlを１つずつ調べる    
    for y in restaurant_link_list:
        url=y
        time.sleep(3)
        res= requests.get(url)
        res.encoding = res.apparent_encoding
        soup=BeautifulSoup(res.text,'html.parser')
        #店舗名
        name=soup.find('p',class_="fn org summary").string
        #電話番号
        phone_number=soup.find('span', class_="number").string
        #メール
        mail=soup.find('a', href=True, text='お問い合わせ')
        if mail is None:
            mail = ''
        #住所を取得
        address=soup.find('span', class_="region").string
        #住所を分割
        prefecture, city, block= split_address(address)
        if prefecture is None:
            prefecture = ''
        if city is None:
            city = ''
        if block is None:
            block = ''
        #建物名    
        building_name_tag = soup.find('span', class_="locality")
        building_name = building_name_tag.string if building_name_tag else ''
        #ssl
        is_ssl = url.startswith('https')

        if is_ssl:
            SSL='TRUE'
        else:
            SSL='FALSE'
        #店の情報
        shop_list=[name,phone_number,mail,prefecture,city,block,building_name,url,SSL]
        #店の情報のリスト
        Big_list.append(shop_list)
#データフレイム
df=pd.DataFrame(Big_list,columns=['店舗名','電話番号','メールアドレス','都道府県','市区町村','番地','建物名','URL','SSL'])

df_50=df.head(50)
#csvfile 
csv_filename = '1-1.csv'  # 保存するCSVファイル名
df_50.to_csv(csv_filename, encoding='utf-8-sig', index=False,sep=',')  # index=Falseでインデックスを保存しない
