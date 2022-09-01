"""
B00 gui for room-temp NV experiment control

dates: somme date in July -> 083122

Author: MDA

What it does:                                       last updated: 083022
    1. print hello
    2. have buttons

What it needs to do:                                       last updated: 083022
    1. XY scanning
    2. XZ scanning
    3. YZ scanning
    4. dataset option saving
    5. include scanning parameters / save somehow
"""

# TODO: remove unused imports
# TODO: update naming conventions throughout scripts and entire file

#################################################################### imports ###################################################################################
import sys
import nidaqmx
import numpy
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import time

# packages 083122 start
import qcodes as qc
import nidaqmx
import os
from time import sleep
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

# import qcodes contrib_drivers NI package (all)
from qcodes_contrib_drivers.drivers.NationalInstruments.DAQ import *
from qcodes_contrib_drivers.drivers.NationalInstruments.class_file import *

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

############### globals ##############
any_script_run_one_Q = False

################################################### MatPlotLib class ######################################################################################
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent = None, width = 10, height = 10, dpi = 1000):
        # fig = Figure(figsize = (width, height), dpi = dpi)
        # self.axes = fig.add_subplot()
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi, tight_layout = True)
        super(MplCanvas, self).__init__(self.fig)

########################################################################## "Parent" class #####################################################################
class Parent(QtWidgets.QMainWindow):

    # ?
    def __init__(self, parent = None):
        super().__init__(parent)

        ######################################################################### prelims ##############################################################################

        # setting up GUI window
        self.child_widget = Child(parent = self)
        self.setCentralWidget(self.child_widget)
        gui_window_height = 440
        gui_window_width = 800
        self.setGeometry(300, 100, gui_window_width, gui_window_height) # x-coord, y-coord, width, height
        self.setMinimumSize(gui_window_width, gui_window_height) # window min size
        self.setMaximumSize(gui_window_width, gui_window_height) # window max size
        self.setWindowTitle("mda_b00_gui")

        ################################################################### menu bar #############################################################################
        menu_bar = self.menuBar() # create the menu bar
        
        one_menu = menu_bar.addMenu("File")
        one_sub1 = QtWidgets.QAction("sub1", self)
        one_menu.addAction(one_sub1)
        one_sub2 = QtWidgets.QAction("sub2", self)
        one_menu.addAction(one_sub2)
        one_sub3 = QtWidgets.QAction("sub3", self)
        one_menu.addAction(one_sub3)
        
        two_menu = menu_bar.addMenu("Help")
        two_sub1 = QtWidgets.QAction("sub1", self)
        two_menu.addAction(two_sub1)

        about_menu = menu_bar.addMenu("About")
        # about_menu_info = QtWidgets.QAction("sub1", self)
        about_menu_info = QtWidgets.QAction("GUI-based control for the room-temp NV center measurement setup", self)
        about_menu.addAction(about_menu_info)

############################################################################# "Chid" class #######################################################################
class Child(QtWidgets.QWidget):#, **kwargs): # kwargs needed?

    # ?
    def __init__(self, parent = None):#, **kwargs): # kwargs needed?
        super().__init__(parent)
        hbox = QHBoxLayout(self)
        plotwin = pg.GraphicsLayoutWidget(show = True)

        ########################################################## CHILD functions ################################################################################
        
        # print_XY_scan_parameters_fnc
        def print_XY_scan_parameters_fnc(self, parent = Child): # this fnc does...
            print("XY_SCAN PARAMETERS/INFO: ", end = "")
            print("XY_scan resolution = %d, " % int(xy_scan_resolution_qlineedit.text()), end = "")
            print("XY_scan counter read time = %2f, " % round(float(xy_scan_read_time_qlineedit.text()), 2), end = "")
            print("XY_scan min x driving voltage = %2f, " % float(xy_scan_x_voltage_min_qlineedit.text()), end = "")
            print("XY_scan max x driving voltage = %2f, " % float(xy_scan_x_voltage_max_qlineedit.text()), end = "")
            print("XY_scan min y driving voltage = %2f, " % float(xy_scan_y_voltage_min_qlineedit.text()), end = "")
            print("XY_scan max y driving voltage = %2f, " % float(xy_scan_y_voltage_max_qlineedit.text()), end = "")
            print("XY_scan z-piezo driving voltage = %2f." % float(xy_scan_z_piezo_voltage_qlineedit.text()))
        
        # print_XZ_scan_parameters_fnc
        def print_XZ_scan_parameters_fnc(self, parent = Child): # this fnc does...
            print("XZ_SCAN PARAMETERS/INFO: ", end = "")
            print("XZ_scan resolution = %d, " % int(xz_scan_resolution_qlineedit.text()), end = "")
            print("XZ_scan counter read time = %2f, " % round(float(xz_scan_read_time_qlineedit.text()), 2), end = "")
            print("XZ_scan min x driving voltage = %2f, " % float(xz_scan_x_voltage_min_qlineedit.text()), end = "")
            print("XZ_scan max x driving voltage = %2f, " % float(xz_scan_x_voltage_max_qlineedit.text()), end = "")
            print("XZ_scan y driving voltage = %2f, " % float(xz_scan_y_voltage_qlineedit.text()), end = "")
            print("XZ_scan z-piezo min driving voltage = %2f, " % float(xz_scan_z_piezo_min_voltage_qlineedit.text()), end = "")
            print("XZ_scan z-piezo max driving voltage = %2f." % float(xz_scan_z_piezo_max_voltage_qlineedit.text()))
        
        # print_YZ_scan_parameters_fnc
        def print_YZ_scan_parameters_fnc(self, parent = Child): # this fnc does...
            print("YZ_SCAN PARAMETERS/INFO: ", end = "")
            print("YZ_scan resolution = %d, " % int(yz_scan_resolution_qlineedit.text()), end = "")
            print("YZ_scan counter read time = %2f, " % round(float(yz_scan_read_time_qlineedit.text()), 2), end = "")
            print("YZ_scan min Y driving voltage = %2f, " % float(yz_scan_y_voltage_min_qlineedit.text()), end = "")
            print("YZ_scan max Y driving voltage = %2f, " % float(yz_scan_y_voltage_max_qlineedit.text()), end = "")
            print("YZ_scan X driving voltage = %2f, " % float(yz_scan_x_voltage_qlineedit.text()), end = "")
            print("YZ_scan z-piezo min driving voltage = %2f, " % float(yz_scan_z_piezo_min_voltage_qlineedit.text()), end = "")
            print("YZ_scan z-piezo max driving voltage = %2f." % float(yz_scan_z_piezo_max_voltage_qlineedit.text()))

        # XY scanning function
        def run_xy_scan_fnc(): # this fnc runs the xy_scan per the user-entered parameters in the xy_scan qlineedits
            # print("xy_scan started")

            ############################################################### begin scanning script #############################################################################################
                
            ################################################################################## card 2 (AO) ########################################################################

            # naming the instrument
            scan_galvo_card_name = "cDAQ1Mod2"

            # dictionary of analog output channels
            scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

            # defining the instrument (ni_9263)
            scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

            ############################################################################### def other variables #####################################################################

            ################### setting variales and array ####################

            # counter read time:
            scan_counter_acquisition_time = float(xy_scan_read_time_qlineedit.text())                          # note a reading time <0.05 s is likely too short

            # def
            grid_size = int(xy_scan_resolution_qlineedit.text())
            grid_size_x = grid_size_y = grid_size

            # def the initial driving voltage for the x-mirror
            initial_x_driving_voltage = round(float(xy_scan_x_voltage_min_qlineedit.text()), 2)
            # def the initial driving voltage for the y-mirror
            initial_y_driving_voltage = round(float(xy_scan_y_voltage_min_qlineedit.text()), 2)

            z_piezo_set_voltage = round(float(xy_scan_z_piezo_voltage_qlineedit.text()), 2)

            # setup parameter for the program to use based on defined variables
            x_driving_voltage_to_change = initial_x_driving_voltage
            y_driving_voltage_to_change = initial_y_driving_voltage

            # set desired end mirror voltages
            desired_end_x_mirror_voltage = round(float(xy_scan_x_voltage_max_qlineedit.text()), 2)
            desired_end_y_mirror_voltage = round(float(xy_scan_y_voltage_max_qlineedit.text()), 2)

            # def the internal stepping voltages based on user-entered settings above
            x_drive_voltage_step = ((np.absolute(initial_x_driving_voltage)) + (desired_end_x_mirror_voltage)) / grid_size_x
            y_drive_voltage_step = ((np.absolute(initial_y_driving_voltage)) + (desired_end_y_mirror_voltage)) / grid_size_y

            # create dataset to populate
            xy_scan_data_array = np.zeros((grid_size_x, grid_size_y))

            # initializing variables to store read counter info.
            output_value = 0
            counter_value = 0

            ################### resetting position of mirrors ####################

            scan_galvo.voltage_cdaq1mod2ao0(initial_x_driving_voltage) # this is for the x-mirror

            scan_galvo.voltage_cdaq1mod2ao1(initial_y_driving_voltage) # this is for the y-mirror

            scan_galvo.voltage_cdaq1mod2ao2(z_piezo_set_voltage) # setting the z_piezo to z_piezo_set_voltage microns

            ########################################################### setting up NI-DAQmx tasks and channels for counting ########################################################

            with nidaqmx.Task() as task1, nidaqmx.Task() as counter_output_task: # this defines 2 NI-DAQmx tasks (one for the counter and one for the counter's clock)

                # adding dig pulse train chan
                counter_output_task.co_channels.add_co_pulse_chan_freq(
                    counter = "cDAQ1Mod1/ctr1",
                    name_to_assign_to_channel = "",
                    units = nidaqmx.constants.FrequencyUnits.HZ,
                    idle_state = nidaqmx.constants.Level.LOW,
                    initial_delay = 0.0,
                    freq = 1000,
                    duty_cycle = 0.5
                    )

                # cfg implict timing
                counter_output_task.timing.cfg_implicit_timing(
                    sample_mode = AcquisitionType.CONTINUOUS,
                    samps_per_chan = 1
                    )

                # adding count egdes chan
                task1.ci_channels.add_ci_count_edges_chan(
                    counter = "cDAQ1Mod1/ctr0",
                    name_to_assign_to_channel = "",
                    edge = nidaqmx.constants.Edge.RISING,
                    initial_count = 0,
                    count_direction = nidaqmx.constants.CountDirection.COUNT_UP
                    )

                # cfg sample clk timing
                task1.timing.cfg_samp_clk_timing(
                    rate = 1000,
                    source = "/cDAQ1/Ctr1InternalOutput",
                    active_edge = nidaqmx.constants.Edge.RISING,
                    sample_mode = AcquisitionType.CONTINUOUS,
                    samps_per_chan = 1
                    )
                
                counter_output_task.start() # this starts the counter NI-DAQmx task
                task1.start() # this starts the hardware-based internal clock NI-DAQmx task
                                
            ######################################################################## X and Y scanning #########################################################################

                for f in range(grid_size_y): # this loops for rows (y)

                    for k in range(grid_size_x): # this loops for columns (x)

                        ################## important section #################

                        for my_var_not_named_i in range(int(scan_counter_acquisition_time * 1000)): # this reads/lets the counter accumulate for the set time and returns value
                            counter_value = task1.read()
                            output_value += counter_value

                        if f % 2 != 0: # this loop populates the created xy_scan_data_array (the if else strucuture is present bc of the snaking scanning pattern)
                            xy_scan_data_array[f][((-k) + 1)] = (output_value - np.sum(xy_scan_data_array)) # add counter result to data array                           # saving (082422)
                            output_value == 0
                            counter_value == 0
                        else:
                            if f == 0 and k == 0:
                                xy_scan_data_array[0][0] = output_value # add counter result to data array                                                      # saving
                            else:
                                xy_scan_data_array[f][k] = (output_value - np.sum(xy_scan_data_array)) # add counter result to data array                               # saving (082422)
                        output_value = 0
                        counter_value = 0

                        ############# end important section ############

                        if f % 2 == 0: # this loop adjusts for sweeping back and forth along each alternating row
                            if k < (grid_size_x - 1):
                                x_driving_voltage_to_change += x_drive_voltage_step # increment drive voltage forwards
                                scan_galvo.voltage_cdaq1mod2ao0(x_driving_voltage_to_change) # step x motor
                            else:
                                break
                        else:
                            if k < (grid_size_x - 1):
                                x_driving_voltage_to_change -= x_drive_voltage_step # increment drive voltage backwards
                                scan_galvo.voltage_cdaq1mod2ao0(x_driving_voltage_to_change) # step x motor
                            else:
                                break

                    if f < (grid_size_y - 1): # this loop prevents from scanning an upper undesired row
                        y_driving_voltage_to_change += y_drive_voltage_step # increment drive voltage
                        scan_galvo.voltage_cdaq1mod2ao1(y_driving_voltage_to_change) # step y motor
                    else:
                        break

                counter_output_task.stop() # this stops the counter NI-DAQmx task - free-ing the reserved cDAQ card resources
                task1.stop() # this stops the hardware-based internal clock NI-DAQmx task - free-ing the reserved cDAQ card resources

            ############################################################### end scanning script #############################################################################################
            
            ############################################### plotting XY scan data in plot ####################################################
            self.sc.axes.cla()
            plot = self.sc.axes.pcolormesh(xy_scan_data_array, cmap = "inferno")
            # self.sc.colorbar(plot, ax = self.sc.axes)
            self.sc.axes.set_xticks(np.arange(0, grid_size + 10, grid_size / 2), [initial_x_driving_voltage, int((initial_x_driving_voltage + desired_end_x_mirror_voltage) / 2), desired_end_x_mirror_voltage])
            self.sc.axes.set_yticks(np.arange(0, grid_size + 10, grid_size / 2), [initial_y_driving_voltage, int((initial_y_driving_voltage + desired_end_y_mirror_voltage) / 2), desired_end_y_mirror_voltage])
            self.sc.axes.set_xlabel("x_mirror_driving_voltage_(V)", fontsize = 8)
            self.sc.axes.set_ylabel("y_mirror_driving_voltage_(V)", fontsize = 8)
            self.sc.axes.set_title("XY_scan_083122_z-piezo@%d_microns" % int((z_piezo_set_voltage * 10)), fontsize = 8)
            self.sc.draw()
            # print("xy_scan finished")
        
        # run XZ scan fnc
        def run_xz_scan_fnc(): # this fnc runs the xy_scan per the user-entered parameters in the xy_scan qlineedits
            # print("xz_scan started")
            ################################################################################## card 2 (AO) ########################################################################

            # naming the instrument
            scan_galvo_card_name = "cDAQ1Mod2"

            # dictionary of analog output channels
            scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

            # defining the instrument (ni_9263)
            scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

            ############################################################################### def other variables #####################################################################

            ################### setting variales and array ####################

            # counter read time:
            scan_counter_acquisition_time = float(xz_scan_read_time_qlineedit.text())                                     # note a reading time <0.05 s is likely too short

            # def grid_size of scan (resolution)
            grid_size = int(xz_scan_resolution_qlineedit.text())

            # def the initial driving voltage for the x-mirror
            initial_x_driving_voltage = float(xz_scan_x_voltage_min_qlineedit.text())
            # def the initial driving voltage for the y-mirror
            initial_y_driving_voltage = float(xz_scan_y_voltage_qlineedit.text())
            #
            initial_z_piezo_driving_voltage = float(xz_scan_z_piezo_min_voltage_qlineedit.text())

            # set desired end mirror voltages
            desired_end_x_mirror_voltage = float(xz_scan_x_voltage_max_qlineedit.text())
            desired_end_z_piezo_voltage = float(xz_scan_z_piezo_max_voltage_qlineedit.text())

            # setup parameter for the program to use based on defined variables
            x_driving_voltage_to_change = initial_x_driving_voltage
            z_piezo_driving_voltage_to_change = initial_z_piezo_driving_voltage

            # def the internal stepping voltages based on user-entered settings above
            x_drive_voltage_step = ((np.absolute(initial_x_driving_voltage)) + (desired_end_x_mirror_voltage)) / grid_size
            z_piezo_drive_voltage_step = (initial_z_piezo_driving_voltage + (desired_end_z_piezo_voltage)) / grid_size

            # create dataset to populate
            xz_scan_data_array = np.zeros((grid_size, grid_size))

            # initializing variables to store read counter info.
            output_value = 0
            counter_value = 0

            ################### resetting position of mirrors ####################

            scan_galvo.voltage_cdaq1mod2ao0(initial_x_driving_voltage) # this is for setting the initial x voltage

            scan_galvo.voltage_cdaq1mod2ao1(initial_y_driving_voltage) # this is for fixing the x-mirror at defined setting (voltage)

            scan_galvo.voltage_cdaq1mod2ao2(initial_z_piezo_driving_voltage) # starting z-piezo at 0.0 V (0 microns); this variable will increase during scanning

            ########################################################### setting up NI-DAQmx tasks and channels for counting ########################################################

            with nidaqmx.Task() as task1, nidaqmx.Task() as counter_output_task: # this defines 2 NI-DAQmx tasks (one for the counter and one for the counter's clock)

                # adding dig pulse train chan
                counter_output_task.co_channels.add_co_pulse_chan_freq(
                    counter = "cDAQ1Mod1/ctr1",
                    name_to_assign_to_channel = "",
                    units = FrequencyUnits.HZ,
                    idle_state = nidaqmx.constants.Level.LOW,
                    initial_delay = 0.0,
                    freq = 1000,
                    duty_cycle = 0.5
                    )

                # cfg implict timing
                counter_output_task.timing.cfg_implicit_timing(
                    sample_mode = AcquisitionType.CONTINUOUS,
                    samps_per_chan = 1
                    )

                # adding count egdes chan
                task1.ci_channels.add_ci_count_edges_chan(
                    counter = "cDAQ1Mod1/ctr0",
                    name_to_assign_to_channel = "",
                    edge = Edge.RISING,
                    initial_count = 0,
                    count_direction = CountDirection.COUNT_UP
                    )

                # cfg sample clk timing
                task1.timing.cfg_samp_clk_timing(
                    rate = 1000,
                    source = "/cDAQ1/Ctr1InternalOutput",
                    active_edge = Edge.RISING,
                    sample_mode = AcquisitionType.CONTINUOUS,
                    samps_per_chan = 1
                    )
                
                counter_output_task.start() # this starts the counter NI-DAQmx task
                task1.start() # this starts the hardware-based internal clock NI-DAQmx task
                        
            ####################################################################### x and z scanning #########################################################################

                for f in range(grid_size): # this loops for stacks in z

                    for k in range(grid_size): # this loops for columns (varying y voltage/setting)

                        ################## important section #################

                        for my_var_not_named_i in range(int(scan_counter_acquisition_time * 1000)): # this reads/lets the counter accumulate for the set time and returns value
                            counter_value = task1.read()
                            output_value += counter_value

                        if f % 2 != 0: # this loop populates the created xz_scan_data_array (the if else strucuture is present bc of the snaking scanning pattern)
                            xz_scan_data_array[f][((-k) + 1)] = (output_value - np.sum(xz_scan_data_array)) # add counter result to data array                           # saving (082422)
                            output_value == 0
                            counter_value == 0
                        else:
                            if f == 0 and k == 0:
                                xz_scan_data_array[0][0] = output_value # add counter result to data array                                                      # saving
                            else:
                                xz_scan_data_array[f][k] = (output_value - np.sum(xz_scan_data_array)) # add counter result to data array                               # saving (082422)
                        output_value = 0
                        counter_value = 0

                        ############# end important section ############

                        if f % 2 == 0: # this loop adjusts for sweeping back and forth along each alternating row
                            if k < (grid_size - 1):
                                x_driving_voltage_to_change += x_drive_voltage_step # increment y mirro drive voltage forwards
                                scan_galvo.voltage_cdaq1mod2ao0(x_driving_voltage_to_change) # step y mirror
                            else:
                                break
                        else:
                            if k < (grid_size - 1):
                                x_driving_voltage_to_change -= x_drive_voltage_step # increment y mirror drive voltage backwards
                                scan_galvo.voltage_cdaq1mod2ao0(x_driving_voltage_to_change) # step y mirror
                            else:
                                break

                    if f < (grid_size - 1): # this loop
                        z_piezo_driving_voltage_to_change += z_piezo_drive_voltage_step # increment drive voltage
                        scan_galvo.voltage_cdaq1mod2ao2(z_piezo_driving_voltage_to_change) # step z
                    else:
                        break

                counter_output_task.stop() # this stops the counter NI-DAQmx task - free-ing the reserved cDAQ card resources
                task1.stop() # this stops the hardware-based internal clock NI-DAQmx task - free-ing the reserved cDAQ card resources

                ############################################ end XZ scanning script #################################################

            ############################################### plotting XZ scan data in plot ####################################################
            self.sc.axes.cla()
            xz_scan_plot = self.sc.axes.pcolormesh(xz_scan_data_array, cmap = "inferno")
            # self.sc.colorbar(plot, ax = self.sc.axes)
            self.sc.axes.set_xticks(np.arange(0, grid_size + 10, grid_size / 2), [initial_x_driving_voltage, int((initial_x_driving_voltage + desired_end_x_mirror_voltage) / 2), desired_end_x_mirror_voltage])
            self.sc.axes.set_yticks(np.arange(0, grid_size + 10, grid_size / 2), [int(initial_z_piezo_driving_voltage * 10), (int(initial_z_piezo_driving_voltage * 10) + int(desired_end_z_piezo_voltage * 10)) / 2, int(desired_end_z_piezo_voltage * 10)])
            self.sc.axes.set_xlabel("x_mirror_driving_voltage_(V)", fontsize = 8)
            self.sc.axes.set_ylabel("objective_z-piezo_height_(microns)", fontsize = 8)
            self.sc.axes.set_title("XZ_scan_083122_y_voltage=%f_V" % initial_y_driving_voltage, fontsize = 8)
            self.sc.draw()
            # print("xz_scan finished")

        # YZ scan function
        def run_yz_scan_fnc(): # this fnc runs the YZ scan script
            # print("YZ scan started")
            ################################################################################## card 2 (AO) ########################################################################

            # naming the instrument
            scan_galvo_card_name = "cDAQ1Mod2"

            # dictionary of analog output channels
            scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

            # defining the instrument (ni_9263)
            scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

            ############################################################################### def other variables #####################################################################

            ################### setting variales and array ####################

            # counter read time:
            scan_counter_acquisition_time = 0.05                                                                               # note a reading time <0.05 s is likely too short

            # def
            grid_size = int(yz_scan_resolution_qlineedit.text())

            # def the initial driving voltage for the x-mirror
            initial_x_driving_voltage = float(yz_scan_x_voltage_qlineedit.text())

            # def the initial driving voltage for the y-mirror
            initial_y_driving_voltage = float(yz_scan_y_voltage_min_qlineedit.text())
            #
            initial_z_piezo_driving_voltage = float(yz_scan_z_piezo_min_voltage_qlineedit.text())

            # setup parameter for the program to use based on defined variables
            y_driving_voltage_to_change = initial_y_driving_voltage
            z_piezo_driving_voltage_to_change = initial_z_piezo_driving_voltage

            # set desired end mirror voltages
            desired_end_y_mirror_voltage = float(yz_scan_y_voltage_max_qlineedit.text())
            desired_end_z_piezo_voltage = float(yz_scan_z_piezo_max_voltage_qlineedit.text())

            # def the internal stepping voltages based on user-entered settings above
            y_drive_voltage_step = ((np.absolute(initial_y_driving_voltage)) + (desired_end_y_mirror_voltage)) / grid_size
            z_piezo_drive_voltage_step = (initial_z_piezo_driving_voltage + (desired_end_z_piezo_voltage)) / grid_size

            # create dataset to populate
            yz_scan_data_array = np.zeros((grid_size, grid_size))

            # initializing variables to store read counter info.
            output_value = 0
            counter_value = 0

            ################### resetting position of mirrors ####################

            scan_galvo.voltage_cdaq1mod2ao0(initial_x_driving_voltage) # this is for fixing the x-mirror at defined setting (voltage)

            scan_galvo.voltage_cdaq1mod2ao1(initial_y_driving_voltage) # this is for setting the initial x voltage

            scan_galvo.voltage_cdaq1mod2ao2(initial_z_piezo_driving_voltage) # starting z-piezo at 0.0 V (0 microns); this variable will increase during scanning

            ########################################################### setting up NI-DAQmx tasks and channels for counting ########################################################

            with nidaqmx.Task() as task1, nidaqmx.Task() as counter_output_task: # this defines 2 NI-DAQmx tasks (one for the counter and one for the counter's clock)

                # adding dig pulse train chan
                counter_output_task.co_channels.add_co_pulse_chan_freq(
                    counter = "cDAQ1Mod1/ctr1",
                    name_to_assign_to_channel = "",
                    units = FrequencyUnits.HZ,
                    idle_state = nidaqmx.constants.Level.LOW,
                    initial_delay = 0.0,
                    freq = 1000,
                    duty_cycle = 0.5
                    )

                # cfg implict timing
                counter_output_task.timing.cfg_implicit_timing(
                    sample_mode = AcquisitionType.CONTINUOUS,
                    samps_per_chan = 1
                    )

                # adding count egdes chan
                task1.ci_channels.add_ci_count_edges_chan(
                    counter = "cDAQ1Mod1/ctr0",
                    name_to_assign_to_channel = "",
                    edge = Edge.RISING,
                    initial_count = 0,
                    count_direction = CountDirection.COUNT_UP
                    )

                # cfg sample clk timing
                task1.timing.cfg_samp_clk_timing(
                    rate = 1000,
                    source = "/cDAQ1/Ctr1InternalOutput",
                    active_edge = Edge.RISING,
                    sample_mode = AcquisitionType.CONTINUOUS,
                    samps_per_chan = 1
                    )
                
                counter_output_task.start() # this starts the counter NI-DAQmx task
                task1.start() # this starts the hardware-based internal clock NI-DAQmx task
                        
            ####################################################################### x and z scanning #########################################################################

                for f in range(grid_size): # this loops for stacks in z

                    for k in range(grid_size): # this loops for columns (varying y voltage/setting)

                        ################## important section #################

                        for my_var_not_named_i in range(int(scan_counter_acquisition_time * 1000)): # this reads/lets the counter accumulate for the set time and returns value
                            counter_value = task1.read()
                            output_value += counter_value

                        if f % 2 != 0: # this loop populates the created yz_scan_data_array (the if else strucuture is present bc of the snaking scanning pattern)
                            yz_scan_data_array[f][((-k) + 1)] = (output_value - np.sum(yz_scan_data_array)) # add counter result to data array                           # saving (082422)
                            output_value == 0
                            counter_value == 0
                        else:
                            if f == 0 and k == 0:
                                yz_scan_data_array[0][0] = output_value # add counter result to data array                                                      # saving
                            else:
                                yz_scan_data_array[f][k] = (output_value - np.sum(yz_scan_data_array)) # add counter result to data array                               # saving (082422)
                        output_value = 0
                        counter_value = 0

                        ############# end important section ############

                        if f % 2 == 0: # this loop adjusts for sweeping back and forth along each alternating row
                            if k < (grid_size - 1):
                                y_driving_voltage_to_change += y_drive_voltage_step # increment y mirro drive voltage forwards
                                scan_galvo.voltage_cdaq1mod2ao1(y_driving_voltage_to_change) # step y mirror
                            else:
                                break
                        else:
                            if k < (grid_size - 1):
                                y_driving_voltage_to_change -= y_drive_voltage_step # increment y mirror drive voltage backwards
                                scan_galvo.voltage_cdaq1mod2ao1(y_driving_voltage_to_change) # step y mirror
                            else:
                                break

                    if f < (grid_size - 1): # this loop
                        z_piezo_driving_voltage_to_change += z_piezo_drive_voltage_step # increment drive voltage
                        scan_galvo.voltage_cdaq1mod2ao2(z_piezo_driving_voltage_to_change) # step z
                    else:
                        break

                counter_output_task.stop() # this stops the counter NI-DAQmx task - free-ing the reserved cDAQ card resources
                task1.stop() # this stops the hardware-based internal clock NI-DAQmx task - free-ing the reserved cDAQ card resources

            ############################################### plotting XZ scan data in plot ####################################################
            self.sc.axes.cla()
            xz_scan_plot = self.sc.axes.pcolormesh(yz_scan_data_array, cmap = "inferno")
            # self.sc.colorbar(plot, ax = self.sc.axes)
            self.sc.axes.set_xticks(np.arange(0, grid_size + 10, grid_size / 2), [initial_y_driving_voltage, int((initial_y_driving_voltage + desired_end_y_mirror_voltage) / 2), desired_end_y_mirror_voltage])
            self.sc.axes.set_yticks(np.arange(0, grid_size + 10, grid_size / 2), [int(initial_z_piezo_driving_voltage * 10), (int(initial_z_piezo_driving_voltage * 10) + int(desired_end_z_piezo_voltage * 10)) / 2, int(desired_end_z_piezo_voltage * 10)])
            self.sc.axes.set_xlabel("y_mirror_driving_voltage_(V)", fontsize = 8)
            self.sc.axes.set_ylabel("objective_z-piezo_height_(microns)", fontsize = 8)
            self.sc.axes.set_title("YZ_scan_083122_x_voltage=%f_V" % initial_x_driving_voltage, fontsize = 8)
            self.sc.draw()
            # print("YZ scan complete")

        ############################################################# left window #####################################################################
        left_window = QFrame(self)
        left_window.setFrameShape(QFrame.StyledPanel)
        left_window.setFixedSize(380, 390)

        ############################################################### right window ###################################################################
        right_window = QFrame(self)
        right_window.setFrameShape(QFrame.StyledPanel)
        right_window.setFixedSize(390, 390)

        ##################################################### plot ##################################################################

        plot_res = 3.85
        self.sc = MplCanvas(self, width = plot_res, height = plot_res, dpi = 100.5)                         # changing dpi does something
        self.sc.move(2, 2)
        self.sc.setParent(right_window)
        self.sc.axes.set_title("plot_title_here", fontsize = 9)
        self.sc.axes.set_xlabel("plot_x_label_here", fontsize = 8)
        self.sc.axes.set_ylabel("plot_y_label_here", fontsize = 8)

        ############################################################# split left and right windows #########################################################
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(left_window)
        splitter1.addWidget(right_window)
        hbox.addWidget(splitter1) # set layout and show window
        self.setLayout(hbox)
        self.show()

        ############################################################# scanning (XY, XZ, & YZ) section ############################################################################
        
        ##################################### overall ####################################

        pageSource = """
                    <html>

                    <head>
                    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                    </script>
                    </head>

                    <body>
                    <p><mathjax style = "font-size:1.0em">$$normal_{subscript}$$</mathjax></p>
                    </body>
                    
                    </html>
                    """

        # scan widgets overall "Scanning"
        scan_widget_overall = QLabel("Scanning options:")
        # scan_widget_overall = QLabel()
        # scan_widget_overall = QWebEngineView()
        # scan_widget_overall.setHtml(pageSource)
        scan_widget_overall.setFont(QFont("Times font", 9))
        scan_widget_overall.setParent(left_window)
        scan_widget_overall.move(120, 10)
        # scan_widget_overall.move(30, 10)

        indiv_scan_labels_y_height = 25

        row_y_adjust = 5

        overall_y_adjust = 10

        #########################################################################################
        ########################################### XY scanning #################################
        #########################################################################################

        xy_scan_widgets_left_x_justify = 5

        # XY scan
        xy_scan_label_widget = QLabel("XY scan", self) # widget
        xy_scan_label_widget.setParent(left_window)
        xy_scan_label_widget.move(15 + 10, indiv_scan_labels_y_height + overall_y_adjust)

        # resolution
        xy_scan_resolution_widget = QLabel("Res:", self) # widget
        xy_scan_resolution_widget.setParent(left_window)
        xy_scan_resolution_widget.move(xy_scan_widgets_left_x_justify, 40 + row_y_adjust + overall_y_adjust)

        xy_scan_resolution_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_resolution_qlineedit.setParent(left_window)
        xy_scan_resolution_qlineedit.move(30, 40 + row_y_adjust + overall_y_adjust)
        xy_scan_resolution_qlineedit.resize(55, 15)

        # read time
        xy_scan_read_time_widget = QLabel("APD_t:", self) # widget
        xy_scan_read_time_widget.setParent(left_window)
        xy_scan_read_time_widget.move(xy_scan_widgets_left_x_justify, 65 + row_y_adjust + overall_y_adjust)

        xy_scan_read_time_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_read_time_qlineedit.setParent(left_window)
        xy_scan_read_time_qlineedit.move(40, 65 + row_y_adjust + overall_y_adjust)
        xy_scan_read_time_qlineedit.resize(45, 15)
        
        # x voltage (min and max)
        xy_scan_x_voltage_min_widget = QLabel("x_V_min:", self) # widget
        xy_scan_x_voltage_min_widget.setParent(left_window)
        xy_scan_x_voltage_min_widget.move(xy_scan_widgets_left_x_justify, 90 + row_y_adjust + overall_y_adjust)

        xy_scan_x_voltage_min_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_x_voltage_min_qlineedit.setParent(left_window)
        xy_scan_x_voltage_min_qlineedit.move(50, 90 + row_y_adjust + overall_y_adjust)
        xy_scan_x_voltage_min_qlineedit.resize(35, 15)

        xy_scan_x_voltage_max_widget = QLabel("x_V_max:", self) # widget
        xy_scan_x_voltage_max_widget.setParent(left_window)
        xy_scan_x_voltage_max_widget.move(xy_scan_widgets_left_x_justify, 115 + row_y_adjust + overall_y_adjust)

        xy_scan_x_voltage_max_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_x_voltage_max_qlineedit.setParent(left_window)
        xy_scan_x_voltage_max_qlineedit.move(55, 115 + row_y_adjust + overall_y_adjust)
        xy_scan_x_voltage_max_qlineedit.resize(30, 15)

        # y voltage (min and max)
        xy_scan_y_voltage_min_widget = QLabel("y_V_min:", self) # widget
        xy_scan_y_voltage_min_widget.setParent(left_window)
        xy_scan_y_voltage_min_widget.move(xy_scan_widgets_left_x_justify, 140 + row_y_adjust + overall_y_adjust)

        xy_scan_y_voltage_min_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_y_voltage_min_qlineedit.setParent(left_window)
        xy_scan_y_voltage_min_qlineedit.move(50, 140 + row_y_adjust + overall_y_adjust)
        xy_scan_y_voltage_min_qlineedit.resize(35, 15)

        xy_scan_y_voltage_max_widget = QLabel("y_V_max:", self) # widget
        xy_scan_y_voltage_max_widget.setParent(left_window)
        xy_scan_y_voltage_max_widget.move(xy_scan_widgets_left_x_justify, 165 + row_y_adjust + overall_y_adjust)

        xy_scan_y_voltage_max_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_y_voltage_max_qlineedit.setParent(left_window)
        xy_scan_y_voltage_max_qlineedit.move(55, 165 + row_y_adjust + overall_y_adjust)
        xy_scan_y_voltage_max_qlineedit.resize(30, 15)
        
        # z piezo
        xy_scan_z_piezo_voltage_widget = QLabel("z_V:", self) # widget
        xy_scan_z_piezo_voltage_widget.setParent(left_window)
        xy_scan_z_piezo_voltage_widget.move(xy_scan_widgets_left_x_justify, 190 + row_y_adjust + overall_y_adjust)

        xy_scan_z_piezo_voltage_qlineedit = QLineEdit(self) # qclineedit
        xy_scan_z_piezo_voltage_qlineedit.setParent(left_window)
        xy_scan_z_piezo_voltage_qlineedit.move(30, 190 + row_y_adjust + overall_y_adjust)
        xy_scan_z_piezo_voltage_qlineedit.resize(55, 15)

        # run xy scan button
        xy_scan_run_button = QPushButton("run\nXY scan", self) # button
        xy_scan_run_button.setParent(left_window)
        xy_scan_run_button.resize(60, 40)
        xy_scan_run_button.move(15, 215 + row_y_adjust + overall_y_adjust)
        xy_scan_run_button.clicked.connect(print_XY_scan_parameters_fnc)
        xy_scan_run_button.clicked.connect(run_xy_scan_fnc)
        # try:
        #     xy_scan_run_button.clicked.connect(run_xy_scan_fnc)
        # except KeyError:
        #     scan_galvo.close()
        #     xy_scan_run_button.clicked.connect(run_xy_scan_fnc)

        #######################################################################################
        ####################################### XZ scanning ###################################
        #######################################################################################

        xz_scan_widgets_left_x_justify = 130

        # scan widget 2 "XZ"
        scan_widget_2 = QLabel("XZ scan", self)
        scan_widget_2.setParent(left_window)
        scan_widget_2.move(145 + 5, indiv_scan_labels_y_height + overall_y_adjust)

        # resolution
        xz_scan_resolution_widget = QLabel("Res:", self) # widget
        xz_scan_resolution_widget.setParent(left_window)
        xz_scan_resolution_widget.move(xz_scan_widgets_left_x_justify, 40 + row_y_adjust + overall_y_adjust)

        xz_scan_resolution_qlineedit = QLineEdit(self) # qclineedit
        xz_scan_resolution_qlineedit.setParent(left_window)
        xz_scan_resolution_qlineedit.move(25 + xz_scan_widgets_left_x_justify, 40 + row_y_adjust + overall_y_adjust)
        xz_scan_resolution_qlineedit.resize(55, 15)

        # read time
        xz_scan_read_time_widget = QLabel("APD_t:", self) # widget
        xz_scan_read_time_widget.setParent(left_window)
        xz_scan_read_time_widget.move(xz_scan_widgets_left_x_justify, 65 + row_y_adjust + overall_y_adjust)

        xz_scan_read_time_qlineedit = QLineEdit(self) # qclineedit
        xz_scan_read_time_qlineedit.setParent(left_window)
        xz_scan_read_time_qlineedit.move(35 + xz_scan_widgets_left_x_justify, 65 + row_y_adjust + overall_y_adjust)
        xz_scan_read_time_qlineedit.resize(45, 15)
        
        # x voltage (min and max)
        xz_scan_x_voltage_min_widget = QLabel("x_V_min:", self) # widget
        xz_scan_x_voltage_min_widget.setParent(left_window)
        xz_scan_x_voltage_min_widget.move(xz_scan_widgets_left_x_justify, 90 + row_y_adjust + overall_y_adjust)

        xz_scan_x_voltage_min_qlineedit = QLineEdit(self) # qclineedit
        xz_scan_x_voltage_min_qlineedit.setParent(left_window)
        xz_scan_x_voltage_min_qlineedit.move(45 + xz_scan_widgets_left_x_justify, 90 + row_y_adjust + overall_y_adjust)
        xz_scan_x_voltage_min_qlineedit.resize(35, 15)

        xz_scan_x_voltage_max_widget = QLabel("x_V_max:", self) # widget
        xz_scan_x_voltage_max_widget.setParent(left_window)
        xz_scan_x_voltage_max_widget.move(xz_scan_widgets_left_x_justify, 115 + row_y_adjust + overall_y_adjust)

        xz_scan_x_voltage_max_qlineedit = QLineEdit(self) # qclineedit
        xz_scan_x_voltage_max_qlineedit.setParent(left_window)
        xz_scan_x_voltage_max_qlineedit.move(50 + xz_scan_widgets_left_x_justify, 115 + row_y_adjust + overall_y_adjust)
        xz_scan_x_voltage_max_qlineedit.resize(30, 15)

        # y voltage single setting
        xz_scan_y_voltage_widget = QLabel("y_V:", self) # widget
        xz_scan_y_voltage_widget.setParent(left_window)
        xz_scan_y_voltage_widget.move(xz_scan_widgets_left_x_justify, 140 + row_y_adjust + overall_y_adjust)

        xz_scan_y_voltage_qlineedit = QLineEdit(self) # qclineedit
        xz_scan_y_voltage_qlineedit.setParent(left_window)
        xz_scan_y_voltage_qlineedit.move(25 + xz_scan_widgets_left_x_justify, 140 + row_y_adjust + overall_y_adjust)
        xz_scan_y_voltage_qlineedit.resize(55, 15)
                                
        # z piezo (min and max)
        xz_scan_z_piezo_min_voltage_widget = QLabel("z_V_min:", self) # widget
        xz_scan_z_piezo_min_voltage_widget.setParent(left_window)
        xz_scan_z_piezo_min_voltage_widget.move(xz_scan_widgets_left_x_justify, 165 + row_y_adjust + overall_y_adjust)

        xz_scan_z_piezo_min_voltage_qlineedit = QLineEdit(self) # qclineedit
        xz_scan_z_piezo_min_voltage_qlineedit.setParent(left_window)
        xz_scan_z_piezo_min_voltage_qlineedit.move(45 + xz_scan_widgets_left_x_justify, 165 + row_y_adjust + overall_y_adjust)
        xz_scan_z_piezo_min_voltage_qlineedit.resize(35, 15)

        xz_scan_z_piezo_max_voltage_widget = QLabel("z_V_max:", self) # widget
        xz_scan_z_piezo_max_voltage_widget.setParent(left_window)
        xz_scan_z_piezo_max_voltage_widget.move(xz_scan_widgets_left_x_justify, 190 + row_y_adjust + overall_y_adjust)

        xz_scan_z_piezo_max_voltage_qlineedit = QLineEdit(self) # qclineedit
        xz_scan_z_piezo_max_voltage_qlineedit.setParent(left_window)
        xz_scan_z_piezo_max_voltage_qlineedit.move(50 + xz_scan_widgets_left_x_justify, 190 + row_y_adjust + overall_y_adjust)
        xz_scan_z_piezo_max_voltage_qlineedit.resize(30, 15)

        # run xz scan button
        xz_scan_run_button = QPushButton("run\nXZ scan", self) # button
        xz_scan_run_button.setParent(left_window)
        xz_scan_run_button.resize(60, 40)
        xz_scan_run_button.move(10 + xz_scan_widgets_left_x_justify, 215 + row_y_adjust + overall_y_adjust)
        xz_scan_run_button.clicked.connect(print_XZ_scan_parameters_fnc)
        xz_scan_run_button.clicked.connect(run_xz_scan_fnc)

        #####################################################################################
        ####################################### YZ scanning #################################
        #####################################################################################

        yz_scan_widgets_left_x_justify = 255

        # scan widget 3 "YZ"
        scan_widget_3 = QLabel("YZ scan", self)
        scan_widget_3.setParent(left_window)
        scan_widget_3.move(265 + 10, indiv_scan_labels_y_height + overall_y_adjust)

        # resolution
        yz_scan_resolution_widget = QLabel("Res:", self) # widget
        yz_scan_resolution_widget.setParent(left_window)
        yz_scan_resolution_widget.move(yz_scan_widgets_left_x_justify, 40 + row_y_adjust + overall_y_adjust)

        yz_scan_resolution_qlineedit = QLineEdit(self) # qclineedit
        yz_scan_resolution_qlineedit.setParent(left_window)
        yz_scan_resolution_qlineedit.move(25 + yz_scan_widgets_left_x_justify, 40 + row_y_adjust + overall_y_adjust)
        yz_scan_resolution_qlineedit.resize(55, 15)

        # read time
        yz_scan_read_time_widget = QLabel("APD_t:", self) # widget
        yz_scan_read_time_widget.setParent(left_window)
        yz_scan_read_time_widget.move(yz_scan_widgets_left_x_justify, 65 + row_y_adjust + overall_y_adjust)

        yz_scan_read_time_qlineedit = QLineEdit(self) # qclineedit
        yz_scan_read_time_qlineedit.setParent(left_window)
        yz_scan_read_time_qlineedit.move(35 + yz_scan_widgets_left_x_justify, 65 + row_y_adjust + overall_y_adjust)
        yz_scan_read_time_qlineedit.resize(45, 15)
        
        # y voltage (min and max)
        yz_scan_y_voltage_min_widget = QLabel("y_V_min:", self) # widget
        yz_scan_y_voltage_min_widget.setParent(left_window)
        yz_scan_y_voltage_min_widget.move(yz_scan_widgets_left_x_justify, 90 + row_y_adjust + overall_y_adjust)

        yz_scan_y_voltage_min_qlineedit = QLineEdit(self) # qclineedit
        yz_scan_y_voltage_min_qlineedit.setParent(left_window)
        yz_scan_y_voltage_min_qlineedit.move(45 + yz_scan_widgets_left_x_justify, 90 + row_y_adjust + overall_y_adjust)
        yz_scan_y_voltage_min_qlineedit.resize(35, 15)

        yz_scan_y_voltage_max_widget = QLabel("y_V_max:", self) # widget
        yz_scan_y_voltage_max_widget.setParent(left_window)
        yz_scan_y_voltage_max_widget.move(yz_scan_widgets_left_x_justify, 115 + row_y_adjust + overall_y_adjust)

        yz_scan_y_voltage_max_qlineedit = QLineEdit(self) # qclineedit
        yz_scan_y_voltage_max_qlineedit.setParent(left_window)
        yz_scan_y_voltage_max_qlineedit.move(50 + yz_scan_widgets_left_x_justify, 115 + row_y_adjust + overall_y_adjust)
        yz_scan_y_voltage_max_qlineedit.resize(30, 15)

        # x voltage single setting
        yz_scan_x_voltage_widget = QLabel("x_V:", self) # widget
        yz_scan_x_voltage_widget.setParent(left_window)
        yz_scan_x_voltage_widget.move(yz_scan_widgets_left_x_justify, 140 + row_y_adjust + overall_y_adjust)

        yz_scan_x_voltage_qlineedit = QLineEdit(self) # qclineedit
        yz_scan_x_voltage_qlineedit.setParent(left_window)
        yz_scan_x_voltage_qlineedit.move(25 + yz_scan_widgets_left_x_justify, 140 + row_y_adjust + overall_y_adjust)
        yz_scan_x_voltage_qlineedit.resize(55, 15)
                                
        # z piezo (min and max)
        yz_scan_z_piezo_min_voltage_widget = QLabel("z_V_min:", self) # widget
        yz_scan_z_piezo_min_voltage_widget.setParent(left_window)
        yz_scan_z_piezo_min_voltage_widget.move(yz_scan_widgets_left_x_justify, 165 + row_y_adjust + overall_y_adjust)

        yz_scan_z_piezo_min_voltage_qlineedit = QLineEdit(self) # qclineedit
        yz_scan_z_piezo_min_voltage_qlineedit.setParent(left_window)
        yz_scan_z_piezo_min_voltage_qlineedit.move(45 + yz_scan_widgets_left_x_justify, 165 + row_y_adjust + overall_y_adjust)
        yz_scan_z_piezo_min_voltage_qlineedit.resize(35, 15)

        yz_scan_z_piezo_max_voltage_widget = QLabel("z_V_max:", self) # widget
        yz_scan_z_piezo_max_voltage_widget.setParent(left_window)
        yz_scan_z_piezo_max_voltage_widget.move(yz_scan_widgets_left_x_justify, 190 + row_y_adjust + overall_y_adjust)

        yz_scan_z_piezo_max_voltage_qlineedit = QLineEdit(self) # qclineedit
        yz_scan_z_piezo_max_voltage_qlineedit.setParent(left_window)
        yz_scan_z_piezo_max_voltage_qlineedit.move(50 + yz_scan_widgets_left_x_justify, 190 + row_y_adjust + overall_y_adjust)
        yz_scan_z_piezo_max_voltage_qlineedit.resize(30, 15)

        # run yz scan button
        yz_scan_run_button = QPushButton("run\nYZ scan", self) # button
        yz_scan_run_button.setParent(left_window)
        yz_scan_run_button.resize(60, 40)
        yz_scan_run_button.move(15 + yz_scan_widgets_left_x_justify, 215 + row_y_adjust + overall_y_adjust)
        yz_scan_run_button.clicked.connect(print_YZ_scan_parameters_fnc)
        yz_scan_run_button.clicked.connect(run_yz_scan_fnc)

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

# # button1
# button1 = QPushButton("change plot (basic)", self)
# button1.resize(100, 25)
# button1.move(280, 25)
# button1.clicked.connect(button_1_clicked)

# ################### not yet #####################
# def update_plot():
#     # print("update_call called")
#     self.sc.axes.cla()
#     self.x_data = numpy.random.randint(9, size = 5)
#     self.y_data = numpy.random.randint(9, size = 5)
#     self.sc.axes.plot(self.x_data, self.y_data)
#     self.sc.draw()

# def button_1_clicked(self, parent = Child):
#     # print("button 1 clicked")
#     update_plot()

# def scan_update():                                          # use this for demo
#     self.sc.axes.cla()
#     output_data_set = numpy.load("file_name_by_time.npy")
#     self.sc.axes.pcolormesh(output_data_set, cmap = "RdBu_r")
#     self.sc.draw()
# ################### not yet ######################

# self.x_data = numpy.random.randint(9, size = 5)
# self.y_data = numpy.random.randint(9, size = 5)
# # self.z_data = numpy.random.randint(9, size = 5)
# self.sc.axes.plot(self.x_data, self.y_data)

# data_set = numpy.load("082422_faster_scan_03.npy")
# self.sc.axes.pcolormesh(data_set, cmap = "RdBu_r")
# self.sc.axes.colorbar(plot_1, ax = self.sc.axes)
# self.sc.axes.colorbar(plot_1)
