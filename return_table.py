"""
    这个 flask 服务专门用来返回 表格 和 图表
"""
import os
from flask import Flask, make_response, send_from_directory, render_template


app = Flask(__name__)


@app.route("/<url>")
def return_table(url):
    print(f"url:{url}")
    if url not in os.listdir("./forms"):
        return "没有找到数据"
    response = make_response(
        send_from_directory("./forms", url, as_attachment=True))
    return response


@app.route("/table/<user>")
def table(user):
    return render_template(f"./{user}_table.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True,port=8015)

