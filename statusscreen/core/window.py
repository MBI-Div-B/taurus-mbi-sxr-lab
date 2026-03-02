# core/window.py
from .panel import HeaderWidget, EnvironmentPanel, VacuumPanel, LaserPanel

from taurus.external.qt import Qt
# from taurus.qt.qtgui.application import TaurusApplication
# from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from pathlib import Path
# from PyQt5 import QtSvg

# from taurus_pyqtgraph import TaurusTrend


class BaseWindow(Qt.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('SXR Lab Status')
        self.setMinimumSize(1400, 800)    
        
        # load MBI fonts
        # core/window.py -> statusscreen/
        base_dir = Path(__file__).parent.parent  
        fonts_dir = base_dir / 'styles' / 'fonts'
        for font_file in fonts_dir.glob('*.ttf'):
            Qt.QFontDatabase.addApplicationFont(str(font_file))

        # load styles specified in mbi-styles.qss
        style_path = base_dir / 'styles' / 'mbi-styles.qss'
        self.setStyleSheet(style_path.read_text())

        # switch to different icon...
        self.setWindowIcon(Qt.QIcon(str(base_dir / 'styles' / 'mbi-logo.png')))

        # set base layout to align the panels
        central = Qt.QWidget()
        self.central_layout = Qt.QVBoxLayout(central)
        self.setCentralWidget(central)
        
        # add panels
        self.header = HeaderWidget()
        self.central_layout.addWidget(self.header)

        env_panel = EnvironmentPanel()
        vac_panel = VacuumPanel()

        envvac_widget = Qt.QWidget()
        envvac_layout = Qt.QHBoxLayout(envvac_widget)
        envvac_layout.addWidget(env_panel)
        envvac_layout.addItem(Qt.QSpacerItem(20, 40, Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum))
        envvac_layout.addWidget(vac_panel)
        envvac_layout.setAlignment(Qt.Qt.AlignTop)

        self.central_layout.addWidget(envvac_widget)

        self.laser = LaserPanel()
        self.central_layout.addWidget(self.laser)

        self.central_layout.setAlignment(Qt.Qt.AlignTop)


        # Set the central widget of the Window.
        # self.setCentralWidget(self.centralWidget)
        
