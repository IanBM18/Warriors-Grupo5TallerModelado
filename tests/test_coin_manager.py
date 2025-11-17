import types
import pygame
from juego.coin_manager import CoinManager

# Evitar que pygame trate de cargar imágenes reales
pygame.display.init()
pygame.display.set_mode((1, 1))   # Pantalla mínima para evitar errores

def crear_coin_manager_sin_imagenes():
    """Crea un CoinManager sin cargar imágenes reales."""
    cm = CoinManager(
        rows=3,
        cols=3,
        cell_size=50,
        margin=5,
        grid_width=200,
        screen_width=300,
        max_coins=5
    )

    # Reemplaza imágenes reales por una superficie vacía
    for coin in cm.coins_tipo:
        coin["imagen"] = pygame.Surface((40, 40))

    return cm

def test1Collected_IniciaEnCero():
    cm = crear_coin_manager_sin_imagenes()
    assert cm.collected == 0

def test2Collected_SumaUnaMoneda():
    cm = crear_coin_manager_sin_imagenes()
    
    # Simular moneda (x, y, tipo)
    cm.active_coins.append((0, 0, {"valor": 25, "imagen": pygame.Surface((40, 40))}))
    
    # Simular click en coordenadas exactas
    cm.check_collect((cm.left_offset + 5, cm.y_offset + 5))
    
    assert cm.collected == 25

def test3Collected_SumaVarias():
    cm = crear_coin_manager_sin_imagenes()
    
    cm.active_coins.append((0, 0, {"valor": 25, "imagen": pygame.Surface((40, 40))}))
    cm.active_coins.append((1, 0, {"valor": 50, "imagen": pygame.Surface((40, 40))}))

    # Click moneda 25
    cm.check_collect((cm.left_offset + 5, cm.y_offset + 5))
    
    # Click moneda 50 (simulada un poco a la derecha)
    cm.check_collect((cm.left_offset + 60, cm.y_offset + 5))

    assert cm.collected == 75
        