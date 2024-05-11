import os
import time


def _rgb_to_ansi(r: int, g: int, b: int) -> str:
    """ Формула для вычисления ближайшего цвета ANSI 256 """
    index = 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
    return f'\x1b[38;5;{index}m'


def apply_color(text: str, color: list[int, int, int], colored: bool) -> str:
    if not colored:
        return text
    ansi_color = _rgb_to_ansi(*color)
    return f'{ansi_color}{text}\x1b[0m'


def print_layer(matrix) -> list[list[str]]:
    circle = '\n'.join(''.join(row) for row in matrix)
    print(circle, end='')


def new_console():
    terminal = os.get_terminal_size()
    width, height = terminal.columns, terminal.lines
    # width, height = 120, 30
    aspect_symbol = 11 / 23
    colored = True
    # [*'.x@'] можно использовать разные варианты градиентов
    gradient = [*' .:!/r(l1Z4H9W8$@']
    color_gradient = [
        (0, 0, 0),
        (255, 116, 132), (255, 113, 144), (255, 111, 155), (255, 108, 167),
        (255, 106, 178), (255, 103, 190), (255, 100, 202), (255, 98, 213),
        (255, 95, 225), (255, 92, 236), (255, 90, 248), (253, 90, 248),
        (250, 90, 248), (247, 90, 248), (244, 90, 248), (241, 90, 248),
    ]

    # Переворачиваем список
    color_gradient.reverse()
    index = color_gradient.index((0, 0, 0))
    color_gradient.insert(0, color_gradient.pop(index))

    # Определение центральных координат консоли
    center_y = height // 2

    # Радиус круга (берем половину минимальной стороны)
    radius = min(width, height)
    radius_horizontal = radius * aspect_symbol

    # Начальное положение центра круга
    center_x = width // 2

    # Создание пустого массива для хранения изображения круга
    circle_matrix = [[' ' for _ in range(width)] for _ in range(height)]

    while True:
        for y in range(height):
            for x in range(width):
                circle_matrix[y][x] = gradient[0]
                rel_x = x - center_x
                rel_y = y - center_y
                if rel_x ** 2 / radius ** 2 + rel_y ** 2 / radius_horizontal ** 2 <= 1:
                    # Расчет интенсивности цвета в зависимости от расстояния от центра
                    intensity = 1 - (rel_x ** 2 / radius ** 2 + rel_y ** 2 / radius_horizontal ** 2) ** 0.5
                    gradient_index = int(intensity * (len(gradient) - 1))
                    color_rgb = color_gradient[gradient_index]
                    circle_matrix[y][x] = apply_color(gradient[gradient_index], color_rgb, colored)
                    if not gradient_index:
                        circle_matrix[y][x] = gradient[gradient_index]

        print_layer(circle_matrix)

        center_x += 1
        if center_x >= width:
            center_x = 0

        time.sleep(0.1)
        print()


if __name__ == '__main__':
    try:
        os.system('')  # без этого не работают цвета в консоли
        new_console()
    except Exception as e:
        print(e)
        input()
