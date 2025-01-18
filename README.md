# idol_live_scrapy

爬虫项目。从微博中抓取地偶的主办的活动信息，并保存到数据库中。

## 开始安装

* 创建venv：`python -m venv .venv`
* 安装依赖：`.venv/Scripts/python -m pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple`
* cron服务依赖node。

## 爬虫配置文件

爬虫配置文件为resources/live_spider_config.xlsx。定义列有：
* uid：用户UID
* lfid：lfid，通过这个id才能抓到列表，移动端微博可以查看。
* area：活动的主办是哪个地方的，用逗号","分割。

## 执行爬虫
使用命令`scrapy crawl live_spider -L WARNING`。