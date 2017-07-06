#!/usr/bin/python3

import socketserver
import os
import datetime

CONFIG_FILE = '/home/pczajka/.config/maillogger/maillogger'

def get_config():
    ret = {}
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line[0] == b'#':
                continue
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('ascii')
            if not line:
                continue
            key, value = line.split('=')
            key = key.lower()
            ret[key] = value.strip().strip("\"'")

config = get_config()

try:
    logdir = config['logdir']
    if not os.path.isdir(logdir()):
        raise RuntimeError('')
except:
    print('You have to specify valid logdir in your config file, example:\nlogdir=/var/log/maillogger')
    exit()
os.chdir(logdir)

def handle_msg(msg, ip):
    if type(ip) == 'bytes':
        ip = ip.decode('utf-8')
    filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    to_write = ip + ' ' + msg + '\n'
    with open(filename, 'a') as f:
        f.write(to_write)

class ConnectionHandler:
    def handle(self):
        self.data = self.request.recv(2048).strip()
        try:
            response = handle_msg(self.data.decode('utf-8'), self.client_address[0])
        except:
            response = handle_msg(self.data.decode('ascii'), self.client_address[0])
        try:
            self.request.sendall(response)
        except:
            self.request.sendall(response.encode('utf-8'))

if __name__ == '__main__':
    try:
        host, port = config['host'], config['port']
    except:
        print('You have to provide host and port in your config file')
        exit()
    server = socketserver.TCPServer((host, int(port)), ConnectionHandler)
    server.allow_reuse_address = True
    server.serve_forever()
