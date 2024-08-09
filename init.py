import sqlite3

from sql import *


def database_init():
    connect = sqlite3.connect('data/database.db')
    cursor = connect.cursor()
    cursor.execute(sql_create_info_table)
    cursor.execute(sql_create_xf_table)
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
