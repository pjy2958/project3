import socket
import argparse
import glob
import os

file_size = 0

def run_server(port=4000, dir=""):
    host = ""

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        
        conn, addr = s.accept()
        file_name = conn.recv(1024)     
        file_name = file_name.decode()

        if(os.path.isfile("%s/%s" %(dir, file_name))==True):        ##디렉토리안에 파일이 존재하면 파일사이즈를, 존재하지않으면 -1를 전송.
            file_size = os.path.getsize("%s/%s" %(dir, file_name))    
            conn.sendall(str(file_size).encode())

        else:
            conn.sendall(str("-1").encode())
            print("파일이 존재하지 않습니다.")

        file_address = ("%s/%s" %(dir, file_name))      ##파일 경로/이름
        
        resp = conn.recv(1024)      ##client의 응답.
        resp = resp.decode()

        if(resp=="OK") :            ##OK를 응답받았다면 파일 전송.
            f = open(file_address, "r", encoding="utf8")    ##파일을 읽기 모드로 열기.
            text_str = f.read()
            conn.sendall(str(text_str).encode())
            print("file name : %s" %file_address)
            print("size : %d" %file_size)
            f.close()

        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo server -p port -d directory")
    parser.add_argument("-p", help="port_number", required=True)
    parser.add_argument("-d", help="directory_address", required=True)

    args = parser.parse_args()
    run_server(port=int(args.p), dir=args.d)