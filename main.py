import sys

from PySide6.QtWidgets import QApplication

from settings import PetSettings
from world import World
from pet import Pet


def main():

    app = QApplication(sys.argv)

    # Загружаем настройки
    settings = PetSettings.load()

    # Создаём мир
    world = World()

    world.update()

    # Создаём персонажа
    pet = Pet(
        world,
        settings
    )

    screen = (
        QApplication
        .primaryScreen()
        .availableGeometry()
    )

    # Позиция персонажа
    x = (
        screen.center().x()
        - pet.width() // 2
    )

    y = (
        screen.bottom()
        - pet.height()
    )

    pet.move(x, y)

    pet.show()

    pet.grounded = True

    # Начальное поведение
    if settings.behavior == "fly":

        pet.state = "fly"

    else:

        pet.state = "walk"

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()