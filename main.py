import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.move(650, 400)
        self.setFixedSize(650, 280)
        self.setWindowTitle('Фурье фильтрация')
        lbl = QLabel("Фурье фильтрация ВСР")
        lbl.setFont(QFont('Times', 24))
        lbl.setGeometry(120, -20, 650, 100)
        self.layout().addWidget(lbl)

        self.load_button = QPushButton('Загрузить данные', self)
        self.load_button.setGeometry(50, 100, 160, 30)
        self.load_button.clicked.connect(self.load_file)

        self.res_button = QPushButton('Показать результат', self)
        self.res_button.setGeometry(250, 100, 160, 30)
        self.res_button.clicked.connect(self.filt)

        self.label = QLabel("Введите диапазон частот:", self)
        self.label.setGeometry(250, 150, 200, 30)

        self.combo = QComboBox(self)
        self.combo.setGeometry(250, 180, 210, 30)
        self.combo.addItems(["ВЧ (0.15 - 0.4 Гц)", "НЧ (0.04 - 0.15 Гц)", "ОНЧ (0 - 0.04 Гц)"])
        self.combo.setFont(QFont("Times New Roman", 14))

        self.res_button = QPushButton('Сохранить', self)
        self.res_button.setGeometry(250, 230, 160, 30)
        self.res_button.clicked.connect(self.save)

        self.spectrum_button = QPushButton('Спектрограмма', self)
        self.spectrum_button.setGeometry(450, 100, 160, 30)
        self.spectrum_button.clicked.connect(self.spec)

        self.filename = None
        self.rr_data = None
        self.bottom_filt = None
        self.top_filt = None

    def change(self, bot, top):
        self.bottom_filt = bot
        self.top_filt = top

    def save(self):
        self.change(float(self.combo.currentText().split("(")[1].split(" ")[0]),
                    float(self.combo.currentText().split("(")[1].split(" ")[2]))

    def load_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', '(*.rr)')

        if self.filename:
            with open(self.filename, 'r') as f:
                f.readline()
                data = f.read()

            self.rr_data = [int(x) for x in data.split()]

    def filt(self):
        self.filtration(self.bottom_filt, self.top_filt)

    def filtration(self, bot, top):
        if self.rr_data and self.top_filt:
            N = len(self.rr_data)
            t = np.linspace(0, N, N)
            x = self.rr_data
            x -= np.mean(self.rr_data)
            X = np.fft.fft(x)
            freqs = np.fft.fftfreq(N, 1)
            mask = np.abs(np.logical_and(freqs > bot, freqs < top))

            X_filt = X * mask

            x_filt = np.real(np.fft.ifft(X_filt))

            plt.plot(t, x, label='Исходный сигнал')
            plt.plot(t, x_filt, label='Отфильтрованный сигнал')
            plt.ylabel('Отличие RR-интервалов от средних значений (мСек)')
            plt.show()

    def spec(self):
        self.show_spectrum(self.bottom_filt, self.top_filt)

    def show_spectrum(self, bot, top):
        if self.rr_data and self.top_filt:
            N = len(self.rr_data)
            x = self.rr_data
            x -= np.mean(self.rr_data)
            X = np.fft.fft(x)
            freqs = np.fft.fftfreq(N, 1)
            mask = np.abs(np.logical_and(freqs > bot, freqs < top))

            X_filt = X * mask

            amp_rr = np.abs(X)
            amp_rr1 = np.abs(X_filt)

            plt.plot(freqs[1:len(freqs) // 2], amp_rr[1:len(amp_rr) // 2])
            plt.plot(freqs[1:len(freqs) // 2], amp_rr1[1:len(amp_rr) // 2])
            plt.ylabel('Амплитуда')
            plt.xlabel('Частота (Гц)')
            plt.show()


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
