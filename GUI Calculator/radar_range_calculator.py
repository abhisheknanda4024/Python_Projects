import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QMessageBox, QGridLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from math import sqrt, pi
import numpy as np

class RadarDetection(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        main_layout = QVBoxLayout()
        input_layout = QGridLayout()
        
        font = QFont('Arial', 10, QFont.Bold)
        
        self.power_label = QLabel('Transmitted Power (W):', self)
        self.power_label.setFont(font)
        self.power_input = QLineEdit(self)
        
        self.gain_label = QLabel('Antenna Gain (dB):', self)
        self.gain_label.setFont(font)
        self.gain_input = QLineEdit(self)
        
        self.wavelength_label = QLabel('Wave length (m):', self)
        self.wavelength_label.setFont(font)
        self.wavelength_input = QLineEdit(self)
        
        self.target_rcs_label = QLabel('Radar Cross Section (m²):', self)
        self.target_rcs_label.setFont(font)
        self.target_rcs_input = QLineEdit(self)
        
        self.snr_label = QLabel('Signal-to-Noise Ratio (dB):', self)
        self.snr_label.setFont(font)
        self.snr_input = QLineEdit(self)
        
        self.delta1_label = QLabel('Delta 1 (dB):', self)
        self.delta1_label.setFont(font)
        self.delta1_input = QLineEdit(self)
        
        self.delta2_label = QLabel('Delta 2 (dB):', self)
        self.delta2_label.setFont(font)
        self.delta2_input = QLineEdit(self)
        
        self.pt1_label = QLabel('Percent 1 (%):', self)
        self.pt1_label.setFont(font)
        self.pt1_input = QLineEdit(self)
        
        self.pt2_label = QLabel('Percent 2 (%):', self)
        self.pt2_label.setFont(font)
        self.pt2_input = QLineEdit(self)
        
        input_layout.addWidget(self.power_label, 0, 0)
        input_layout.addWidget(self.power_input, 0, 1)
        input_layout.addWidget(self.gain_label, 1, 0)
        input_layout.addWidget(self.gain_input, 1, 1)
        input_layout.addWidget(self.wavelength_label, 2, 0)
        input_layout.addWidget(self.wavelength_input, 2, 1)
        input_layout.addWidget(self.target_rcs_label, 3, 0)
        input_layout.addWidget(self.target_rcs_input, 3, 1)
        input_layout.addWidget(self.snr_label, 4, 0)
        input_layout.addWidget(self.snr_input, 4, 1)
        input_layout.addWidget(self.delta1_label, 5, 0)
        input_layout.addWidget(self.delta1_input, 5, 1)
        input_layout.addWidget(self.delta2_label, 6, 0)
        input_layout.addWidget(self.delta2_input, 6, 1)
        input_layout.addWidget(self.pt1_label, 7, 0)
        input_layout.addWidget(self.pt1_input, 7, 1)
        input_layout.addWidget(self.pt2_label, 8, 0)
        input_layout.addWidget(self.pt2_input, 8, 1)
        
        self.calc_button = QPushButton('Calculate Detection', self)
        self.calc_button.setFont(font)
        self.calc_button.clicked.connect(self.calculate_detection)
        input_layout.addWidget(self.calc_button, 9, 0, 1, 2)
        
        main_layout.addLayout(input_layout)
        
        self.range_label = QLabel('Calculated Range (m):', self)
        self.range_label.setFont(font)
        self.range_output = QLabel('', self)
        self.range_output.setFont(font)
        main_layout.addWidget(self.range_label)
        main_layout.addWidget(self.range_output)
        
        graph_layout = QHBoxLayout()

        self.figure1 = plt.figure(figsize=(8, 6))
        self.canvas1 = FigureCanvas(self.figure1)
        self.toolbar1 = NavigationToolbar(self.canvas1, self)
        graph_frame1 = QFrame()
        graph_frame1.setLayout(QVBoxLayout())
        graph_frame1.layout().addWidget(self.toolbar1)
        graph_frame1.layout().addWidget(self.canvas1)
        graph_layout.addWidget(graph_frame1)

        self.figure2 = plt.figure(figsize=(8, 6))
        self.canvas2 = FigureCanvas(self.figure2)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        graph_frame2 = QFrame()
        graph_frame2.setLayout(QVBoxLayout())
        graph_frame2.layout().addWidget(self.toolbar2)
        graph_frame2.layout().addWidget(self.canvas2)
        graph_layout.addWidget(graph_frame2)

        main_layout.addLayout(graph_layout)
        
        self.setLayout(main_layout)
        self.setWindowTitle('Radar Detection Simulation')
        self.setGeometry(100, 100, 1800, 900)
        
    def calculate_detection(self):
        try:
            transmitted_power = self.get_value(self.power_input)
            antenna_gain_dB = self.get_value(self.gain_input)
            wave_length = self.get_value(self.wavelength_input)
            target_rcs = self.get_value(self.target_rcs_input)
            snr_dB = self.get_value(self.snr_input)
            delta1_dB = self.get_value(self.delta1_input)
            delta2_dB = self.get_value(self.delta2_input)
            pt1 = self.get_value(self.pt1_input)
            pt2 = self.get_value(self.pt2_input)
            
            if None in (transmitted_power, antenna_gain_dB, wave_length, target_rcs, snr_dB, delta1_dB, delta2_dB, pt1, pt2):
                QMessageBox.warning(self, 'Input Error', 'Please enter all required values')
                return
            
            antenna_gain_linear = 10 ** (antenna_gain_dB / 10)
            snr_linear = 10 ** (snr_dB / 10)
            delta1_linear = 10 ** (delta1_dB / 10)
            delta2_linear = 10 ** (delta2_dB / 10)
            
            range_ =(double(((transmitted_power * antenna_gain_linear ** 2 * target_rcs * wave_length ** 2) / 
                      ((4 * pi) ** 3 * snr_linear)) ** 0.25))
            
            self.range_output.setText(f'{range_:.2f} m')
            self.plot_detection(transmitted_power, antenna_gain_linear, target_rcs, wave_length, snr_dB, delta1_linear, delta2_linear, pt1, pt2)
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter valid numeric values')
    5
    def get_value(self, input_field, value_type=float):
        text = input_field.text()
        return value_type(text) if text else None
            
    def plot_detection(self, transmitted_power, antenna_gain_linear, target_rcs, wave_length, snr_dB, delta1_linear, delta2_linear, pt1, pt2):
        self.figure1.clear()
        self.figure2.clear()

        snr_values = np.linspace(snr_dB - 10, snr_dB + 10, 50)
        # First Graph: SNR vs Range for RCS, RCS + Delta1, and RCS - Delta2
        range_values_rcs = []
        range_values_rcs_plus_delta1 = []
        range_values_rcs_minus_delta2 = []

        for snr_dB_value in snr_values:
            snr_linear_value = 10 ** (snr_dB_value / 10)
            range_rcs = ((transmitted_power * antenna_gain_linear ** 2 * target_rcs * wave_length ** 2) / 
                         ((4 * pi) ** 3 * snr_linear_value)) ** 0.25
            range_rcs_plus_delta1 = ((transmitted_power * antenna_gain_linear ** 2 * (target_rcs * delta1_linear) * wave_length ** 2) / 
                                     ((4 * pi) ** 3 * snr_linear_value)) ** 0.25
            range_rcs_minus_delta2 = ((transmitted_power * antenna_gain_linear ** 2 * (target_rcs / delta2_linear) * wave_length ** 2) / 
                                      ((4 * pi) ** 3 * snr_linear_value)) ** 0.25

            range_values_rcs.append(range_rcs)
            range_values_rcs_plus_delta1.append(range_rcs_plus_delta1)
            range_values_rcs_minus_delta2.append(range_rcs_minus_delta2)

        ax1 = self.figure1.add_subplot(111)
        ax1.plot(snr_values, range_values_rcs, label='RCS')
        ax1.plot(snr_values, range_values_rcs_plus_delta1, label=f'RCS + Delta1 ({delta1_linear:.2f})')
        ax1.plot(snr_values, range_values_rcs_minus_delta2, label=f'RCS - Delta2 ({delta2_linear:.2f})')
        ax1.set_title('SNR vs. Range (RCS Variations)')
        ax1.set_xlabel('SNR (dB)')
        ax1.set_ylabel('Range (m)')
        ax1.legend()
        self.canvas1.draw()
        
        # Second Graph: SNR vs Range for Transmitted Power, Transmitted Power * pt1, and Transmitted Power * pt2
        range_values_power = []
        range_values_power_pt1 = []
        range_values_power_pt2 = []

        for snr_dB_value in snr_values:
            snr_linear_value = 10 ** (snr_dB_value / 10)
            range_power = ((transmitted_power * antenna_gain_linear ** 2 * target_rcs * wave_length ** 2) / 
                           ((4 * pi) ** 3 * snr_linear_value)) ** 0.25
            range_power_pt1 = (((transmitted_power * pt1/100) * antenna_gain_linear ** 2 * target_rcs * wave_length ** 2) / 
                               ((4 * pi) ** 3 * snr_linear_value)) ** 0.25
            range_power_pt2 = (((transmitted_power * pt2/100) * antenna_gain_linear ** 2 * target_rcs * wave_length ** 2) / 
                               ((4 * pi) ** 3 * snr_linear_value)) ** 0.25

            range_values_power.append(range_power)
            range_values_power_pt1.append(range_power_pt1)
            range_values_power_pt2.append(range_power_pt2)

        ax2 = self.figure2.add_subplot(111)
        ax2.plot(snr_values, range_values_power, label='Transmitted Power')
        ax2.plot(snr_values, range_values_power_pt1, label=f'Transmitted Power * {pt1}%')
        ax2.plot(snr_values, range_values_power_pt2, label=f'Transmitted Power * {pt2}%')
        ax2.set_title('SNR vs. Range (Transmitted Power Variations)')
        ax2.set_xlabel('SNR (dB)')
        ax2.set_ylabel('Range (m)')
        ax2.legend()
        
        self.canvas2.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    detector = RadarDetection()
    detector.show()
    sys.exit(app.exec_())
