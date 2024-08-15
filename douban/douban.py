import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

print("start！")

# 创建保存图片的文件夹
if not os.path.exists('images'):
    os.makedirs('images')

# 定義豆瓣照片页面的 URL 模板
# 點進藝人照片總攬內，去看網址，把personage/後面數字換成想要的目標藝人數字，其餘不動
url_template = "https://www.douban.com/personage/27482492/photos/?start={}&sortby=like"

# 定义要抓取的页码
pages_to_crawl = [120]  # 抓取頁數 1=0、2=30、3=60以此類推

# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://www.douban.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

for start in pages_to_crawl:
    url = url_template.format(start)
    response = requests.get(url, headers=headers)
    
    # 如果请求成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到 <ul class="pics"> 标签
        pics_list = soup.find('ul', class_='pics')
        if pics_list:
            # 在 <ul class="pics"> 标签内找到所有的 <li> 标签
            list_items = pics_list.find_all('li')
            
            for index, li in enumerate(list_items):
                # 在 <li> 标签内查找 <a> 标签
                a_tag = li.find('a', href=True)
                if a_tag:
                    # 获取大图页面 URL
                    photo_page_url = "https://www.douban.com" + a_tag['href']
                    print(f"Photo page URL: {photo_page_url}")  # 调试输出
                    
                    # 从大图页面提取实际大图 URL
                    try:
                        img_response = requests.get(photo_page_url, headers=headers)
                        if img_response.status_code == 200:
                            img_soup = BeautifulSoup(img_response.text, 'html.parser')
                            # 查找 <div class="photo-wp"> 中的 <img> 标签
                            img_tag = img_soup.find('div', class_='photo-wp').find('img')
                            if img_tag and 'src' in img_tag.attrs:
                                large_img_url = img_tag['src']
                                print(f"Large image URL: {large_img_url}")  # 调试输出

                                try:
                                    # 发送请求下载图片
                                    img_response = requests.get(large_img_url, headers=headers)
                                    
                                    # 检查响应内容类型
                                    if 'image' not in img_response.headers.get('Content-Type', ''):
                                        print(f"Skipping non-image URL: {large_img_url}")
                                        continue
                                    
                                    img_data = img_response.content
                                    
                                    # 打开图片并转换格式
                                    img = Image.open(BytesIO(img_data))
                                    
                                    # 将图片转换为 RGB 模式以确保可以保存为 JPEG
                                    img = img.convert('RGB')
                                    
                                    # 检查图片格式并转换为 PNG 或 JPEG
                                    if img.format == 'WEBP':
                                        img_name = f"images/image_{start + index}.png"
                                    else:
                                        img_name = f"images/image_{start + index}.jpeg"
                                    
                                    # 保存图片
                                    img.save(img_name)
                                    print(f"Saved {img_name}")
                                except Exception as e:
                                    print(f"Failed to process image {large_img_url}: {e}")
                            else:
                                print("No <div class='photo-wp'> found.")
                        else:
                            print(f"Failed to retrieve photo page: {photo_page_url}, Status code: {img_response.status_code}")
                    except Exception as e:
                        print(f"Failed to retrieve image page {photo_page_url}: {e}")
        else:
            print("No <ul class='pics'> found.")
    else:
        print(f"Failed to retrieve page: {url}, Status code: {response.status_code}")

print("爬取完毕！")
