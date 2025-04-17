项目介绍

这是一个简单的远程屏幕监视工具，允许用户通过服务器连接到客户端，实时查看客户端屏幕。项目包含两个主要部分：后端服务器和前端客户端。

安装依赖库

在运行项目之前，需要安装以下Python库：

pip install opencv-python

pip install numpy

pip install pillow


使用方法

后端服务器（后端.py）

将后端.py文件保存到本地。

在代码中替换IP和端口为服务器的IP地址和端口号。（可以内网穿透）

运行后端服务器（后端.py）

服务器将开始监听客户端连接。

前端客户端（前端.py）

将前端.py文件保存到本地。

在代码中替换IP和端口为服务器的IP地址和端口号。

运行前端客户端（前端.py）

客户端将尝试连接到服务器。


功能说明

服务器功能

远程监视：接收客户端屏幕图像并实时显示。

断开连接：发送断开连接指令给客户端。


客户端功能

屏幕抓取：定时抓取屏幕图像并发送给服务器。

接收指令：根据服务器的指令执行相应操作。
