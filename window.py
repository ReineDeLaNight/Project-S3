import pygame
from pygame.locals import *
from create_button import button
from display import display
from live_display import live_display
from Hive import hive
from Shop import shop

class window():

    def __init__(self):
        pygame.init()

        # self._clock = pygame.time.Clock()
        
        self._call_same = True # Pour savoir si l'appel d'affichage est le même

        # Initialisation des boutons
        self._quit_button = None
        self._launch_game_button = None
        self._bees_button = None
        self._shop_button = None
        self._fight_button = None
        self._buy_bee_button = None
        self._get_honey_button = None
        
        self._w, self._h = self.getSize()
        self._window = pygame.display.set_mode((self._w, self._h), pygame.FULLSCREEN)
        self._title = "BEETTHEFUCKOUTOFMYWIFE"
        self._display = display()
        pygame.display.set_caption(self._title)
        self._surface = self._display.display_menu(self._w, self._h) # _surface est la surface qui doit contenir tout ce qui concerne l'affichage, à bien différencier avec _window
        
        self._live = None # attribut pour déterminer si un affichage doit se faire à chaque itération de la boucle principales
        self.live_display = live_display()
        self.blank_surface = pygame.Surface((1920,1080))
        self.blank_surface.fill((255,255,255))
        
        
    def main_loop(self):
        
        run = True
        while run:

            # ------------------------ Afficher des données à chaque tick
            jaj = pygame.Surface.copy(self._surface) # pour éviter la shadow copie de l'enfer
            live_surface = self.live_display.give_display(self._live, jaj)
            # ------------------------
            
            self._window.blit(pygame.transform.scale(live_surface, (self._w, self._h)), (0,0)) # transforme l'image selon la résolution de l'image
            pygame.display.flip()
            run = self.event_handler(pygame.event.get())
            # self._clock.tick(60)     

            
    def event_handler(self, event_list, run = True):
        
        for event in event_list:
            #print(event)
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            if event.type == MOUSEBUTTONDOWN:
                #print(self._display._button_dic)
                self._last_button = event.type
                if "quit_button" in self._display._button_dic:
                    if self._display._button_dic["quit_button"].is_over(event.pos):
                        run = False
                        pygame.quit()
                        break
                if "launch_game_button" in self._display._button_dic:
                    if self._display._button_dic["launch_game_button"].is_over(event.pos):
                        self.game_init()
                        self._surface = self._display.display_new_game(self._w, self._h)
                        break
                if "bees_button" in self._display._button_dic:
                    if self._display._button_dic["bees_button"].is_over(event.pos):
                        self._surface = self._display.display_management()
                        break
                if "shop_button" in self._display._button_dic:
                    if self._display._button_dic["shop_button"].is_over(event.pos):
                        self._surface = self._display.display_shop(self._w, self._h, self.shop.bees())
                        break
                if "fight_button" in self._display._button_dic:
                    if self._display._button_dic["fight_button"].is_over(event.pos):
                        self._surface = self._display.display_fight()
                        break
                if "buy_bee_button" in self._display._button_dic:
                    if self._display._button_dic["buy_bee_button"].is_over(event.pos):
                        self.test_bee()
                        break

        return run


    def getSize(self):
        return pygame.display.Info().current_w, pygame.display.Info().current_h

    def game_init(self):
        self.hive = hive()
        self.shop = shop()

    def test_bee(self):
        for bee in self.shop._bees:
            if self._display._button_dic["buy_bee_button"]._get == bee._name:
                shop.buy_bee(self, self.hive, bee)

window = window()
window.main_loop()