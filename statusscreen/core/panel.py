# core/panel.py

from pathlib import Path
from taurus.external.qt import Qt
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus_pyqtgraph import TaurusTrend

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

class EnvironmentPanel(Qt.QWidget):
    def __init__(self, attributes, title='Environment', parent=None):
        super().__init__(parent)

        # Main grid
        layout = Qt.QGridLayout(self)
        layout.setAlignment(Qt.Qt.AlignTop)
        self.setLayout(layout)

        # Header
        header_label = Qt.QLabel(title)
        header_label.setObjectName('header')
        layout.addWidget(header_label, 0, 0)

        for i, attr in enumerate(attributes, start=1):
            name_label = Qt.QLabel(attr['name'])
            # name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            sensor_display = TaurusLabel()
            sensor_display.setModel(attr['model'] + '/temperature')
            # sensor_display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            layout.addWidget(name_label, i, 0)
            layout.addWidget(sensor_display, i, 1)


'''
        # Sensors
        sensors = [
            ['Pumps', 'lab/environment/pumps', (1, 0)],
            ['Beamlines', 'sxr/environment/beamlines', (1, 3)],
            ['PXS', 'sxr/environment/pxs', (2, 3)],
            ['TDL Frontend', 'laser/environment/frontend', (1, 6)],
            ['TDL Amplifier', 'laser/environment/thindisk', (2, 6)],
            ['Compressor', 'laser/environment/compressor', (1, 9)],
            ['TiSa', 'laser/environment/tisa', (2, 9)],
        ]

        for s in sensors:
            # Name label
            l = Qt.QLabel(s[0])
            l.setAlignment(Qt.Qt.AlignRight)
            # Temperature TaurusLabel
            t = TaurusLabel()
            t.setModel(s[1] + '/temperature')
            t.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
            layout.addWidget(l, s[2][0], s[2][1])
            layout.addWidget(t, s[2][0], s[2][1]+1)
'''
class VacuumPanel(Qt.QWidget):
    def __init__(self, title='Vacuum', parent=None):
        super().__init__(parent)

        # Main grid
        layout = Qt.QGridLayout(self)
        layout.setAlignment(Qt.Qt.AlignTop)

        # Header label
        header_label = Qt.QLabel(title)
        header_label.setObjectName('header')
        layout.addWidget(header_label, 0, 0)

        # Subheaders
        layout.addWidget(Qt.QLabel('RSXS'), 0, 2)
        layout.addWidget(Qt.QLabel('Spectroscopy'), 0, 4)

        # Gauges
        gauges = [
            ['PXS', 'sxr/tpg261/pxs', (1, 0)],
            ['RZP', 'rsxs/tpg261/rzp', (1, 2)],
            ['Scattering', 'rsxs/tpg261/scattering', (2, 2)],
            ['Optics', 'spec/tpg261/optic', (1, 4)],
            ['CCD', 'spec/tpg261/ccd', (2, 4)],
        ]

        for g in gauges:
            # Name label
            l = Qt.QLabel(g[0])
            l.setAlignment(Qt.Qt.AlignRight)
            # TaurusLabel for pressure
            w = TaurusLabel()
            w.setModel(g[1] + '/pressure')
            w.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
            w.setFormat('{:3.1e}')
            w.setMinimumWidth(200)
            layout.addWidget(l, g[2][0], g[2][1])
            layout.addWidget(w, g[2][0], g[2][1]+1)

class LaserPanel(Qt.QWidget):
    def __init__(self, title='Laser Interlock', parent=None):
        super().__init__(parent)

        # Main layout for this panel
        layout = Qt.QGridLayout(self)  # <- set layout on self
        layout.setAlignment(Qt.Qt.AlignTop)

        # ----- Laser header -----
        laserLabel = Qt.QLabel(title)
        laserLabel.setObjectName('header')
        layout.addWidget(laserLabel, 0, 0)

        # Door interlock
        ledDoor = TaurusLed()
        ledDoor.setOnColor("red")
        ledDoor.setOffColor("green")
        ledDoor.model = 'lab/rpigpio/laserpi/door_tisa'
        ledDoor.setAlignment(Qt.Qt.AlignLeft)
        ledDoor.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        layout.addWidget(ledDoor, 0, 1, 1, 3)

        # TDL Laser
        tdlLabel = Qt.QLabel("Thin Disk Laser")
        tdlLabel.setObjectName('header')
        layout.addWidget(tdlLabel, 1, 0)

        ledShutterTDL= TaurusLed()
        ledShutterTDL.setOnColor("red")
        ledShutterTDL.setOffColor("green")
        ledShutterTDL.model = 'lab/rpigpio/laserpi/shutter_tdl'
        layout.addWidget(ledShutterTDL, 1, 1)

        # TiSa Laser 
        tisaLabel = Qt.QLabel("TiSa Laser")
        tisaLabel.setObjectName('header')
        layout.addWidget(tisaLabel, 1, 2)

        ledShutterTiSa = TaurusLed()
        ledShutterTiSa.setOnColor("red")
        ledShutterTiSa.setOffColor("green")
        ledShutterTiSa.model = 'lab/rpigpio/laserpi/shutter_tisa'
        layout.addWidget(ledShutterTiSa, 1, 3)

        # SC10 Shutter 
        SC10shutterLabel = Qt.QLabel('Shutter')
        layout.addWidget(SC10shutterLabel, 2, 0)
        ledSC10shutter = TaurusLed()
        ledSC10shutter.setOnColor("red")
        ledSC10shutter.setOffColor("green")
        ledSC10shutter.model = 'thindisk/thorlabssc10/seed/open'
        layout.addWidget(ledSC10shutter, 2, 1)

        # Waveplate 
        waveplateLabel = Qt.QLabel("Waveplate")
        layout.addWidget(waveplateLabel, 3, 0)
        waveplateInd = TaurusLabel()
        waveplateInd.setModel('thindisk/agilisagp/power/position')
        waveplateInd.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        waveplateInd.setFixedWidth(200)
        waveplateInd.setFormat('{:3.1f}')
        layout.addWidget(waveplateInd, 3, 1)

        # TDL & TiSa Energy 
        tdlEnergyLabel = Qt.QLabel("Energy")
        layout.addWidget(tdlEnergyLabel, 4, 0)
        tdlEnergyInd = TaurusLabel()
        tdlEnergyInd.setModel('thindisk/coherentpem/energymax/value')
        tdlEnergyInd.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        tdlEnergyInd.setFixedWidth(200)
        layout.addWidget(tdlEnergyInd, 4, 1)

        tisaEnergyLabel = Qt.QLabel("Power")
        layout.addWidget(tisaEnergyLabel, 4, 2)
        tisaEnergyInd = TaurusLabel()
        tisaEnergyInd.setModel('thindisk/thorlabspm100/regen/power')
        tisaEnergyInd.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        tisaEnergyInd.setFixedWidth(200)
        layout.addWidget(tisaEnergyInd, 4, 3)

        # Trends at the bottom
        tdlTrend = TaurusTrend()
        tdlTrend.setModel(['thindisk/coherentpem/energymax/value'])
        tdlTrend.setBackground('#222222')
        tdlTrend.setMaxDataBufferSize(1000)
        layout.addWidget(tdlTrend, 5, 0, 1, 2)  # row 5, spans 2 columns

        tisaTrend = TaurusTrend()
        tisaTrend.setModel(['thindisk/thorlabspm100/regen/power'])
        tisaTrend.setBackground('#222222ff')
        tisaTrend.setMaxDataBufferSize(1000)
        layout.addWidget(tisaTrend, 5, 2, 1, 2)  # row 5, spans 2 columns