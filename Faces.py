#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## Programa demo Blinking Eyes
## Desenvolvido por Plinio GuimarÃ£es
## 04/11/2021

## DemonstraÃ§Ã£o de interface grÃ¡fica para dispositivos mÃ³veis com olhos que piscam.


import os,sys,time
import numpy as np
import cv2
from datetime import datetime
from time import sleep
import imutils
import platform

def PreparaMonitor():
    global cap, faceClassif, face_recognizer, imagePaths, count2blink
    count2blink = 0
    dataPath = '/home/pi/Desktop/reconhecimento/Data' #Caminho das imagens armazenadas
    imagePaths = os.listdir(dataPath)
    print('imagePaths=',imagePaths)

    print("lendo arquivo de treinamento de faces")
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('modeloLBPHFace.xml')

    print("iniciando câmera")
    # A Webcam do notebook no Windows requer um parâmetro a mais para funcionar corretamente (sem erro na finalização)
    if platform.system() == "Windows":
    	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
    	cap = cv2.VideoCapture(0)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')


def monitora(key):
    global cap, faceClassif, face_recognizer, imagePaths, count2blink

    ret,frame = cap.read()

    count2blink = count2blink + 1
    if count2blink > 50:
        blink()
        count2blink= 0

    if ret == False: return

    frame = cv2.resize(frame,(320,250),interpolation= cv2.INTER_CUBIC)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    faces = faceClassif.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        olhosNormais()
        rosto = auxFrame[y:y+h,x:x+w]
        rosto = cv2.resize(rosto,(150,150),interpolation= cv2.INTER_CUBIC)
        result = face_recognizer.predict(rosto)
        #cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

        # LBPHFace
        if result[1] < 70:
            blinkOne(imagePaths[result[0]])
            cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)

    # normaliza o tamanho da imagem para haver um modelo padrão de comparação
    rosto = cv2.resize(frame,(150,150),interpolation=cv2.INTER_CUBIC)
    cv2.imshow('frame',rosto)
    cv2.setWindowProperty('frame', cv2.WND_PROP_TOPMOST, 1)

    main(key)
    if key == 27:
        cap.release()
        cv2.destroyAllWindows()


def DrawImage(back, fore, x, y):
    img = np.array(back)
    img_overlay_rgba = np.array(fore)
    s_img = fore
    l_img = back

    l_img[y:y+s_img.shape[0], x:x+s_img.shape[1]] = s_img


def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY,yo,xe,xd
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(fundo,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y
        print(mouseX,mouseY)
        #yo = mouseY
        #xe = mouseX
        #xd = mouseX

def blink():
    global fundo, OlhoENormal, OlhoDNormal, OlhoEAberto, OlhoDAberto, OlhoEFechado, OlhoDFechado, xd, xe, yo
    DrawImage(fundo, OlhoENormal, xe, yo)
    DrawImage(fundo, OlhoDNormal, xd, yo)
    cv2.imshow('window', fundo)
    cv2.waitKey(1)
    DrawImage(fundo, OlhoEFechado, xe, yo)
    DrawImage(fundo, OlhoDFechado, xd, yo)
    cv2.imshow('window', fundo)
    cv2.waitKey(3)
    DrawImage(fundo, OlhoENormal, xe, yo)
    DrawImage(fundo, OlhoDNormal, xd, yo)
    cv2.imshow('window', fundo)
    cv2.waitKey(1)
    fundo = cv2.imread(pathimg+'Fundo.png', cv2.IMREAD_GRAYSCALE)
    cv2.imshow('window', fundo)
    
def blinkOne(strid):
    global fundo, OlhoENormal, OlhoDNormal, OlhoEAberto, OlhoDAberto, OlhoEFechado, OlhoDFechado, xd, xe, yo
    DrawImage(fundo, OlhoEFechado, xe, yo)
    #DrawImage(fundo, OlhoDNormal, xd, yo)
    cv2.imshow('window', fundo)
    k = cv2.waitKey(2)
    k = cv2.waitKey(20)
    fundo = cv2.imread(pathimg+'Fundo.png', cv2.IMREAD_GRAYSCALE)
    if strid != '':
        if strid == 'DEMO':
            main(122)
        else:
            cv2.putText(fundo,'Identificado: '+strid,(10,25),2,1.1,(0,255,0),1,cv2.LINE_AA)
    cv2.imshow('window', fundo)

    cv2.waitKey(20)

def olhosNormais():
    DrawImage(fundo, OlhoENormal, xe, yo)
    DrawImage(fundo, OlhoDNormal, xd, yo)
    cv2.imshow('window', fundo)

def olhoDFechadoBoca():
    DrawImage(fundo, OlhoDFechado, xd, yo)
    DrawImage(fundo, boca, int((xd + xe) / 2), yo+250)
    cv2.imshow('window', fundo)

def olhoEFechado():
    DrawImage(fundo, OlhoEFechado, xe, yo)
    cv2.imshow('window', fundo)


def main(key):
    global yo, xe, xd

    #olhos normais
    if key==110: olhosNormais()

    #blink (spacebar)
    if key==32: blink()

    #a 
    if key==97: olhoDFechadoBoca()

    #b
    if key==98: olhoEFechado()

    #c
    if key==99:
        DrawImage(fundo, OlhoDAberto, xd, yo)
        cv2.imshow('window', fundo)
    #d
    if key==100:
        DrawImage(fundo, OlhoEAberto, xe, yo)
        cv2.imshow('window', fundo)
    #e
    if key==101:
        DrawImage(fundo, OlhoDNormal, xd, yo)
        cv2.imshow('window', fundo)
    #f
    if key==102:
        DrawImage(fundo, OlhoENormal, xe, yo)
        cv2.imshow('window', fundo)

    # m - reload fundo
    if key==109:
        loadImages()
        #fundo = cv2.imread(pathimg+'Fundo.png', cv2.IMREAD_GRAYSCALE)
        cv2.imshow('window', fundo)
    #p
    if key==112:
        blinkOne('')
    #z
    if key==122:
        DrawImage(fundo, zumbi, 170, 0)
        cv2.imshow('window', fundo)

    if key==13:
        loadImages()
        

def loadImages():
    global pathimg, fundo, OlhoENormal, OlhoDNormal, OlhoEAberto, OlhoDAberto, OlhoEFechado, OlhoDFechado, xd, xe, yo, boca, zumbi
    pathimg = os.path.abspath((os.path.dirname(__file__)))+"/imagens/"
    print(pathimg)
    print(os.path.abspath(__file__))
    
    fundo = cv2.imread(pathimg+'Fundo.png', cv2.IMREAD_GRAYSCALE)
    OlhoEAberto = cv2.imread(pathimg+'OlhoEAberto.png', cv2.IMREAD_GRAYSCALE)  
    OlhoDAberto = cv2.imread(pathimg+'OlhoDAberto.png', cv2.IMREAD_GRAYSCALE)  
    OlhoEFechado = cv2.imread(pathimg+'OlhoEFechado.png', cv2.IMREAD_GRAYSCALE)  
    OlhoDFechado = cv2.imread(pathimg+'OlhoDFechado.png', cv2.IMREAD_GRAYSCALE)  
    OlhoENormal = cv2.imread(pathimg+'OlhoENormal.png', cv2.IMREAD_GRAYSCALE)  
    OlhoDNormal = cv2.imread(pathimg+'OlhoDNormal.png', cv2.IMREAD_GRAYSCALE)  
    boca = cv2.imread(pathimg+'boca.png', cv2.IMREAD_GRAYSCALE)
    zumbi= cv2.imread(pathimg+'zumbi.jpg', cv2.IMREAD_GRAYSCALE)

xe = 336
xd = 525
yo = 131

#constantes de controle dos olhos
kblink = 32

loadImages()    
cv2.namedWindow('window', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('window',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.imshow('window', fundo)
        
cv2.namedWindow('window')
cv2.setMouseCallback('window',draw_circle)

PreparaMonitor()

while True:
    key=cv2.waitKey(1)
    #main(key)
    monitora(key)
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()
print('fim')
