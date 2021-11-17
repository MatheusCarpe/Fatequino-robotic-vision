Projeto Fatequino - Equipe Vis�o (noturno) - 2o Semestre 2021
-------------------------------------------------------------

Os programas deste pacote foram adaptados para rodar diretamente no Raspberry Pi 3 do projeto fatequino e, portanto, os paths
de refer�ncia dos arquivos de dados est�o vinculados ao usu�rio "pi" do sistema Raspbian, ou seja:

/home/pi/Desktop

Estes programas tamb�m foram testados no ambiente Windows e, neste caso, � necess�rio criar pastas com a mesma estrutura, por exemplo:

c:\home\pi\Desktop

Em ambos os casos a pasta raiz usada � a "Desktop" conforme indicado acima.
Obs: No Raspberry Pi a pasta "Desktop" � a �rea de trabalho do usu�rio "pi" mas no Windows � apenas uma pasta comum.


Pasta de imagens:

	Os programas foram adaptados para gravar e ler imagens na seguinte pasta:
	- No Raspberry Pi:
		/home/pi/Desktop/reconhecimento/Data
	- No Windows:
		C:\home\pi\Desktop\reconhecimento\Data

Programas:

1) capturandoRosto.py
	
	Este programa pede a identifica��o do aluno, pode ser um nome (n�o deve conter espa�os, barras, ou caracteres estranos) ou o 		RA do aluno, e cria uma subpasta com essa identifica��o dentro da pasta de imagens.
	
	Ativa a c�mera do Raspberry Pi (ou do Windows, video obs 1) exibe um quadro de tamanho reduzido na tela, localiza um rosto
	humano baseado em um modelo padr�o (haarcascade_frontalface_alt.xml - contido na pasta do projeto) e captura automaticamente
	at� 50 imagens do rosto do aluno fazendo um recorte de tamanho padr�o de 150x150 pixels e adaptando o tamanho para poder
	fazer a an�lise comparativa de imagens posterior. 

	O aluno pode (e deve) movimentar-se naturalmente em frente � c�mera durante o processo de captura para que o sistema tenha
	diversas imagens ligeiramente diferentes do mesmo rosto e possa criar um banco de dados com essas imagens.

	Um contador de imagens capturadas � exibida no topo da tela que mostra o rosto do aluno durante o processo. Caso n�o queira
	esperar a captura das 50 imagens o usu�rio pode teclar ESC (se houver teclado anexado) e abortar o programa.

	Pode-se reiniciar o processo posteriormente fornecendo a mesma identifica��o do aluno dada inicialmente e as novas imagens
	capturadas ser�o anexadas �quelas j� existentes na pasta de imagens.

	Obs 1: No Windows a ativa��o da c�mera, geralmente plugada via porta USB, pode requerer um par�metro complementar no comando
	de ativa��o da c�mera. Por este motivo foi usado nos programas abiblioteca "platform" que permite identificar se o programa
	est� sendo executado no Windows para usar este par�metro adicional.

2) treinandoRF.py

	Este programa ir� processar todas as imagens contidas na pasta de imagens do sistema e ir� gerar um arquivo de parametriza��o
	(modeloLBPHFace.xml) que ser� usado no terceiro programa que faz o reconhecimento facial. 
	Foi escolhido o m�todo "LBPHFaceRecognizer" (Local Binary Patterns Histograms) usado na biblioteca complementar do OpenCV
	chamada "opencv-contrib-python".

	Ap�s o treinamento (que pode demorar de alguns minutos at� v�rias horas dependendo da quantidade de imagens existentes na
	pasta de imagens e do equipamento usado) o programa dever� gerar o arquivo XML com os par�metros de reconhecimento ajustados
	para aquele conjunto de imagens. Obs: n�o misturar na mesma subpasta de imagens de um aluno fotos de outros alunos.

3) ReconhecimentoFacial.py

	Este programa ir� ativar a c�mera do Raspberry Pi (ou do Windows, video obs 1) exibe um quadro de tamanho reduzido na ela,
	localiza um rosto humano baseado em um modelo padr�o (haarcascade_frontalface_alt.xml - contido na pasta do projeto) e usa
	o m�todo "LBPHFaceRecognizer" (Local Binary Patterns Histograms) com o arquivo de modelos gerado pelo programa de treinamento
	(modeloLBPHFace.xml) para obter a identifica��o prov�vel de um rosto capturado pela c�mera. Ao encontrar um ID (sequencial)
	contido nesse arquivo de par�metros ele busca, pela ordem, o nome da pasta de imagens que corresponde ao ID encontrado e
	desenha um quadro ao redor do rosto que aparece na imagem da c�mera e imprime a identifica��o do usu�rio no alto desse
	quadro. 

4) HandGestureV(n).py

	Est�o disponibilizados nesta edi��o do projeto 2 vers�es do programa de reconhecimento de gestos das m�os.

	A primeira vers�o (HandGestureV3.py) � apenas uma corre��o do programa publicado pelas equipes anteriores para poder rodar,
	relativamente sem erros de execu��o e com um pouco mais de velocidade, no ambiente do Raspberry Pi pois este programa,
	originalmente, foi desenvolvidor fora do ambiente deste equipamento (provavelmente num PC) e continha chamadas para exibi��o
	de telas de depura��o de imagens e grava��o de um arquivo de video (desnecess�rio) que deixavam a aplica��o mais lenta. 
	Al�m disso, foi inclu�do um bloco de tratamento de excess�es pois, em determinadas situa��es, a biblioteca de reconhecimento
	de padr�es usada gerava um erro interno que parava o programa completamente. 
	Embora tenha havido alguma melhora e permita executar este programa no Raspberry Pi o modelo usado neste programa (V3) tenta
	inferir o contorno da m�o e �ngulos entre os dedos usando um m�todo que � altamente dependente de ilumina��o adequada e
	pode confundir outros elementos do ambiente como fazendo parte da an�lise. Gera muitos falsos positivos e erros de 
	identifica��o com resultados imprevis�veis.

	Dados os problemas relatados na vers�o V3 foi criada uma nova vers�o (V4) com uma abordagem totalmente diferente da anterior
	e que utiliza a biblioteca "mediapipe" (Google) com um algoritmo baseado no TensorFlow que consegue extrair das imagens a
	posi��o exata de cada dedo das m�os que permitiria at� criar um modelo 3D se necess�rio.
	A biblioteca "mediapipe" foi instalada no Raspberry Pi e nos testes realizados (diretamente no equipamento) conseguiu ler
	com precis�o a posi��o de todos os dedos da m�o. Entretanto, devido ao equipamento ser de reduzido poder de processamento,
	a velocidade de reconhecimento ficou reduzida a 1 frame por segundo mas, mesmo assim, sem erros devido a presen�a de outros
	elementos visuais na imagem e com baixa ilumina��o.
	Foram acrescentados neste programa rotinas que permitem identificar a posi��o de apenas 1 dedo (se necess�rio) ou de v�rios
	(ou todos) de uma m�o ou at� duas ao mesmo tempo. A posi��o dos dedos � desenhada virtualmente sobre a imagem da c�mera
	permitindo mostrar em destaque a posi��o de cada ponto de refer�ncia (4 por dedo e 1 na base da m�o) com cores diferentes.
	Esta vers�o ainda est� em desenvolvimento para permitir calcular os �ngulos dos dedos (em rela��o � base da imagem e entre 
	os dedos) e, eventualmente, determinar se est�o abertos, fechados, curvados, etc. Entretanto, at� essa vers�o, n�o foi 
	criado um dicion�rio de posi��es que permite, por exemplo, obter uma letra da linguagem brasileira de sinais (libras) mas
	com as fun��es implementadas at� o momento isso ser� plenamente poss�vel numa futura vers�o.

5) Faces.py

	Este � um programa exemplo de uma poss�vel interface visual que pode ser implementada no Fatequino (futuramente) no qual,
	usando-se um display de LCD acoplado no equipamento, � exibido um par de olhos que ficam "piscando" quando o equipamento,
	atrav�s da c�mera, consegue encontrar um rosto nas imagens capturadas e, ao identificar um aluno, � exibida sua 
	identifica��o no alto da tela. 
	Foram reunidos, num c�digo s�, rotinas que desenham olhos (com base em imagens que est�o na subpasta imagens) em v�rias
	posi��es (abertos, cerrados, fechados, piscando) e os programas de captura de rostro (item 1) que localiza nas imagens da
	c�mera um rosto gen�rico e, neste caso, mostra os olhos em posi��o "cerrada" (como se estivesse tentando reconhecer algu�m)
	e o programa de reconhecimento facial (item 3) que, quando consegue encontrar um ID correspondente ao rosto, pisca um dos
	olhos e exibe no alto da tela a identifica��o do aluno. Os olhos ficam piscando na tela de tempos em tempos como acontece
	com uma pessoa mostrando que o programa est� em funcionamento normal e gerando uma maior empatia com o usu�rio.
	Al�m disso, caso as imagens do aluno estejam na pasta com nome especial chamada "DEMO" durante o processo de treinamento, 
	ser� exbida uma figura de fundo com uma imagem de terror (zumbi). Isso � um exemplo de uma aplica��o l�dica que pode ser
	criada acoplando-se um display no Fatequino e permita uma maior intera��o com o usu�rio.

	Pode-se tamb�m aprimorar essa interface gr�fica com um "rosto" e com acesso, pela internet, a outros dados relativos ao
	aluno identificado exibindo-se, em forma adequada, tais informa��es na tela tornando o projeto mais interativo e simp�tico
	ao ser humano.



	
