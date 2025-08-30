import pygame
import os

class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad = 5
        self.color = "purple"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.vida = 2
         # Carga la imagen usando ruta relativa
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.imagen = pygame.image.load(os.path.join(base_dir, "media", "ovni.webp"))
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        #self.imagen = pygame.transform.rotate(self.imagen, 90)  #para rotar la imagen

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen,(self.x, self.y))
        
    def movimiento(self):
        self.y += self.velocidad