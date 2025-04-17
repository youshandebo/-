from socket import *
import cv2
from io import BytesIO  
import numpy as np 

# 清理函数，关闭socket连接并销毁所有OpenCV窗口
def cleanup(server_socket=None, client_socket=None):
    if client_socket:
        try:
            client_socket.close()
        except:
            pass
    if server_socket:
        try:
            server_socket.close()
        except:
            pass
    cv2.destroyAllWindows()

# 主函数，运行服务器逻辑
def main():
    # 创建一个socket对象
    S = socket()
    # 绑定socket到本地地址和端口
    S.bind(('IP', "端口"))
    # 开始监听连接
    S.listen()
    print("Server listening...")
    
    try:
        # 接受客户端连接
        s, addr = S.accept()
        print(f"Connected by {addr}")

        # 显示选择菜单
        print('1.远程监视')
        print('2.断开连接')
        choice = input('请选择：')
        # 发送选择指令给客户端
        s.send(choice.encode())
        
        # 如果选择远程监视
        if choice == '1':
            # 创建一个OpenCV窗口用于显示远程监视图像
            cv2.namedWindow('Remote Monitor', cv2.WINDOW_NORMAL)
            while True:
                try:
                    # 接收图像数据的大小
                    size_data = s.recv(1024)
                    if not size_data:
                        print("客户端断开连接（接收大小时）。")
                        break
                    size = int(size_data.decode())
                    # 发送确认信息给客户端
                    s.send('ok'.encode())

                    # 创建一个字节流对象用于接收图像数据
                    img_stream = BytesIO()
                    cursize = 0
                    # 循环接收图像数据直到接收完整个图像
                    while cursize < size:
                        data = s.recv(2048)
                        if not data:
                            print("图像传输过程中客户端断开连接。")
                            break
                        img_stream.write(data)
                        cursize += len(data)

                    if cursize < size:
                        break

                    # 将字节流对象的指针移到开头
                    img_stream.seek(0)
                    # 从字节流对象中读取图像数据并解码为numpy数组
                    image_data = np.frombuffer(img_stream.read(), np.uint8)
                    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

                    # 如果图像解码成功，显示图像
                    if image is not None:
                        cv2.imshow('Remote Monitor', image)
                        # 如果按下ESC键，退出循环
                        if cv2.waitKey(20) & 0xFF == 27:
                            break
                    else:
                        print("图像解码失败")

                    # 发送确认信息给客户端
                    s.send('ok'.encode())
                except ConnectionResetError:
                    print("客户端连接重置。")
                    break
                except Exception as e:
                    print(f"循环中发生错误: {e}")
                    break
        # 如果选择断开连接
        elif choice == '2':
            s.send('ok'.encode())

    except KeyboardInterrupt:
        print("\n接收到退出信号，正在关闭服务器...")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 清理资源
        cleanup(S, s)
        print("服务器已关闭。")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n接收到退出信号，正在关闭服务器...")
        print("服务器已关闭。")