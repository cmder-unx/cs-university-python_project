import pygame
import sys
from constants import *


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
base_font = pygame.font.Font(None, 45)
base_font2 = pygame.font.Font(None, 20)
base_font3 = pygame.font.Font(None,40)

titre = 'Jeu de Dames !'
ordre = 'Entre ton adresse réseau local pour jouer avec un ami (si tu en as)'

#Ce qui sera saisi par l'utilisateur
user_text=''
#Le rectangle du champ de saisie
input_rect = pygame.Rect(150,200,100,32)

#Le rectangle du bouton entrer
join_button_rect=pygame.Rect(175,250,155,40)
#Le texte "Rejoindre"
join_button_text='Rejoindre'

color=pygame.Color('blue')

while True:
    mouse_position: tuple[int, int] = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                #Pour pouvoir utiliser la touche Effacer
                user_text=user_text[:-1]
            elif event.key == pygame.K_RETURN:
                print(user_text)
            else:
                user_text+=event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if join_button_rect.collidepoint(mouse_position):
                print(user_text)
                user_text=''
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0,0,0))

    #Titre
    text_titre=base_font.render(titre,True,BLUE)
    screen.blit(text_titre,(150,70))

    #consigne d'entrer l'IP
    text_ordre=base_font2.render(ordre,True,BLUE)
    screen.blit(text_ordre,(50,150))

    #champ de saisie
    pygame.draw.rect(screen,color,input_rect)

    text_surface=base_font.render(user_text,True,(255,255,255))
    screen.blit(text_surface,(input_rect.x +5,input_rect.y+5))

    #pour redimensionner le champ de saisie
    input_rect.w=max(200,text_surface.get_width()+10)

    #touche Entrée
    pygame.draw.rect(screen,GREEN,join_button_rect)

    #texte entrée
    text_entree=base_font.render(join_button_text,True,WHITE)
    screen.blit(text_entree,(join_button_rect.x+5,join_button_rect.y+5))
    pygame.display.flip()
    CLOCK.tick(60)

    