import os
import sqlite3

# 创建info表
sql_create_info_table = ("CREATE TABLE IF NOT EXISTS info("
                         "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                         "key VARCHAR(32) NOT NULL,"
                         "value VARCHAR(64) NOT NULL"
                         ")")

table_form = ("id VARCHAR(64) PRIMARY KEY NOT NULL,"
              "title VARCHAR(64) NOT NULL,"
              "url VARCHAR(128) NOT NULL,"
              "office VARCHAR(64) NOT NULL,"
              "type VARCHAR(32) NOT NULL,"
              "status TINYINT NOT NULL,"
              "publish VARCHAR(32) NOT NULL,"
              "expiry VARCHAR(32) NOT NULL,"
              "saved TINYINT default 0"
              "")
# 创建宪法法律表
sql_create_xffl_table = ("CREATE TABLE IF NOT EXISTS xffl("
                         f"{table_form}"
                         ")")
# 创建法律法规表
sql_create_flfg_table = ("CREATE TABLE IF NOT EXISTS flfg("
                         f"{table_form}"
                         ")")
# 创建行政法规表
sql_create_xzfg_table = ("CREATE TABLE IF NOT EXISTS xzfg("
                         f"{table_form}"
                         ")")
# 创建监察法规表
sql_create_jcfg_table = ("CREATE TABLE IF NOT EXISTS jcfg("
                         f"{table_form}"
                         ")")
# 创建司法解释表
sql_create_sfjs_table = ("CREATE TABLE IF NOT EXISTS sfjs("
                         f"{table_form}"
                         ")")
# 创建地方性法规表
sql_create_dfxfg_table = ("CREATE TABLE IF NOT EXISTS dfxfg("
                          f"{table_form}"
                          ")")


def database_init():
    if not os.path.isdir("data"):
        os.mkdir("data")
    connect = sqlite3.connect(r'data/database.db')
    cursor = connect.cursor()
    cursor.execute(sql_create_info_table)
    cursor.execute(sql_create_xffl_table)
    cursor.execute(sql_create_flfg_table)
    cursor.execute(sql_create_xzfg_table)
    cursor.execute(sql_create_jcfg_table)
    cursor.execute(sql_create_sfjs_table)
    cursor.execute(sql_create_dfxfg_table)
    cursor.execute('INSERT INTO info VALUES (?,?,?)', (1, "init_complete", "true"))
    connect.commit()
    cursor.close()
    connect.close()


'''
项目初始化执行此代码
'''
if __name__ == '__main__':
    database_init()
