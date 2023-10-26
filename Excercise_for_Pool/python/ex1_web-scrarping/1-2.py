import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ユーザーエージェントを指定
options = Options()
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57")

# Chromeドライバーを作成
driver = webdriver.Chrome(options=options)


driver.implicitly_wait(10)


#店舗検索一覧の１ページを開く
page1='https://r.gnavi.co.jp/area/jp/rs/'
driver.get(page1)


# 住所を都道府県、市区町村、番地に分割する関数
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
#店の情報のリストを格納するリスト   
BIG_LIST=[]   
for p in range(0,3):
    # 現在のページのURLを取得
    
    page = driver.current_url
    print("Current Page:", page)  # 現在のページのURLを表示
    s= driver.find_elements(By.XPATH, '//div[@class="style_title___HrjW"]/a')
    
    for i in range(len(s)):
        # 再度要素を取得
        s = driver.find_elements(By.XPATH, '//div[@class="style_title___HrjW"]/a')
        element = s[i]
        element.click()
        #「店舗名」
        name=driver.find_element(By.ID,'info-name').text
        #「電話番号」
        phone_number=driver.find_element(By.CLASS_NAME,'number').text
        #「メールアドレス」
        mail=''
        #アドレス所得
        address=driver.find_element(By.CLASS_NAME,'region').text
        #「都道府県」#「市区町村」#「番地」
    
    
        prefecture, city, block= split_address(address)
        if prefecture is None:
            prefecture = ''
        if city is None:
            city = ''
        if block is None:
            block = ''

        #「建物名」
        try:
            building_name = driver.find_element(By.CLASS_NAME, 'locality').text
        except:
            building_name = None
        #「URL」
        URL=driver.current_url
        #「SSL」
        is_ssl = URL.startswith('https')

        if is_ssl:
            SSL='TRUE'
        else:
            SSL='FALSE'
        store_infomations=[name,phone_number,mail,prefecture,city,block,building_name,URL,SSL]
        BIG_LIST.append(store_infomations)
        #店舗ページに戻る
        back_botton=driver.find_element(By.ID,"gn_info-breadcrumbs-htpback-go")
        back_botton.click()
    #次のページに行くボタン    
    next_button = driver.find_element(By.CLASS_NAME,"style_nextIcon__M_Me_")
    next_button.click()  
driver.quit()
#データフレームに      
df=pd.DataFrame(BIG_LIST,columns=['店舗名','電話番号','メールアドレス','都道府県','市区町村','番地','建物名','URL','SSL'])
df_50=df.head(50)  
csv_filename='1-2.csv'
df_50.to_csv(csv_filename, encoding='utf-8-sig', index=False,sep=',')  # index=Falseでインデックスを保存しない
