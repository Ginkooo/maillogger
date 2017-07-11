import os


def get_logs(logdir):
    currdir = os.path.abspath(os.path.curdir)
    os.chdir(logdir)
    ret = ''
    files = os.listdir()
    for f_name in files:
        try:
            year, month, day = f_name.split('-')
        except:
            pass
        with open(f_name, 'r') as f:
            for line in f:
                time, ip, msg = line.strip().split(';')
                ret += f_name + ';' + time + ';' + ip +\
                    ';' + msg + '\r\n'
    os.chdir(currdir)
    return ret
