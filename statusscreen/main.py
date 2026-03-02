# main.py

import sys
from taurus.qt.qtgui.application import TaurusApplication
from core.window import BaseWindow
from core.utils import load_yaml


if __name__ == '__main__':
    # load lab specific config and position specific configs
    lab_config = load_yaml('configs/sxr.yaml')
    screen_config = load_yaml('configs/sxr_control.yaml')
    
    # start application
    app_name = lab_config['app_name']
    app = TaurusApplication(sys.argv, cmd_line_parser=None, app_name=app_name)
    window = BaseWindow(lab_config, screen_config)
    window.show()
    sys.exit(app.exec_())