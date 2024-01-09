import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCharts import QChart 
from PySide6.QtCore import Qt, QTimer

def generate_random_data():
    # Genera datos aleatorios para la gráfica
    data = []
    for i in range(10):
        data.append((i, random.randint(0, 100)))
    return data

def update_chart(series):
    # Actualiza los datos de la serie de la gráfica con nuevos valores aleatorios
    data = generate_random_data()
    series.clear()
    for point in data:
        series.append(*point)

def main():
    app = QApplication(sys.argv)
    
    # Creamos una ventana principal
    window = QMainWindow()
    window.setWindowTitle("Gráfico de Líneas Dinámico")
    
    # Creamos un widget para el gráfico
    chart_widget = QWidget()
    layout = QVBoxLayout()
    
    # Creamos una serie de datos para la gráfica de líneas
    series = QChart.QLineSeries()
    
    # Generamos datos aleatorios para la serie inicial
    update_chart(series)
    
    # Creamos un gráfico y añadimos la serie de datos
    chart = QtCharts.QChart()
    chart.addSeries(series)
    chart.createDefaultAxes()
    chart_view = QtCharts.QChartView(chart)
    layout.addWidget(chart_view)
    chart_widget.setLayout(layout)
    
    # Creamos un temporizador para actualizar la gráfica cada cierto tiempo
    timer = QTimer()
    timer.timeout.connect(lambda: update_chart(series))
    timer.start(1000)  # Actualiza cada 1 segundo (1000 ms)
    
    # Establecemos el widget del gráfico como widget central de la ventana
    window.setCentralWidget(chart_widget)
    
    # Mostramos la ventana
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

