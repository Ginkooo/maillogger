import os


def get_logs(logdir):
    currdir = os.path.abspath(os.path.curdir)
    os.chdir(logdir)
    ret = ''
    files = os.scandir()
    for direntry in files:
        try:
            year, month, day = direntry.name.split('-')
        except:
            pass
        with open(direntry.name, 'r') as f:
            for line in f:
                time, ip, msg = line.strip().split(';')
                ret += direntry.name + ';' + time + ';' + ip +\
                    ';' + msg + '\r\n'
    os.chdir(currdir)
    return ret
