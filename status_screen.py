#!/usr/bin/python3 -u
# coding: utf8

import sys
from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from pathlib import Path
from PyQt5 import QtSvg

from taurus_pyqtgraph import TaurusTrend


class StatusScreen(Qt.QMainWindow):
    def __init__(self,parent=None):
        super(StatusScreen, self).__init__(parent)
        self.setWindowTitle('SXR Lab Status')
        self.setWindowIcon(Qt.QIcon('mbi-logo.png'))
        self.setMinimumSize(1400, 800)    
        Qt.QFontDatabase.addApplicationFont('./resources/FiraSans-Regular.tff')    
        self.setStyleSheet(Path(Path(__file__).parent / 'mbi-styles.qss').read_text())
        
        ### header
        # title
        title = Qt.QLabel("SXR Lab Status")
        title.setFont(Qt.QFont('Fira Sans', 40))
        title.setObjectName("title")
        title.setFixedWidth(450)
        # clock
        self.clock = Qt.QLabel('dddd yyyy-MM-dd - hh:mm:ss')
        self.clock.setObjectName("titlelight")
        self.clock.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        # connect timer for clock
        self.timer=Qt.QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        # logo 
        svgWidget = QtSvg.QSvgWidget('resources/mbi-logo.svg')
        svgWidget.setFixedWidth(100)
        svgWidget.setFixedHeight(68)

        headerWidget = Qt.QWidget(self)
        headerLayout = Qt.QHBoxLayout(headerWidget)

        headerLayout.addWidget(title)
        headerLayout.addWidget(self.clock)
        headerLayout.addWidget(svgWidget)

        ### environment vacuum

        # environment
        envWidget = Qt.QWidget(self)
        envLayout = Qt.QGridLayout(envWidget)
        envLayout.setAlignment(Qt.Qt.AlignTop)

        envLabel = Qt.QLabel('Environment')
        envLabel.setObjectName('header')
        envLayout.addWidget(envLabel, 0, 0)

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
            t = TaurusLabel()            
            t.setModel(s[1] + '/temperature')
            t.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
            # h = TaurusLabel()            
            # h.setModel(s[1] + '/humidity')
            # h.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)

            l = Qt.QLabel(s[0])
            l.setAlignment(Qt.Qt.AlignRight)
            envLayout.addWidget(l, s[2][0], s[2][1])
            envLayout.addWidget(t, s[2][0], s[2][1]+1)
            # envLayout.addWidget(h, s[2][0], s[2][1]+2)


        # vacuum
        vacWidget = Qt.QWidget(self)
        vacLayout = Qt.QGridLayout(vacWidget)
        vacLayout.setAlignment(Qt.Qt.AlignTop)

        vacLabel = Qt.QLabel('Vacuum')
        vacLabel.setObjectName('header')
        vacLayout.addWidget(vacLabel, 0, 0)

        vacLabel = Qt.QLabel('RSXS')
        #vacLabel.setObjectName('header')
        vacLayout.addWidget(vacLabel, 0, 2)

        vacLabel = Qt.QLabel('Spectroscopy')
        #vacLabel.setObjectName('header')
        vacLayout.addWidget(vacLabel, 0, 4)

        gauges = [
            ['PXS', 'sxr/tpg261/pxs', (1, 0)],
            ['RZP', 'rsxs/tpg261/rzp', (1, 2)],
            ['Scattering', 'rsxs/tpg261/scattering', (2, 2)],
            ['Optics', 'spec/tpg261/optic', (1, 4)],
            ['CCD', 'spec/tpg261/ccd', (2, 4)],
                  ]  
        
        for g in gauges:
            w = TaurusLabel()            
            w.setModel(g[1] + '/pressure')
            w.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
            w.setFormat('{:3.1e}')
            w.setMinimumWidth(200)

            l = Qt.QLabel(g[0])
            l.setAlignment(Qt.Qt.AlignRight)
            vacLayout.addWidget(l, g[2][0], g[2][1])
            vacLayout.addWidget(w, g[2][0], g[2][1]+1)

        #

        envvacWidget = Qt.QWidget(self)
        envvacLayout = Qt.QHBoxLayout(envvacWidget)
        envvacLayout.addWidget(envWidget)
        envvacLayout.addItem(Qt.QSpacerItem(20, 40, Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum))
        envvacLayout.addWidget(vacWidget)
        envvacLayout.setAlignment(Qt.Qt.AlignTop)

        ### laser

        laserLabel = Qt.QLabel('Laser Interlock')
        laserLabel.setObjectName('header')
        # Door Interlock
        ledDoor = TaurusLed()
        ledDoor.setOnColor("red")
        ledDoor.setOffColor("green")
        ledDoor.model = 'lab/rpigpio/laserpi/door_tisa'
        ledDoor.setAlignment(Qt.Qt.AlignLeft)
        ledDoor.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)

        # TDL
        tdlLabel = Qt.QLabel("Thin Disk Laser")
        tdlLabel.setObjectName('header')

        ledShutterTDL= TaurusLed()
        ledShutterTDL.setOnColor("red")
        ledShutterTDL.setOffColor("green")
        ledShutterTDL.model = 'lab/rpigpio/laserpi/shutter_tdl'
        ledShutterTDL.setAlignment(Qt.Qt.AlignLeft)
        ledShutterTDL.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)

        SC10shutterLabel = Qt.QLabel('Shutter')
        #SC10shutterLabel.setAlignment(Qt.Qt.AlignRight)
        ledSC10shutter = TaurusLed()
        ledSC10shutter.setOnColor("red")
        ledSC10shutter.setOffColor("green")
        ledSC10shutter.model = 'thindisk/thorlabssc10/seed/open'
        ledSC10shutter.setAlignment(Qt.Qt.AlignLeft)

        waveplateLabel = Qt.QLabel("Waveplate")
        #waveplateLabel.setAlignment(Qt.Qt.AlignRight)
        waveplateInd = TaurusLabel()
        waveplateInd.setModel('thindisk/agilisagp/power/position')
        waveplateInd.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        waveplateInd.setFixedWidth(200)
        waveplateInd.setFormat('{:3.1f}')

        tdlEnergyLabel = Qt.QLabel("Energy")
        #tdlEnergyLabel.setAlignment(Qt.Qt.AlignRight)
        tdlEnergyInd = TaurusLabel()            
        tdlEnergyInd.setModel('thindisk/coherentpem/energymax/value')
        tdlEnergyInd.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        tdlEnergyInd.setFixedWidth(200)

        tdlTrend = TaurusTrend()
        tdlTrend.setModel(['thindisk/coherentpem/energymax/value'])
        tdlTrend.setBackground(background='#222222')
        tdlTrend.setMaxDataBufferSize(1000)
        #tdlTrend.setForcedReadingPeriod(500)

        # TiSa
        tisaLabel = Qt.QLabel("TiSa Laser")
        tisaLabel.setObjectName('header')

        ledShutterTiSa = TaurusLed()
        ledShutterTiSa.setOnColor("red")
        ledShutterTiSa.setOffColor("green")
        ledShutterTiSa.model = 'lab/rpigpio/laserpi/shutter_tisa'
        ledShutterTiSa.setAlignment(Qt.Qt.AlignLeft)
        ledShutterTiSa.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)

        
        tisaEnergyLabel = Qt.QLabel("Energy")
        #tisaEnergyLabel.setAlignment(Qt.Qt.AlignRight)
        tisaEnergyInd = TaurusLabel()            
        tisaEnergyInd.setModel('tisa/coherentlabmaxtop/compressor/value')
        tisaEnergyInd.setAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        tisaEnergyInd.setFixedWidth(200)

        tisaTrend = TaurusTrend()
        tisaTrend.setModel(['tisa/coherentlabmaxtop/compressor/value'])
        tisaTrend.setBackground(background='#222222ff')
        tisaTrend.setMaxDataBufferSize(1000)
        #tisaTrend.setForcedReadingPeriod(500)

        #  

        laserWidget = Qt.QWidget(self)
        laserLayout = Qt.QGridLayout(laserWidget)

        laserLayout.addWidget(laserLabel, 0, 0)
        laserLayout.addWidget(ledDoor, 0, 1, 1, 3)

        laserLayout.addWidget(tdlLabel, 1, 0)
        laserLayout.addWidget(ledShutterTDL, 1, 1)    
        laserLayout.addWidget(tisaLabel, 1, 2)
        laserLayout.addWidget(ledShutterTiSa, 1, 3)   
    
        laserLayout.addWidget(SC10shutterLabel, 2, 0)
        laserLayout.addWidget(ledSC10shutter, 2, 1)   
        
        laserLayout.addWidget(waveplateLabel, 3, 0)
        laserLayout.addWidget(waveplateInd, 3, 1)   

        laserLayout.addWidget(tdlEnergyLabel, 4, 0)
        laserLayout.addWidget(tdlEnergyInd, 4, 1)    
        laserLayout.addWidget(tisaEnergyLabel, 4, 2)
        laserLayout.addWidget(tisaEnergyInd, 4, 3)
        laserLayout.addWidget(tdlTrend, 5, 0, 1, 2)
        laserLayout.addWidget(tisaTrend, 5, 2, 1, 2)

        ### central
        centralWidget = Qt.QWidget(self)
        centralLayout = Qt.QVBoxLayout(centralWidget)
        centralLayout.addWidget(headerWidget)
        centralLayout.addWidget(envvacWidget)
        centralLayout.addWidget(laserWidget)

        centralLayout.setAlignment(Qt.Qt.AlignTop)


        # Set the central widget of the Window.
        self.setCentralWidget(centralWidget)
        
    def showTime(self):
        current_time=Qt.QDateTime.currentDateTime()
        formatted_time=current_time.toString('dddd dd.MM.yyyy - hh:mm:ss')
        self.clock.setText(formatted_time)


if __name__ == '__main__':
    app = TaurusApplication(sys.argv, cmd_line_parser=None, app_name='SXR Lab Status')
    window = StatusScreen()
    window.show()
    sys.exit(app.exec_())
