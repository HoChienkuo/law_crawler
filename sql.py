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
              "status INTEGER NOT NULL,"
              "publish VARCHAR(32) NOT NULL,"
              "expiry VARCHAR(32) NOT NULL")
# 创建宪法表
sql_create_xf_table = ("CREATE TABLE IF NOT EXISTS xf("
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
