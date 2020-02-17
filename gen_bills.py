"""
    生成测试数据
"""
import random
source_date = "2"       # 要生成的月份

items = ["早餐", "午餐", "晚餐", "零食", "奶茶", "水果","生活用品", "游戏", "服装", "看电影", "下馆子", "吃饭","早餐", "午餐", "晚餐", "零食", "奶茶", "水果","早餐", "午餐", "晚餐", "零食", "奶茶", "水果","早餐", "午餐", "晚餐", "零食", "奶茶", "水果"]

with open("test_bills.txt", "w", encoding="utf8") as f:
    # 生成到几号
    for i in range(1,18):
        date = source_date + "." + str(i)
        for c in range(1,random.randint(4, 8)):
            f.write(date + " " + random.choice(items) + " " + str(random.randint(12, 38)) + "\n")




