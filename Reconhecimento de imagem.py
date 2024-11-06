#IMPORTA BIBLIOTECAS: opencv - mediapipe - pyserial
import cv2 #opencv para acessar a câmera do notebook
import mediapipe as mp #mediapipe para usar a feature de finger capture
import serial.tools.list_ports #pyserial para comunicação serial com o arduino


# CONFIGURAÇÃO DA COMUNICAÇÃO SERIAL COM O ARDUINO UNO:
# Cria uma variável para armazenar as portas seriais comportadas
# Acessa as portas seriais disponíveis e cria uma lista com elas
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

# Apresenta a lista de portas e seus respectivos itens conectados
for one in ports:
    portsList.append(str(one))
    print(str(one))

# Pede para digitar a porta que o arduino está conectado para estabelecer a conexão
com = input("Selecione a porta COM do Arduino#: ")

for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(use)

# Estabelece a comunicação, a taxa de atualização das informações (baudrate)
# e abre a comunicação com o arduino para o código
serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()


# CONFIGURAÇÃO DO RECONHECIMENTO DE IMAGEM PELA WEBCAM DO NOTEBOOK:
# Abre a webcam e verifica se não houve nenhum erro de inicialização
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Erro ao abrir a webcam.")
    exit()

# Realiza o mapeamento da mão, define o número mãximo de mãos detectadas
# e desenha a ligação de pontos na mão
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Cria uma variável que checa se a câmera está funcionando
# além de apresentar na tela um feedback da imagem que está sendo capturada
while True:
    check, img = video.read()
    if not check:
        print("Erro ao capturar imagem da webcam.")
        break

# Converte a imagem capturada em uma imagem na escala de cinza, para filtrar possíveis ruídos
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)

# Atribui aos pontos do mapeamento, números, para que possam ser comparados para a lógica do contador
    handsPoints = results.multi_hand_landmarks
    altura, largura, _ = img.shape
    pontos = []
    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * largura), int(cord.y * altura)
                pontos.append((cx, cy))

# Informa quais são os pontos mais altos dos dedos, e faz a lógica de comparação
# do ponto mais alto do dedo, com o ponto mais baixo. Caso isso seja verdadeiro
# o algoritmo entende que o dedo está levantado e adiciona um ao contador
        dedos = [8, 12, 16, 20]
        contador = 0
        if points:
            for x in dedos:
                if pontos[x][1] < pontos[x-2][1]:
                    contador += 1

# Exibe na tela um contador para facilitar o feedback de utilização do código
        print(contador)
        cv2.putText(img, str(contador), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 5)

# Envia o número de dedos levantados para o Arduino
        try:
            serialInst.write(str(contador).encode('utf-8'))
        except Exception as e:
            print(f"Erro ao enviar dados para o Arduino: {e}")


# Nomeia a tela de feedback do utilizador e cria um atalho para finalização do código (tecla "q")
    cv2.imshow("Reconhecimento de Imagem - Pardobboots Art 2024", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Ao apertar "q" encerra o acesso a webcam, fecha a janela do retorno e encerra a comunicaçao com o arduino
video.release()
cv2.destroyAllWindows()
serialInst.close()
