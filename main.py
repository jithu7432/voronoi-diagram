import imageio
import numpy as np

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=3).pprint


WIDTH = 1080  
HIEGHT = 1920 
FILENAME = 'data.ppm'
SEED_COUNT = 20
RADIUS = 5

COLOR_GREY = 100
COLOR_BLACK = 0
COLOR_WHITE = 255


def save_image_as_ppm(imarray) -> None:
    imageio.imwrite(FILENAME, imarray)


def generate_seeds() -> list[tuple[int, int]]:
    return [(np.random.randint(WIDTH), np.random.randint(HIEGHT)) for _ in range(SEED_COUNT)]


def fill_background(image: np.ndarray, color: int) -> np.ndarray:
    image[:] = color
    return image


def fill_circle(cx, cy, radius, image, color) -> None:
    for i in range(image.shape[0]):
        if (0 <= i <= WIDTH):
            for j in range(image.shape[1]):
                if (0 <= j <= HIEGHT):
                    dx = cx - i
                    dy = cy - j
                    if (dx**2 + dy**2) < radius**2:
                        image[i, j] = color


def compute_minimum(x0, y0, seeds: list[tuple[int, int]]) -> tuple[int, int]:
    min_seed = seeds[0]
    g = float('inf')
    for i in range(1, len(seeds)):
        x1, y1 = seeds[i]
        d = (x0 - x1)**2 + (y0 - y1)**2
        if d < g:
            g = d
            min_seed = seeds[i]
    return min_seed


def compute_vonoroi(image: np.ndarray, seeds: list[tuple[int, int]]) -> dict:
    vonoroi_map = {}
    for i in range(image.shape[0]):
        if (0 <= i <= WIDTH):
            for j in range(image.shape[1]):
                if (0 <= j <= HIEGHT):
                    vonoroi_map[(i, j)] = compute_minimum(i, j, seeds)
    return vonoroi_map


def fill_seeds(seeds, image, radius, color) -> np.ndarray:
    for s in seeds:
        fill_circle(s[0], s[1], radius, image, color)
    return image


def generate_color_palette(seeds, vonoroi_map: dict) -> dict:
    colors = [np.random.randint(0, 255) for _ in range(SEED_COUNT)]
    _palette = {seeds[i]: colors[i] for i in range(SEED_COUNT)}
    palette = {}
    for k, v in vonoroi_map.items():
        palette[k] = _palette[v]
    return palette


def fill_vonoroi_map(image, vonoroi_map: dict, color_palette: dict) -> None:
    for i in range(image.shape[0]-1):
        for j in range(image.shape[1]-1):
                image[i, j] = color_palette[vonoroi_map[(i, j)]]


def main() -> None:
    seeds = generate_seeds()
    image = np.zeros((WIDTH, HIEGHT), dtype=np.uint8)
    image = fill_background(image, COLOR_BLACK)
    vonoroi_map = compute_vonoroi(image, seeds)
    palette = generate_color_palette(seeds, vonoroi_map)
    fill_vonoroi_map(image, vonoroi_map, palette)
    fill_seeds(seeds, image, RADIUS, COLOR_BLACK)
    save_image_as_ppm(image)


if __name__ == '__main__':
    main()
