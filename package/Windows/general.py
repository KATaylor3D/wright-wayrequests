import sys
import winsound
from time import sleep


def repeat_alarm():
    for i in range(0, 5):
        winsound.MessageBeep()
        sleep(.75)    

def while_crash_alarm(func):
    try:
        func()
        return True
    except:
        repeat_alarm()
        for i in sys.exc_info():
            print(i)
        return False

if __name__ == '__main__':
    print("Not Run Directly")
