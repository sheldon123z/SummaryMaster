from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.text_splitter import CharacterTextSplitter
from langchain_community.chains.summarize import load_summarize_chain
from langchain_community.llms import OpenAI
# 设置 OpenAI API 密钥
import os
api_key = "你的 api key"
base_url="https://api.moonshot.cn/v1"

# 定义文件路径
file_path = "/Users/xiaodongzheng/Desktop/articles/VVC/markdown/Yang 等 - 2020 - Two-Timescale Voltage Control in Distribution Grids Using Deep Reinforcement Learning.md"

# 加载 Markdown 文件
loader = UnstructuredMarkdownLoader(file_path)
documents = loader.load()

# 分割文档
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# 使用 LangChain 的 summarize 链进行文章信息提取
llm = OpenAI(temperature=0.7,api_key=api_key, base_url=base_url)
chain = load_summarize_chain(llm, chain_type="map_reduce")
results = chain.run(texts)

# 提取并整理文章信息
article_info = []
for result in results:
    article = {}
    article["title"] = result.split("\n\n")[0]
    article["authors"] = result.split("\n\n")[1].replace("**作者:** ", "")
    article["publication_year"] = result.split("\n\n")[2].replace("**文章发表时间:** ", "")
    article["institution"] = result.split("\n\n")[3].replace("**文章发表机构:** ", "")
    article["summary"] = "\n\n".join(result.split("\n\n")[4:])
    article_info.append(article)

# 输出结果
import json
print(json.dumps(article_info, indent=2, ensure_ascii=False))