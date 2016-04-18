import time
import sys


def countdown(t):
    t = t*60
    while t >= 0:
 	mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
	sys.stdout.write("\r" + timeformat)
        sys.stdout.flush()
	time.sleep(1)
        t -= 1
    print('Goodbye!\n\n\n\n\n')

countdown(1)
