import imageio
import numpy as np

from pathlib import Path
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=2).pprint

RADIUS = 5
WIDTH = 600
HIEGHT = 800
SEED_COUNT = 100
FILENAME = str((Path('__file__').parent / 'data.ppm').resolve().absolute())

COLOR_BLACK = 0
COLOR_GREY = 128
COLOR_WHITE = 255


def save_image_as_ppm(imarray) -> None:
    imageio.imwrite(FILENAME, imarray)


def generate_seeds() -> list[tuple[int, int]]:
    return [(np.random.randint(HIEGHT), np.random.randint(WIDTH)) for _ in range(SEED_COUNT)]


def fill_background(image: np.ndarray, color: int) -> np.ndarray:
    image[:] = color
    return image


def fill_circle(cx, cy, radius, image, color) -> None:
    x0 = cx - radius
    x1 = cx + radius
    y0 = cy - radius
    y1 = cy + radius
    for i in range(x0, x1):
        if (0 <= i < HIEGHT):
            for j in range(y0, y1):
                if (0 <= j < WIDTH):
                    dx = cx - i
                    dy = cy - j
                    if (dx**2 + dy**2) < radius**2:
                        image[j, i] = color


def compute_minimum(x0, y0, seeds: list[tuple[int, int]]) -> tuple[int, int]:
    min_seed = seeds[0]
    g = float('inf')
    for i in range(1, SEED_COUNT):
        x1, y1 = seeds[i]
        d = (x0 - x1)**2 + (y0 - y1)**2
        if d < g:
            g = d
            min_seed = seeds[i]
    return min_seed


def compute_vonoroi(seeds: list[tuple[int, int]]) -> dict:
    vonoroi_map = {}
    for i in range(WIDTH):
            for j in range(HIEGHT):
                    vonoroi_map[(j, i)] = compute_minimum(j, i, seeds)
    return vonoroi_map


def fill_seeds(seeds, image, radius, color) -> np.ndarray:
    for s in seeds:
        fill_circle(s[0], s[1], radius, image, color)
    return image


def generate_color_palette(seeds, vonoroi_map: dict) -> dict:
    _palette = {seeds[i]: np.random.randint(0, 255) for i in range(SEED_COUNT)}
    palette = {}
    for k, v in vonoroi_map.items():
        palette[k] = _palette[v]
    return palette


def fill_vonoroi_map(image, vonoroi_map: dict, color_palette: dict) -> None:
    for i in range(WIDTH):
        for j in range(HIEGHT):
            image[i, j] = color_palette[vonoroi_map[(j, i)]]


def main() -> None:
    seeds = generate_seeds()
    image = np.zeros((WIDTH, HIEGHT), dtype=np.uint8)
    image = fill_background(image, COLOR_BLACK)
    vonoroi_map = compute_vonoroi(seeds)
    palette = generate_color_palette(seeds, vonoroi_map)
    fill_vonoroi_map(image, vonoroi_map, palette)
    #  fill_seeds(seeds, image, RADIUS, COLOR_BLACK)
    save_image_as_ppm(image)


if __name__ == '__main__':
    main()
