import sys
import os
import PyQt5.QtWidgets as qw
from PyQt5 import QtGui, QtCore
import matplotlib.pyplot as plt
import json
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from lissajousgen import LissajousGenerator


class LissajousWindow(qw.QMainWindow):
    """
    Главное окно приложения
    """

    # Настройки фигуры по умолчанию
    default_settings = {
        "freq_x": 2,
        "freq_y": 3,
        "shift": 0,
        "resolution": 20,
        "color": "blue",
        "width": 2}

    # Цвета для matplotlib
    with open("mpl.json", mode="r", encoding="utf-8") as f:
        mpl_color_dict = json.load(f)

    def __init__(self):
        super().__init__()
        # Объявление объектов Qt
        self.button_save = qw.QPushButton("Сохранить фигуру")
        self.button_update = qw.QPushButton("Обновить фигуру")
        self.combobox_width = qw.QComboBox()
        self.color_combobox = qw.QComboBox()
        self.line_edit_resolution = qw.QLineEdit()
        self.line_edit_shift = qw.QLineEdit()
        self.line_edit_y = qw.QLineEdit()
        self.line_edit_x = qw.QLineEdit()

        self.generator = LissajousGenerator()
        self.init_ui()
        self.plot_lissajous_figure()

    def create_form_layout(self):
        """
        Функция создания формы с полями.
        """
        # Ограничения на ввод только чисел
        validator = QtGui.QRegExpValidator(
            QtCore.QRegExp(r"[0-9]*[\.]?[0-9]*"))
        # Ограничения на ввод целых чисел
        validator_res = QtGui.QRegExpValidator(
            QtCore.QRegExp("[1-9][0-9]*"))

        layout = qw.QFormLayout()

        self.line_edit_x.setText(str(self.default_settings["freq_x"]))
        self.line_edit_x.setValidator(validator)
        layout.addRow(qw.QLabel("Частота X"), self.line_edit_x)

        self.line_edit_y.setText(str(self.default_settings["freq_y"]))
        self.line_edit_y.setValidator(validator)
        layout.addRow(qw.QLabel("Частота Y"), self.line_edit_y)

        self.line_edit_shift.setText(
            str(self.default_settings["shift"]))
        self.line_edit_shift.setValidator(validator)
        layout.addRow(qw.QLabel("Сдвиг фаз"),
                      self.line_edit_shift)

        self.line_edit_resolution.setText(
            str(self.default_settings["resolution"]))

        self.line_edit_resolution.setValidator(validator_res)
        layout.addRow(qw.QLabel("Количество точек"),
                      self.line_edit_resolution)

        self.color_combobox.addItems(self.mpl_color_dict.keys())
        # Выбор цвета
        color = ""
        for key, value in self.mpl_color_dict.items():
            if value == self.default_settings["color"]:
                color = key
                break
        self.color_combobox.setCurrentText(color)
        layout.addRow(qw.QLabel("Цвет линии"), self.color_combobox)

        # Выбор толщины линии
        self.combobox_width.addItems(list(map(str, range(1, 5))))
        self.combobox_width.setCurrentText(
            str(self.default_settings["width"]))
        layout.addRow(qw.QLabel("Толщина линии"), self.combobox_width)

        group = qw.QGroupBox("Параметры фигуры Лиссажу")
        group.setLayout(layout)
        return group

    def init_ui(self):
        """
        Метод располагает виджеты на главном окне.
        """

        # Ставим версию и иконку
        with open("version.txt", "r") as file:
            version = file.readline()
        self.setWindowTitle(
            "Генератор фигур Лиссажу. Версия {}.".format(version))
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(script_dir + os.path.sep + "icon.bmp"))

        # Захватываем клики с кнопки
        self.button_update.clicked.connect(self.click_on_button_update)
        self.button_save.clicked.connect(self.handle_click_on_button_save)

        # Расположение на экране
        v_box = qw.QVBoxLayout()
        v_box.addWidget(self.create_form_layout())
        v_box.addWidget(self.button_update)
        v_box.addWidget(self.button_save)
        v_box.addStretch(1)

        self.fig = plt.figure(figsize=(4, 3), dpi=72)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas: FigureCanvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)

        h_box = qw.QHBoxLayout()
        h_box.addWidget(self.canvas, 1)
        h_box.addLayout(v_box)
        widget = qw.QWidget()
        widget.setLayout(h_box)
        self.setCentralWidget(widget)

    @QtCore.pyqtSlot()
    def click_on_button_update(self):
        """
        Обработчик нажатия на кнопку 'Обновить фигуру'.
        """

        settings = {"freq_x": float(self.line_edit_x.text()),
                    "freq_y": float(self.line_edit_y.text()),
                    "shift": float(self.line_edit_shift.text()),
                    "resolution": int(self.line_edit_resolution.text()),
                    "color": self.mpl_color_dict[
                        self.color_combobox.currentText()],
                    "width": int(self.combobox_width.currentText())}
        self.plot_lissajous_figure(settings)

    @QtCore.pyqtSlot()
    def handle_click_on_button_save(self):
        """
        Обработчик нажатия на кнопку 'Сохранить фигуру'.
        """
        # Выбор пути сохранения
        path = os.path.abspath("save img")
        filename, extension = qw.QFileDialog.getSaveFileName(self,
                                                             "Сохранение "
                                                             "изображения",
                                                             path,
                                                             "PNG(*.png);;"
                                                             "JPEG(*.jpg "
                                                             "*.jpeg)")
        if extension == "PNG(*.png)":
            extension = "png"
        elif extension == "JPEG(*.jpg *.jpeg)":
            extension = "jpg"
        # Если не указано имя или расширение неверное, не сохраняем изображение
        if filename == "" or extension not in ("png", "jpg"):
            return
        self.fig.savefig(filename, format=extension)

    def plot_lissajous_figure(self, setting: dict[str, [float, str]] = default_settings):
        """
        Метод рисует фигуру Лиссажу.
        """

        self.generator.set_resolution(setting["resolution"])
        figure = self.generator.generate_figure(setting["freq_x"],
                                                setting["freq_y"],
                                                setting["shift"])
        self.ax.clear()
        self.ax.plot(figure.x_arr, figure.y_arr,
                     color=setting["color"],
                     linewidth=setting["width"])
        plt.axis("off")
        plt.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    # Инициализируем приложение Qt
    app = qw.QApplication(sys.argv)

    # Создаём и настраиваем главное окно
    main_window = LissajousWindow()

    # Показываем окно
    main_window.show()

    # Запуск приложения
    # На этой строке выполнение основной программы блокируется
    # до тех пор, пока пользователь не закроет окно.
    # Вся дальнейшая работа должна вестись либо в отдельных потоках,
    # либо в обработчиках событий Qt.
    sys.exit(app.exec_())
