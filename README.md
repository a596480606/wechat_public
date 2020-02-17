# 简单介绍
		
因为本人平常有记账的习惯，所以突发奇想，想做一个可以记账的公众号。
先贴上公众号的二维码，有兴趣的朋友可以尝试一下。
	![超级记账小能手](https://img-blog.csdnimg.cn/20200217212952569.jpg)
具体使用方法：
		1、消费记录
			可以把一些日常消费按照一个格式发送给公众号，格式为"时间 消费项目 金额"或"消费项目 金额"，时间和消费项目、消费项目和消费金额之间一定要加空格，例如"2.17 早餐 6"、"午餐 15"，时间格式目前只支持"月份.日期"	，如果不加时间，则默认记录在当天的消费中；消费金额以元为单位。发送消费记录到公众号之后，公众号就会帮你自己动记录。也可以一次发送多个消费记录，以换行分隔，例如下图
		![使用方法](https://img-blog.csdnimg.cn/20200217215545775.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMjg1Mg==,size_16,color_FFFFFF,t_70)
	2、统计消费金额
				发送"统计"到公众后，公众号就会返回当月消费、当天消费、当月日均消费的情况，具体见上图。
			3、将消费记录生成csv文件、日均消费趋势图
				发送"表格"到公众后，公众号会返回一个链接，打开链接可以下载一个包含当月所有消费的csv文件，见下图。
				发送"图表"到公众后，公众号会返回一个链接，打开链接可以看到当月的一个日均消费趋势情况，见下图。
				![表格和图表](https://img-blog.csdnimg.cn/20200217220702659.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMjg1Mg==,size_16,color_FFFFFF,t_70)
				![表格](https://img-blog.csdnimg.cn/20200217220719242.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMjg1Mg==,size_16,color_FFFFFF,t_70)
				![图表](https://img-blog.csdnimg.cn/20200217220735811.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzIxMjg1Mg==,size_16,color_FFFFFF,t_70)
			4、撤销
				发送"撤销"到公众号，可以撤销发送的上一条消费记录。*
# 实现方法

整个服务是通过 flask 来实现的，就是在微信公众号绑定的ip服务器上开启一个 flask 服务，来接收用户发来的信息，检查信息中是否包含之前预设好的一些关键词，来调用相应的函数实现服务。
用到的第三方库：flask、wechatpy、pymysql、DBUtils、pyecharts。
个人感觉有些逻辑实现的还是太复杂了，欢迎朋友们指出不足的地方，谢谢