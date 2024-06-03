import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def is_valid_url(url):
    """检查URL是否有效且完整"""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def sanitize_filename(filename):
    """去除文件名中的非法字符"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_pdf_files(url, download_folder, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()

    # 避免重复访问相同的URL
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        response = requests.get(url, proxies={"http": None, "https": None})
        response.raise_for_status()  # 确保请求成功
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

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
        link_text = link.get_text(strip=True)
        full_url = urljoin(url, href)

        if full_url.lower().endswith('.pdf'):
            # 下载PDF文件
            try:
                pdf_response = requests.get(full_url, proxies={"http": None, "https": None})
                pdf_response.raise_for_status()  # 确保请求成功

                # 提取文件名并保存文件
                filename = sanitize_filename(link_text) + '.pdf'
                if not filename.endswith('.pdf'):
                    filename += '.pdf'
                filename = os.path.join(download_folder, filename)

                with open(filename, 'wb') as f:
                    f.write(pdf_response.content)
                print(f"Downloaded: {filename}")
            except requests.RequestException as e:
                print(f"Failed to download {full_url}: {e}")
        elif is_valid_url(full_url):
            # 递归地处理子页面
            download_pdf_files(full_url, download_folder, visited_urls)

# 示例使用
webpage_url = 'https://openscience.fr/Numero-1-783'  # 需要抓取的网页URL
download_directory = './pdf_downloads'  # 保存PDF文件的文件夹
download_pdf_files(webpage_url, download_directory)
