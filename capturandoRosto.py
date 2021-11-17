#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Code adapted from Solano, Gabriela(2020).
# Reconhecimento facial - Programa de captura de imagens
# Retrieved from: https://github.com/GabySol/OmesTutorials2020
# Adapted by: Group Fatequino
# Adapted by: Plinio GuimarÃ£es (grupo Fatequino) 2021-2o Semestre noite

import cv2
import os
import imutils
import platform

print('Programa de registro de imagens de aluno.')

personName = input('Informe o RA do aluno: ')
dataPath = '/home/pi/Desktop/reconhecimento/Data' #Caminho das imagens armazenadas
personPath = dataPath + '/' + personName

if not os.path.exists(personPath):
	print('Criando pasta: ',personPath)
	os.makedirs(personPath)

#verificando se existem imagens antigas nessa pasta para não sobrescrever
listdir = os.listdir(personPath)
qtde = len(listdir)
count = 0

# A Webcam do notebook no Windows requer um parâmetro a mais para funcionar corretamente (sem erro na finalização)
if platform.system() == "Windows":
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
else:
	cap = cv2.VideoCapture(0)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

while (count < 50):

	ret, frame = cap.read()
	if ret == False: break

	frame =  imutils.resize(frame, width=640)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	auxFrame = frame.copy()

	faces = faceClassif.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		#desenha um quadrado em volta do rosto na imagem original (da tela)
		cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
		# recorta o rosto para uma imagem separada que será gravada na pasta
		rosto = auxFrame[y:y+h,x:x+w]
		# normaliza o tamanho da imagem para haver um modelo padrão de comparação
		rosto = cv2.resize(rosto,(150,150),interpolation=cv2.INTER_CUBIC)
		# grava a imagem na pasta com um número sequencial
		cv2.imwrite(personPath + '/rosto_{}.jpg'.format(qtde),rosto)
		#incrementa contador de capturas
		count = count + 1
		#incrementa contador do nome do arquivo
		qtde = qtde + 1

	# Escreve na imagem a ser exibida algumas informações para acompanhamento do usuário
	cv2.putText(frame, "img: "+str(count), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 1,cv2.LINE_AA)
	# Mostra a imagem da janela de exibição padrão
	winname = 'Fatequino - Record - press ESC para encerrar'
	cv2.imshow(winname,frame)
	cv2.setWindowProperty(winname, cv2.WND_PROP_TOPMOST, 1)

	k =  cv2.waitKey(1)
	if k == 27 or count == 50:
		break

print("encerrando programa")
try:
	cap.release()
	cv2.destroyAllWindows()
except:
	print("Câmera encerrada com falha.")

print('Programa encerrado.')
