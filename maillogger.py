#!/usr/bin/python3

import socketserver
import os
import datetime

CONFIG_FILE = '/home/ginkooo/.config/maillogger/maillogger.conf'

def get_config():
    ret = {}
    with open(CONFIG_FILE, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue
            try:
                key, value = line.split('=')
            except:
                print('Bad config line on line ' + str(i))
                exit()
            key = key.lower()
            ret[key] = value.strip().strip("\"'")
    return ret

config = get_config()
print(config)

try:
    logdir = config['logdir']
except:
    print('You have to provide logdir config')
    exit()
if not os.path.isdir(logdir):
    print('Bad logdir path')
    exit()
os.chdir(logdir)

def handle_msg(msg, ip):
    if type(ip) == 'bytes':
        ip = ip.decode('utf-8')
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d') + '.log'
    to_write = now.strftime('%H:%M') + ' ' + ip + ' ' + msg + '\n'
    try:
        with open(filename, 'a') as f:
            f.write(to_write)
    except:
        print('Cound not write to file')
        response = 'ERR Could not write to file'
    response = 'OK'
    return response + '\r\n'


class ConnectionHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(2048).strip()
        try:
            response = handle_msg(self.data.decode('utf-8'), self.client_address[0])
        except:
            response = handle_msg(self.data.decode('ascii'), self.client_address[0])
        try:
            self.request.sendall(response)
        except:
            try:
                self.request.sendall(response.encode('utf-8'))
            except:
                self.request.sendall(response.encode('ascii'))

if __name__ == '__main__':
    try:
        host, port = config['host'], config['port']
    except:
        print('You have to provide host and port in your config file')
        exit()
    server = socketserver.TCPServer((host, int(port)), ConnectionHandler)
    server.allow_reuse_address = True
    server.serve_forever()
