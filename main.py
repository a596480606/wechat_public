from flask import Flask, request
from wechatpy import parse_message
from table_funs import get_day_data, gen_day_table
from wechatpy.replies import TextReply
from tools import parse_items, get_today_date, get_consume, get_avg_consume, gen_table, Mymysql, RegexConverter

server_ip = "your server ip"

# 创建 flask 应用
app = Flask(__name__)
app.url_map.converters['re'] = RegexConverter   # 通过正则匹配路由

# 暂时存放用户对象的字典，后期可替换成redis
USERS = {}

# 实例化数据库对象
DB = Mymysql()



@app.route("/<re('.?'):url>", methods=["GET", "POST"])
def index(url):
    global USERS
    print("收到请求！",url)

    # 解析收到的用户数据
    data = parse_message(request.data)
    print("data:", data)

    if not data:
        return "无效的请求！"

    # 提取出用户发送给公众号的信息和用户名
    msg = data.content
    user = data.source.replace("@", "_").replace("-","_")

    # 如果用户不在USERS中，则为其新建一张表
    if user not in USERS:
        USERS[user] = {}
        DB.create(user)

    # 用户发送的信息中包含统计
    if "统计" in msg:
        today = get_today_date()            # 获取当天日期
        all_consume = DB.select(user)       # 获取用户数据中的所有记录
        # 统计出日消费和月总消费
        day_consume, month_consume = get_consume(all_consume,  today)
        avg_consume = get_avg_consume(month_consume)
        reply_text = "今日消费：" + str(day_consume) + "元\n当月消费：" + str(month_consume) + "元\n日均消费：" + str(avg_consume) + "元"
        return TextReply(content=reply_text, message=data).render()

    # 用户发送的信息中包含表格
    elif "表格" in msg:
        all_consume = DB.select(user)          # 获取数据库中关于用户的所有记录
        path = f"http://{server_ip}:8015/" + gen_table(user, all_consume)
        reply_text = path
        return TextReply(content=reply_text, message=data).render()

    # 用户发送的信息中包含撤销
    elif "撤销" in msg:
        res = DB.get_last_record(user)          # 获取数据库中关于用户的最后一条记录
        if not res:
            return TextReply(content="暂无数据可撤销！", message=data).render()
        last_record = eval(res)
        reply_text = f"已撤销  {' '.join(last_record)} 的记录！"
        DB.drop_a_record(user)
        return TextReply(content=reply_text, message=data).render()

    # 用户发送的信息中包含图表
    elif '图表' in msg:
        dates, values = get_day_data(user, DB)
        gen_day_table(user,dates,values)
        url = f"http://{server_ip}:8015/table/{user}"
        return TextReply(content=url, message=data).render()

    # 切割提取用户发送的消费信息
    try:
        items = [item for item in msg.split("\n")]
        items = [[xs for xs in s.split(" ") if xs] for s in items if s]

    except:
        print("split error")
        reply_text = "数据格式不正确！"
        return TextReply(content=reply_text, message=data).render()

    # 向数据库插入记录成功的数据，并返回记录失败的数据
    results = "以下数据记录失败:\n"
    for num, item in enumerate(items):
        res = parse_items(item, user, DB)
        print(res)
        if res != "已记录!":
            results += "  ".join(item) + "\n"

    if results == "以下数据记录失败:\n":
        reply_text = "记录成功！"
    else:
        reply_text = results

    xml = TextReply(content=reply_text, message=data).render()
    
    return xml

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)






