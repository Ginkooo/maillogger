from os import path, chdir
try:
    from os import scandir
except ImportError:
    from scandir import scandir


def get_logs(logdir):
    currdir = path.abspath(path.curdir)
    chdir(logdir)
    ret = ''
    files = scandir()
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
    chdir(currdir)
    return ret
