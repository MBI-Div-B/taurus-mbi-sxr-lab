import sys
from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.panel import TaurusForm
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.qt.qtgui.button import TaurusCommandButton
from taurus.qt.qtgui.input import TaurusValueSpinBox, TaurusValueLineEdit, TaurusValueCheckBox
from taurus.core.util.colors import DEVICE_STATE_DATA
from taurus.qt.qtgui.compact.basicswitcher import TaurusLabelEditRW, TaurusBoolRW
import taurus
from pathlib import Path

door = 'Door/qttesting/1'
macroserver = 'Macroserver/qttesting/1'

motors = [
    "motor/motctrl01/1",
    "motor/motctrl01/2",
    "motor/motctrl01/3",
    "motor/motctrl01/4",
    ]
counters = [
    "expchan/ctctrl01/1",
    "expchan/ctctrl01/2",
    "expchan/ctctrl01/3",
    "expchan/ctctrl01/4",
    ]

def main():

    app = TaurusApplication(sys.argv, cmd_line_parser=None, app_name='sardana scattering status')
    app.setStyleSheet(Path('mbi-styles.qss').read_text())
    device_door = taurus.Device(door)
    device_macroserver = taurus.Device(macroserver)
    elements = device_macroserver.read_attribute('Elements')
    import json
    data = elements.value[1]
    jess_dict = json.loads(data)

    # Create an empty dictionary and lists for pseudomotors and controllers
    data = {}
    correctTypes=["Motor", "PseudoMotor", "CTExpChannel", "ZeroDExpChannel"]

    for dict in jess_dict["new"]:
        # If the element type is already in the data dictionary
        # and is one of the correct types
        if dict["type"] in data and dict["type"] in correctTypes:            
            data[dict["type"]].append(dict["name"])
        # If the element type is one of the correct types but not in the
        # data dictionary yet
        elif dict["type"] in correctTypes:
            data[dict["type"]] = [dict["name"]]

    # Define the layout and panels

    parent = Qt.QWidget()
    parent_layout = Qt.QVBoxLayout()
    parent_layout.setSpacing(0)
    parent_layout.setContentsMargins(0, 0, 0, 0)
    parent.setLayout(parent_layout)

    parent.setWindowTitle("Sardana scattering")
    parent.setFont(Qt.QFont('Fira Sans', 12))
    parent.setMinimumSize(1400, 800)

    ######################### header

    header = Qt.QFrame()
    header_layout = Qt.QHBoxLayout()
    header_layout.setSpacing(0)
    header_layout.setContentsMargins(10, 10, 10, 10)
    header.setLayout(header_layout)    
    parent_layout.addWidget(header)

    buttons = Qt.QFrame()
    buttons_layout = Qt.QGridLayout()    
    buttons_layout.setSpacing(0)
    buttons_layout.setContentsMargins(0, 0, 0, 0)
    buttons.setLayout(buttons_layout)
    header_layout.addWidget(buttons)

    pause = TaurusCommandButton(command='PauseMacro', icon='actions:media_playback_pause.svg', text='pause')
    resume = TaurusCommandButton(command='ResumeMacro', icon='actions:media_playback_start.svg', text='resume')    
    stop = TaurusCommandButton(command='StopMacro', icon='actions:media_playback_stop.svg', text='stop')
    abort = TaurusCommandButton(command='AbortMacro', icon='actions:stop.svg', text='abort')
    buttons_layout.addWidget(pause, 0, 0)
    buttons_layout.addWidget(resume, 0, 1)
    buttons_layout.addWidget(stop, 1, 0)
    buttons_layout.addWidget(abort, 1, 1)
    pause.setModel(door)
    resume.setModel(door)
    stop.setModel(door)
    abort.setModel(door)


    # create a form panel to show the macro status
    formPanel = Qt.QFrame()
    # formPanel.setFixedHeight(300)
    formPanelLayout = Qt.QGridLayout()
    formPanel.setLayout(formPanelLayout)

    # create a label widget to show the status
    statusLabel = TaurusLabel()
    statusLabel.setAlignment(Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter)
    statusLabel.setAutoTrim(False)
    statusLabel.setWordWrap(True)
    statusLabel.setModel(door + '/status')
    statusLabel.setFixedWidth(350)

    # create a label widget to name the status
    statusName = Qt.QLabel("Status")
    statusName.setFixedSize(40, 80)
    formPanelLayout.addWidget(statusName, 0, 0)
    formPanelLayout.addWidget(statusLabel, 0, 1)

    # create a LED widget to show the state
    stateLabel = TaurusLed()
    stateLabel.setModel(door + '/state')
    # create a label widget to name the state
    stateName = Qt.QLabel("State")
    stateName.setFixedSize(75, 50)
    formPanelLayout.addWidget(stateName, 0, 2)
    formPanelLayout.addWidget(stateLabel, 0, 3)

    # Change color status
    state_string = str(stateLabel.modelObj.rvalue)
    color_data = DEVICE_STATE_DATA[str(state_string)]
    color_str = str(color_data[1]) + ", " + str(color_data[2]) \
                + ", " + str(color_data[3])
    label_stylesheet = "QLabel { background-color: rgb(" + color_str + \
                        "); border: 2px solid rgba(255, 255, 255, 125);}"
    tooltip_stylesheet = "QToolTip { \
                        background-color: black; \
                        color: white; \
                        border: white solid 1px \
                        }"

    statusLabel.setStyleSheet(label_stylesheet + tooltip_stylesheet)

    # create a spacer widget to expand the panel
    spacer = Qt.QSpacerItem(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
    header_layout.addItem(spacer)

    # add the form panel to the grid layout
    header_layout.addWidget(formPanel)


    ##################### tab

    tab = Qt.QTabWidget()
    parent_layout.addWidget(tab)    

    page_overview = Qt.QWidget(tab)
    page_overview_layout = Qt.QGridLayout()
    page_overview.setLayout(page_overview_layout)
    
    form_tv = TaurusForm(withButtons=False)
    form_tv.setModifiableByUser(False)
    form_tv.setModel(data['Motor'] + data['PseudoMotor'])
    page_overview_layout.addWidget(form_tv, 0, 0)

    form_tv = TaurusForm(withButtons=False)
    form_tv.setModifiableByUser(False)
    form_tv.setModel(data['CTExpChannel'] + data['ZeroDExpChannel'])
    page_overview_layout.addWidget(form_tv, 0, 1)
    
    page_showscan = Qt.QWidget(tab)
    page_showscan_layout = Qt.QGridLayout()
    page_showscan.setLayout(page_showscan_layout)

    from sardana.taurus.qt.qtgui.extra_sardana import ScanWindow
    showscan = ScanWindow()
    showscan.plot_widget.setGroupMode('x-axis')
    showscan.setModel(door)
    page_showscan_layout.addWidget(showscan)

    page_expconf = Qt.QWidget(tab)
    page_expconf_layout = Qt.QGridLayout()
    page_expconf.setLayout(page_expconf_layout)

    from sardana.taurus.qt.qtgui.extra_sardana import ExpDescriptionEditor
    exp_conf = ExpDescriptionEditor()
    exp_conf.setModel(door)
    page_expconf_layout.addWidget(exp_conf)

    page_macroserver = Qt.QWidget(tab)
    page_macroserver_layout = Qt.QGridLayout()
    page_macroserver.setLayout(page_macroserver_layout)

    from sardana.taurus.qt.qtgui.extra_macroexecutor import DoorOutput

    door_output = DoorOutput()
    page_macroserver_layout.addWidget(door_output)

    device_door.outputUpdated.connect(door_output.onDoorOutputChanged)
    device_door.infoUpdated.connect(door_output.onDoorInfoChanged)
    device_door.warningUpdated.connect(door_output.onDoorWarningChanged)
    device_door.errorUpdated.connect(door_output.onDoorErrorChanged)
    device_door.debugUpdated.connect(door_output.onDoorDebugChanged)

    tab.addTab(page_overview, 'overview')
    tab.addTab(page_showscan, 'showscan')
    tab.addTab(page_expconf, 'expconf')
    tab.addTab(page_macroserver, 'Door output')

    parent.show()
    sys.exit(app.exec_())




def compact_attribute(address, show_label=True, highlight_status=True, inline=False):
    attr = Qt.QFrame()
    if inline==True:
        attr_format = Qt.QHBoxLayout()
    else:
        attr_format = Qt.QVBoxLayout()
    attr_format.setSpacing(0)
    attr_format.setContentsMargins(0, 0, 0, 0)
    attr.setLayout(attr_format)

    label, value = TaurusLabel(), TaurusLabel()

    label.model, label.bgRole = address+'#label', ''
    value.model = address

    if highlight_status==False:
        value.bgRole = ''

    if show_label==True:
        attr_format.addWidget(label)

    attr_format.addWidget(value)

    return attr

def compact_rw_attribute(address, show_label=True, highlight_status=True, inline=False):
    attr = Qt.QFrame()
    if inline==True:
        attr_format = Qt.QHBoxLayout()
    else:
        attr_format = Qt.QVBoxLayout()
    attr_format.setSpacing(0)
    attr_format.setContentsMargins(0, 0, 0, 0)
    attr.setLayout(attr_format)

    label, value = TaurusLabel(), TaurusLabelEditRW()

    label.model, label.bgRole = address+'#label', ''
    value.model = address

    if show_label==True:
        attr_format.addWidget(label)

    attr_format.addWidget(value)

    return attr

def switch(address):
    attr = Qt.QFrame()
    attr_format = Qt.QHBoxLayout()
    attr_format.setSpacing(0)
    attr_format.setContentsMargins(0, 0, 0, 0)
    attr.setLayout(attr_format)

    label, value = TaurusLabel(), TaurusBoolRW()

    label.model, label.bgRole = address+'#label', ''
    value.model = address

    attr_format.addWidget(value)
    attr_format.addWidget(label)

    return attr

if __name__ == "__main__": 
    main()
