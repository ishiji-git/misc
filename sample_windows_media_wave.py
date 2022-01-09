import sys
import wave
import winsound as ws
import time
import readchar

class BeepSound:
    file = "c:\\windows\\media\\ring01.wav"
    mode = ws.SND_FILENAME | ws.SND_LOOP | ws.SND_ASYNC
    mode_stop = ws.SND_PURGE
    def until_keyhit(self):
        ws.PlaySound(self.file, self.mode)
        print()
        print("press any key ...")
        print()
        k = readchar.readkey()
        ws.PlaySound(None, self.mode_stop)
        return k

    def until_keyhit(self, file):
        ws.PlaySound(file, self.mode)
        print()
        print("press any key ...")
        print()
        k = readchar.readkey()
        ws.PlaySound(None, self.mode_stop)
        return k

if __name__ == "__main__":
    import glob
    import os
    import random

    sounds_dir = "c:\\windows\\media\\"

    bs = BeepSound()

    cwd = os.getcwd()
    os.chdir(sounds_dir)
    file_name_list = glob.glob("*.wav")

    line_limit = 79
    m = 0
    buf = ""
    for file_name in file_name_list:
        fn = len(file_name)
        tm = m + fn + 4
        if tm > line_limit:
            print(buf)
            buf = "'" + file_name + "'"
            m = fn
        else:
            buf = buf + "  " + "'" + file_name + "'"
            m = tm
    print(buf)

    random.shuffle(file_name_list)
    for file_name in file_name_list:
        print("sample file: {}".format(file_name))
        key = bs.until_keyhit(file_name)
        if key == "Q" or key == "q":
            break
    
    os.chdir(cwd)

    sys.exit(0)
