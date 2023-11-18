import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt, QPropertyAnimation, QSize, QPointF, QPoint
from formulario import Ui_Form
from conexion_sqlite import ConexionSQLite

class MiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.conexion = ConexionSQLite('lista_de_precios.db')
        self.listar_productos()
       
        # configuro frame_superior y su desplazamiento 
        self.ui.frame_superior.mousePressEvent = self.on_drag_start
        self.ui.frame_superior.mouseMoveEvent = self.on_drag_move
        self.drag_position = QPoint()
        self.drag_active = False
        self.drag_position = None
        
        # elimina la barra que viene por defecto
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint) 
        
        # Configura los botones de manejo de ventana
        self.ui.btn_cerrar.clicked.connect(self.btn_cerrar)
        self.ui.btn_maximizar.clicked.connect(self.btn_maximizar)
        self.ui.btn_minimizar.clicked.connect(self.btn_minimizar)
        self.ui.btn_hidden.clicked.connect(self.btn_hidden)

        # Configura los botones para realizar operaciones de base de datos
        self.ui.btn_PListar.clicked.connect(self.listar_productos)
        self.ui.btn_PCrear.clicked.connect(self.crear_producto)
        self.ui.btn_crear.clicked.connect(self.insertar_producto)
        self.ui.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.ui.btn_editar.clicked.connect(self.ver_editar)
        self.ui.btn_guardar_cambios.clicked.connect(self.guardar_cambios)
        
# < Animacion del side_menu >
        self.ui.btn_menu.clicked.connect(self.btn_menu)
        self.menu_expanded = True
        self.menu_animation = QPropertyAnimation(self.ui.frame_controles, b'size')

    def btn_menu(self):
        if not self.menu_expanded:
            self.expand_menu()
        else:
            self.collapse_menu()
        self.menu_expanded = not self.menu_expanded

    def expand_menu(self):
        current_size = self.ui.frame_controles.size()
        new_width = 100  # Ancho deseado
        new_size = QSize(new_width, current_size.height())
        self.animate_menu(new_size)

    def collapse_menu(self):
        current_size = self.ui.frame_controles.size()
        new_width = 0  # Ancho para cerrar el menú
        new_size = QSize(new_width, current_size.height())
        self.animate_menu(new_size)

    def animate_menu(self, new_size):
        self.menu_animation.setStartValue(self.ui.frame_controles.size())
        self.menu_animation.setEndValue(new_size)
        self.menu_animation.setDuration(300)  # Duración de la animación en milisegundos
        self.menu_animation.start()
# < / Animacion del side_menu >
        
# <  Frame superior - botones >
    def btn_cerrar(self):
        self.close()
        
    def btn_maximizar(self):
         self.showFullScreen()
         
    def btn_minimizar(self):
        self.setGeometry(200, 200, 700, 300)
    
    def btn_hidden(self):
        self.showMinimized()
# < / Frame superior - botones >

# -------------------------------------------------  <  CRUD >  
               
    def listar_productos(self):
        # Lógica para mostrar los productos en la tabla
        indice_pagina_crear = 0  # Ajusta el índice según la posición de la página en tu QStackedWidget
        self.ui.stackedWidget.setCurrentIndex(indice_pagina_crear)  
        productos = self.conexion.get_productos()
        self.mostrar_en_tabla(productos)

    def mostrar_en_tabla(self, productos):
        self.ui.tabla_productos.setRowCount(0)  # Limpia la tabla antes de agregar datos nuevos

        for row_index, producto in enumerate(productos):
            self.ui.tabla_productos.insertRow(row_index)  # Inserta una nueva fila en la tabla

            # Agrega los datos del producto a cada celda de la fila
            for col_index, valor in enumerate(producto):
                cell = QTableWidgetItem(str(valor))  # Convierte el valor a texto
                self.ui.tabla_productos.setItem(row_index, col_index, cell)

    def crear_producto(self):
        indice_pagina_crear = 2  # Ajusta el índice según la posición de la página en tu QStackedWidget
        self.ui.stackedWidget.setCurrentIndex(indice_pagina_crear)   
   
    def insertar_producto(self):
        codigo = self.ui.lineEdit_codigo.text()
        producto = self.ui.lineEdit_producto.text()
        precio = self.ui.lineEdit_precio.text()
        self.conexion.insert_producto(codigo, producto, precio)
        
        indice_pagina_crear = 0 # Ajusta el índice según la posición de la página en tu QStackedWidget
        self.ui.stackedWidget.setCurrentIndex(indice_pagina_crear) 
        self.listar_productos()
        
        self.ui.lineEdit_codigo.clear()
        self.ui.lineEdit_producto.clear()
        self.ui.lineEdit_precio.clear()

    def eliminar_producto(self):
        fila_actual = self.ui.tabla_productos.currentRow()
        id = self.ui.tabla_productos.item(fila_actual, 0)
        if id is not None:
            self.conexion.delete_producto(id.text())
            self.listar_productos()
            indice_pagina_crear = 0 # Ajusta el índice según la posición de la página en tu QStackedWidget
            self.ui.stackedWidget.setCurrentIndex(indice_pagina_crear)
        else:
            self.mostrar_alerta()
   
    
   
    def ver_editar(self):
        # redirecciono a pagina editar
        fila_actual = self.ui.tabla_productos.currentRow()
        id = self.ui.tabla_productos.item(fila_actual, 0)
        if id is not None:
            self.ver_datos_x_id(id.text())
            indice_pagina_crear = 1 # Ajusta el índice según la posición de la página en tu QStackedWidget
            self.ui.stackedWidget.setCurrentIndex(indice_pagina_crear)
        else:
            self.mostrar_alerta()
            return
            
    def ver_datos_x_id(self, id):
        valores = self.conexion.get_producto_by_id(id)
        id,codigo,producto,precio = valores
        
        self.ui.lineEdit_codigo_2.clear()
        self.ui.lineEdit_producto_2.clear()
        self.ui.lineEdit_precio_2.clear()
        self.ui.label_id.clear()
        
        self.ui.label_id.setText(str(id))
        self.ui.lineEdit_codigo_2.insert(codigo)
        self.ui.lineEdit_producto_2.insert(producto)
        self.ui.lineEdit_precio_2.insert(precio)
        
    def guardar_cambios(self):
        id = self.ui.label_id.text()
        codigo = self.ui.lineEdit_codigo_2.text()
        producto = self.ui.lineEdit_producto_2.text()
        precio = self.ui.lineEdit_precio_2.text()
        id = int(id)
        self.conexion.update_producto( id, codigo, producto, precio)
        self.listar_productos()
        indice_pagina = 0 # menu inicial
        self.ui.stackedWidget.setCurrentIndex(indice_pagina)
        
        self.ui.lineEdit_codigo_2.clear()
        self.ui.lineEdit_producto_2.clear()
        self.ui.lineEdit_precio_2.clear()
# -------------------------------------------------  < / CRUD >  

# -------------------------------------------------  <  ALERT >  
    def mostrar_alerta(self):
        alerta = QMessageBox()
        alerta.setIcon(QMessageBox.Icon.Warning)  # Puedes usar diferentes íconos como Information, Critical, etc.
        alerta.setText("¡Selecciona un elemento!")
        alerta.setWindowTitle("Alerta")
        alerta.exec()
# -------------------------------------------------  < / ALERT >  
        


# <  Despalazar desde frame_superior >
    def on_drag_start(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_active = True
            frame_top_left = self.frameGeometry().topLeft()
            frame_top_left_as_pointf = QPointF(frame_top_left)
            self.drag_position = event.globalPosition() - frame_top_left_as_pointf

    def on_drag_move(self, event):
        if self.drag_active:
            new_position = event.globalPosition() - self.drag_position
            self.move(new_position.toPoint())
# < / Despalazar desde frame_superior >


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiApp()
    ventana.show()
    sys.exit(app.exec())
