import getopt
import json
import sqlite3
import sys
import time

import requests


def usage():
    print("Usage:")
    print("python main.py --help\\--type")
    print("")
    print("Options:")
    print("-h, --help\t\t展示帮助并退出函数")
    print("-t, --type\t\t选择要爬取的法律类型,使用方法 python main.py --type 0")
    print("\t\t\t\t0: 以下全部")
    print("\t\t\t\t1: xf(宪法)")
    print("\t\t\t\t2: flfg(法律法规)")
    print("\t\t\t\t3: xzfg(行政法规)")
    print("\t\t\t\t4: jcfg(监察法规)")
    print("\t\t\t\t5: sfjs(司法解释)")
    print("\t\t\t\t6: dfxfg(地方性法规)")


def get_type_cn_prefix(type_num):
    match type_num:
        case 1:
            return 'xf'  # 宪法
        case 2:
            return "flfg"  # 法律法规
        case 3:
            return "xzfg"  # 行政法规
        case 4:
            return "xzfg"  # 监察法规
        case 5:
            return "sfjs"  # 司法解释
        case 6:
            return "dfxfg"  # 地方性法规


def get_type_cn(type_num):
    match type_num:
        case 1:
            return '宪法'
        case 2:
            return "法律法规"
        case 3:
            return "行政法规"
        case 4:
            return "监察法规"
        case 5:
            return "司法解释"
        case 6:
            return "地方性法规"


def get_base_url(type_num):
    cn_prefix = get_type_cn_prefix(type_num)
    return f'https://flk.npc.gov.cn/api/?type={cn_prefix}&searchType=title%3Bvague&sortTr=f_bbrq_s%3Bdesc&sort=true'


def send_msg(base_url, page):
    url = f'{base_url}&page={page}&size=10&_={time.time()}'
    headers = {
        "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      f"Version/17.4 Safari/605.1.15",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive"
    }
    count = 1
    while count <= 3:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return json.loads(response.text)
        except Exception as e:
            print(f"请求接口{url}错误，第{count}次请求，将重试三次")
            print("错误详情: ", str(e))
            count += 1
            time.sleep(1)
    raise ConnectionError(f"连接{url}失败，有可能是IP被封，请更新IP尝试")


def crawl_all(download_flag):
    law_crawler(1, download_flag)
    law_crawler(2, download_flag)
    law_crawler(3, download_flag)
    law_crawler(4, download_flag)
    law_crawler(5, download_flag)
    law_crawler(6, download_flag)


def crawl_xf(download_flag):
    # todo 宪法爬取并保存数据库
    print("save result to database success")


def transfer_data_list(data_list):
    res = []
    for data in data_list:
        id0 = data['id']
        title = data['title']
        url = data['url']
        office = data['office']
        type0 = data['type']
        status = data['status']
        publish = data['publish']
        expiry = data['expiry']
        res.append((id0, title, url, office, type0, status, publish, expiry))
    return res


def law_crawler(type_num: int, download_flag: bool):
    if type_num == 0:  # all
        crawl_all(download_flag)
        return
    if type_num == 1:  # 宪法
        crawl_xf(download_flag)
        return
    # 其他
    base_url = get_base_url(type_num)
    res0 = send_msg(base_url, 1)
    total_num = int(res0['result']['totalSizes'])
    page_num = total_num // 10 if total_num % 10 == 0 else total_num // 10 + 1
    print(f"{get_type_cn(type_num)}共{page_num}页")
    data_list = []
    for i in range(1, page_num + 1):
        res = send_msg(base_url, i)
        data_list.append(res['result']['data'])
        print(f"{get_type_cn(type_num)}第{i}页成功, sleep一秒")
        time.sleep(1)
    new_data_list = transfer_data_list(data_list)
    print("crawl success")
    connect = sqlite3.connect('data/database.db')
    cursor = connect.cursor()
    sql = f'INSERT INTO {get_type_cn_prefix(type_num)} VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    # 多次插入
    cursor.executemany(sql, new_data_list)
    connect.commit()
    cursor.close()
    connect.close()
    print("save result to database success")


if __name__ == '__main__':
    download = False
    crawl_type = -1
    opts, args = getopt.getopt(sys.argv[1:], "ht:", ["help", "type=", "download"])
    if len(opts) == 0:
        raise ValueError("参数错误，使用-h或--help查看帮助")
    for opt_name, opt_value in opts:
        if opt_name in ("-h", "--help"):
            usage()
            exit(0)
        if opt_name in ("-t", "--type"):
            if not opt_value.isdigit() or opt_value not in ["0", "1", "2", "3", "4", "5", "6"]:
                raise TypeError("错误的type类型，使用-h或--help查看帮助")
            crawl_type = int(opt_value)
            continue
        if opt_name in "--download":
            download = True
    law_crawler(crawl_type, download)
