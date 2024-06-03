# SummaryMaster
通过大语言模型帮助你快速了解一篇 pdf 论文的主要内容


## 界面是这个样子：

![interface](./img/interface.png)

## 效果是这个样子：
![result](./img/result.png)



# 使用方法：
## 直接使用release 中打包好的软件
1. 输入自己的 apikey，最好使用月之暗面 moonshot 的，因为其他很多厂商不支持上传 pdf 文件和 ocr
2. 如果开了代理，需要点击开启代理，修改为自己的代理端口，默认为 clash 的 127.0.0.1:7890 端口
3. 生成 word 文档目前还不太 ok，生成的格式还需要调整

## 使用代码
1. 首先创建一个新的conda 环境
   ```
   conda create --name summary_master
   conda activate summary_master
   ```
2. 下载依赖
   ```
   pip install -r requirement.txt
   ```
3. 启动脚本
   ```
   python mac_version/SummaryProxy.py
   ```


## 待办事项

- [x] 完成项目文档
- [x] 提交代码
- [ ] 增加自定义 prompt 选项
- [ ] 网页版实现
- [ ] UI 美化
- [ ] 实现多文档格式输出
- [ ] 整合图像输出
  - [ ] markdown
  - [ ] word
- [ ] 兼容性：
  - [x] windows
  - [ ] mac M 系列
  - [ ] mac intel
  - [ ] linux
