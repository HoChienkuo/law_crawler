# 国家法律法规数据库爬取

---
## 免责申明
本项目仅用于学术研究，必须遵守相关法律法规，不得利用爬虫进行非法活动</br>
用户应当自行承担使用网络爬虫的风险和后果

---
## 介绍
law_crawler 是用于爬取[国家法律法规数据库](https://flk.npc.gov.cn/)的工具，将爬取到的数据保存到data/database.db，<br/>
并把相应doc/docx/pdf文件下载到download文件夹下。<br/>
结构如下:<br/>
```
├─data              # 数据库存放目录
│  └─database.db    # sqlite3数据库
├─download          # 文档存放目录 
│  └─xffl           # 宪法法律目录，相对应还会有flfg(法律法规)等目录
│     └─exmaple.docx# 下载的文档
├─init.py           # 初始化脚本
└─main.py           # 主执行脚本
```

---
## 如何使用
1. 克隆或下载本项目到您的本地环境
    ```
    git clone https://github.com/HoChienkuo/law_crawler.git
    ```
2. 安装依赖项(pip命令参考，如使用其他包管理自行修改)
    ```
    pip install -r requirements.txt
    ```
3. run ```python init.py``` 初始化数据库<br/><br/>

4. run ```python main.py --type number --download```爬取对应文档<br/>
参数参考:<br/>
-h, --help 展示帮助并退出函数<br/>
-t, --type 选择要爬取的法律类型<br/>
0: 全部
1: xffl(宪法)
2: flfg(法律法规)
3: xzfg(行政法规)
4: jcfg(监察法规)
5: sfjs(司法解释)
6: dfxfg(地方性法规)<br/>
-d,  --download  下载到项目download文件夹<br/>
--begin 爬取的开始页，默认第一页<br/>
--end   爬取的结束页，默认最后一页<br/>

---
## 协议
本仓库的代码依照 [Apache-2.0](LICENSE) 协议开源