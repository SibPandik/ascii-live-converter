import os
import sys
import time

import cv2


def _rgb_to_ansi(r: int, g: int, b: int, colorize_symbol=True, colorize_bg=False) -> str:
    """ Формула для вычисления ближайшего цвета ANSI 256 """
    index = 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
    if colorize_symbol and colorize_bg:
        return f'\x1b[38;5;{index};48;5;{index}m'
    if colorize_symbol:
        return f'\x1b[38;5;{index}m'
    return f'\x1b[38;5;0;48;5;{index}m'


def _apply_color(symbol: str, color: list[int, int, int], colored: bool) -> str:
    """ Метод который возвращает покрашенный символ"""
    if not colored:
        return symbol
    ansi_color = _rgb_to_ansi(*color, colorize_symbol=True, colorize_bg=False)
    # для обозначения окончания проименения стилей используется \x1b[0m, но он тут не нужен так как мы красим каждый символ
    return f'{ansi_color}{symbol}'


def _get_gradient():
    """Получение градиента и его длинны"""
    gradient = [*' .:!/r(l1Z4H9W8$@']
    return gradient, len(gradient)


def _process_frame(frame, circle_matrix):
    """Метод который берет frame и делает список списков с каждой строкой замененой на один из символ градиента"""
    gradient, length = _get_gradient()
    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            color = frame[y, x]
            color_rgb = (color[2], color[1], color[0])
            brightness = sum(color) / (255 * 3)  # нормализуем яркость к диапазону [0, 1]
            index = round(brightness * length - 1)
            index = max(0, min(index, length - 1))
            circle_matrix[y][x] = _apply_color(gradient[index], color_rgb, True)
    return circle_matrix


def _print_frame(matrix) -> list[list[str]]:
    """Вывод кадра"""
    circle = '\n'.join(''.join(row) for row in matrix)
    sys.stdout.write(circle)  # как говорят это должно работать быстрее print'a


def _get_console_size():
    """Получаем размеры терминала"""
    terminal = os.get_terminal_size()
    return terminal.columns, terminal.lines


def _get_camera_size():
    """Получение размеры камеры"""
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return width, height


def _resize_console(console_width, console_height, cam_width, cam_height):
    """Подстраиваем размеры консоли, под размеры камеры"""
    if console_width < cam_width:
        os.system(f"mode con cols={cam_width}")
    if console_height < cam_height:
        os.system(f"mode con lines={cam_height}")


def get_camera():
    debug = False
    t_width, t_height = _get_console_size()
    cap = cv2.VideoCapture(0)
    width, height = _get_camera_size()  # fixme: не используется, но что то не дает мне это удалить

    resolution = 2  # изменяя данную переменную мы увеличиваем размер выводимого окна
    width = int(t_width * resolution)
    height = int(t_height * resolution)
    _resize_console(t_width, t_height, width, height)

    circle_matrix = [[' ' for _ in range(width)] for _ in range(height)]

    print(f"Разрешение камеры: {width}x{height}")

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру.")
        exit()

    # Чтение и отображение кадров с камеры
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Ошибка: Не удалось захватить кадр.")
            break

        resized_frame = cv2.resize(frame, (width, height))
        console_frame = _process_frame(resized_frame, circle_matrix)
        start_time = time.time()
        _print_frame(console_frame)
        end_time = time.time()

        duration = end_time - start_time
        if debug:
            print("Время вывода:", duration, "секунд")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()