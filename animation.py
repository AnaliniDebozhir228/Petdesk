from pathlib import Path

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QPixmap


class AnimationController(QObject):
    frame_changed = Signal(QPixmap)

    def __init__(self, base_path="assets/pet", parent=None):
        super().__init__(parent)

        self.base_path = Path(base_path)

        self.animations = {}
        self.current_animation = None
        self.current_frame = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)

        self.load_animations()

    def load_animations(self):
        animation_names = [
            "idle",
            "walk",
            "fall",
            "fly",
        ]

        for name in animation_names:
            folder = self.base_path / name

            if not folder.exists():
                continue

            files = sorted(
                [
                    file
                    for file in folder.iterdir()
                    if file.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]
                ]
            )

            frames = []

            for file in files:
                pixmap = QPixmap(str(file))

                if not pixmap.isNull():
                    frames.append(pixmap)

            if frames:
                self.animations[name] = frames

        print("Загружены анимации:", list(self.animations.keys()))

    def play(self, name, interval=120):
        if name not in self.animations:
            return

        if self.current_animation != name:
            self.current_animation = name
            self.current_frame = 0
            self.timer.start(interval)
            self.show_current_frame()
        elif not self.timer.isActive():
            self.timer.start(interval)

    def next_frame(self):
        frames = self.animations.get(self.current_animation)

        if not frames:
            return

        self.current_frame += 1

        if self.current_frame >= len(frames):
            self.current_frame = 0

        self.show_current_frame()

    def show_current_frame(self):
        frames = self.animations.get(self.current_animation)

        if not frames:
            return

        self.frame_changed.emit(frames[self.current_frame])

    def stop(self):
        self.timer.stop()