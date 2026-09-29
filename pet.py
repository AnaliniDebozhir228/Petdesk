import random
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QApplication

from settings_windows import SettingsWindow
from animation import AnimationController


class Pet(QWidget):

    def __init__(self, world, settings):
        super().__init__()

        self.world = world
        self.settings = settings

        # ==========================================
        # ОКНО ПЕРСОНАЖА
        # ==========================================

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        # ==========================================
        # ПЕРСОНАЖ
        # ==========================================

        self.label = QLabel(self)

        self.animation = AnimationController(parent=self)
        self.animation.frame_changed.connect(self.set_animation_frame)

        self.pixmap = QPixmap("Assets/you-are-an-idiot.png")

        self.update_size()

        # ==========================================
        # СОСТОЯНИЕ
        # ==========================================

        self.state = "idle"

        self.direction = random.choice([-1, 1])

        # Вертикальная скорость
        self.velocity_y = 0

        # Скорость полёта
        self.velocity_x = 0
        self.velocity_fly_y = 0

        self.grounded = False

        # ==========================================
        # ПЕРЕТАСКИВАНИЕ
        # ==========================================

        self.dragging = False
        self.drag_offset = QPoint()

        # ==========================================
        # ОСНОВНОЙ ТАЙМЕР
        # ==========================================

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pet)
        self.timer.start(16)

        # ==========================================
        # ОБНОВЛЕНИЕ WINDOWS
        # ==========================================

        self.world_timer = QTimer(self)
        self.world_timer.timeout.connect(
            self.world.update
        )
        self.world_timer.start(1000)

        # ==========================================
        # СЛУЧАЙНОЕ ПОВЕДЕНИЕ
        # ==========================================

        self.behavior_timer = QTimer(self)
        self.behavior_timer.timeout.connect(
            self.choose_behavior
        )
        self.behavior_timer.start(3000)

    # ==================================================
    # РАЗМЕР
    # ==================================================

    def update_size(self):

        size = self.settings.size

        self.pixmap_scaled = self.pixmap.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label.setPixmap(
            self.pixmap_scaled
        )

        self.label.resize(
            self.pixmap_scaled.size()
        )

        self.resize(
            self.pixmap_scaled.size()
        )

    # ==================================================
    # НАСТРОЙКИ
    # ==================================================

    def set_animation_frame(self, pixmap):
        if self.direction < 0:
            pixmap = pixmap.transformed(
                QTransform().scale(-1, 1)
            )

        size = self.settings.size

        scaled = pixmap.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label.setPixmap(scaled)
        self.label.resize(scaled.size())
        self.resize(scaled.size())

    def open_settings(self):

        print("Открываем настройки...")

        window = SettingsWindow(
            self.settings,
            self
        )

        window.settings_changed.connect(
            self.apply_settings
        )

        window.exec()

    def apply_settings(self):

        print("Настройки применены")

        # Обновляем размер
        self.update_size()

        # Сбрасываем скорость полёта
        self.velocity_x = 0
        self.velocity_fly_y = 0

        # Выбираем новое состояние
        if self.settings.behavior == "fly":

            self.state = "fly"

        elif self.settings.behavior == "walk":

            self.state = "walk"

        else:

            self.state = "walk"

    # ==================================================
    # ВЫБОР ПОВЕДЕНИЯ
    # ==================================================

    def choose_behavior(self):

        if self.dragging:
            return

        behavior = self.settings.behavior

        # Принудительная ходьба
        if behavior == "walk":

            if self.grounded:
                self.state = "walk"

            return

        # Принудительный полёт
        if behavior == "fly":

            self.state = "fly"

            return

        # Автоматический режим
        choices = [
            "idle",
            "walk"
        ]

        if self.settings.gravity_enabled:
            choices.append("fall")

        self.state = random.choice(
            choices
        )

    # ==================================================
    # ГЛАВНОЕ ОБНОВЛЕНИЕ
    # ==================================================

    def update_pet(self):
        if self.dragging:
            return

        if self.settings.behavior == "fly":
            self.animation.play("fly", 100)
            self.update_flying()
            return

        if self.state == "fly":
            self.animation.play("fly", 100)
            self.update_flying()
            return

        if self.state == "idle":
            self.animation.play("idle", 180)
            self.update_idle()
            return

        if self.state == "walk":
            animation_speed = max(50, int(220 - self.settings.speed * 20))
            self.animation.play("walk", animation_speed)
            self.update_walking()
            return

        if self.state == "fall":
            self.animation.play("fall", 180)
            self.update_falling()
            return

        def set_animation_frame(self, pixmap):
            if self.direction < 0:
                pixmap = pixmap.transformed(
                    pixmap.transformationMode()
                )

    # ==================================================
    # IDLE
    # ==================================================

    def update_idle(self):

        surface = self.get_surface_below()

        if surface:

            self.grounded = True

            self.move(
                self.x(),
                surface.y - self.height()
            )

    # ==================================================
    # ХОДЬБА
    # ==================================================

    def update_walking(self):

        surface = self.get_surface_below()

        if surface is None:

            self.grounded = False
            self.state = "fall"

            return

        self.grounded = True

        center_x = (
            self.x()
            + self.width() // 2
        )

        # Персонаж ушёл с поверхности
        if not surface.contains_x(center_x):

            self.grounded = False
            self.state = "fall"

            return

        new_x = (
            self.x()
            + self.settings.speed
            * self.direction
        )

        # Левая граница
        if new_x <= surface.left:

            new_x = surface.left
            self.direction = 1

        # Правая граница
        elif (
            new_x + self.width()
            >= surface.right
        ):

            new_x = (
                surface.right
                - self.width()
            )

            self.direction = -1

        self.move(
            int(new_x),
            int(surface.y - self.height())
        )

    # ==================================================
    # ПАДЕНИЕ
    # ==================================================

    def update_falling(self):

        self.grounded = False

        # Если гравитация отключена
        if not self.settings.gravity_enabled:

            self.state = "walk"
            return

        self.velocity_y += (
            self.settings.gravity
        )

        if (
            self.velocity_y
            > self.settings.max_fall_speed
        ):

            self.velocity_y = (
                self.settings.max_fall_speed
            )

        new_y = (
            self.y()
            + self.velocity_y
        )

        surface = self.get_surface_below()

        if surface:

            bottom = (
                new_y
                + self.height()
            )

            if bottom >= surface.y:

                new_y = (
                    surface.y
                    - self.height()
                )

                self.velocity_y = 0

                self.grounded = True

                self.state = "walk"

        self.move(
            self.x(),
            int(new_y)
        )

    # ==================================================
    # ПОЛЁТ
    # ==================================================

    def update_flying(self):

        screen = (
            QApplication
            .primaryScreen()
            .availableGeometry()
        )

        speed = self.settings.fly_speed

        if self.velocity_x == 0:

            self.velocity_x = (
                random.choice([-1, 1])
                * speed
            )

        if self.velocity_fly_y == 0:

            self.velocity_fly_y = (
                random.choice([-1, 1])
                * speed
            )

        x = (
            self.x()
            + self.velocity_x
        )

        y = (
            self.y()
            + self.velocity_fly_y
        )

        # Левая граница
        if x <= screen.left():

            x = screen.left()
            self.velocity_x = speed

        # Правая граница
        elif (
            x + self.width()
            >= screen.right()
        ):

            x = (
                screen.right()
                - self.width()
            )

            self.velocity_x = -speed

        # Верхняя граница
        if y <= screen.top():

            y = screen.top()
            self.velocity_fly_y = speed

        # Нижняя граница
        elif (
            y + self.height()
            >= screen.bottom()
        ):

            y = (
                screen.bottom()
                - self.height()
            )

            self.velocity_fly_y = -speed

        self.move(
            int(x),
            int(y)
        )

    # ==================================================
    # ПОИСК ПОВЕРХНОСТИ
    # ==================================================

    def get_surface_below(self):

        if not self.settings.walk_on_windows:

            surfaces = (
                self.world.surfaces[:1]
            )

        else:

            surfaces = (
                self.world.surfaces
            )

        pet_left = self.x()

        pet_right = (
            self.x()
            + self.width()
        )

        pet_bottom = (
            self.y()
            + self.height()
        )

        best = None

        best_distance = float("inf")

        for surface in surfaces:

            overlap = (
                pet_right > surface.left
                and pet_left < surface.right
            )

            if not overlap:
                continue

            distance = (
                surface.y
                - pet_bottom
            )

            if distance < -5:
                continue

            if distance < best_distance:

                best_distance = distance
                best = surface

        return best

    # ==================================================
    # МЫШЬ
    # ==================================================

    def mousePressEvent(self, event):

        # ------------------------------------------
        # ЛЕВАЯ КНОПКА
        # ------------------------------------------

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            self.dragging = True
            self.state = "dragged"

            self.velocity_y = 0
            self.velocity_x = 0
            self.velocity_fly_y = 0

            self.drag_offset = (
                event.globalPosition().toPoint()
                - self.pos()
            )

            event.accept()

            return

        # ------------------------------------------
        # ПРАВАЯ КНОПКА
        # ------------------------------------------

        if (
            event.button()
            == Qt.MouseButton.RightButton
        ):

            self.open_settings()

            event.accept()

            return

    def mouseMoveEvent(self, event):

        if self.dragging:

            position = (
                event.globalPosition().toPoint()
                - self.drag_offset
            )

            self.move(position)

            event.accept()

    def mouseReleaseEvent(self, event):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            self.dragging = False

            self.velocity_y = 0

            self.state = "fall"

            event.accept()