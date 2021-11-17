#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Code adapted from Solano, Gabriela(2020).
# Reconhecimento facial - Programa de treinamento de imagens e geração de modelo
# Retrieved from: https://github.com/GabySol/OmesTutorials2020
# Adapted by: Group Fatequino
# Adapted by: Plinio GuimarÃ£es (grupo Fatequino) 2021-2o Semestre noite

import cv2
import os
import numpy as np

dataPath = '/home/pi/Desktop/reconhecimento/Data' #Caminho das imagens armazenadas
peopleList = os.listdir(dataPath)
print('Lista de pessoas: ', peopleList)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
	personPath = dataPath + '/' + nameDir
	print('Lendo imagens')

	for fileName in os.listdir(personPath):
		print('Rostos: ', nameDir + '/' + fileName)
		labels.append(label)
		facesData.append(cv2.imread(personPath+'/'+fileName,0))
		image = cv2.imread(personPath+'/'+fileName,0)
		#cv2.imshow('image',image)
		#cv2.waitKey(10)
	label = label + 1


# MÃ©todos para treinar reconhecedor
#face_recognizer = cv2.face.EigenFaceRecognizer_create()
#face_recognizer = cv2.face.FisherFaceRecognizer_create()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Treinando reconhecedor
print("Treinando...")
face_recognizer.train(facesData, np.array(labels))

# Armazenando o modelo obtido
#face_recognizer.write('modeloEigenFace.xml')
#face_recognizer.write('modeloFisherFace.xml')
face_recognizer.write('modeloLBPHFace.xml')
print("Modelo armazenado...")
