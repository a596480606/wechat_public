"""
    main.py 用到的函数集合
"""
import csv
import time
import pymysql
import datetime
from DBUtils.PooledDB import PooledDB
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        # 将接受的第1个参数当作匹配规则进行保存
        self.regex = args[0]

def parse_items(item, user, DB):
    """
        处理用户消费信息的函数
    :param item: 消费记录
    :param user: 用户名
    :param DB:  数据库
    :return:
    """
    if len(item) == 2:
        today = get_today_date()

        if item[0].split(".")[0].isdigit():
            reply_text = "格式错误！请输入例如：早餐 12"
            return reply_text

        if is_number(item[1]):
            item.insert(0, today)
            DB.insert(user,str(item))
            reply_text = "已记录!"
        else:
            reply_text = "格式错误！请输入例如：早餐 12"

    elif len(item) == 3:
        today = format_date(item[0])

        if not today:
            reply_text = "日期格式不正确！请输入例如：12.2 或 12.02"

            return reply_text

        if is_number(item[2]):
            reply_text = "已记录!"
            item[0] = today
            DB.insert(user,str(item))
        else:
            reply_text = "格式错误！请输入例如：早餐 12"
    else:
        reply_text = "暂不支持其他消息，请见谅！"

    return reply_text


def get_today_date(detail=False):
    """detail 日期细节，默认False，返回到日, 为 s 返回 到时分秒"""
    if not detail:
        t = time.strftime("%Y%m%d", time.localtime())
        return t

    if detail == "s":
        t = time.strftime("%Y%m%d%H%M%S", time.localtime())
        return t


def time_to_timestmap(t):
    """把 类似 20191122 格式的时间转为时间戳"""
    new_t = time.mktime(time.strptime(t, "%Y%m%d"))
    return round(new_t)


def get_current_month():
    """返回当前月份的第一天的日期 20191201"""
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    tomonth = str(year) + str(month) + "01"
    return tomonth


def get_consume(all_consume, today):
    """
        统计用户消费的函数
    :param all_consume: 数据库中关于用户的所有记录
    :param today: 当天日期
    :return: 日总消费，月总消费
    """
    tomonth = get_current_month()       # 当月第一天的日期
    month_consume = 0                   # 月总消费
    today_consume = 0                   # 日总消费
    # 遍历数据库中关于用户的所有记录
    for consume in all_consume:
        record = eval(consume[0])
        consume_day = record[0]
        fee = float(record[2])
        if consume_day == today:
            today_consume += fee
        if time_to_timestmap(consume_day) >= time_to_timestmap(tomonth):
            month_consume += float(fee)
    return round(today_consume,2), round(month_consume,2)


def get_avg_consume(month_consume):
    """生成月平均消费的函数"""
    day = datetime.datetime.today().day
    avg_consume = round(month_consume/day,2)
    return avg_consume


def format_date(s):
    year = str(datetime.datetime.today().year)
    if "." in s:
        sl = s.split(".")
    else:
        return False
    if len(sl) != 2:
        return False
    month, day = sl
    if month.isdigit() and day.isdigit():
        month, day = int(month),  int(day)
    else:
        return False
    if 0 < month < 10:
        month = "0" + str(month)
    elif 10 <= month < 13:
        month = str(month)
    else:
        return False

    every_month_last_day = 31
    if int(month) in [1,3,5,7,8,10,12]:
        every_month_last_day = 32

    if 0 < day < 10:
        day = "0" + str(day)
    elif 10 <= day < every_month_last_day:
        day = str(day)
    else:
        return False
    return year + month + day


def is_number(string):
    try:
        float(string)
    except ValueError:
        return False
    return string


def gen_table(user, all_consume):
    """
        生产用户消费表格的函数
    :param user:    用户名
    :param all_consume: 获取数据库中关于用户的所有记录
    :return: 用户消费表格的路径
    """
    path = f"{user}_details.csv"
    with open(f"./forms/{user}_details.csv", "w", encoding="utf8", newline="" ) as f:
        csvf = csv.writer(f, delimiter=",")
        for consume in all_consume:
            record = eval(consume[0])
            csvf.writerow(record)
    return path



class Mymysql:
    """
        mysql数据库类
    """
    def __init__(self):
        # 通过 PooledDB 生成一个连接数最大为10的连接池
        self.pool = PooledDB(pymysql, 10, host="127.0.0.1", port=3306, user="root", password="123456", db="accounts")

    def create(self, user):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        # self.conn.cursor.execute("""DROP TABLE IF EXISTS {};""".format(user))
        sql = """create table IF NOT EXISTS {}( content varchar(50), id INT(20) AUTO_INCREMENT, primary key(id));""".format(user)
        print(sql)
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        self.cursor.close()
        self.conn.close()

    def insert(self, user, value):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        sql = """insert into {}(content) value ("{}");""".format(user,value)
        print(sql)
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def get_last_record(self, user):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        sql = """select * from {} order by id desc limit 1;""".format(user)
        print(sql)
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        try:
            res = self.cursor.fetchall()[0][0]
        except IndexError:
            return None
        print(type(res))
        print(res)
        self.cursor.close()
        self.conn.close()
        return res

    def drop_a_record(self, user):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        # sql = """delete from {} where id = (select id from {} Limit (count-1),1);""".format(user,user)
        sql = """delete from {}  order by id desc limit 1;""".format(user)
        print(sql)
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def select(self,user):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        sql = """select * from {};""".format(user)
        print(sql)
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        try:
            res = self.cursor.fetchall()
        except IndexError:
            return None
        self.cursor.close()
        self.conn.close()
        return res

