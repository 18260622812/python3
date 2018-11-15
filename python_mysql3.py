#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "test")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO info(fans, \
       name, email) \
       VALUES ('%s', '%s', '%s')" % \
      ('100', 'Mohan', '1085115928@qq.com')
try:
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()
except:
    # 发生错误时回滚
    print("error")
    db.rollback()

# 关闭数据库连接
db.close()