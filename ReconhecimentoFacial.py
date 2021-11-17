#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Code adapted from Solano, Gabriela(2020).
# Reconhecimento facial - Programa de reconhecimento facial
# Retrieved from: https://github.com/GabySol/OmesTutorials2020
# Adapted by: Group Fatequino
# Adapted by: Plinio GuimarÃ£es (grupo Fatequino) 2021-2o Semestre noite

import cv2
import os
import platform


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

faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

while True:
	ret,frame = cap.read()
	if ret == False: break
	frame = cv2.resize(frame,(320,250),interpolation= cv2.INTER_CUBIC)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	auxFrame = gray.copy()

	faces = faceClassif.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		#desenha um quadrado em volta do rosto na imagem original (da tela)
		cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
		# recorta o rosto para uma imagem separada que será gravada na pasta
		rosto = auxFrame[y:y+h,x:x+w]
		# normaliza o tamanho da imagem para haver um modelo padrão de comparação
		rosto = cv2.resize(rosto,(150,150),interpolation=cv2.INTER_CUBIC)        
		
		result = face_recognizer.predict(rosto)
		#cv2.putText(frame,'{}'.format(result),(x,y-5),1,1(255,255,0),1,cv2.LINE_AA)
		
		# LBPHFace
		if result[1] < 70:
			print('Identificado {}'.format(imagePaths[result[0]]))
			cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-5),2,1,(0,255,0),1,cv2.LINE_AA)
			cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
		
	cv2.imshow('frame',frame)
	k = cv2.waitKey(1)
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
