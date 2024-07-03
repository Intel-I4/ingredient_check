import threading
import socket
import ctypes


class file_receive_thread(threading.Thread):
    def __init__(self, server_ip, server_port, refresh_func):
        super().__init__()  # 부모 클래스의 초기화를 수행합니다.
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((server_ip, server_port))
        self.refresh_func = refresh_func

    def run(self):
        # target function of the thread class
        try:
            while True:
                self.server_socket.listen(1)
                print(f"Server listening on {self.server_ip}:{self.server_port}")

                # 클라이언트 연결 수락
                conn, addr = self.server_socket.accept()
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
                self.refresh_func()

                conn.close()
        finally:
            print('ended')

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        self.server_socket.close()

        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id,
            ctypes.py_object(SystemExit)
        )

        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
