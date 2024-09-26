import getopt
import json
import os
import sqlite3
import sys
import time

import requests


def usage():
    print("Usage:")
    print("python main.py --help\\--type")
    print("")
    print("Options:")
    print("-h, --help\t\t\t展示帮助并退出函数")
    print("-t, --type\t\t\t选择要爬取的法律类型,使用方法 python main.py --type 0")
    print("\t\t\t\t\t0: 以下全部")
    print("\t\t\t\t\t1: xffl(宪法)")
    print("\t\t\t\t\t2: flfg(法律法规)")
    print("\t\t\t\t\t3: xzfg(行政法规)")
    print("\t\t\t\t\t4: jcfg(监察法规)")
    print("\t\t\t\t\t5: sfjs(司法解释)")
    print("\t\t\t\t\t6: dfxfg(地方性法规)")
    print("--only-download\t\t配合-t\\--type(必选)选择的法律类型，仅追加下载未下载的文件到项目download文件夹")
    print("-d,  --download\t\t配合-t\\--type(必选)选择的法律类型，下载到项目download文件夹")
    print("-s,  --sleep\t\t遇到网站限流时的睡眠时间，单位为秒，默认1秒")
    print("--begin\t\t\t\t爬取的开始页，默认第一页")
    print("--end\t\t\t\t爬取的结束页，默认最后一页")


def get_type_cn_prefix(type_num):
    match type_num:
        case 1:
            return 'xffl'  # 宪法
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


def send_msg(base_url, page, sleep_time):
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
            time.sleep(sleep_time * count)
    raise ConnectionError(f"连接{url}失败，有可能是IP被封，请更新IP尝试")


def crawl_all(download_flag, begin_page, end_page, sleep_time):
    law_crawler(1, download_flag, begin_page, end_page, sleep_time)
    law_crawler(2, download_flag, begin_page, end_page, sleep_time)
    law_crawler(3, download_flag, begin_page, end_page, sleep_time)
    law_crawler(4, download_flag, begin_page, end_page, sleep_time)
    law_crawler(5, download_flag, begin_page, end_page, sleep_time)
    law_crawler(6, download_flag, begin_page, end_page, sleep_time)


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


def get_document_url(legal_id, sleep_time):
    base_url = f'https://flk.npc.gov.cn'
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/17.4 Safari/605.1.15",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    body = {
        "id": legal_id
    }
    count = 1
    res = {}
    while count <= 3:
        try:
            response = requests.post(f"{base_url}/api/detail", data=body, headers=headers)
            response.raise_for_status()
            response.encoding = 'utf-8'
            res = json.loads(response.text)
            break
        except Exception as e:
            print(f"请求接口{base_url}/api/detail错误，第{count}次请求，将重试三次")
            print("错误详情: ", str(e))
            count += 1
            time.sleep(sleep_time * count)
    if count > 3:
        raise Exception(f"连接{base_url}/api/detail失败，有可能是IP被封，请更新IP尝试")
    doc_name = res['result']['body'][0]['path']
    return doc_name


def download_source(type_num, sleep_time):
    table_name = get_type_cn_prefix(type_num)
    if not os.path.isdir(f'download/{table_name}'):
        os.makedirs(f'download/{table_name}')
    connect = sqlite3.connect('data/database.db')
    cursor = connect.cursor()
    sql = f'SELECT id, title FROM {table_name} WHERE saved = 0'
    cursor.execute(sql)
    rows = cursor.fetchall()
    requests.packages.urllib3.disable_warnings()
    for row in rows:
        legal_id, legal_title = row
        update_sql = f"UPDATE {table_name} SET saved = 1 WHERE id = '{legal_id}'"
        doc_url = f"https://wb.flk.npc.gov.cn{get_document_url(legal_id, sleep_time)}"
        file_extension = os.path.splitext(doc_url)[1]
        if os.path.isfile(f'download/{table_name}/{legal_title}{file_extension}'):
            cursor.execute(update_sql)
            connect.commit()
            continue
        count = 1
        while count <=3:
            try:
                response = requests.get(doc_url, verify=False)
                with open(f'download/{table_name}/{legal_title}{file_extension}', 'wb') as f:
                    f.write(response.content)
                break
            except Exception as e:
                print(f"请求接口{doc_url}错误，第{count}次请求，将重试三次")
                print("错误详情: ", str(e))
                count += 1
                time.sleep(sleep_time * count)
        if count > 3:
            raise Exception(f"连接{doc_url}失败，有可能是IP被封，请更新IP尝试")
        cursor.execute(update_sql)
        connect.commit()
        print(f"file {legal_title} saved, save result to database success")
        time.sleep(sleep_time)
    cursor.close()
    connect.close()
    print("download finished")


def law_crawler(type_num: int, download_flag: bool, begin_page: int, end_page: int, sleep_time: int):
    if type_num == 0:  # all
        crawl_all(download_flag, begin_page, end_page, sleep_time)
        return
    # 其他
    base_url = get_base_url(type_num)
    res0 = send_msg(base_url, 1, sleep_time)
    total_count = int(res0['result']['totalSizes'])
    page_count = total_count // 10 if total_count % 10 == 0 else total_count // 10 + 1
    print(f"{get_type_cn(type_num)}共{page_count}页")
    data_list = []
    r1 = begin_page if begin_page != -1 else 1
    r2 = end_page + 1 if end_page != -1 and end_page < page_count else page_count + 1
    for i in range(r1, r2):
        res = send_msg(base_url, i, sleep_time)
        data_list.extend(res['result']['data'])
        print(f"{get_type_cn(type_num)}第{i}页成功, sleep{sleep}秒")
        time.sleep(sleep_time)
    new_data_list = transfer_data_list(data_list)
    print("crawl success")
    connect = sqlite3.connect('data/database.db')
    cursor = connect.cursor()
    # 已存在的项忽略
    sql = f'INSERT OR IGNORE INTO {get_type_cn_prefix(type_num)} VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)'
    # 多次插入
    cursor.executemany(sql, new_data_list)
    connect.commit()
    cursor.close()
    connect.close()
    print("save result to database success")
    if download_flag:
        download_source(type_num, sleep_time)


if __name__ == '__main__':
    download = False
    only_download = False
    crawl_type = -1
    begin = -1
    end = -1
    sleep = 3
    opts, args = getopt.getopt(sys.argv[1:], "ht:ds:",
                               ["help", "type=", "download", "begin=", "end=", "only-download", "sleep="])
    if len(opts) == 0:
        raise ValueError("参数错误，使用-h或--help查看帮助")
    for opt_name, opt_value in opts:
        if opt_name in ("-h", "--help"):
            usage()
            exit(0)
        if opt_name in ("-d", "--download"):
            download = True
            continue
        if opt_name in ("-t", "--type"):
            if not opt_value.isdigit() or opt_value not in ["0", "1", "2", "3", "4", "5", "6"]:
                raise TypeError("错误的type类型，使用-h或--help查看帮助")
            crawl_type = int(opt_value)
            continue
        if opt_name in "--begin":
            begin = int(opt_value)
            continue
        if opt_name in "--end":
            end = int(opt_value)
            continue
        if opt_name in "--only-download":
            only_download = True
            continue
        if opt_name in ("-s", "--sleep"):
            sleep = int(opt_value)
    if crawl_type == -1:
        raise Exception("type为空，使用-h或--help查看帮助")
    if only_download:
        download_source(crawl_type, sleep)
    law_crawler(crawl_type, download, begin, end, sleep)
