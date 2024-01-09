import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar
from PySide6 import QtCore 

def main():
    app = QApplication(sys.argv)
    
    # Creamos un widget principal
    window = QWidget()
    
    # Creamos un layout vertical principal
    layout = QVBoxLayout()
    
    # Creamos la barra de progreso vertical
    progress_bar = QProgressBar()
    progress_bar.setStyleSheet("""
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: red;
}
""")
    
    # Configuramos la barra de progreso para que sea vertical
    progress_bar.setOrientation(QtCore.Qt.Vertical)  # 1 es la orientación vertical
    
    # Establecemos el rango de la barra de progreso (0 a 100)
    progress_bar.setRange(0, 100)
    
    # Establecemos el valor inicial de la barra de progreso
    progress_bar.setValue(50)  # Cambia este valor para ajustar la posición inicial
    
    # Añadimos la barra de progreso al layout vertical principal
    layout.addWidget(progress_bar)
    
    # Establecemos el layout como el diseño principal del widget
    window.setLayout(layout)
    
    # Mostramos la ventana
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

