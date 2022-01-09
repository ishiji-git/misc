import readchar
c = readchar.readchar()
print("readchar:", c)

c = readchar.readkey()
print("readkey:", c)

#######
import msvcrt
while True:
      if msvcrt.kbhit():
          c = msvcrt.getch()
          break
print("getch:", c)
