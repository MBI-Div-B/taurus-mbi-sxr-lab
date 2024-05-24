#!/usr/bin/python3 -u
# coding: utf8

import sys
from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from pathlib import Path
from PyQt5 import QtSvg
from status_screen import StatusScreen


class Entry(Qt.QMainWindow):
    def __init__(self,parent=None):
        super(Entry, self).__init__(parent)
        self.setWindowTitle('SXR Lab Entry')
        self.setWindowIcon(Qt.QIcon('mbi-logo.png'))
        self.setFixedSize(800, 600)        
        Qt.QFontDatabase.addApplicationFont('./resources/FiraSans-Regular.tff')
        self.setStyleSheet(Path(Path(__file__).parent / 'mbi-styles.qss').read_text())
        

        self.button_height = 75

        centralWidget = Qt.QWidget(self)
        # centralWidget.setFixedSize(800, 600)     
        centralLayout = Qt.QGridLayout(centralWidget)
        centralLayout.setAlignment(Qt.Qt.AlignTop)
        ### header
        # title
        title = Qt.QLabel("SXR Lab Entry")
        title.setObjectName("title")
        title.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        
        # logo 
        svgWidget = QtSvg.QSvgWidget('resources/mbi-logo.svg')
        svgWidget.setFixedWidth(100)
        svgWidget.setFixedHeight(68)

        centralLayout.addWidget(title, 0, 0)
        centralLayout.addWidget(svgWidget, 0, 1, Qt.Qt.AlignRight)
        
        centralLayout.addWidget(self.window_button("SXR Lab Status", "StatusScreen"), 1, 0, 1, 2)
        centralLayout.addWidget(self.window_button("Scattering Status", "NotImplemented"), 2, 0)
        centralLayout.addWidget(self.window_button("Spectroscopy Status", "NotImplemented"), 2, 1)
        centralLayout.addWidget(self.window_button("Environment", "NotImplemented"), 3, 0)
        centralLayout.addWidget(self.window_button("Vacuum", "NotImplemented"), 3, 1)
        centralLayout.addWidget(self.window_button("Lasers", "NotImplemented"), 4, 0)
        centralLayout.addWidget(self.window_button("DAQ/Synchronization", "NotImplemented"), 4, 1)
        centralLayout.addWidget(self.window_button("Raspis", "Raspis"), 5, 0)
        
        self.setCentralWidget(centralWidget)

    def window_button(self, label, widget_class=""):
        button = Qt.QPushButton(label)
        button.setFixedHeight(self.button_height)
        button.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        button.clicked.connect((lambda: self.show_new_window(label, widget_class)))

        return button

    def show_new_window(self, label, widget_class):
        unique_name = (label + widget_class).strip()
        try:
            attr = getattr(self, unique_name)
            attr.close()
            del self.__dict__[unique_name]
        except AttributeError:
            setattr(self, unique_name, globals()[widget_class]())
            attr = getattr(self, unique_name)
            attr.show()


class NotImplemented(Qt.QMainWindow):
    def __init__(self,parent=None):
        super(NotImplemented, self).__init__(parent)
        self.setWindowTitle('Not Implemented')
        self.setWindowIcon(Qt.QIcon('mbi-logo.png'))
        self.setFixedSize(300, 100)
        Qt.QFontDatabase.addApplicationFont('./resources/FiraSans-Regular.tff')
        self.setStyleSheet(Path(Path(__file__).parent / 'mbi-styles.qss').read_text())
        
        label = Qt.QLabel("Not Implemented")
        label.setAlignment(Qt.Qt.AlignCenter)
        self.setCentralWidget(label)

class Raspis(Qt.QMainWindow):
    def __init__(self,parent=None):
        super(Raspis, self).__init__(parent)
        self.setWindowTitle('Raspis')
        self.setWindowIcon(Qt.QIcon('mbi-logo.png'))
        self.setFixedSize(800, 600)
        Qt.QFontDatabase.addApplicationFont('./resources/FiraSans-Regular.tff')
        self.setStyleSheet(Path(Path(__file__).parent / 'mbi-styles.qss').read_text())
                
        centralWidget = Qt.QWidget(self)
        # centralWidget.setFixedSize(800, 600)     
        centralLayout = Qt.QGridLayout(centralWidget)
        centralLayout.setAlignment(Qt.Qt.AlignTop)


        ### header
        # title
        title = Qt.QLabel("Raspis")
        title.setObjectName("title")
        title.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        
        # logo 
        svgWidget = QtSvg.QSvgWidget('mbi-logo.svg')
        svgWidget.setFixedWidth(100)
        svgWidget.setFixedHeight(68)

        centralLayout.addWidget(title, 0, 0)
        centralLayout.addWidget(svgWidget, 0, 1, Qt.Qt.AlignRight)

        tabs = Qt.QTabWidget()

        tab1 = Qt.QWidget() 
        tab2 = Qt.QWidget() 
        tab3 = Qt.QWidget()
  
        # Add tabs 
        tabs.addTab(tab1, "Geeks") 
        tabs.addTab(tab2, "For") 
        tabs.addTab(tab3, "Geeks") 
  
        # Create first tab 
        tab1.layout = Qt.QVBoxLayout(self) 
        l = Qt.QLabel() 
        l.setText("This is the first tab") 
        tab1.layout.addWidget(l) 
        tab1.setLayout(tab1.layout) 

        centralLayout.addWidget(tabs, 1, 0, 1, 2)
        

        self.setCentralWidget(centralWidget)

if __name__ == '__main__':
    app = TaurusApplication(sys.argv, cmd_line_parser=None, app_name='SXR Entry')
    window = Entry()
    window.show()
    sys.exit(app.exec_())
