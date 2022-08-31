"""
B00 gui for room-temp NV experiment control

dates: somme date in July -> 083022

Author: MDA

What it does:
    1. print hello
    2. have buttons

What it needs to do:
    1. XY scanning
    2. XZ scanning
    3. YZ scanning
    4. dataset option saving
    5. include scanning parameters / save somehow
"""

#################################################################### imports ###################################################################################
import sys
import nidaqmx
import numpy
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtgraph.Qt import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from xy_scan_file import *
import time

################################################### MatPlotLib class ######################################################################################
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent = None, width = 100, height = 100, dpi = 100):
        fig = Figure(figsize = (width, height), dpi = dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

########################################################################## "Parent" class #####################################################################
class Parent(QtWidgets.QMainWindow):

    # ?
    def __init__(self, parent = None):
        super().__init__(parent)

        ######################################################################### prelims ##############################################################################

        # setting up GUI window
        self.child_widget = Child(parent = self)
        self.setCentralWidget(self.child_widget)
        self.setGeometry(300, 100, 800, 500) # x-coord, y-coord, width, height
        self.setMinimumSize(800, 500)
        self.setWindowTitle("mda_b00_gui")

        ################################################################### menu bar #############################################################################
        menu_bar = self.menuBar() # create the menu bar
        
        one_menu = menu_bar.addMenu("one")
        one_sub1 = QtWidgets.QAction("sub1", self)
        one_menu.addAction(one_sub1)
        one_sub2 = QtWidgets.QAction("sub2", self)
        one_menu.addAction(one_sub2)
        one_sub3 = QtWidgets.QAction("sub3", self)
        one_menu.addAction(one_sub3)
        
        two_menu = menu_bar.addMenu("two")
        two_sub1 = QtWidgets.QAction("sub1", self)
        two_menu.addAction(two_sub1)
        
        three_menu = menu_bar.addMenu("three")
        three_sub1 = QtWidgets.QAction("sub1", self)
        three_menu.addAction(three_sub1)
        
        four_menu = menu_bar.addMenu("four")
        four_sub1 = QtWidgets.QAction("sub1", self)
        four_menu.addAction(four_sub1)

############################################################################# "Chid" class #######################################################################
class Child(QtWidgets.QWidget):#, **kwargs): # kwargs needed?

    # ?
    def __init__(self, parent = None):#, **kwargs): # kwargs needed?
        super().__init__(parent)
        hbox = QHBoxLayout(self)
        plotwin = pg.GraphicsLayoutWidget(show = True)

        ########################################################## functions ################################################################################

        def update_plot():
            # print("update_call called")
            # print(self.x_data)
            self.sc.axes.cla()
            self.x_data = numpy.random.randint(9, size = 5)
            self.y_data = numpy.random.randint(9, size = 5)
            self.sc.axes.plot(self.x_data, self.y_data)
            self.sc.draw()

        def button_1_clicked(self, parent = Child):
            # print("button 1 clicked")
            update_plot()
        
        def scan_update():                                          # use this for demo
            self.sc.axes.cla()
            output_data_set = numpy.load("file_name_by_time.npy")
            self.sc.axes.pcolormesh(output_data_set, cmap = "RdBu_r")
            self.sc.draw()

        def button_clicked_print_hello_fnc(self, parent = Child):
            print("Hello world!")

        ############################################################# left window #####################################################################
        left_window = QFrame(self)
        left_window.setFrameShape(QFrame.StyledPanel)
        left_window.setFixedSize(435, 460)

        ############################################################### right window ###################################################################
        right_window = QFrame(self)
        right_window.setFrameShape(QFrame.StyledPanel)
        right_window.setFixedSize(335, 460)

        ##################################################### plot ##################################################################

        self.sc = MplCanvas(self, width = 3.25, height = 3.25, dpi = 102)
        self.sc.move(2, 2)
        self.sc.setParent(right_window)
        self.x_data = numpy.random.randint(9, size = 5)
        self.y_data = numpy.random.randint(9, size = 5)
        # self.z_data = numpy.random.randint(9, size = 5)
        self.sc.axes.plot(self.x_data, self.y_data)
        self.sc.axes.set_title("plot_title_here", fontsize = 8)
        self.sc.axes.set_xlabel("plot_x_label_here", fontsize = 8)
        self.sc.axes.set_ylabel("plot_y_label_here", fontsize = 8)

        # data_set = numpy.load("082422_faster_scan_03.npy")
        # self.sc.axes.pcolormesh(data_set, cmap = "RdBu_r")
        # self.sc.axes.colorbar(plot_1, ax = self.sc.axes)
        # self.sc.axes.colorbar(plot_1)

        ############################################################# split left and right windows #########################################################
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(left_window)
        splitter1.addWidget(right_window)
        hbox.addWidget(splitter1) # set layout and show window
        self.setLayout(hbox)
        self.show()

        ############################################################# scanning (XY, XZ, & YZ) section ############################################################################
        
        ##################################### overall ####################################

        # scan widgets overall "Scanning"
        scan_widget_overall = QLabel("Scanning options:")
        scan_widget_overall.setParent(left_window)
        scan_widget_overall.move(80, 10)

        indiv_scan_labels_y_height = 25

        ###################################### XY scanning #################################

        # XY scan
        xy_scan_label_widget = QLabel("XY scan", self) # widget
        xy_scan_label_widget.setParent(left_window)
        xy_scan_label_widget.move(15, indiv_scan_labels_y_height)

        # resolution
        xy_scan_resolution_widget = QLabel("Res:", self) # widget
        xy_scan_resolution_widget.setParent(left_window)
        xy_scan_resolution_widget.move(5, 40)

        xy_scan_resolution_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_resolution_qlineedit.setParent(left_window)
        xy_scan_resolution_qlineedit.move(30, 40)
        xy_scan_resolution_qlineedit.resize(30, 15)

        # read time
        xy_scan_read_time_widget = QLabel("APD_t:", self) # widget
        xy_scan_read_time_widget.setParent(left_window)
        xy_scan_read_time_widget.move(5, 65)

        xy_scan_read_time_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_read_time_qlineedit.setParent(left_window)
        xy_scan_read_time_qlineedit.move(40, 65)
        xy_scan_read_time_qlineedit.resize(30, 15)
        
        # x voltage (min and max)
        xy_scan_x_voltage_min_widget = QLabel("x_V_min:", self) # widget
        xy_scan_x_voltage_min_widget.setParent(left_window)
        xy_scan_x_voltage_min_widget.move(5, 90)

        xy_scan_x_voltage_min_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_x_voltage_min_qlineedit.setParent(left_window)
        xy_scan_x_voltage_min_qlineedit.move(50, 90)
        xy_scan_x_voltage_min_qlineedit.resize(30, 15)

        xy_scan_x_voltage_max_widget = QLabel("x_V_max:", self) # widget
        xy_scan_x_voltage_max_widget.setParent(left_window)
        xy_scan_x_voltage_max_widget.move(5, 115)

        xy_scan_x_voltage_max_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_x_voltage_max_qlineedit.setParent(left_window)
        xy_scan_x_voltage_max_qlineedit.move(55, 115)
        xy_scan_x_voltage_max_qlineedit.resize(30, 15)

        # y voltage (min and max)
        xy_scan_y_voltage_min_widget = QLabel("y_V_min:", self) # widget
        xy_scan_y_voltage_min_widget.setParent(left_window)
        xy_scan_y_voltage_min_widget.move(5, 140)

        xy_scan_y_voltage_min_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_y_voltage_min_qlineedit.setParent(left_window)
        xy_scan_y_voltage_min_qlineedit.move(50, 140)
        xy_scan_y_voltage_min_qlineedit.resize(30, 15)

        xy_scan_y_voltage_max_widget = QLabel("y_V_max:", self) # widget
        xy_scan_y_voltage_max_widget.setParent(left_window)
        xy_scan_y_voltage_max_widget.move(5, 165)

        xy_scan_y_voltage_max_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_y_voltage_max_qlineedit.setParent(left_window)
        xy_scan_y_voltage_max_qlineedit.move(55, 165)
        xy_scan_y_voltage_max_qlineedit.resize(30, 15)
        
        # z piezo
        xy_scan_z_piezo_voltage_widget = QLabel("z_V:", self) # widget
        xy_scan_z_piezo_voltage_widget.setParent(left_window)
        xy_scan_z_piezo_voltage_widget.move(5, 190)

        xy_scan_z_piezo_voltage_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_z_piezo_voltage_qlineedit.setParent(left_window)
        xy_scan_z_piezo_voltage_qlineedit.move(55, 190)
        xy_scan_z_piezo_voltage_qlineedit.resize(30, 15)

        # run xy scan button
        xy_scan_run_button = QPushButton("run\nXY scan", self)
        xy_scan_run_button.resize(80, 40)
        xy_scan_run_button.move(15, 220)
        xy_scan_run_button.clicked.connect(button_clicked_print_hello_fnc)

        ####################################### XZ scanning ###################################

        # scan widget 2 "XZ"
        scan_widget_2 = QLabel("XZ scan", self)
        scan_widget_2.setParent(left_window)
        scan_widget_2.move(95, indiv_scan_labels_y_height)

        ####################################### YZ scanning #################################

        # scan widget 3 "YZ"
        scan_widget_3 = QLabel("YZ scan", self)
        scan_widget_3.setParent(left_window)
        scan_widget_3.move(165, indiv_scan_labels_y_height)

        ############################################################## buttons ##############################################################################

        # button1
        button1 = QPushButton("change plot (basic)", self)
        button1.resize(100, 25)
        button1.move(280, 25)
        button1.clicked.connect(button_1_clicked)

####################################################################### context menu ######################################################################

    # context (right-click) menu
    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        cmenuoneAct = cmenu.addAction("one")
        cmenutwoAct = cmenu.addAction("two")
        cmenuthreeAct = cmenu.addAction("three")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

############################################################## start gui ################################################################################

# ?
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = Parent()
    mw.show()
    sys.exit(app.exec_())

#################################################################### END #######################################################################################

# issues
"""
1. leftwindow fixed sized presents window scaling prob
2. multiple context menus appear over plot
"""
    
# comments/questions
"""
1.
"""

################################################################## old useful code ##########################################################################
# # combo select box 1
# combobox1 = QComboBox(self)
# combobox1.move(12, 30)
# combobox1.resize(98, 20)
# combobox1.addItem("one")
# combobox1.addItem("two")
# combobox1.addItem("three")

# # line edit 1
# qle1 = QLineEdit(self)
# qle1.move(12, 52)
# qle1.resize(395, 20)

# # creating progress bar
# pbar = QProgressBar(self)
# # pbar.resize(80, 25)
# pbar.move(160, 250)


# def scan_update(self, parent = Child):
#     self.x_data = numpy.random.randint(9, size = 5)
#     self.y_data = numpy.random.randint(9, size = 5)
#     self.sc.axes.cla()
#     self.sc.axes.plot(self.x_data, self.y_data)
#     self.sc.draw()

# def button_2_clicked(self, parent = Child):                   # use this for demo
#     # print("button 2 clicked")
#     xy_scan_function()
#     sleep(0.75)
#     scan_update()

# rightwindow.label = QLabel(rightwindow)
# rightwindow.pixmap = QPixmap("082422_img_1.png")
# rightwindow.label.setPixmap(rightwindow.pixmap)
# rightwindow.label.resize(300, 300) # other width, height: rightwindow.pixmap.width(), rightwindow.pixmap.height()
