import win32gui

from PySide6.QtWidgets import QApplication


class Surface:

    def __init__(self, left, right, y):
        self.left = left
        self.right = right
        self.y = y

    def contains_x(self, x):
        return self.left <= x <= self.right


class World:

    def __init__(self):
        self.surfaces = []

    def update(self):

        self.surfaces.clear()

        screen = QApplication.primaryScreen().availableGeometry()

        # Рабочий стол
        self.surfaces.append(
            Surface(
                screen.left(),
                screen.right(),
                screen.bottom()
            )
        )

        def callback(hwnd, _):

            if not win32gui.IsWindowVisible(hwnd):
                return

            try:
                left, top, right, bottom = (
                    win32gui.GetWindowRect(hwnd)
                )
            except Exception:
                return

            width = right - left
            height = bottom - top

            if width < 150 or height < 80:
                return

            title = win32gui.GetWindowText(hwnd)

            if not title:
                return

            self.surfaces.append(
                Surface(
                    left,
                    right,
                    top
                )
            )

        win32gui.EnumWindows(callback, None)