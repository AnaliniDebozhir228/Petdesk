from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSlider,
    QCheckBox,
    QPushButton,
)


class SettingsWindow(QDialog):

    settings_changed = Signal()

    def __init__(self, settings, parent=None):

        super().__init__(parent)

        self.settings = settings

        self.setWindowTitle(
            "Desktop Pet — Настройки"
        )

        self.setMinimumWidth(380)

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout()

        # ==========================================
        # ПОВЕДЕНИЕ
        # ==========================================

        behavior_layout = QHBoxLayout()

        behavior_label = QLabel(
            "Поведение:"
        )

        self.behavior_combo = QComboBox()

        self.behavior_combo.addItem(
            "Автоматически",
            "auto"
        )

        self.behavior_combo.addItem(
            "Ходить",
            "walk"
        )

        self.behavior_combo.addItem(
            "Летать",
            "fly"
        )

        index = self.behavior_combo.findData(
            self.settings.behavior
        )

        if index >= 0:
            self.behavior_combo.setCurrentIndex(
                index
            )

        behavior_layout.addWidget(
            behavior_label
        )

        behavior_layout.addWidget(
            self.behavior_combo
        )

        layout.addLayout(
            behavior_layout
        )

        # ==========================================
        # СКОРОСТЬ
        # ==========================================

        layout.addWidget(
            QLabel("Скорость")
        )

        self.speed_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.speed_slider.setRange(
            1,
            10
        )

        self.speed_slider.setValue(
            int(self.settings.speed)
        )

        self.speed_label = QLabel()

        self.update_speed_label(
            self.speed_slider.value()
        )

        self.speed_slider.valueChanged.connect(
            self.update_speed_label
        )

        layout.addWidget(
            self.speed_slider
        )

        layout.addWidget(
            self.speed_label
        )

        # ==========================================
        # РАЗМЕР
        # ==========================================

        layout.addWidget(
            QLabel("Размер")
        )

        self.size_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.size_slider.setRange(
            50,
            300
        )

        self.size_slider.setValue(
            self.settings.size
        )

        self.size_label = QLabel()

        self.update_size_label(
            self.size_slider.value()
        )

        self.size_slider.valueChanged.connect(
            self.update_size_label
        )

        layout.addWidget(
            self.size_slider
        )

        layout.addWidget(
            self.size_label
        )

        # ==========================================
        # ХОДЬБА ПО ОКНАМ
        # ==========================================

        self.windows_checkbox = QCheckBox(
            "Ходить по окнам"
        )

        self.windows_checkbox.setChecked(
            self.settings.walk_on_windows
        )

        layout.addWidget(
            self.windows_checkbox
        )

        # ==========================================
        # ГРАВИТАЦИЯ
        # ==========================================

        self.gravity_checkbox = QCheckBox(
            "Падать с краёв"
        )

        self.gravity_checkbox.setChecked(
            self.settings.gravity_enabled
        )

        layout.addWidget(
            self.gravity_checkbox
        )

        # ==========================================
        # КНОПКА
        # ==========================================

        self.apply_button = QPushButton(
            "Применить"
        )

        self.apply_button.clicked.connect(
            self.apply_settings
        )

        layout.addWidget(
            self.apply_button
        )

        self.setLayout(layout)

    # ==========================================
    # LABELS
    # ==========================================

    def update_speed_label(self, value):

        self.speed_label.setText(
            f"Скорость: {value}"
        )

    def update_size_label(self, value):

        self.size_label.setText(
            f"Размер: {value}px"
        )

    # ==========================================
    # APPLY
    # ==========================================

    def apply_settings(self):

        self.settings.behavior = (
            self.behavior_combo.currentData()
        )

        self.settings.speed = (
            float(self.speed_slider.value())
        )

        self.settings.size = (
            self.size_slider.value()
        )

        self.settings.walk_on_windows = (
            self.windows_checkbox.isChecked()
        )

        self.settings.gravity_enabled = (
            self.gravity_checkbox.isChecked()
        )

        self.settings.save()

        self.settings_changed.emit()

        self.accept()