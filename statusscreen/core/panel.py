# core/panel.py

from pathlib import Path
from taurus.external.qt import Qt
from PyQt5 import QtSvg
class HeaderWidget(Qt.QWidget):
    # constructor to run when creating an instance of HeaderWidget 
    def __init__(self):
        # runs QWidget constructor
        super().__init__()
        # lines up elements horizontally
        layout = Qt.QHBoxLayout(self)
        
        # title
        title = Qt.QLabel('SXR Lab Status')
        title.setFont(Qt.QFont('Fira Sans', 40))
        title.setObjectName('title')
        title.setFixedWidth(450)
        layout.addWidget(title)
        
        # clock
        self.clock = Qt.QLabel()
        self.clock.setObjectName('titlelight')
        self.clock.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        layout.addWidget(self.clock)
        
        # update clock every second
        timer = Qt.QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()          
        
        # logo
        base_dir = Path(__file__).parent.parent  
        svg_path = base_dir / 'styles' / 'mbi-logo.svg'
        svg_widget = QtSvg.QSvgWidget(str(svg_path))
        svg_widget.setFixedWidth(100)
        svg_widget.setFixedHeight(68)
        layout.addWidget(svg_widget)

    def update_time(self):
        self.clock.setText(Qt.QDateTime.currentDateTime().toString('dddd dd.MM.yyyy - hh:mm:ss'))