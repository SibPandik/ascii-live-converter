import os
import cv2


def _rgb_to_ansi(r: int, g: int, b: int) -> str:
    """ Формула для вычисления ближайшего цвета ANSI 256 """
    index = 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
    return f'\x1b[38;5;{index}m'


def _apply_color(symbol: str, color: list[int, int, int], colored: bool) -> str:
    """ Метод который возвращает покрашенный символ"""
    if not colored:
        return symbol
    ansi_color = _rgb_to_ansi(*color)
    return f'{ansi_color}{symbol}\x1b[0m'


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
            circle_matrix[y][x] = _apply_color(gradient[index], color_rgb, False)
    return circle_matrix


def _print_frame(matrix) -> list[list[str]]:
    """Вывод кадра"""
    circle = '\n'.join(''.join(row) for row in matrix)
    print(circle, end='')


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
    t_width, t_height = _get_console_size()
    cap = cv2.VideoCapture(0)
    width, height = _get_camera_size()
    width = t_width
    height = t_height
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
        _print_frame(console_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()