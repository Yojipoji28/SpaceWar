import pygame
import os
import sys
from personaje import Cubo
from enemigo import Enemigo
from bala import Bala
from item import Item
import random

# Obtiene la ruta de la carpeta donde está el ejecutable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pygame.init()
pygame.mixer.init()

ANCHO = 1000  # ancho de ventana
ALTO = 800  # alto de ventana
VENTANA = pygame.display.set_mode([ANCHO, ALTO])  # creamos ventana
FPS = 60  # fps a los que irá el juego

# Declaramos las distintas fuentes a usar
FUENTE = pygame.font.SysFont("Comic Sans", 40)
FUENTE_OVER = pygame.font.SysFont("Comic Sans", 70)
FUENTE_NAME = pygame.font.SysFont("Comic Sans", 50)
FUENTE_INICIO = pygame.font.SysFont("Comic Sans", 80)

fondo = pygame.image.load(os.path.join(BASE_DIR, 'media', 'espacio.jpg'))
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Declaramos los sonidos usados en el juego
SONIDO_FONDO = pygame.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'fondo.wav'))
SONIDO_DISPARO = pygame.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'laser2.wav'))
MUERTE_OVNI = pygame.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'muerteovni.wav'))
MUERTE_NAVE = pygame.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'muertenave.wav'))
VIDA_EXTRA = pygame.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'vida.mp3'))

SONIDO_FONDO.play(loops=-1)  # hacemos que se repita sin parar

ultima_bala = 0

def pantalla_inicio():
    # Muestra la pantalla de inicio y espera que el usuario presione Enter para comenzar.
    mostrando_inicio = True
    while mostrando_inicio:
        VENTANA.blit(fondo, (0,0))
        titulo = FUENTE_INICIO.render("SpaceWar", True, "white")
        instruccion = FUENTE.render("Presiona ENTER para comenzar", True, "white")
        
        VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 2 - 150))
        VENTANA.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO // 2 + 250))
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Si se presiona Enter
                    mostrando_inicio = False

def pantalla_game_over(puntos):
    nombre = ""
    continuar_rect = pygame.Rect(ANCHO // 2 - 120, ALTO // 2, 250, 60)
    salir_rect = pygame.Rect(ANCHO // 2 - 120, ALTO // 2 + 70, 250, 60)

    escribiendo_nombre = True

    while escribiendo_nombre:
        VENTANA.blit(fondo, (0,0))

        # Mostrar "GAME OVER"
        texto_game_over = FUENTE_OVER.render("GAME OVER", True, "white")
        VENTANA.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 350))

        # Mostrar campo para ingresar nombre
        texto_nombre = FUENTE_NAME.render(f"Nombre: {nombre}", True, "white")
        VENTANA.blit(texto_nombre, (ANCHO // 2 - texto_nombre.get_width() // 2, ALTO // 2 - 150))

        # Mostrar botones de continuar y salir
        texto_continuar = FUENTE.render("Continuar", True, "black")
        texto_salir = FUENTE.render("Salir", True, "black")
        pygame.draw.rect(VENTANA, "grey", continuar_rect)
        pygame.draw.rect(VENTANA, "grey", salir_rect)
        VENTANA.blit(texto_continuar, (continuar_rect.x + 40, continuar_rect.y - 1))
        VENTANA.blit(texto_salir, (salir_rect.x + 80, salir_rect.y + 3))

        # Mostrar los puntajes más altos en la esquina inferior izquierda
        puntajes_altos = obtener_puntajes_altos()
        y_offset = ALTO - 160  # Comenzar desde la parte inferior
        posiciones = ["1º", "2º", "3º"]  # Etiquetas para las posiciones
        for i, (nombre_puntaje, puntaje) in enumerate(puntajes_altos):
            texto_puntaje = FUENTE.render(f"{posiciones[i]} {nombre_puntaje}: {puntaje}", True, "white")
            VENTANA.blit(texto_puntaje, (20, y_offset))
            y_offset += 40  # Espacio entre cada puntaje

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Usa sys.exit() para salir del programa
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.key == pygame.K_RETURN:
                    if nombre:
                        escribiendo_nombre = False
                else:
                    if evento.key >= pygame.K_a and evento.key <= pygame.K_z or evento.key >= pygame.K_0 and evento.key <= pygame.K_9:
                        nombre += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if continuar_rect.collidepoint(evento.pos):
                    if nombre:
                        guardar_puntuacion(nombre, puntos)
                        return True
                elif salir_rect.collidepoint(evento.pos):
                    if nombre:
                        guardar_puntuacion(nombre, puntos)
                        pygame.quit()
                        sys.exit()  # Usa sys.exit() para salir del programa


def guardar_puntuacion(nombre, puntos):
    # Asegúrate de que el archivo se maneje correctamente
    try:
        with open('puntuaciones.txt', 'a') as archivo:
            archivo.write(f"{nombre} - {puntos}\n")
    except IOError as e:
        print(f"Error al guardar la puntuación: {e}")

def obtener_puntajes_altos():
    puntajes = []
    try:
        with open('puntuaciones.txt', 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()  # Quita espacios en blanco al principio y al final
                if not linea:
                    continue  # Ignora líneas vacías
                try:
                    nombre, puntos = linea.split(' - ')
                    puntos = int(puntos)
                    puntajes.append((nombre, puntos))
                except ValueError:
                    print(f"Formato incorrecto en la línea: '{linea}'")
        puntajes.sort(key=lambda x: x[1], reverse=True)  # Ordenar de mayor a menor
        return puntajes[:3]  # Devolver solo los tres mejores puntajes
    except FileNotFoundError:
        print("El archivo de puntuaciones no existe, se creará uno nuevo.")
        with open('puntuaciones.txt', 'w') as archivo:  # Crear un archivo nuevo vacío
            pass
        return []
    except IOError as e:
        print(f"Error al leer el archivo de puntuaciones: {e}")
        return []

def guardar_puntuacion(nombre, puntos):
    with open('puntuaciones.txt', 'a') as archivo:
        archivo.write(f"{nombre} - {puntos}\n")

def juego():
    global ultima_bala
    jugando = True
    vida = 5
    puntos = 0
    reloj = pygame.time.Clock()
    cubo = Cubo(ANCHO // 2, ALTO - 75)

    enemigos = []
    balas = []
    items = []

    tiempo_pasado = 0
    tiempo_entre_enemigos = 500
    tiempo_pasado_vidas = 0
    tiempo_entre_vidas = 1500

    while jugando and vida > 0:
        tiempo_pasado += reloj.tick(FPS)

        if tiempo_pasado > tiempo_entre_enemigos:
            enemigos.append(Enemigo(random.randint(10, ANCHO - 50), -100))
            tiempo_pasado = 0
            tiempo_pasado_vidas += 1
            if tiempo_pasado_vidas >= 15:
                items.append(Item(random.randint(10, ANCHO - 50), -100))
                tiempo_pasado_vidas = 0

        eventos = pygame.event.get()
        teclas = pygame.key.get_pressed()

        gestionar_teclas(teclas, cubo, balas, SONIDO_DISPARO)

        for evento in eventos:
            if evento.type == pygame.QUIT:
                jugando = False

        VENTANA.blit(fondo, (0, 0))

        cubo.dibujar(VENTANA)

        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)
            enemigo.movimiento()

            if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
                vida -= 1
                MUERTE_NAVE.play()
                enemigos.remove(enemigo)

            if enemigo.y > ALTO:
                enemigos.remove(enemigo)

            for bala in balas:
                if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                    enemigo.vida -= 1
                    balas.remove(bala)

                if bala.y < 0:
                    balas.remove(bala)

            if enemigo.vida <= 0:
                MUERTE_OVNI.play()
                enemigos.remove(enemigo)
                puntos += 1

        for bala in balas:
            bala.dibujar(VENTANA)
            bala.movimiento()

        for item in items:
            item.dibujar(VENTANA)
            item.movimiento()

            if pygame.Rect.colliderect(item.rect, cubo.rect):
                items.remove(item)

                if vida != 5:
                    vida += 1
                    VIDA_EXTRA.play()

            if item.y > ALTO:
                items.remove(item)

        texto_vida = FUENTE.render(f"Vidas: {vida}", True, "white")
        texto_puntos = FUENTE.render(f"Puntos: {puntos}", True, "white")

        VENTANA.blit(texto_vida, (20, 20))
        VENTANA.blit(texto_puntos, (20, 50))

        pygame.display.update()

    if vida <= 0:
        if pantalla_game_over(puntos):
            juego()

def gestionar_teclas(teclas, cubo, balas, sonido_disparo):
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        if cubo.x >= 3:
            cubo.x -= cubo.velocidad

    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        if cubo.x + cubo.ancho + 3 <= ANCHO:
            cubo.x += cubo.velocidad

    if teclas[pygame.K_SPACE]:
        crear_bala(cubo, balas, sonido_disparo)

def crear_bala(cubo, balas, sonido_disparo):
    global ultima_bala

    if pygame.time.get_ticks() - ultima_bala > 200:
        balas.append(Bala(cubo.rect.centerx - 14, cubo.rect.centery))
        ultima_bala = pygame.time.get_ticks()
        sonido_disparo.play()

# Muestra la pantalla de inicio antes de empezar el juego
pantalla_inicio()
juego()
pygame.quit()
