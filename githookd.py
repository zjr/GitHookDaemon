#!/usr/bin/env python2.7

import sys
import time
import githook
from daemon import Daemon


class GitHD(Daemon):
    def run(self):
        while True:
            time.sleep(1)
            githook.app.run()

if __name__ == "__main__":
    daemon = GitHD(
        '/tmp/githd.pid',
        '/dev/null',
        '/var/log/githd/output_log',
        '/var/log/githd/error_log')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            sys.argv[1] = '1337'
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            sys.argv[1] = '1337'
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
