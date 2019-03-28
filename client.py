import socket
import argparse
import os

def run(host, port, file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(file_name.encode())   ##전송받을 파일이름을 서버로 전달.

        file_size = s.recv(1024)        ##서버로부터 파일 크기를 전달받는 변수.
        file_size = int(file_size.decode()) 

        if(file_size == -1) :         ##서버로부터 파일이 없다면 연결을 종료. 정상적으로 전달받았으면 OK로 응답.
                print("파일이 존재하지 않습니다.")
                return -1

        else :
                s.sendall("OK".encode())

        respfile = s.recv(file_size)
        respfile = respfile.decode()
        
        print("file name : %s" %file_name)
        print("size : %d" %file_size)
        f = open(file_name, 'w', encoding = 'utf8')     ##파일을 쓰기모드로 열기.
        f.write(respfile)
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Echo client -p port -i host -f file_name")
    parser.add_argument("-p", help="port_number", required=True)
    parser.add_argument("-i", help="host_name", required=True)
    parser.add_argument("-f", help="file_name")

    args = parser.parse_args()
    run(host=args.i, port=int(args.p), file_name=args.f)