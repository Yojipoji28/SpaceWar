import pygame
import os

class Cubo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 80
        self.alto = 80
        self.velocidad = 10
        self.color = "red"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        # Carga la imagen usando ruta relativa
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.imagen = pygame.image.load(os.path.join(base_dir, "media", "nave.webp"))
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        #self.imagen = pygame.transform.rotate(self.imagen, 90)  #para rotar la imagen

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        #al comentar el rectangulo, hacemos que solo se dibuje la imagen
        ventana.blit(self.imagen,(self.x, self.y))
        