import pygame
import math
import sys

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hexágono Giratorio con Pelota Rebotando")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Parámetros del hexágono
centro_x = width // 2
centro_y = height // 2
radio_hex = 150
angulo_rotacion = 0
velocidad_rotacion = 1  # grados por fotograma

# Parámetros de la pelota
radio_pelota = 10
pelota_x = centro_x
pelota_y = centro_y
pelota_vx = 3
pelota_vy = 2
gravedad = 0.1
amortiguacion = 0.8
fuerza_rebote = 2  # Fuerza adicional al rebotar

def obtener_puntos_hexagono(centro_x, centro_y, radio, angulo_rotacion):
    puntos = []
    for i in range(6):
        angulo_grados = angulo_rotacion + i * 60
        angulo_radianes = math.radians(angulo_grados)
        x = centro_x + radio * math.cos(angulo_radianes)
        y = centro_y + radio * math.sin(angulo_radianes)
        puntos.append((x, y))
    return puntos

def distancia_punto_a_linea(punto, linea_inicio, linea_fin):
    x0, y0 = punto
    x1, y1 = linea_inicio
    x2, y2 = linea_fin
    numerador = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominador = math.hypot(y2 - y1, x2 - x1)
    return numerador / denominador if denominador != 0 else 0

# Bucle principal
ejecutando = True
reloj = pygame.time.Clock()

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Actualizar ángulo de rotación
    angulo_rotacion += velocidad_rotacion
    angulo_rotacion %= 360

    # Obtener puntos del hexágono
    puntos_hex = obtener_puntos_hexagono(centro_x, centro_y, radio_hex, angulo_rotacion)

    # Aplicar gravedad a la pelota
    pelota_vy += gravedad

    # Actualizar posición de la pelota
    pelota_x += pelota_vx
    pelota_y += pelota_vy

    # Verificar colisiones con los bordes del hexágono
    colision = False
    for i in range(6):
        # Puntos del borde actual
        x1, y1 = puntos_hex[i]
        x2, y2 = puntos_hex[(i + 1) % 6]

        # Calcular distancia de la pelota al borde
        distancia = distancia_punto_a_linea((pelota_x, pelota_y), (x1, y1), (x2, y2))

        # Verificar si la pelota está colisionando con el borde
        if distancia < radio_pelota:
            # Vector del borde
            dx = x2 - x1
            dy = y2 - y1

            # Calcular normal hacia adentro
            normal_x = -dy
            normal_y = dx

            # Normalizar la normal
            longitud = math.hypot(normal_x, normal_y)
            if longitud == 0:
                continue
            normal_x /= longitud
            normal_y /= longitud

            # Reflejar velocidad
            producto_punto = pelota_vx * normal_x + pelota_vy * normal_y
            pelota_vx -= 2 * producto_punto * normal_x
            pelota_vy -= 2 * producto_punto * normal_y

            # Aplicar fuerza adicional hacia el interior
            pelota_vx += normal_x * fuerza_rebote
            pelota_vy += normal_y * fuerza_rebote

            # Aplicar amortiguación
            pelota_vx *= amortiguacion
            pelota_vy *= amortiguacion

            # Corregir posición para evitar que la pelota se salga
            superposicion = radio_pelota - distancia
            pelota_x += normal_x * superposicion
            pelota_y += normal_y * superposicion

            colision = True
            break  # Manejar solo una colisión por fotograma

    # Limpiar pantalla
    screen.fill(NEGRO)

    # Dibujar hexágono
    pygame.draw.polygon(screen, BLANCO, puntos_hex, 2)

    # Dibujar pelota
    pygame.draw.circle(screen, ROJO, (int(pelota_x), int(pelota_y)), radio_pelota)

    # Actualizar pantalla
    pygame.display.flip()

    # Controlar FPS
    reloj.tick(60)

pygame.quit()
sys.exit()