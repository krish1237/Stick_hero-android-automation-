import cv2
import os
import matplotlib.pyplot as plt
import timeit
import time
def velocity(y,x):
    y = y-1
    os.system("adb shell input swipe 20 20 30 30 1000")
    os.system("adb shell screencap -p \"./storage/emulated/0/screen.png\"")
    os.system("adb pull \"./storage/emulated/0/screen.png\"")
    time.sleep(5)
    os.system("adb shell input tap 570 930")
    print("touched")
    img = cv2.imread("screen.png",0)
    ret,img = cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    dist = 0
    while True:
        dist+=1
        y-=1
        if img[y,x] == 255:
            break
    vel = dist/1000
    print(vel)
    return vel
#find_x
def find_y(img,y):
    for i in range(y):
        i+=1
        if img[i,0] == 0:
            row = i
            return row
#MAIN
os.system("adb devices")
c = 0
while True:
    os.system("adb shell screencap -p \"./storage/emulated/0/screen.png\"")
    os.system("adb pull \"./storage/emulated/0/screen.png\"")
    img = cv2.imread("screen.png",0)
    ret,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
    #cv2.imshow('screen',img)
    y,x = img.shape
    img = img[y//2:3*y//4,0:x]
    cv2.imwrite('screen.png',img)
    y1,x1 = img.shape
    if c == 0:
        row = find_y(img,y1)
    px = 0
    a1 = tuple()
    count = 0
    while True:
        prev = px
        px+=1
        if img[row,px] == 255 and img[row,prev] == 0:
            a1 += (px,)
            count += 1
            if count == 2:
                dist = a1[1] - a1[0]
                if c == 0:
                    v = velocity(row + y//2,a1[0])
                print(v," ",dist)
                del a1
                time1 = dist//v
                time1 = int(time1)
                time1 += 10
                count = 0
                c+=1
                a1 = tuple()
                os.system("adb shell input swipe 100 100 100 100 "+str(time1))
                time.sleep(3)
                break
