#解決png不能下載的問題
import requests as req
import bs4
import os
from concurrent.futures import ThreadPoolExecutor
import random
from time import sleep

#set useer-agent and cookie
#設定user-agent和cookie
def basic_setting():
    global u_a, cookie, your_path
    u_a = input('User-Agent: ')
    cookie = input('Cookie: ')
    your_path = input("Your Director's Path: ")

def main():
    global your_path
    #change director to nhentai
    #移動路徑到nhentai
    os.chdir(your_path)
    
    #get number
    #取得要下載的車號
    nh_list = get_nh_num()
    
    #get images
    #取得圖片
    get_img(nh_list)

#get number
#取得要下載的車號
def get_nh_num():
    print('\nEnter以開始下載')
    nh_list = []
    
    while True:
        nh_number = input('想下載的車號是: ')
        if nh_number == '':
            return nh_list
        elif len(nh_number)==6:
            nh_list.append(nh_number)
        else:
            print('請輸入六位數')

#get images
#取得圖片
def get_img(nh_list):
    global u_a, cookie, your_path
    #one by one
    #一次一篇漫畫
    for nh_number in nh_list:
        print(nh_number)
        os.chdir(your_path)
        src_list = []
        #set dir
        #建立資料夾
        if not os.path.exists(nh_number):
            os.mkdir(nh_number)
            os.chdir(f'{your_path}\{nh_number}')

            #get preview src
            #取得預覽圖片的src
            nh_url = f'https://nhentai.net/g/{nh_number}/'
            r = req.get(nh_url, headers = {'User-Agent': u_a, 'Cookie': cookie})
            soup = bs4.BeautifulSoup(r.text, 'html.parser')

            img_data = soup.find_all('img', attrs = {'class':'lazyload'})
            for img in img_data:
                img_preview = img['data-src']

                #get true src
                #取得圖片的src
                if 'thumb' not in img_preview and 'cover' not in img_preview:
                    id = img_preview.split('/')[-2]
                    page_type = img_preview.split('/')[-1]
                    page_type = page_type.replace('t', '')

                    acc = [3, 5, 7]
                    accc = random.choice(acc)
                    src = f'https://i{accc}.nhentai.net/galleries/{id}/{page_type}'
                
                    #add to download list
                    #加到下載列表裡
                    if src not in src_list:
                        src_list.append(src)
                        #print(src)
            
            
            #download images
            #開執行緒下載
            print('開始下載')
            with ThreadPoolExecutor(max_workers = 5) as exe:
                exe.map(download, src_list)
            print(f'{nh_number}下載完畢')
            sleep(3)
        
        else:
            print(f'{nh_number}下載過了')

#download image
#下載圖片
def download(src):
    global u_a, cookie
    print(src)
    #get image
    #取得圖片
    r = req.get(src, headers = {'User-Agent':u_a, 'Cookie':cookie})

    #filename
    #檔名
    filename = src.split('/')[-1]

    #download
    #二進制寫入
    with open(filename, 'wb') as f:
        f.write(r.content)
    
    sleept = [0.5, 0.7, 1.0]
    slt = random.choice(sleept)
    sleep(slt)
    


if __name__ == '__main__':
    basic_setting()
    main()
