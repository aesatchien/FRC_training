# pyqt example for teaching GUI development for FRC dashboard
# make sure to pip install pyqt5 pyqt5-tools

# print(f'Loading Modules ...', flush=True)
import time
from datetime import datetime
from pathlib import Path
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer  # QObject, QThread, pyqtSignal
#from PyQt5.QtWidgets import  QApplication, QTreeWidget, QTreeWidgetItem

import networktables

print(f'Initializing GUI ...', flush=True)
# trick to inherit all the UI elements from the design file  - DO NOT CODE THE LAYOUT!
class Ui(QtWidgets.QMainWindow):
    # set the root dir for the project, knowing we're one deep
    root_dir = Path('.').absolute()  # set this to be in the root, not a child, so no .parent. May need to change this.
    png_dir = root_dir / 'png'
    save_dir = root_dir / 'save'

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('example.ui', self)  # if this isn't in the directory, you got no program

        # set up network tables
        self.ntinst = networktables.NetworkTablesInstance.getDefault()
        self.servers = ["127.0.0.1", "10.24.29.2"] #  "roboRIO-2429-FRC.local"]  # need to add the USB one here
        self.ntinst.startClient(servers=self.servers)
        self.connected = self.ntinst.isConnected()
        self.sorted_tree = []  # keep a global list of all the nt addresses

        self.refresh_time = 50  # milliseconds before refreshing
        self.widget_dict = {}
        self.command_dict = {}
        self.initialize_widgets()
        #QTimer.singleShot(2000, self.initialize_widgets())  # wait 2s for NT to initialize


        # all of your setup code goes here - linking buttons to functions, etc (move to seperate funciton if too long)

        self.qaction_show_hide.triggered.connect(self.toggle_network_tables)  # show/hide networktables
        self.qaction_refresh.triggered.connect(self.refresh_tree)

        #self.qlistwidget_commands.setStyleSheet("QListView::item:selected{background-color: rgb(255,255,255);color: rgb(0,0,0);}")
        self.qlistwidget_commands.clicked.connect(self.command_list_clicked)
        self.qt_button_test.clicked.connect(self.command_list_clicked)

        #QtWidgets.QLabel.image
        #self.qlabel_hub_image.

        self.qt_tree_widget_nt.hide()

        # at the end of init, you need to show yourself
        self.show()

        # set up the refresh
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_widgets)
        self.timer.start(self.refresh_time)

        # children = [(child.objectName()) for child in self.findChildren(QtWidgets.QWidget) if child.objectName()]
        # children.sort()
        # for child in children:
        #    print(child)

    def test(self):
        pass

    def initialize_widgets(self):

        self.widget_dict = {
        'qlabel_camera_view': {'widget':self.qlabel_camera_view, 'nt':None},
        'qlabel_climber_indicator':{'widget':self.qlabel_climber_indicator, 'nt':'/SmartDashboard/climber_state'},
        'qlabel_compressor_indicator': {'widget':self.qlabel_compressor_indicator, 'nt':'/SmartDashboard/compressor_state'},
        'qlabel_indexer_indicator': {'widget':self.qlabel_indexer_indicator, 'nt':'/SmartDashboard/indexer_state'},
        'qlabel_intake_indicator': {'widget': self.qlabel_intake_indicator, 'nt': '/SmartDashboard/intake_motor_state'},
        'qlabel_intake_piston_indicator': {'widget':self.qlabel_intake_piston_indicator, 'nt':'/SmartDashboard/intake_extended'},
        'qlabel_long_arm_indicator': {'widget':self.qlabel_long_arm_indicator, 'nt':'/SmartDashboard/climber_long_arm'},
        'qlabel_shooter_indicator': {'widget':self.qlabel_shooter_indicator, 'nt':'/SmartDashboard/shooter_state'},
        'qlabel_shooter_speed_indicator': {'widget':self.qlabel_shooter_speed_indicator, 'nt':'/SmartDashboard/shooter_ready'},
        'qlabel_short_arm_indicator': {'widget':self.qlabel_short_arm_indicator, 'nt':'/SmartDashboard/climber_short_arm'},
        'qlcd_climber_current': {'widget':self.qlcd_climber_current, 'nt':'/SmartDashboard/climber_current'},
        'qlcd_shooter_rpm': {'widget':self.qlcd_shooter_rpm, 'nt':'/SmartDashboard/shooter_rpm'}
        }

        # get all the entries
        for key, d in self.widget_dict.items():
            if d['nt'] is not None:
                d.update({'entry':self.ntinst.getEntry(d['nt'])})
            else:
                d.update({'entry': None})
            # print(key, d)

    def update_widgets(self):
        """ Main function which is looped to update the GUI with NT values"""
        for key, d in self.widget_dict.items():
            if d['entry'] is not None:
                if 'indicator' in key:
                    #  print(f'Indicator: {key}')
                    style_on = "border: 7px; border-radius: 7px; background-color:rgb(80, 235, 0); color:rgb(0, 0, 0);"
                    style_off = "border: 7px; border-radius: 7px; background-color:rgb(220, 0, 0); color:rgb(200, 200, 200);"
                    style = style_on if d['entry'].getBoolean(False) else style_off
                    d['widget'].setStyleSheet(style)
                elif 'lcd' in key:
                    #  print(f'LCD: {key}')
                    value = int(d['entry'].getDouble(0))
                    d['widget'].display(str(value))
                else:
                    pass
                    # print(f'Skipping: {key}')

        green = QtGui.QColor(227, 255, 227)
        white = QtGui.QColor(255, 255, 255)
        for ix, (key, d) in enumerate(self.command_dict.items()):
            bg_color = green if d['entry'].getBoolean(True) else white
            self.qlistwidget_commands.item(ix).setBackground(bg_color)


        x0, y0 = self.qlabel_ball.x(),  self.qlabel_ball.y()
        self.qlabel_ball.move((x0 + 5) % 500, (y0 + 5) % 380)

    def command_list_clicked(self, item):
        # shortcut where we click the command list, fire off (or end) the command
        cell_content = item.data()
        toggled_state = not self.command_dict[cell_content]['entry'].getBoolean(True)
        print(f'You clicked {cell_content} which is currently {not toggled_state}.  Firing command...')
        self.command_dict[cell_content]['entry'].setBoolean(toggled_state)

    def toggle_network_tables(self):
        # tree = QtWidgets.QTreeWidget
        if self.qt_tree_widget_nt.isHidden():
            self.refresh_tree()
            self.qt_tree_widget_nt.show()
        else:
            self.qt_tree_widget_nt.hide()

    def report_nt_status(self):
        id, ip = self.ntinst.getConnections()[0].remote_id, self.ntinst.getConnections()[0].remote_ip
        self.qt_text_status.appendPlainText(f'{datetime.today().strftime("%H:%M:%S")}: NT status: id={id}, ip={ip}')

    def refresh_tree(self):
        self.connected = self.ntinst.isConnected()
        if self.connected:
            self.report_nt_status()
            self.qt_tree_widget_nt.clear()
            entries = self.ntinst.getEntries('/', types=0)
            self.sorted_tree = sorted([e.getName() for e in entries])


            # generate the dictionary - some magic I found on the internet
            nt_dict = {}
            levels = [s[1:].split('/') for s in self.sorted_tree]
            for path in levels:
                current_level = nt_dict
                for part in path:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]

            ages = []

            self.qlistwidget_commands.clear()
            for item in self.sorted_tree:
                if 'running' in item:  # quick test of the list view for commands
                    # print(f'Command found: {item}')
                    command_name = item.split('/')[2]
                    self.qlistwidget_commands.addItem(command_name)
                    self.command_dict.update({command_name: {'nt':item, 'entry': self.ntinst.getEntry(item)}})

                entry_value = self.ntinst.getEntry(item).getValue()
                value = entry_value.value()
                age = int(time.time() - entry_value.last_change()/1E6)
                levels = item[1:].split('/')
                if len(levels) == 2:
                    nt_dict[levels[0]][levels[1]] = value, age
                elif len(levels) == 3:
                    nt_dict[levels[0]][levels[1]][levels[2]] = value, age
                elif len(levels) == 4:
                    nt_dict[levels[0]][levels[1]][levels[2]][levels[3]] = value, age

            self.fill_item(self.qt_tree_widget_nt.invisibleRootItem(), nt_dict)
            self.qt_tree_widget_nt.resizeColumnToContents(0)
            self.qt_tree_widget_nt.setColumnWidth(1, 60)
        else:
            self.qt_text_status.appendPlainText(f'{datetime.today().strftime("%H:%M:%S")}: Unable to connect to server')

    def depth(self, d):
        if isinstance(d, dict):
            return 1 + (max(map(self.depth, d.values())) if d else 0)
        return 0

    ## helper functions for filling the NT tree widget
    def fill_item(self, widget, value):
        if value is None:
            # keep recursing until nothing is passed
            return
        elif isinstance(value, dict) and self.depth(value) > 1:
            for key, val in sorted(value.items()):
                self.new_item(parent=widget, text=str(key), val=val)
        elif isinstance(value, dict):
            # now we actually add the bottom level item
            #self.new_item(parent=widget, text=str(value))
            for key, val in sorted(value.items()):
                child = QtWidgets.QTreeWidgetItem([str(key), str(val[0]), str(val[1])])
                self.fill_item(child, val)
                widget.addChild(child)
        else:
            pass

    def new_item(self, parent, text, val=None):
        if val is None:
            child = QtWidgets.QTreeWidgetItem([text, 'noval'])
        else:
            if isinstance(val,dict):
                child = QtWidgets.QTreeWidgetItem([text])
            else:
                child = QtWidgets.QTreeWidgetItem([text, str(val[0]), str(val[1])])
        self.fill_item(child, val)
        parent.addChild(child)
        child.setExpanded(True)



# -------------------  MAIN --------------------------
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # compensate for dpi scaling way up above with the setAttribute calls - don't really need this now
    screen = app.screens()[0]
    dpi_logical = int(screen.logicalDotsPerInchX())
    if dpi_logical > 96:  # 150% scaling on AVIT North, vs 96 for unscaled
        print(f"We're on a scaled screen: logical dpi is {dpi_logical}")
    else:
        print(f"We're not on a scaled screen: logical dpi is {dpi_logical}")

    ui = Ui()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Still has garbage collection issues. Closing.')
