import socket

renew_db = False

def receive_file(server_ip, server_port, refresh_func):
    global renew_db

    # 서버 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))

    while True:
        server_socket.listen(1)
        print(f"Server listening on {server_ip}:{server_port}")

        # 클라이언트 연결 수락
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # 파일 수신
        with open('./database/ingredients.db', 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)

        print("File received successfully.")

        # 리스트 실시간 갱신
        refresh_func()

        conn.close()

    server_socket.close()
