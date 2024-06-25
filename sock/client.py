import socket

def send_file(server_ip, server_port, file_path):
    # make client socket 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server {server_ip}:{server_port}")

    # send file
    with open(file_path, 'rb') as f:
        data = f.read(1024)
        while data:
            client_socket.sendall(data)
            data = f.read(1024)

    print("File sent successfully.")
    client_socket.close()


# 라즈베리 파이에서 사용하는 코드
# if __name__ == "__main__":
#     send_file("10.10.15.103", 12309, "./ingredients.db")
