import numpy as np


class LissajousFigure:
    """
    Фигуры Лиссажу.
    Задаётся набором точек с координатами x и y.
    """

    def __init__(self, x_array, y_array):
        self.x_arr = x_array
        self.y_arr = y_array


class LissajousGenerator:
    """
    Генерирует фигуры Лиссажу с заданными параметрами
    """

    def __init__(self, resolution=20):
        """
        Убрал задержку
        """
        self.resolution = None
        self.set_resolution(resolution)

    def set_resolution(self, resolution):
        """
        resolution определяет количество точек в кривой
        """
        self.resolution = resolution

    def generate_figure(self, freq_x, freq_y, shift):
        """
        Генерирует фигуру (массивы x и y координат точек) с заданными частотами.
        Добавил сдвиг фаз, которого не хватало по формуле
        """
        t = np.linspace(0, 2 * np.pi, self.resolution)
        x = np.sin(freq_x * t + shift)
        y = np.cos(freq_y * t)
        return LissajousFigure(x, y)
