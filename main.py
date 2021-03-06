import pygame
from random import randint
from pygame.locals import *


# Initialisation de la bibliotheque pygame
pygame.init()

#Tableau de sauvegarde de bonnes balles
bulletnew = []
#tableau pour tirs multiples
bullets = []

#tableau des enemis
ennemis = []

#creation de la fenetre
largeur = 1280
hauteur = 720
fenetre=pygame.display.set_mode((largeur,hauteur))

# lecture de l'image du perso
#imagePerso = pygame.image.load("perso.png").convert_alpha()
#############################################################
# Animation personnage
imagesPerso = []
imagesPerso.append(pygame.image.load('ship1.png'))
imagesPerso.append(pygame.image.load('ship2.png'))
imagesPerso.append(pygame.image.load('ship3.png'))
imagesPerso.append(pygame.image.load('ship4.png'))
index = 0
imagePerso = imagesPerso[index]
#############################################################

#lecture de l'image de l'enemie
imageEnemi = pygame.image.load("perso2.png").convert_alpha()

#son background
pygame.mixer.music.load('OST.mp3')

# creation d'un rectangle pour positioner l'image du personnage
rectPerso = imagePerso.get_rect()
rectPerso.x = 90
rectPerso.y = 100


#lecture du projectile
imageBullet = pygame.image.load("balle.png").convert_alpha()
time = 0
timer = 0

#bordures
borderLeft = (hauteur - rectPerso.y)
borderRight = ( largeur - rectPerso.x)

# lecture de l'image du fond
imageFond = pygame.image.load("background.png").convert()
imageFond2 = pygame.image.load("background.png").convert()

# creation d'un rectangle pour positioner l'image du fond
rectFond = imageFond.get_rect()
rectFond.x = 0
rectFond.y = 0
rectFond2 = imageFond2.get_rect()
rectFond2.x = 0
rectFond2.y = 720

# creation d'un rectangle pour positioner du perso
rectPerso = imagePerso.get_rect()
rectPerso.x = 400
rectPerso.y = 100

# Choix de la police pour le texte
font = pygame.font.Font(None, 34)

score=0
# Creation de l'image correspondant au texte
imageText = font.render('SCORE : '+str(score), True, (255, 255, 255))
rectText = imageText.get_rect()
rectText.x = 10
rectText.y = 10

vie=3
# Creation de l'image correspondant au texte
imageText2 = font.render('Life : '+str(vie), True, (255, 255 , 255))
rectText2 = imageText2.get_rect()
rectText2.x = 1200
rectText2.y = 10


# servira a regler l'horloge du jeu
horloge = pygame.time.Clock()
i=1;
continuer=1
time=0
tps=0

son = pygame.mixer.music.play()
while continuer:

    # fixons le nombre max de frames / secondes
    horloge.tick(60)
    time+=1
    i=i+1
    #print (i)
    #print(score)
    #score = 0

    rectFond.y += 1
    rectFond2.y += 1

    if rectFond.y >= borderLeft:
                rectFond.y = - hauteur
    if rectFond2.y >= borderLeft:
                rectFond2.y = - hauteur


    # on recupere l'etat du clavier
    touches = pygame.key.get_pressed();


        #deplacement de perso
    if touches[K_RIGHT] :
            rectPerso.x = rectPerso.x + 10

    if touches[K_LEFT] :
            rectPerso.x = rectPerso.x - 10

    if touches[K_UP] :
            rectPerso.y = rectPerso.y - 10

    if touches[K_DOWN] :
            rectPerso.y = rectPerso.y + 10

    if rectPerso.x <= 0 :
            rectPerso.x = 0

    if rectPerso.x > borderRight :
            rectPerso.x = borderRight

    if rectPerso.y <= 400 :
            rectPerso.y = 400

    if rectPerso.y > borderLeft :
            rectPerso.y = borderLeft

    #Creation des enemis

    if tps==0:
        Enemi= imageEnemi.get_rect()

        Enemi.x = randint(100,1100)
        Enemi.y = -100

        ennemis.append(Enemi)
        tps= 100

    tps-=1

    # deplacement des ennemis
    for Enemi in ennemis :
           Enemi.y = Enemi.y + 2


    # le perso tire
    if touches[K_SPACE] and time/30>=0.7:
        rectBullet = imageBullet.get_rect()
        rectBullet.x =  rectPerso.x +20
        rectBullet.y = rectPerso.y
        bullets.append(rectBullet)
        time=0

    # nettoyage des ennemis sortis
    TAB=[]
    for r in ennemis:
        if r.y < hauteur :
            TAB.append(r)

    ennemis = TAB


    # deplacement des tirs
    for rectBullet in bullets:
            rectBullet.y = rectBullet.y - 10

    #rafraichissement tirs
    bullets2=[]

    for rectBullet in bullets:
        if rectBullet.y >0 :
            bullets2.append(rectBullet)
            rectBullet.y = rectBullet.y - 10
    bullets=bullets2


    #VIRER LES TIRS UTILISES
    eAvirer = []
    tAvirer = []

    for Enemi in ennemis:
        for rectBullet in bullets:
            if  Enemi.colliderect(rectBullet):
                eAvirer.append(Enemi)
                tAvirer.append(rectBullet)
                score = score + 50

    #collision ennemi-perso
    coup = 0
    for Enemi in ennemis:
        if Enemi.colliderect(rectPerso):
            eAvirer.append(Enemi)
            coup += 1

    if coup == 1:
        vie = vie - 1

    if vie == 0:
        continuer = 0


    for Enemi in eAvirer:
        ennemis.remove(Enemi)


    for rectBullet in tAvirer:
        bullets.remove(rectBullet)

    if score > 500 :
        if tps==0 :
            Enemi= imageEnemi.get_rect()
            Enemi.x = randint(500,1150)
            Enemi.y = -500
            ennemis.append(Enemi)


    tps -= 1

    #print ("nb Bullets "+ str(len(bullets)))
    #print ("nb enemie "+ str(len(Enemi)))

    # si la touche ESC est enfoncee, on sortira
    # au debut du prochain tour de boucle
    if touches[pygame.K_ESCAPE] :
        continuer=0



    # Affichage du fond
    fenetre.blit(imageFond, rectFond)
    fenetre.blit(imageFond2, rectFond2)

    # Affichage Perso
    #fenetre.blit(imagePerso, rectPerso)
    if i%5==0 :
        index=(index+1)%len(imagesPerso)
    fenetre.blit(imagesPerso[index], rectPerso)

    # Affichage enemi
    for Enemi in ennemis:
        fenetre.blit(imageEnemi, Enemi)

    # Affichage du Texte
    fenetre.blit(imageText, rectText)
    fenetre.blit(imageText2, rectText2)


    #affichage des balles
    for rectBullet in bullets:
            fenetre.blit(imageBullet, rectBullet)


    imageText = font.render('SCORE : '+str(score), True, (255, 255, 255))
    rectText = imageText.get_rect()
    rectText.x = 10
    rectText.y = 10

    imageText2 = font.render('Vie : '+str(vie), True, (255, 255 , 255))
    rectText2 = imageText2.get_rect()
    rectText2.x = 1200
    rectText2.y = 10

    # rafraichissement
    pygame.display.update()
    # rafraichissement
    pygame.display.flip()

    # Si on a clique sur le bouton de fermeture on sortira
    # au debut du prochain tour de boucle
    # Pour cela, on parcours la liste des evenements
    # et on cherche un QUIT...
    for event in pygame.event.get():   # parcours de la liste des evenements recus
        if event.type == pygame.QUIT:     #Si un de ces evenements est de type QUIT
            continuer = 0          # On arrete la boucle

# fin du programme principal...
pygame.quit()
