import pygame,time,sys, os 
import random as rd 

pygame.init()
display = pygame.display.set_mode([800,600]) #resolução
displayColor = (192,217,217)
display.fill(displayColor) #cor da tela //chama
pygame.display.set_caption("Game") #título da aba

class cCar(): ##classe do objeto carro
    image = 'car.png'
    car = pygame.image.load(image).convert_alpha() #variavel car recebe a imagem
    carXY = car.get_rect() #pega as posições X e Y da imagem
    carY = carXY.y
    carX = carXY.x
    carSpeed = 10 # se movimenta 10 a cada vez que passar no while true
    rotate = 0
class cBoost(): ##classe do objeto impulso
    image = 'boost.png'
    boost = pygame.image.load(image).convert_alpha()
    boostXY = boost.get_rect()
    boostY = boostXY.y
    boostX = boostXY.x
    boostSpeed = 6

class cTree(): ##classe do objeto arvore
    image = 'arvore1.png'
    arvore = pygame.image.load(image).convert_alpha()
    arvoreXY = arvore.get_rect()
    arvoreY = arvoreXY.y
    arvoreX = arvoreXY.x
    arvoreSpeed = 20 # a arvore se 'move' 20 a cada vez que passar no while true

class cBarrier(): ##classe do objeto barreira
    image = 'barreira.png'
    barreira = pygame.image.load(image).convert_alpha()
    barreiraXY = barreira.get_rect()
    barreiraY = barreiraXY.y
    barreiraX = barreiraXY.x
    barreiraSpeed = 10
    colision = False # para contar só uma colisão e não 30 em uma só

class cRocket(): ##classe do objeto foguete
    image = 'rocket.png'
    rocket = pygame.image.load(image).convert_alpha()
    rocketXY = rocket.get_rect()
    rocketY = rocketXY.y
    rocketX = rocketXY.x
    rocketSpeed = 5
    rocketAmmo = 0 #munição

def createSurface(size=(300,600), color=(112,219,13)): #Metodo para criar superficies
    surface = pygame.Surface((size)) #seta o tamanho da surpeficie
    surface.fill(color) ##preenche a cor da surpeficie
    return surface

# ESSA FUNÇÃO PODE SER SUBSTITUIDA PELO COLID, MAS FUNCINA ASSIM ENTAO TA TOP (verifica a colisão - recebe as posições X e Y 
# de dois objetos, e verifica se um está dentro do outro)
def colision(enemyX, enemyY, playerX, playerY):
    if enemyY < playerY+20 and enemyY > playerY-20 and playerX-30 < enemyX  and enemyX < playerX +30:
        return True
    else:
        return False

 # ESPERA O USUARIO APERTAR UMA TECLA
def waitKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                return True

# MOTRA NA TELA PRO USUARIO PRESSIONAR TECLA
def draw():
    fontstart = pygame.font.Font('freesansbold.ttf', 40) # tipo e tamanho da letra
    start = 'Pressione qualquer tecla para iniciar'
    textstart = fontstart.render(start, True, (0,0,205), displayColor ) # recebe a variavel start, (que é
    # o que vai aparecer na tela) e as cores
    textstartRect = textstart.get_rect()
    textstartRect.center = (400,350) #posição do texto na tela
    display.blit(textstart, textstartRect) #TUDO O QUE VAI APARECER NA TELA
    pygame.display.update() ##atualiza tela
    time.sleep(2) #em segundos
    return waitKey() #função booleana

# TELA DE GAME OVER
def gameOver(p):
    fontstart = pygame.font.Font('freesansbold.ttf', 34)
    start = 'Você foi capturado! Perdeu! Pontos: ' + str(p)
    textstart = fontstart.render(start, True, (0,0,205), displayColor )
    textstartRect = textstart.get_rect()
    textstartRect.center = (400,350)
    display.blit(textstart, textstartRect)
    pygame.display.update()
    time.sleep(3)
    __main__()

def __main__():
    pygame.init()
    policeSound = pygame.mixer.music.load('police.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.07)
    # AUDIO DE EXPLOSAO E POLICIA ### POLICIA N TA FUNCIONANDO PQ POR ALGUM MOTIVO O AUDIO DO SOM DA POLICIA SUMIU ???
    explosion = pygame.mixer.music.load('explosion.mp3')

    display = pygame.display.set_mode([800,700]) #resolução
    displayColor = (105,105,105)

    display.fill(displayColor) #cor da tela //chama
    pygame.display.set_caption("Game") #título da aba
    timeClock = pygame.time.Clock()
     #variavel para sair do jogo

     # CARRO DO JOGADOR
    carPlayer = cCar()
    carPlayer.carY = 400
    carPlayer.carX = 300
    carPlayer.carSpeed = 14
    carRotate = carPlayer.car
    ammo = 0

    #CARRO DA POLICIAAAAAA
    car = cCar() #CARRO DA POLICIA
    car.carX =  carPlayer.carX
    car.carY = 600
    car.carSpeed = 1
    car.car = pygame.image.load('policeCar.png').convert_alpha()

    #RAIOZINHO QUE CAI
    boost = cBoost()
    boost.boostX = rd.randint(200,500)
    boost.boostY = -40

    # ARVORE KK
    arvore =cTree()
    arvore.arvoreX = rd.randint(20,120) # gera posição aleatorio pro eixo x da arvore entre o campo verde la, do gramado 
    # supostamente
    arvore.arvoreY = -50
    arvore2 = cTree()

    #A OUTRA ARVORE KKK
    arvore2.arvore = pygame.image.load('arvore2.png').convert_alpha()
    arvore.arvoreX = rd.randint(20,120)
    arvore.arvoreY = -75

    #BARREIRA QUE CAI
    barreira = cBarrier()
    barreira.barreiraX = rd.randint(200,500)
    barreira.barreiraY = -40

    #REPETE A ULTIMA TECLA CLICADA PRO USUARIO NÃO PRECISAR FICAR CLICANDO NA TECLA TODA VEZ QUE QUISER SE MOVIMENTAR POR EX
    pygame.key.set_repeat(2)

    #FOGUETE POW POW
    rocket = cRocket()
    rocket.rocketX = rd.randint(200,500)
    rocket.rocketY = -40
    rocket.rocketAmmo = 0
    rocket.rocket = pygame.transform.rotate(rocket.rocket, 180) #efeito de rotação no carro quando colide com a barreira.
    # Altera o angulo da imagem do carro


    #TIRO DO FOGUETE ## ACONTECE QUANDO O CARRO PEGA O FOGUETE
    shot = cRocket()
    shot.rocketY = -50
    shot.rocketX = -50
    shot.rocket = pygame.transform.rotate(shot.rocket, 180)
    shooting = False

 #PONTUAÇÃO
    score=0

#MOSTRA MUNIÇÃOOOOOO
    font = pygame.font.Font('freesansbold.ttf', 26)
    municao = 'Munição: ' + str(ammo)
    text = font.render(municao, True, (105,140,105),(105,15,105))
    textRect = text.get_rect()
    textRect.center = (700,30)

#MOSTRA OS PONTOS
    scoreShow = 'Pontos: ' + str(score)
    textScore = font.render(scoreShow, True, (105,140,105),(105,15,105))
    textScoreRect = textScore.get_rect()
    textScoreRect.center = (700,30)

    ##tecla para iniciar o jogo

#CHAMA A FUNÇÃO PRA MOSTRAR "PRESSIONE TECLA"
    inGame = draw()

    while inGame: #enquanto True o jogo fica ativo
        timeClock.tick(30) # 30 é a taxa de FPS (Frames por segundo)

        #VELOCIDADE E MOVIMENTO DO CARRO DA POLICIA ###
        car.carY -= car.carSpeed
        car.carSpeed += 0.05
        

        #FAZ COM QUE AS ARVORES SE 'MOVAM'
        barreira.barreiraY += arvore.arvoreSpeed
        arvore.arvoreY += arvore.arvoreSpeed
        arvore2.arvoreY += arvore2.arvoreSpeed
        display.fill(displayColor) #cor da tela //chama

        # ACHO QUE ISSO AQUI COLOCA AS GRAMAS DO LADO
        display.blit(createSurface((500,700),(34,139,34)), [600,0])
        display.blit(createSurface((200,700),(34,139,34)), [0,0])
        

        ## FOR PARA VERIFICAR SE TECLA FOI CLICADA
        for event in pygame.event.get():  #captura cada evento que ocorrer na tela

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #se o evento for do tipo 'quit', a váriavel quitGame é true e sai do While
                    inGame = False
                if (event.key == pygame.K_LEFT or event.key == ord('a')) and carPlayer.carX > 205:
                    carPlayer.carX -= carPlayer.carSpeed
                if (event.key == pygame.K_RIGHT or event.key == ord('d')) and carPlayer.carX < 580:
                    carPlayer.carX += carPlayer.carSpeed
                if (event.key == pygame.K_UP or event.key == ord('w')):
                    carPlayer.carY -= carPlayer.carSpeed - 9.8
                    car.carSpeed = car.carSpeed - 0.1
                    arvore.arvoreSpeed += 0.08
                    arvore2.arvoreSpeed += 0.08
                if (event.key == pygame.K_DOWN or event.key == ord('s')):
                    carPlayer.carY += carPlayer.carSpeed - 9
                    car.carSpeed = car.carSpeed + 0.3
                    arvore.arvoreSpeed -= 0.2
                    arvore2.arvoreSpeed -= 0.2
                # SE A ESPAÇO PRA ATIRAR FOR CLIDADA, A VARIAVEL SHOOTING É 'ATIVADA'
                if (event.key == pygame.K_SPACE or event.key == ord(' ')) and shooting == False:
                    if ammo>0: # SE A MUNIÇÃO FOR MANOR DO QUE 0, ELE ATIRA
                        shooting = True
                    shot.rocketY = carPlayer.carY
        showAmmo = ammo # VARIAVEL PRA MOSTRAR A MUNIÇÃO

        #IF PRA ATIRAR
        if shooting == True and ammo>0: # SE A VARIAVEL SHOOTING FOR TRUE E TIVER MUNIÇÃO, ELE ATIRA
            shot.rocketX = carPlayer.carX
            shot.rocketY += shot.rocketSpeed + 3
            showAmmo-=1
            if shot.rocketY > car.carY: #SE A ROCKET PASSAR DO Y DO CARRO É COMO SE TIVESSE ACERTADO E ELE VOLTA PRO INICIO
                shooting = False
                car.carY = 730
                car.carSpeed = 0.3
                ammo-=1
                shot.rocketY = -50
                shot.rocketX = -50

        # SE O CARRO DO JOGADOR FOR MAIOR QUE 140 ELE FICA SEMPRE EM 140
        if carPlayer.carY < 140:
            carPlayer.carY = 140

        # NÃO DEIXA O CARRO DO JOGADOR SUMIR DA TELA POR BAIXO
        if carPlayer.carY > 680:
            carPlayer.carY = 680

    #CARRO DA POLICIA NAO SAIR DA TELA
        if car.carY > 640:
            car.carY = 640

    #SE O CARRO DA POLICIA COLIDE COM O PLAYER
        if carPlayer.carY > car.carY - 35 :
            car.carY = 730
            car.carSpeed = 1
            gameOver(score)
            score = 0
 ### ROCKET E O RAIZINHO SE MOVIMETAM
        boost.boostY+= boost.boostSpeed
        rocket.rocketY+= rocket.rocketSpeed

######### 'SETA' O CARRO DO JOGADOR NA TELA
        display.blit(carPlayer.car, [carPlayer.carX, carPlayer.carY])
        car.carX = carPlayer.carX

    #SE O FOGUETE SAI DA TELA
        if rocket.rocketY > 720:
            rocket.rocketY = -500

        #O RAIO DESAPARECE QUANDO FICA LONGE DO CARRO
        if  boost.boostY - carPlayer.carY > 150: ##calcula se o raio está longe do carro, aí da respawn de novo
            boost.boostX = rd.randint(200,500)
            boost.boostY = -400

        #VELOCIDDES DAS ARVORES
        if (arvore2.arvoreSpeed and arvore.arvoreSpeed) > 31:
                arvore2.arvoreSpeed = 30
                arvore.arvoreSpeed = 30

            #colisão do raio com o carro
        if  colision(boost.boostX, boost.boostY, carPlayer.carX, carPlayer.carY): #boost.boostY < carPlayer.carY+20 and boost.boostY > carPlayer.carY and carPlayer.carX-20 < boost.boostX  and boost.boostX < carPlayer.carX +30:
            car.carSpeed = -3.0
            boost.boostY = -400
            boost.boostX = rd.randint(200,500)
            boost.boostSpeed += 0.4
            arvore.arvoreSpeed += 0.1
            arvore2.arvoreSpeed += 0.1

       ##COLISAO DO FOGUETE COM O CARRO/MUNICAO
        if  colision(rocket.rocketX, rocket.rocketY, carPlayer.carX, carPlayer.carY):
            rocket.rocketY = -1200

            if ammo < 3:
                ammo += 1
            else:
                ammo = 3

            rocket.rocketX = rd.randint(200,570)

            #se as arvores saiRAM da tela
        if arvore.arvoreY > 720 and arvore2.arvoreY > 720:
            arvore.arvoreY = -700
            arvore.arvoreX = rd.randint(20,120)
            arvore2.arvoreY = -300
            arvore2.arvoreX = rd.randint(20,120)

            #se a barreira saiu da tela
        if barreira.barreiraY > 720:
            barreira.colision = False
            barreira.barreiraY = -300
            barreira.barreiraX = rd.randint(200,570)

            #colisão da barreira com o carro
        if barreira.colision == False and colision(barreira.barreiraX, barreira.barreiraY, carPlayer.carX, carPlayer.carY):
            car.carSpeed += 6
            barreira.colision = True
            carPlayer.rotate = 40
            carPlayer.car = pygame.transform.rotate(carRotate, carPlayer.rotate) #muda a rotação da imagem pra simular q ele batue no obstaculos
            if arvore.arvoreSpeed > 5:
                arvore.arvoreSpeed -= 5
            if arvore2.arvoreSpeed > 5:
                arvore2.arvoreSpeed -= 5

        ## O EFEITO DE 'RODOPIAR' NO CARRO USANDO A ROTAÇÃO DO ANGULO DA IMAGEM
        if carPlayer.rotate > 0:
            carPlayer.rotate -= 5
            carPlayer.car = pygame.transform.rotate(carRotate, carPlayer.rotate)
   ##### MOSTRAM AS MUNIÇÕES E A PONTUAÇÃO
        score +=1
        scoreShow = 'Pontos: ' +str(score)
        textScore = font.render(scoreShow, True, (105,140,105),(105,15,105))
        textScoreRect = textScore.get_rect()
        textScoreRect.center = (700,80)
        display.blit(textScore, textScoreRect)

        municao = 'Munição: ' + str(showAmmo)
        text = font.render(municao, True, (105,140,105),(105,15,105))
        display.blit(text, textRect)


        ## TODOS ESSES 'BLITS' COLOCAM OS OBJETOS NA TELA DISPLAY QUE CRIAMOS LA EM CIMA
        display.blit(barreira.barreira, [barreira.barreiraX, barreira.barreiraY])
        display.blit(arvore2.arvore, [arvore2.arvoreX, arvore2.arvoreY])
        display.blit(arvore.arvore, [arvore.arvoreX, arvore.arvoreY])
        display.blit(boost.boost, [boost.boostX,boost.boostY])
        display.blit(car.car, [car.carX,car.carY])
        display.blit(rocket.rocket, [rocket.rocketX,rocket.rocketY])
        display.blit(shot.rocket, [shot.rocketX,shot.rocketY])
        pygame.display.update()
        #print('police:', car.carSpeed)
    pygame.quit() #fecha o jogo

__main__()
