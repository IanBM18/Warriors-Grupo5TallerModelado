import pygame
pygame.init()
pygame.display.set_mode((1, 1))

import time
from juego.enemy_manager import EnemyManager

ROWS = 5
COLS = 9
CELL = 64
MARGIN = 2
SCREEN_WIDTH = 1200


def create_em():
    return EnemyManager(ROWS, COLS, CELL, MARGIN, SCREEN_WIDTH)


def test_spawn_enemy_adds_to_list():
    em = create_em()
    em.spawn_enemy()
    assert len(em.enemies) == 1


def test_update_triggers_enemy_spawn():
    em = create_em()

    em.last_spawn_time = time.time() - 10
    em.next_spawn_delay = 1

    em.update(dt=0.1, rook_manager=type("x", (), {"rooks": []})())
    assert len(em.enemies) == 1


def test_enemy_moves_when_no_rook():
    em = create_em()

    em.spawn_enemy()
    enemy = em.enemies[0]

    y_before = enemy["y"]

    em.update(dt=0.1, rook_manager=type("x", (), {"rooks": []})())

    y_after = enemy["y"]

    # Si no hay torre debería moverse hacia arriba (menor y)
    assert y_after < y_before