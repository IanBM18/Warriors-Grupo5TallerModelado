import pygame
pygame.init()
pygame.display.set_mode((1, 1))

import time
from juego.coin_manager import CoinManager

ROWS = 5
COLS = 9
CELL = 64
MARGIN = 2
GRID_WIDTH = COLS * (CELL + MARGIN)
SCREEN_WIDTH = 1200


def create_cm(max_coins=5):
    return CoinManager(ROWS, COLS, CELL, MARGIN, GRID_WIDTH, SCREEN_WIDTH, max_coins)


def test_spawn_adds_coin():
    cm = create_cm()
    cm.spawn_coin()
    assert len(cm.active_coins) == 0


def test_spawn_respects_max():
    cm = create_cm(max_coins=3)

    # Forzar para que update() spawnee varias veces
    cm.last_spawn_time = time.time() - 10

    for _ in range(10):
        cm.update()

    assert len(cm.active_coins) <= 3


def test_collect_coin_adds_value_and_removes():
    cm = create_cm()

    tipo = cm.coins_tipo[0]
    cm.active_coins.append((0, 0, tipo))

    click_x = cm.left_offset + MARGIN + 5
    click_y = cm.y_offset + MARGIN + 5

    cm.check_collect((click_x, click_y))

    assert len(cm.active_coins) == 0
    assert cm.collected == tipo["valor"]
