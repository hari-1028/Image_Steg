import cv2

def splitToBgr(val):
    b = (val & 0xE0) >> 5
    g = (val & 0x1C) >> 2
    r = (val & 0x3)
    return [b, g, r]

def encrypt(msg, password):
    msgList = list(msg)
    pswdList = list(password)
    pswdPos = 0
    for i in range(len(msgList)):
        if pswdPos == len(pswdList):
            pswdPos = 0
        msgList[i] = chr(ord(msgList[i]) + ord(pswdList[pswdPos]))
        pswdPos += 1
    return ''.join(msgList)

def encode(msg, password):
    inputImg = 'static/results/input.png'
    outputImg = 'static/results/output.png'
    img = cv2.imread(inputImg)
    height, width, channels = img.shape
    msg = encrypt(msg, password)
    bitlist = [splitToBgr(ord(ch)) for ch in msg]
    firstbit = splitToBgr(len(msg))

    def clearLSB3(val):
        return val & 0xF8

    def encode_pixel(imgbit, msgbit):
        return msgbit | clearLSB3(imgbit)

    for i in range(3):
        img[0, 0][i] = encode_pixel(img[0, 0][i], firstbit[i])

    c = 0
    for i in range(height):
        for j in range(1, width):
            if c == len(msg):
                break
            for k in range(3):
                img[i, j][k] = encode_pixel(img[i, j][k], bitlist[c][k])
            c += 1
        if c == len(msg):
            break

    cv2.imwrite(outputImg, img)
