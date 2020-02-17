"""
    存放一些生成图片的方法
"""

from pyecharts.charts import Line
from pyecharts import options as opts



def line_base(money, date) -> Line:
    c = (
        Line()
        .add_xaxis( date)
        .add_yaxis("金额：元", money, is_smooth=True, linestyle_opts=opts.LineStyleOpts(color="#0283A0"),itemstyle_opts=opts.ItemStyleOpts(color="#000000"))
        .set_global_opts(title_opts=opts.TitleOpts(title="day trends"))
    )
    c.render()


def gen_day_table(user,date,money):
    c = (
        Line()
            .add_xaxis(date)
            .add_yaxis("金额：元", money, is_smooth=True, linestyle_opts=opts.LineStyleOpts(color="#0283A0"),
                       itemstyle_opts=opts.ItemStyleOpts(color="#000000"))
            .set_global_opts(title_opts=opts.TitleOpts(title="日消费趋势"))
    )

    c.render(path=f"./templates/{user}_table.html")


def get_day_data(user, DB):
    res = {}
    datas = DB.select(user)
    if datas:
        datas = [ eval(d[0]) for d in datas]
    print(datas)
    for d in datas:

        if d[0] not in res:
            res[d[0]] = float(d[2])
        else:
            res[d[0]] += float(d[2])
    dates = []
    values = []
    data = [dates.append(k) or values.append(v) for k, v in res.items()]
    return dates, values


