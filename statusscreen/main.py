# main.py

import sys
from taurus.qt.qtgui.application import TaurusApplication
from core.window import BaseWindow
# from core.utils import load_yaml


if __name__ == '__main__':
    # load lab specific config and position specific configs
    
    # lab_config = load_yaml('configs/sxr.yaml')
    # position_config = load_yaml('configs/sxr_control.yaml')
    
    # start application
    app = TaurusApplication(sys.argv, cmd_line_parser=None, app_name='SXR Lab Status')
    # window = BaseWindow(lab_config, position_config)
    window = BaseWindow()
    window.show()
    sys.exit(app.exec_())