import threading
import socket
import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
from datetime import datetime

UDP_IP = '127.0.0.1'
UDP_PORT_SERVER = 5000
UDP_PORT_SITE = 3000
DATA_STORAGE_PATH = 'storage/data.json'

class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data_parse = urllib.parse.unquote_plus(data.decode(encoding='utf-8'))
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

        global MESSAGE
        MESSAGE = data_dict.get('message', '')
        username = data_dict.get('username', 'user')  # Если нет email, используем "user"

        # Отправка сообщения по сокету UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(f'{username}:{MESSAGE}'.encode(encoding='utf-8'), (UDP_IP, UDP_PORT_SERVER))
        print(f"Sent Data: {username}:{MESSAGE}")
        sock.close()


        # Перенаправление на главную страницу
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

def run_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('0.0.0.0', UDP_PORT_SITE)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def echo_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = host, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            data_str = data.decode(encoding='utf-8')
            username, message = data_str.split(':', 1)
            parsed_data = {
                timestamp: {
                    "username": username,
                    "message": message
                }
            }
            with open(DATA_STORAGE_PATH, 'a+', encoding='utf-8') as storage_file:
                current_pos = storage_file.tell()  # Получаем текущую позицию курсора
                print(current_pos)
                if current_pos != 0:                    
                    storage_file.seek(0, 2)  # Переходим в конец файла
                    storage_file.truncate(storage_file.tell() - 3)
                    storage_file.write(',\n')
                    # Добавляем новую запись                   
                    storage_file.write(f'  "{timestamp}": ')   
                    storage_file.write('{\n')
                    storage_file.write(f'    "username": "{username}",\n') 
                    storage_file.write(f'    "message": "{message}"\n')
                    storage_file.write('  }\n}')
                else:
                    json.dump(parsed_data, storage_file, indent=2, ensure_ascii=False)


                print(f'Received data: {parsed_data} from: {address}')

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


if __name__ == '__main__':
    # Запуск HTTP-сервера в одном потоке
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    # Запуск UDP-сервера в другом потоке
    udp_server_thread = threading.Thread(target=echo_server, args=(UDP_IP, UDP_PORT_SERVER))
    udp_server_thread.start()

    # Ждем завершения обоих потоков
    server_thread.join()
    udp_server_thread.join()
