"""Класс для работы с сущностью локатора"""
from selenium.webdriver.common.by import By


class Locator:
    def __init__(self, name: str, locator: tuple[str, str]):
        """Инициализация локатора

        Args:
            name: Название локатора
            locator: Значение локатора
        """
        self.name = name
        self.locator = locator

    def __add__(self, other):
        return self.locator[1] + other

    def __radd__(self, other):
        return other + self.locator[1]

    def __repr__(self):
        return f'Locator(name={self.name}, type={self.locator})'

    def __str__(self):
        return f'Элемент {self.name} с локатором {self.locator}'

    def __call__(self, **kwargs):
        return Locator(
            name=self.name.format(**kwargs),
            locator=(self.locator[0], self.locator[1].format(**kwargs)),
        )
