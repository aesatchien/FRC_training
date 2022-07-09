import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMenu, QAction, QMenuBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

def window():
    app = QApplication(sys.argv)
    widget = QWidget()
   
    menu_bar = QMenuBar(widget)
    #app.setMenuBar(menu_bar)
    file_menu = QMenu("&File",)
    menu_bar.addMenu(file_menu)
    edit_menu = QMenu("&Edit",)
    menu_bar.addMenu(edit_menu)
    
    print_action = QAction("&Say hello...", widget)
    file_menu.addAction(print_action)
    print_action.triggered.connect(menu_item_triggered)
    
    widget.setGeometry(50,50,320,200)
    widget.setWindowTitle("PyQt5 Menu Item Example")
    widget.show()
    sys.exit(app.exec_())

    

def menu_item_triggered():
    print("Menu item triggered with a function call")
    
    
if __name__ == '__main__':
    window()