import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
from urllib.parse import urljoin, urlparse

# 设置要下载的页面的URL
base_url = 'https://openscience.fr/Numero-1-783'

# 用于存储已经访问过的URL，避免重复下载
visited_urls = set()

def is_valid(url):
    """检查URL是否有效，并且是同一个域名下的链接"""
    parsed = urlparse(url)
    return bool(parsed.netloc) and parsed.netloc == urlparse(base_url).netloc

def download_pdf(url):
    # 避免重复下载相同的URL
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    # 发送HTTP请求获取页面内容
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
    except requests.RequestException as e:
        print(f"Error occurred while requesting {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找所有PDF链接
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    
    # 下载并保存PDF文件
    for link in pdf_links:
        pdf_url = urljoin(base_url, link)
        if is_valid(pdf_url):
            try:
                response = requests.get(pdf_url)
                response.raise_for_status()  # 确保请求成功
                with open('temp.pdf', 'wb') as f:
                    f.write(response.content)
                with open('temp.pdf', 'rb') as f:
                    pdf = PdfFileReader(f)
                    title = pdf.getDocumentInfo().title
                if title:
                    filename = f"{title}.pdf"
                else:
                    filename = os.path.basename(pdf_url)
                # 下载PDF文件
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
            except requests.RequestException as e:
                print(f"Error occurred while downloading {pdf_url}: {e}")
    
    # 查找所有链接并递归处理
    for a in soup.find_all('a', href=True):
        next_url = urljoin(base_url, a['href'])
        if is_valid(next_url):
            download_pdf(next_url)

# 从base_url开始下载PDF文件
download_pdf(base_url)

# 删除临时文件
if os.path.exists('temp.pdf'):
    os.remove('temp.pdf')