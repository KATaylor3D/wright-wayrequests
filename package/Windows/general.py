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
        
def text_timer(text, duration):
    for i in reversed(range(0, int(duration))):
        os.system("cls")
        print(text, i)
        sleep(1)
        i -= 1

if __name__ == '__main__':
    print("Not Run Directly")
