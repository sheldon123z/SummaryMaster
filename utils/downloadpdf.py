import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdf_files(url, download_folder):
    # 获取网页内容
    response = requests.get(url)
    response.raise_for_status()  # 确保请求成功

    # 解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找所有的链接
    links = soup.find_all('a', href=True)

    # 创建下载文件夹
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # 过滤并下载PDF文件
    for link in links:
        href = link['href']
        if href.lower().endswith('.pdf'):
            pdf_url = urljoin(url, href)
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()  # 确保请求成功

            # 提取文件名并保存文件
            filename = os.path.join(download_folder, os.path.basename(href))
            with open(filename, 'wb') as f:
                f.write(pdf_response.content)
            print(f"Downloaded: {filename}")

# 示例使用
webpage_url = 'https://openscience.fr/La-legitimite-civile-de-la-guerre-cognitive'  # 需要抓取的网页URL
download_directory = './pdf_downloads'  # 保存PDF文件的文件夹
download_pdf_files(webpage_url, download_directory)
