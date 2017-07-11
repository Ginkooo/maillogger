#!/usr/bin/python3

import socketserver
import os
import datetime
import get_handler

CONFIG_FILE = '/home/pczajka/.config/maillogger/maillogger.conf'


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
    print('logdir like that does not exist')
    exit()
os.chdir(logdir)


def handle_msg(msg, ip):
    if type(ip) == 'bytes':
        ip = ip.decode('utf-8')
    if msg == 'GET':
        return get_handler.get_logs(logdir)
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d') + '.log'
    msg = msg.replace(';', ':')
    to_write = now.strftime('%H:%M') + ';' + ip + ';' + msg + '\n'
    with open(filename, 'a') as f:
        f.write(to_write)
    print('Wrote: ' + to_write)
    response = 'OK'
    return response + '\r\n'


class ConnectionHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(2048).strip()
        try:
            response = handle_msg(self.data.decode('utf-8'),
                                  self.client_address[0])
        except:
            response = handle_msg(self.data.decode('ascii'),
                                  self.client_address[0])
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
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((host, int(port)), ConnectionHandler)
    server.serve_forever()
