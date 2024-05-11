import os
import cv2


def _rgb_to_ansi(r: int, g: int, b: int) -> str:
    """ Формула для вычисления ближайшего цвета ANSI 256 """
    index = 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)
    return f'\x1b[38;5;{index}m'


def apply_color(text: str, color: list[int, int, int], colored: bool) -> str:
    if not colored:
        return text
    ansi_color = _rgb_to_ansi(*color)
    return f'{ansi_color}{text}\x1b[0m'


def get_gradient():
    gradient = [*' .:!/r(l1Z4H9W8$@']
    return gradient, len(gradient)


def process_image(image, circle_matrix):
    gradient, length = get_gradient()
    # Проходим по каждому пикселю изображения
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            # Получаем цвет пикселя
            color = image[y, x]
            # Преобразуем цвет из BGR в RGB
            color_rgb = (color[2], color[1], color[0])
            # Получаем яркость пикселя
            brightness = sum(color) / (255 * 3)  # нормализуем яркость к диапазону [0, 1]
            # Выводим цвет и яркость пикселя
            index = round(brightness * length - 1)
            index = max(0, min(index, length - 1))
            circle_matrix[y][x] = apply_color(gradient[index], color_rgb, True)
    return circle_matrix


def print_frame(matrix) -> list[list[str]]:
    circle = '\n'.join(''.join(row) for row in matrix)
    print(circle, end='')


def get_console_size():
    terminal = os.get_terminal_size()
    return terminal.columns, terminal.lines


def get_camera_resolution():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return width, height


def resize_console(console_width, console_height, cam_width, cam_height):
    if console_width < cam_width:
        os.system(f"mode con cols={cam_width}")

        # Если высота консоли меньше высоты кадра, устанавливаем новую высоту консоли
    if console_height < cam_height:
        os.system(f"mode con lines={cam_height}")


def get_camera():
    t_width, t_height = get_console_size()
    cap = cv2.VideoCapture(0)

    width, height = get_camera_resolution()
    aspect_symbol = 11 / 23
    width = t_width * 4
    height = t_height * 4
    resize_console(t_width, t_height, width, height)

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
        console_frame = process_image(resized_frame, circle_matrix)
        print_frame(console_frame)

        cv2.imshow('Camera', resized_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()