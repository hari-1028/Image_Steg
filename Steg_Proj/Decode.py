import cv2
import os

def decrypt(msg, password):
    msgList = list(msg)
    pswdList = list(password)
    pswdPos = 0
    for i in range(len(msgList)):
        if pswdPos == len(pswdList):
            pswdPos = 0
        msgList[i] = chr(ord(msgList[i]) - ord(pswdList[pswdPos]))
        pswdPos += 1
    return ''.join(msgList)

def decode(password):
    img = cv2.imread('static/results/inbyus4dec.png')
    height, width, channels = img.shape

    def jointomsg(imgbit):
        return ((imgbit[0] & 7) << 5) | ((imgbit[1] & 7) << 2) | (imgbit[2] & 3)

    msglen = jointomsg(img[0, 0])

    c = 0
    msg = ''
    for i in range(height):
        for j in range(1, width):
            if c == msglen:
                break
            msg += chr(jointomsg(img[i, j]))
            c += 1
        if c == msglen:
            break

    finalMsg = decrypt(msg, password)
    os.remove('static/results/inbyus4dec.png')
    return finalMsg
