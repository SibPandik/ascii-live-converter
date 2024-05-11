import os

from camera_tracker import get_camera
from circle import new_console


if __name__ == '__main__':
    try:
        os.system('')  # без этого не работают цвета в консоли
        # new_console()
        get_camera()
    except Exception as e:
        print(e)
        input()
