# text file for notes, code sections
# ongoing

```python
# naming the device
device_name_mod1 = "cDAQ1Mod1"

# sample rate per channel in Hz
sample_rate_per_channel = 1e3

# define number of digital input channels
num_di_channels = 4

# dictionary of digital input channels
di_channels_mod1 = {'port0/line{}'.format(i): i for i in range(num_di_channels)}
# print(di_channels_mod1) # delete this line

# define finite number of smaples to be taken
num_samples_want = 2

# defining the instrument (ni_9402)
with nidaqmx.Task("ni_9402") as ni_9402:
    digital_inputs_ni_9402 = DAQDigitalInputs(
        "ni_9402",
        device_name_mod1,
        sample_rate_per_channel,
        di_channels_mod1,
        ni_9402,
        samples_to_read = num_samples_want,
        target_points = num_samples_want
    )
    ## trial for ni_9402 taking data

    # starting the task
    ni_9402.start()

    # populating "result" with measured data
    result = digital_inputs_ni_9402.voltage()

    # allowing data collection to be completed
    ni_9402.wait_until_done()
```

###########################################################################


```python
# reading the counter value
result_counter = ni_9402.read_counter_cdaq1mod1ctr0(1)
```


###########################################################################

"""

# Setting output voltage paremeters on ni_9263

___

# set channel 0 of ni_9263 to 0 V
ni_9263.voltage_cdaq1mod2ao0(0)

# set channel 1 of ni_9263 to 0 V
ni_9263.voltage_cdaq1mod2ao1(0)

# set channel 2 of ni_9263 to 0 V
ni_9263.voltage_cdaq1mod2ao2(0)

# set channel 3 of ni_9263 to 0 V
ni_9263.voltage_cdaq1mod2ao3(0)
"""

"""
# meas = Measurement(exp=exp, name='exponential_decay')
# meas.register_parameter(dac.ch1)  # register the first independent parameter
# meas.register_parameter(dmm.v1, setpoints=(dac.ch1,))  # now register the dependent oone

# meas.add_before_run(numbertwo, (dmm, dac))  # add another set-up action

# meas.write_period = 0.5

# with meas.run() as datasaver:             
#     for set_v in np.linspace(0, 25, 10):
#         dac.ch1.set(set_v)
#         get_v = dmm.v1.get()
#         datasaver.add_result((dac.ch1, set_v),
#                              (dmm.v1, get_v))
    
#     dataset1D = datasaver.dataset  # convenient to have for data access and plotting
"""

"""
# adding single counter read value per time
with measurement.run() as datasaver:
    ctr_values = 0
    time.reset_clock()
    
    # for get_ctr_val in np.linspace(0, 5, 10):
    #     ni_9402.read_counter_cdaq1mod1ctr0(get_ctr_val)
    #     datasaver.add_result(ni_9402.read_counter_cdaq1mod1ctr0)
    
    for i in range(10):
        ctr_values += int(ni_9402.read_counter_cdaq1mod1ctr0()[1])
        time_value = time()
        datasaver.add_result((ni_9402.read_counter_cdaq1mod1ctr0, ctr_values), (time, time_value))
        
my_dataset = datasaver.dataset
"""

"""python
sleep(15)
ni_9263.voltage_cdaq1mod2ao0(0)

ni_9263.voltage_cdaq1mod2ao0(1.5)
sleep(1.0)
ni_9263.voltage_cdaq1mod2ao0(2)
sleep(1.0)
ni_9263.voltage_cdaq1mod2ao0(2.5)
sleep(1.0)
ni_9263.voltage_cdaq1mod2ao0(3.0)
sleep(1.0)
ni_9263.voltage_cdaq1mod2ao0(3.5)
sleep(1.0)
ni_9263.voltage_cdaq1mod2ao0(4)
sleep(1.0)
"""

"""python
#################### resetting position of mirrors ####################

# x-mirror
ni_9263.voltage_cdaq1mod2ao0(0)

# y-mirror
ni_9263.voltage_cdaq1mod2ao1(0)

#################### delay to watch sweeping ####################

# sleep(13)

#################### setting variales and array ####################

# get time @ start of scanning
start_time = time.time()

# initial driving voltage for x
drive_voltage_x = 0.0

# initial driving voltage for y
drive_voltage_y = 0.0

# drive voltage step for sweep
drive_voltage_step = 0.01

# def size of grid to scan (array is square)
grid_size = 64

# set delay in seconds (time to let counter accumulate per point)
delay_time = 0.0001

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

#################### looping over grid (scanning) ####################

from tqdm import tqdm
# scan over array reading counter @ each point
for k in tqdm(range(grid_size)): # y rows
    
    for i in range(grid_size): # x cols
        
        ni_9263.voltage_cdaq1mod2ao0(drive_voltage_x) # moving on x motor
        sleep(delay_time)
        
        result = ni_9402.read_counter_cdaq1mod1ctr0() # reading counter
        
        if k == 1 & i == 1: # correcting counter values point to point
            result == data_array[k][i]
        else:
            result == data_array[k][i] - data_array[k - 1][i - 1]
            
        if k % 2 != 0: # correcting for sweeping back and forth on x
            drive_voltage_x -= drive_voltage_step
        else:
            drive_voltage_x += drive_voltage_step # stepping x voltage
            
    ni_9263.voltage_cdaq1mod2ao1(drive_voltage_y) # moving on y motor
    drive_voltage_y += drive_voltage_step # stepping y voltage
    sleep(delay_time) # correcting delay for edge data points

#################### displaying dataset info. ####################

# printing parameters
print("counter read time per point: " + str(delay_time) + " s")
print("num points collected: %s" % (str(grid_size * grid_size)))
print("elapsed scanning time: %.1f s" % (time.time() - start_time) + "\n")

# printing dataset
print("dataset:\n" + str(data_array))

# plotting dataset
print("\nplot:")
fig, axs = plt.subplots(figsize = (7.5, 7.5), layout = "constrained")
plot1 = axs.pcolormesh(data_array)
fig.colorbar(plot1, ax = axs)
axs.set_title("galvo_scan");
"""

# 081522

## test cell for "read_counter"
"""python
result = ni_9402.read_counter_cdaq1mod1ctr0()
print(result)
# print(type(result))
"""

"""python
with measurement.run() as datasaver:
    ctr_values = 0
    time.reset_clock()

    ############################################# FINITE #############################################
    for i in range(10):
        ctr_values += int(ni_9402.read_counter_cdaq1mod1ctr0()[1])
        time_value = time()
        datasaver.add_result((ni_9402.read_counter_cdaq1mod1ctr0, ctr_values), (time, time_value))

# labeling the dataset
my_dataset = datasaver.dataset

print("\n")
print(my_dataset)
print("\n")
plot_dataset(my_dataset);

MatPlot(
    my_dataset.get_parameter_data()['ni_9402_module_read_counter_cdaq1mod1ctr0']['ni_9402_module_read_counter_cdaq1mod1ctr0'],
    figsize = (6, 4),
    interval = 0.01
    ).update_plot()
"""

081522

experiment_name = "room_temp_NV_exp_control_experiment"

database_name = "room_temp_NV_exp_control_database"

station_name = "room_temp_NV_exp_control_station"

ATTEMpT
"""python
meas_two = Measurement(exp = room_temp_NV_exp_control_experiment, station = room_temp_NV_exp_control_station, name = 'small_example_2')

time_value = time()

# Register the independent parameter...
meas_two.register_parameter(ni_9402.read_counter_cdaq1mod1ctr0)

# ...then register the dependent parameter
meas_two.register_parameter(time_value, setpoints = (ni_9402.read_counter_cdaq1mod1ctr0))

# Time for periodic background database writes
# meas_two.write_period = 2

ctr_values = 0
time.reset_clock()

with meas_two.run() as datasaver:
    for set_v in range(5):
        ctr_values += int(ni_9402.read_counter_cdaq1mod1ctr0()[1])
        time_value
        datasaver.add_result((ni_9402.read_counter_cdaq1mod1ctr0, ctr_values), (time, time_value))

    # Convenient to have for plotting and data access
    dataset_2 = datasaver.dataset
"""

081622
"""python
# setup parameters for the finite measurement
counter_value_to_read = ni_9402.read_counter_cdaq1mod1ctr0
time = ElapsedTimeParameter("time")

# user-defined variable for the measurement
num_counter_values_to_read = 50

# setup the measurement
counter_finite_samples_meas = Measurement(
    exp = room_temp_NV_exp_control_experiment,
    station = room_temp_NV_exp_control_station,
    name = "counter_finite_samples_meas"
    )

# registering defined parameters to the measurement (counter_finite_samples_meas)
counter_finite_samples_meas.register_parameter(time)
counter_finite_samples_meas.register_parameter(counter_values, setpoints = [time])

# loop to read finite number of values from counter
with counter_finite_samples_meas.run() as datasaver:
    
    # before loop statements
    counter_values_list = 0
    time.reset_clock()
    
    # measurement loop
    for i in trange(num_counter_values_to_read, desc = "counter read progress"): # use tqdm for progress bar
        counter_values_list += counter_value_to_read()
        current_time = time()
        datasaver.add_result((counter_value_to_read, counter_values_list), (time, current_time))

# save to user-defined/named dataset for later viewing
counter_finite_samples_dataset = datasaver.dataset
"""

# QCoDeS doNd measurement example
"""python
# Setting up Measurement
meas = Measurement(name= '2d_measurement of dmm from dac sweep', exp=tutorial_exp)
meas.register_parameter(dac.ch1)
meas.register_parameter(dac.ch2)
meas.register_parameter(dmm.v1, setpoints=(dac.ch1,dac.ch2))
meas.register_parameter(dmm.v2, setpoints=(dac.ch1,dac.ch2))

# Running Measurement
with meas.run() as datasaver:
    for dac1_sweep in np.linspace(-1, 1, 20): # sweep points over channel 1
        dac.ch1(dac1_sweep)
        for dac2_sweep in np.linspace(-1, 1, 20): # sweep points over channel 2
            dac.ch2(dac2_sweep)
            datasaver.add_result(
                (dac.ch1, dac.ch1()),
                (dac.ch2, dac.ch2()),
                (dmm.v1, dmm.v1()),
                (dmm.v2, dmm.v2())
                )
            time.sleep(0.01) # Can be removed if there is no intention to see a live plot

    dataset2 = datasaver.dataset
    
plot_dataset(dataset2)
"""

081822 working scan example
"""python
dac.x = ni_9263.voltage_cdaq1mod2ao0
dac.y = ni_9263.voltage_cdaq1mod2ao1

# dmm = DummyInstrumentWithMeasurement('dmm', setter_instr = dac)
dmm = ni_9402.read_counter_cdaq1mod1ctr0

#meas = Measurement(name= '081822_test', exp = room_temp_NV_exp_control_experiment)
meas.register_parameter(dac.x)
meas.register_parameter(dac.y)
meas.register_parameter(dmm, setpoints = (dac.x,dac.y))

size = 4

#
with meas.run() as datasaver:
    for x_motor_sweep in np.linspace(0, size, size+1): # sweep points over channel 1
        dac.x(x_motor_sweep)
        for y_motor_sweep in np.linspace(0, size, size+1): # sweep points over channel 2
            dac.y(y_motor_sweep)
            datasaver.add_result(
                (dac.x, dac.x()),
                (dac.y, dac.y()),
                (dmm, dmm())
                )

    dataset2 = datasaver.dataset

plot_dataset(dataset2)
"""

081922
"""python
# def the parameters of the instrument
ni_9402_device_name = "cDAQ1Mod1"
ni_9402_counter_channel = "cDAQ1Mod1/ctr0"
ni_9402_clock_channel = "cDAQ1Mod1/ctr1"
ni_9402_source_channel = "/cDAQ1/Ctr1InternalOutput"
ni_9402_sampling_rate = 1000
ni_9402_samples_per_channel = 1
ni_9402_duty_cycle = 0.5
ni_9402_integration_time = 0.3
ni_9402_timeout = 0.01

# creating the instrument for mod1
ni_9402 = Counter("ni_9402_module", ni_9402_device_name, ni_9402_counter_channel,
    ni_9402_clock_channel, ni_9402_source_channel, ni_9402_sampling_rate,
    ni_9402_samples_per_channel, ni_9402_duty_cycle,
    ni_9402_integration_time, ni_9402_timeout
    )
"""

082022
"""python
# def the parameters of the instrument
ni_9402_device_name = "cDAQ1Mod1"
ni_9402_counter_channel = "cDAQ1Mod1/ctr0"
ni_9402_clock_channel = "cDAQ1Mod1/ctr1"
ni_9402_source_channel = "/cDAQ1/Ctr1InternalOutput"
ni_9402_sampling_rate = 1000
ni_9402_samples_per_channel = 1
ni_9402_duty_cycle = 0.5
ni_9402_integration_time = 0.3
ni_9402_timeout = 0.01

# creating the instrument for mod1
ni_9402 = Counter("ni_9402_module", ni_9402_device_name, ni_9402_counter_channel,
    ni_9402_clock_channel, ni_9402_source_channel, ni_9402_sampling_rate,
    ni_9402_samples_per_channel, ni_9402_duty_cycle,
    ni_9402_integration_time, ni_9402_timeout
    )
"""

"""
# ORIGINAL CELL

#################### resetting position of mirrors ####################

# x-mirror
ni_9263.voltage_cdaq1mod2ao0(0)

# y-mirror
ni_9263.voltage_cdaq1mod2ao1(0)

#################### delay to watch sweeping ####################

# sleep(13)

#################### setting variales and array ####################

# get time @ start of scanning
start_time = time()

# initial driving voltage for x
drive_voltage_x = 0.0

# initial driving voltage for y
drive_voltage_y = 0.0

# drive voltage step for sweep
drive_voltage_step = 0.005

# def size of grid to scan (array is square)
grid_size = 16

# set delay in seconds (time to let counter accumulate per point)
delay_time = 0.001

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

#################### looping over grid (scanning) ####################

# scan over array reading counter @ each point
for k in trange(grid_size, desc = "scan progress"): # y rows
    
    for i in range(grid_size): # x cols
        
        ni_9263.voltage_cdaq1mod2ao0(drive_voltage_x) # moving on x motor
        sleep(delay_time)
        
        result = ni_9402.read_counter_cdaq1mod1ctr0() # reading counter
        # print(result)
        
        
        if k != 1 & i != 1: # correcting counter values point to point

            (data_array[k][i] - data_array[k - 1][i - 1]) == result
        else:

            data_array[k][i] = result
            
            
            
        if k % 2 != 0: # correcting for sweeping back AND forth on x
            drive_voltage_x -= drive_voltage_step
        else:
            drive_voltage_x += drive_voltage_step # stepping x voltage
            
    ni_9263.voltage_cdaq1mod2ao1(drive_voltage_y) # moving on y motor
    drive_voltage_y += drive_voltage_step # stepping y voltage
    sleep(delay_time) # correcting delay for edge data points

#################### displaying dataset info. ####################

# printing parameters
print("motor step voltage: %s V" % str(drive_voltage_step))
print("counter read time per point: " + str(delay_time) + " s")
print("num points collected: %s" % (str(grid_size * grid_size)))
print("elapsed scanning time: %.1f s" % (time() - start_time) + "\n")

# printing dataset
print("dataset:\n" + str(data_array))

# plotting dataset
print("\nplot:")
fig, axs = plt.subplots(figsize = (7.5, 7.5), layout = "constrained")
plot1 = axs.pcolormesh(data_array)
fig.colorbar(plot1, ax = axs)
axs.set_title("galvo_scan");
"""

082222

an older scanning attempt
"""
# what this is; scanning

# close instruments
scan_counter.close()
scan_galvo.close()
#

#################################################################################### card 1 ###################################################################

# notes: need x output. need y output

# name_that_i_need = "my_string_name"

scan_counter = Scan_Counter(
    "name_for_inst",
    # name = name_that_i_need.encode('utf-8'),
    scan_counter_device_name = "cDAQ1Mod1",
    scan_counter_counter_channel = "cDAQ1Mod1/ctr0",
    scan_counter_clock_channel = "cDAQ1Mod1/ctr1",
    scan_counter_source_channel = "/cDAQ1/Ctr1InternalOutput",
    scan_counter_sampling_rate = 1000,
    scan_counter_samples_per_channel = 1,
    scan_counter_duty_cycle = 0.5,
    scan_counter_acquisition_time = 0.01 # this is in seconds. As long as sampling_rate is 1000. If not, math must change for acquisition time
    )

########################################################################################### card 2 ##################################################################

# notes: need counter; needs req. parameters

# naming the instrument
scan_galvo_card_name = "cDAQ1Mod2"

# dictionary of analog output channels
scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

# defining the instrument (ni_9263)
scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

########################################################################## other variables ###############################################################

#################### setting variales and array ####################

# get time @ start of scanning
# start_time = time()

# initial driving voltage for x
drive_voltage_x = 0.0

# initial driving voltage for y
drive_voltage_y = 0.0

# drive voltage step for sweep
drive_voltage_step = 0.001

# def size of grid to scan (array is square)
grid_size = 315

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

############################################################################################ scanning ###########################################################

################### omit ##################################
# # scan_counter.Scan_Counter_Read(1) # set
# result = scan_counter.Scan_Counter_Read() # get
# print(result)

# scan_galvo.voltage_cdaq1mod2ao0(0)
##########################################################

#################### resetting position of mirrors ####################

# x-mirror
scan_galvo.voltage_cdaq1mod2ao0(0)

# y-mirror
scan_galvo.voltage_cdaq1mod2ao1(0)

#################### delay to watch sweeping ####################

# sleep(10)

###########################
galvo_meas_3 = Measurement(name= '082022_test_1', exp = room_temp_NV_exp_control_experiment)
galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao0)
galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao1)
galvo_meas_3.register_parameter(scan_counter.Scan_Counter_Read, setpoints = (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao1))

#################### looping over grid (scanning) ####################

with galvo_meas_3.run() as datasaver:

    # scan over array reading counter @ each point
    for k in trange(grid_size, desc = "scanning progress"): # y rows

        for i in range(grid_size): # x cols

            ########################            
            datasaver.add_result(
                (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
                (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
                (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
                )
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            result_1 = scan_counter.Scan_Counter_Read()
            # print(result_1)
            data_array[k][i] = result_1
            
            if k % 2 != 0 : # correcting for sweeping back AND forth on x
                drive_voltage_x -= drive_voltage_step
            else:
                drive_voltage_x += drive_voltage_step # stepping x voltage
            
            if k % 2 != 0 : #(scanning L to R)
                if i != (grid_size - 1):
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # moving on x motor
                elif k % 2 != 0:
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # moving on x motor
                    # print("check: k == odd")
                    datasaver.add_result(
                        (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
                        (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
                        (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
                        )
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    result_2 = scan_counter.Scan_Counter_Read()
                    data_array[k][i] = result_2
                else:
                    break
            else: # (if k is even OR ZERO; scanning R to L):
                if i == grid_size-1:
                    # print("0 or even row")
                    break
                else:
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # moving on x motor
                    datasaver.add_result(
                        (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
                        (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
                        (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
                        )
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    result_3 = scan_counter.Scan_Counter_Read()
                    data_array[k][i] = result_3

        drive_voltage_y += drive_voltage_step
        scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y) # moving on y motor

    dataset_galvo_meas_3 = datasaver.dataset

#
plot_dataset(dataset_galvo_meas_3)

###########################################################################################################################################################
# print(data_array)
# fig, axs = plt.subplots(figsize = (6.5, 6.5), layout = "constrained")
# plot1 = axs.pcolormesh(data_array)
# fig.colorbar(plot1, ax = axs)
# axs.set_title("scan");
"""

the original scanning cell (failed)
"""# ORIGINAL CELL

#################### resetting position of mirrors ####################

# x-mirror
ni_9263.voltage_cdaq1mod2ao0(0)

# y-mirror
ni_9263.voltage_cdaq1mod2ao1(0)

#################### delay to watch sweeping ####################

# sleep(13)

#################### setting variales and array ####################

# get time @ start of scanning
start_time = time()

# initial driving voltage for x
drive_voltage_x = 0.0

# initial driving voltage for y
drive_voltage_y = 0.0

# drive voltage step for sweep
drive_voltage_step = 0.005

# def size of grid to scan (array is square)
grid_size = 16

# set delay in seconds (time to let counter accumulate per point)
delay_time = 0.001

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

#################### looping over grid (scanning) ####################

# scan over array reading counter @ each point
for k in trange(grid_size, desc = "scan progress"): # y rows
    
    for i in range(grid_size): # x cols
        
        ni_9263.voltage_cdaq1mod2ao0(drive_voltage_x) # moving on x motor
        sleep(delay_time)
        
        result = ni_9402.read_counter_cdaq1mod1ctr0() # reading counter
        # print(result)
        
        # if k == 1 & i == 1: # correcting counter values point to point
        #     # data_array[k][i].append(result)
        #     # data_array.append(result)
        #     data_array[k][i] = result
        # else:
        #     # result == data_array[k][i] - data_array[k - 1][i - 1]
        #     (data_array[k][i] - data_array[k - 1][i - 1]) == result
        
        
        
        if k != 1 & i != 1: # correcting counter values point to point
            # data_array[k][i].append(result)
            # data_array.append(result)
            # data_array[k][i] = result
            (data_array[k][i] - data_array[k - 1][i - 1]) == result
        else:
            # result == data_array[k][i] - data_array[k - 1][i - 1]
            # (data_array[k][i] - data_array[k - 1][i - 1]) == result
            data_array[k][i] = result
            
            
            
        if k % 2 != 0: # correcting for sweeping back AND forth on x
            drive_voltage_x -= drive_voltage_step
        else:
            drive_voltage_x += drive_voltage_step # stepping x voltage
            
    ni_9263.voltage_cdaq1mod2ao1(drive_voltage_y) # moving on y motor
    drive_voltage_y += drive_voltage_step # stepping y voltage
    sleep(delay_time) # correcting delay for edge data points

#################### displaying dataset info. ####################

# printing parameters
print("motor step voltage: %s V" % str(drive_voltage_step))
print("counter read time per point: " + str(delay_time) + " s")
print("num points collected: %s" % (str(grid_size * grid_size)))
print("elapsed scanning time: %.1f s" % (time() - start_time) + "\n")

# printing dataset
print("dataset:\n" + str(data_array))

# plotting dataset
print("\nplot:")
fig, axs = plt.subplots(figsize = (7.5, 7.5), layout = "constrained")
plot1 = axs.pcolormesh(data_array)
fig.colorbar(plot1, ax = axs)
axs.set_title("galvo_scan");

"""

082322

##### working XY scanning code
"""
# what this is; scanning

# close instruments
scan_counter.close()
scan_galvo.close()

#################################################################################### card 1 ###################################################################

scan_counter = Scan_Counter(
    "name_for_inst",
    scan_counter_device_name = "cDAQ1Mod1",
    scan_counter_counter_channel = "cDAQ1Mod1/ctr0",
    scan_counter_clock_channel = "cDAQ1Mod1/ctr1",
    scan_counter_source_channel = "/cDAQ1/Ctr1InternalOutput",
    scan_counter_sampling_rate = 1000,
    scan_counter_samples_per_channel = 1,
    scan_counter_duty_cycle = 0.5,
    scan_counter_acquisition_time = 0.051 # this is in seconds. As long as sampling_rate is 1000. If not, math must change for acquisition time
    )

########################################################################################### card 2 ##################################################################

# notes: need counter; needs req. parameters

# naming the instrument
scan_galvo_card_name = "cDAQ1Mod2"

# dictionary of analog output channels
scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

# defining the instrument (ni_9263)
scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

########################################################################## other variables ###############################################################

#################### setting variales and array ####################

# def size of grid to scan (array is square)
grid_size = int(int(int(46 * 2) * 2) * 2) + 7

# drive voltage step for sweep
drive_voltage_step = ((0.0155 / 2) / 2) / 2

# initial driving voltage for (x and y)
drive_voltage_x = -0.300

# initial driving voltage for y
drive_voltage_y = drive_voltage_x

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

############################################################################################ scanning ###########################################################

#################### resetting position of mirrors ####################

# x-mirror
scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x)

# y-mirror
scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y)

#################### delay to watch sweeping ####################

# sleep(10)

####################################################################### setting up QCoDeS measurement ##############################################################

galvo_meas_3 = Measurement(name= "082222_scan", exp = room_temp_NV_exp_control_experiment)

galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao0)
galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao1)
galvo_meas_3.register_parameter(scan_counter.Scan_Counter_Read, setpoints = (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao1))

##################### looping over grid (scanning) #################################

# print(data_array)

start_time = datetime.datetime.now()

with galvo_meas_3.run() as datasaver:
    
    for i in trange(grid_size): #
        # print("i = %d" % i)
        
        for k in range(grid_size): #
            # print("k = %d" % k)
            
            result = scan_counter.Scan_Counter_Read() # read counter (w/ delay)
            if i % 2 != 0:
                data_array[i][-(k + 1)] = result # add counter result to data array
            else:
                data_array[i][k] = result # add counter result to data array
            
            datasaver.add_result(
                (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
                (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
                (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
                )
            
            if i % 2 == 0: # if i is 0 or even
                if k < (grid_size - 1):
                    drive_voltage_x += drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
            else:
                if k < (grid_size - 1):
                    drive_voltage_x -= drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
                    
        # print("end of k loop")
        if i < (grid_size - 1):
            drive_voltage_y += drive_voltage_step # increment drive voltage
            scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y) # step y motor
        else:
            break
        # print("end of i loop")

    dataset_galvo_meas_3 = datasaver.dataset

end_time = datetime.datetime.now()

################################################################## visualizing scan data ##########################################################################

scanning_time = end_time - start_time
print("scanning time: %s" % scanning_time)

# print(data_array)

fig, axs = plt.subplots(figsize = (6, 6), layout = "constrained")
plot1 = axs.pcolormesh(data_array)
fig.colorbar(plot1, ax = axs)
axs.set_title("scan_");

plot_dataset(dataset_galvo_meas_3) # QCoDeS plotting
"""

cell for getting data from QCoDeS measurement
"""
my_dataset = dataset_galvo_meas_3.get_parameter_data()

# print(my_dataset)

# print("\n")

# print(my_dataset["name_for_inst_Scan_Counter_Read"])

# print("\n")

print(my_dataset["name_for_inst_Scan_Counter_Read"]["name_for_inst_Scan_Counter_Read"])
my_counter_values = my_dataset["name_for_inst_Scan_Counter_Read"]["name_for_inst_Scan_Counter_Read"]

print("\n")

print(my_dataset["name_for_inst_Scan_Counter_Read"]["name_two_voltage_cdaq1mod2ao0"])
my_x_values = my_dataset["name_for_inst_Scan_Counter_Read"]["name_two_voltage_cdaq1mod2ao0"]

print("\n")

print(my_dataset["name_for_inst_Scan_Counter_Read"]["name_two_voltage_cdaq1mod2ao1"])
my_y_values = my_dataset["name_for_inst_Scan_Counter_Read"]["name_two_voltage_cdaq1mod2ao1"]
"""

""" use this correct loop
for i in trange(grid_size): #
        # print("i = %d" % i)

        # i_timing_start = datetime.datetime.now()                                                        # timing line

        for k in range(grid_size): #
            # k_timing_start = datetime.datetime.now()                                                                    # timing line
            # print("k = %d" % k)

            # result = scan_counter.Scan_Counter_Read() # read counter (w/ delay) OLD
            start_time = datetime.datetime.now()
            for i in range(int(scan_counter_acquisition_time * 1000)):
                counter_value = task1.read()
                output_value += counter_value
            end_time = datetime.datetime.now()
            result = output_value
            
            if i % 2 != 0:
                data_array[i][-(k + 1)] = result # add counter result to data array
            else:
                data_array[i][k] = result # add counter result to data array

            # datasaver.add_result(
            #     (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
            #     (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
            #     (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
            #     )

            if i % 2 == 0: # if i is 0 or even
                if k < (grid_size - 1):
                    drive_voltage_x += drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
            else:
                if k < (grid_size - 1):
                    drive_voltage_x -= drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break

            # k_timing_end = datetime.datetime.now()                                                                    # timing line
            # print("k loop timing: %s" % (k_timing_end - k_timing_start))                                              # timing line

        # print("end of k loop")
        if i < (grid_size - 1):
            drive_voltage_y += drive_voltage_step # increment drive voltage
            scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y) # step y motor
        else:
            break
"""

""" temporary loop
    for i in range(grid_size):
        for k in range(grid_size):
            print("k = " + str(k))
            start_time = datetime.datetime.now()
            for i in range(int(scan_counter_acquisition_time * 1000)):
                counter_value = task1.read()
                output_value += counter_value
            end_time = datetime.datetime.now()
            result = output_value
            print("result:" + str(result))
        print("i = " + str(i))
"""
082422

faster scanning try from 082322
"""
# what this is; faster scanning try #1

scan_galvo.close()

##################################################################################### card 2 ###########################################################################

# notes: need counter; needs req. parameters

# naming the instrument
scan_galvo_card_name = "cDAQ1Mod2"

# dictionary of analog output channels
scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

# defining the instrument (ni_9263)
scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

############################################################################### def other variables #####################################################################

#################### setting variales and array ####################

# adjust factor (maintains resolution at current scanning window)
adjust_factor = 3.5

# def size of grid to scan (array is square)
grid_size = int(42 / adjust_factor)

# drive voltage step for sweep
drive_voltage_step = adjust_factor * 0.0155

# initial driving voltage for (x and y)
drive_voltage_x = -0.300

# initial driving voltage for y
drive_voltage_y = drive_voltage_x

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

#################################################### ORIGINAL FROM RIGHT #################################################################################################
scan_counter_acquisition_time = 0.003

start_fnc_call_time = datetime.datetime.now()

from tqdm.notebook import trange, tqdm

output_value = 0

with nidaqmx.Task() as task1, nidaqmx.Task() as counter_output_task:

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

    counter_output_task.start()
    task1.start()

    #####
    ############################################################################################ scanning ##################################################################

    ################### resetting position of mirrors ####################

    # x-mirror
    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x)

    # y-mirror
    scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y)

    ################ setting up QCoDeS measurement #######################

#     galvo_meas_3 = Measurement(name= "082322_scan", exp = room_temp_NV_exp_control_experiment)

#     galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao0)
#     galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao1)
#     galvo_meas_3.register_parameter(scan_counter.Scan_Counter_Read, setpoints = (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao1))

    ################ looping over grid (scanning) ############################

    # print(data_array)

    start_time = datetime.datetime.now()

    # with galvo_meas_3.run() as datasaver:

    for i in trange(grid_size): #
        # print("i = %d" % i)

        # i_timing_start = datetime.datetime.now()                                                        # timing line

        for k in range(grid_size): #
            # k_timing_start = datetime.datetime.now()                                                                    # timing line
            # print("k = %d" % k)

            # result = scan_counter.Scan_Counter_Read() # read counter (w/ delay) OLD
            start_time = datetime.datetime.now()
            for i in range(int(scan_counter_acquisition_time * 1000)):
                counter_value = task1.read()
                output_value += counter_value
            end_time = datetime.datetime.now()
            result = output_value
            
            
            if i % 2 != 0:
                data_array[i][-(k + 1)] = result # add counter result to data array
            else:
                data_array[i][k] = result # add counter result to data array
            
            output_value = 0

            # datasaver.add_result(
            #     (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
            #     (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
            #     (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
            #     )

            if i % 2 == 0: # if i is 0 or even
                if k < (grid_size - 1):
                    drive_voltage_x += drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
            else:
                if k < (grid_size - 1):
                    drive_voltage_x -= drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break

            # k_timing_end = datetime.datetime.now()                                                                    # timing line
            # print("k loop timing: %s" % (k_timing_end - k_timing_start))                                              # timing line

        # print("end of k loop")
        if i < (grid_size - 1):
            drive_voltage_y += drive_voltage_step # increment drive voltage
            scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y) # step y motor
        else:
            break

            # i_timing_end = datetime.datetime.now()                                                            # timing line
            # print("i loop timing: %s" % (i_timing_end - i_timing_start))                                              # timing line
            # print("end of i loop")

        # dataset_galvo_meas_3 = datasaver.dataset

    end_time = datetime.datetime.now()
        
#########################################################################################################################################

print("loop_time (physical reading time): " + str(end_time - start_time))
end_fnc_call_time = datetime.datetime.now()
print("total called fnc time: " + str(end_fnc_call_time - start_fnc_call_time))

 ##################################################################### visualizing scan data ############################################################################

scanning_time = end_time - start_time
print("scanning info:\n")
print("total scanning time: %s" % scanning_time)
print("counter acquisition time: %s s" % read_acquisition_time)
print("grid_size = %s" % (grid_size))

# print(data_array)

fig, axs = plt.subplots(figsize = (6, 6), layout = "constrained")
plot1 = axs.pcolormesh(data_array)
fig.colorbar(plot1, ax = axs)
axs.set_title("scan_082322");

# plot_dataset(dataset_galvo_meas_3) # QCoDeS plotting
"""

###### BREAK ###########

faster scanning try
"""
scan_galvo.close()

##################################################################################### card 2 ###########################################################################

# notes: need counter; needs req. parameters

# naming the instrument
scan_galvo_card_name = "cDAQ1Mod2"

# dictionary of analog output channels
scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

# defining the instrument (ni_9263)
scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

############################################################################### def other variables #####################################################################

#################### setting variales and array ####################

# adjust factor (maintains resolution at current scanning window)
adjust_factor = 3

# def size of grid to scan (array is square)
grid_size = int(42 / adjust_factor)

# drive voltage step for sweep
drive_voltage_step = adjust_factor * 0.0155

# initial driving voltage for (x and y)
drive_voltage_x = -0.300

# initial driving voltage for y
drive_voltage_y = drive_voltage_x

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

output_value = 0
counter_value = 0

print("initial output_value = " + str(output_value))
print("initial counter_value = " + str(counter_value))

################### resetting position of mirrors ####################

# x-mirror
scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x)

# y-mirror
scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y)

################ setting up QCoDeS measurement #######################

with nidaqmx.Task() as task1, nidaqmx.Task() as counter_output_task:

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

    # counter_output_task.start()
    # task1.start()
    
    counter_output_task.start()
    task1.start()
    
    for f in trange(grid_size): #
        output_value = 0
        counter_value = 0
        output_value == 0
        counter_value == 0
        print("f = %d" % f)

        # i_timing_start = datetime.datetime.now()                                                        # timing line

        for k in range(grid_size): #
            # k_timing_start = datetime.datetime.now()                                                                    # timing line
            print("k = %d" % k)

            # result = scan_counter.Scan_Counter_Read() # read counter (w/ delay) OLD
            ################################################################ important section #####################################################

            start_time = datetime.datetime.now()
            output_value == 0
            counter_value == 0
            print("                                      counter_value = " + str(counter_value))
            # counter_output_task.start()
            # task1.start()
            for my_var_not_named_i in range(int(scan_counter_acquisition_time * 1000)):
                counter_value = task1.read()
                output_value += counter_value
            end_time = datetime.datetime.now()

            print("                                      END END ENDcounter_value = " + str(counter_value))
            
            if f % 2 != 0:
                print("                                   output_value before append #1: " + str(output_value))
                print("                                   counter_value before append #2: " + str(counter_value))
                # print("                                   before 1 append: i = " + str(i) + " k = " + str(k))
                # if f > 0:
                    # print("________________________________________________pickoff_________ " + str(data_array[(f) -1][-((k + 1)) - 1]))
                # data_array[f][-(k + 1)] = output_value # add counter result to data array                                                    # saving
                data_array[f][-(k + 1)] = output_value - np.sum(data_array) # add counter result to data array                               # saving (082422)
                output_value == 0
                counter_value == 0
                print(data_array)
                print("APPENDED #1")
            else:
                print("                                   output_value before append #2: " + str(output_value))
                print("                                   counter_value before append #2: " + str(counter_value))
                # print("                                   before 2 append: i = " + str(i) + " k = " + str(k))
                # data_array[f * 1][k] = output_value # add counter result to data array                                                    # saving
                data_array[f * 1][k] = output_value - np.sum(data_array) # add counter result to data array                               # saving (082422)
                output_value == 0
                counter_value == 0
                print(data_array)
                print("APPENDED #2")
            output_value = 0
            counter_value = 0
            print("********************************************************* " + str(output_value))
            print("********************************************************* " + str(counter_value))

            # datasaver.add_result(
            #     (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
            #     (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
            #     (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
            #     )

            if f % 2 == 0: # if i is 0 or even
                if k < (grid_size - 1):
                    drive_voltage_x += drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
            else:
                if k < (grid_size - 1):
                    drive_voltage_x -= drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break

            # k_timing_end = datetime.datetime.now()                                                                    # timing line
            # print("k loop timing: %s" % (k_timing_end - k_timing_start))                                              # timing line

        # print("end of k loop")
        # if i < (grid_size - 1):
        #     drive_voltage_y += drive_voltage_step # increment drive voltage
        #     scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y) # step y motor
        # else:
        #     print("broken ?")
        #     break
        # if i < grid_size:
        drive_voltage_y += drive_voltage_step # increment drive voltage
        scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y) # step y motor
        # else:
        print("broken ?")
            # break
    
print("output counter value = %s" % output_value)
    
    #########################################################################################################################################

print("loop_time (physical reading time): " + str(end_time - start_time))
end_fnc_call_time = datetime.datetime.now()
# print("total called fnc time: " + str(end_fnc_call_time - start_fnc_call_time))


# print(data_array)


##################################################################### visualizing scan data ############################################################################

scanning_time = end_time - start_time
print("scanning info:\n")
print("total scanning time: %s" % scanning_time)
# print("counter acquisition time: %s s" % read_acquisition_time)
print("grid_size = %s" % (grid_size))

# print(data_array)

fig, axs = plt.subplots(figsize = (6, 6), layout = "constrained")
plot1 = axs.pcolormesh(data_array)
fig.colorbar(plot1, ax = axs)
axs.set_title("scan_082422");
"""

break

original working scanning program
"""python:
# what this is; scanning. started 081922
# X and Y scanning. No Z. Plots both manually from created data array and QCoDeS plotting (when run, data is saved as QCoDeS measurement)
# note: maintaining ratio btw grid_size and drive_voltae_step ensures only the resoulution of the scanned image changes, not the scanning window itself
# note: this cell uses functions written in "class_file"
#@ "C:\Users\lukin2dmaterials\miniconda3\envs\qcodes\Lib\site-packages\qcodes_contrib_drivers\drivers\NationalInstruments\class_file"

# close instruments
scan_counter.close()
scan_galvo.close()

#################################################################################### card 1 ############################################################################

read_acquisition_time = 0.003

scan_counter = Scan_Counter(
    "name_for_inst",
    scan_counter_device_name = "cDAQ1Mod1",
    scan_counter_counter_channel = "cDAQ1Mod1/ctr0",
    scan_counter_clock_channel = "cDAQ1Mod1/ctr1",
    scan_counter_source_channel = "/cDAQ1/Ctr1InternalOutput",
    scan_counter_sampling_rate = 1000,
    scan_counter_samples_per_channel = 1,
    scan_counter_duty_cycle = 0.5,
    scan_counter_acquisition_time = read_acquisition_time # this is in seconds. As long as sampling_rate is 1000. If not, math must change for acquisition time
    )

##################################################################################### card 2 ###########################################################################

# notes: need counter; needs req. parameters

# naming the instrument
scan_galvo_card_name = "cDAQ1Mod2"

# dictionary of analog output channels
scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

# defining the instrument (ni_9263)
scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

############################################################################### def other variables #####################################################################

#################### setting variales and array ####################

# adjust factor (maintains resolution at current scanning window)
adjust_factor = 3.5

# def size of grid to scan (array is square)
grid_size = int(42 / adjust_factor)

# drive voltage step for sweep
drive_voltage_step = adjust_factor * 0.0155

# initial driving voltage for (x and y)
drive_voltage_x = -0.300

# initial driving voltage for y
drive_voltage_y = drive_voltage_x

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

############################################################################################ scanning ##################################################################

################### resetting position of mirrors ####################

# x-mirror
scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x)

# y-mirror
scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y)

################ setting up QCoDeS measurement #######################

galvo_meas_3 = Measurement(name= "082322_scan", exp = room_temp_NV_exp_control_experiment)

galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao0)
galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao1)
galvo_meas_3.register_parameter(scan_counter.Scan_Counter_Read, setpoints = (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao1))

################ looping over grid (scanning) ############################

# print(data_array)

start_time = datetime.datetime.now()

with galvo_meas_3.run() as datasaver:
    
    for i in trange(grid_size): #
        # print("i = %d" % i)
        
        # i_timing_start = datetime.datetime.now()                                                        # timing line
        
        for k in range(grid_size): #
            # k_timing_start = datetime.datetime.now()                                                                    # timing line
            # print("k = %d" % k)
            
            result = scan_counter.Scan_Counter_Read() # read counter (w/ delay)
            if i % 2 != 0:
                data_array[i][-(k + 1)] = result # add counter result to data array
            else:
                data_array[i][k] = result # add counter result to data array
            
            datasaver.add_result(
                (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
                (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
                (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
                )
            
            if i % 2 == 0: # if i is 0 or even
                if k < (grid_size - 1):
                    drive_voltage_x += drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
            else:
                if k < (grid_size - 1):
                    drive_voltage_x -= drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
            
            # k_timing_end = datetime.datetime.now()                                                                    # timing line
            # print("k loop timing: %s" % (k_timing_end - k_timing_start))                                              # timing line
            
        # print("end of k loop")
        if i < (grid_size - 1):
            drive_voltage_y += drive_voltage_step # increment drive voltage
            scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y) # step y motor
        else:
            break
        
        # i_timing_end = datetime.datetime.now()                                                            # timing line
        # print("i loop timing: %s" % (i_timing_end - i_timing_start))                                              # timing line
        # print("end of i loop")

    dataset_galvo_meas_3 = datasaver.dataset

end_time = datetime.datetime.now()

##################################################################### visualizing scan data ############################################################################

scanning_time = end_time - start_time
print("scanning info:\n")
print("total scanning time: %s" % scanning_time)
print("counter acquisition time: %s s" % read_acquisition_time)
print("grid_size = %s" % (grid_size))

# print(data_array)

fig, axs = plt.subplots(figsize = (6, 6), layout = "constrained")
plot1 = axs.pcolormesh(data_array)
fig.colorbar(plot1, ax = axs)
axs.set_title("scan_082322");

plot_dataset(dataset_galvo_meas_3) # QCoDeS plotting
"""

last paste of old working scanning program before improving timing speed
"""
# what this is; scanning. started 081922
# X and Y scanning. No Z. Plots both manually from created data array and QCoDeS plotting (when run, data is saved as QCoDeS measurement)
# note: maintaining ratio btw grid_size and drive_voltae_step ensures only the resoulution of the scanned image changes, not the scanning window itself
# note: this cell uses functions written in "class_file"
#@ "C:\Users\lukin2dmaterials\miniconda3\envs\qcodes\Lib\site-packages\qcodes_contrib_drivers\drivers\NationalInstruments\class_file"

# close instruments
scan_counter.close()
scan_galvo.close()

#################################################################################### card 1 ############################################################################

read_acquisition_time = 0.003

scan_counter = Scan_Counter(
    "name_for_inst",
    scan_counter_device_name = "cDAQ1Mod1",
    scan_counter_counter_channel = "cDAQ1Mod1/ctr0",
    scan_counter_clock_channel = "cDAQ1Mod1/ctr1",
    scan_counter_source_channel = "/cDAQ1/Ctr1InternalOutput",
    scan_counter_sampling_rate = 1000,
    scan_counter_samples_per_channel = 1,
    scan_counter_duty_cycle = 0.5,
    scan_counter_acquisition_time = read_acquisition_time # this is in seconds. As long as sampling_rate is 1000. If not, math must change for acquisition time
    )

##################################################################################### card 2 ###########################################################################

# notes: need counter; needs req. parameters

# naming the instrument
scan_galvo_card_name = "cDAQ1Mod2"

# dictionary of analog output channels
scan_galvo_ao_channels = {f'{scan_galvo_card_name}/ao{i}': i for i in range(4)}

# defining the instrument (ni_9263)
scan_galvo = DAQAnalogOutputs("name_two", scan_galvo_card_name, scan_galvo_ao_channels)

############################################################################### def other variables #####################################################################

#################### setting variales and array ####################

# adjust factor (maintains resolution at current scanning window)
adjust_factor = 3.5

# def size of grid to scan (array is square)
grid_size = int(42 / adjust_factor)

# drive voltage step for sweep
drive_voltage_step = adjust_factor * 0.0155

# initial driving voltage for (x and y)
drive_voltage_x = -0.300

# initial driving voltage for y
drive_voltage_y = drive_voltage_x

# create dataset to populate
data_array = np.zeros((grid_size, grid_size))

############################################################################################ scanning ##################################################################

################### resetting position of mirrors ####################

# x-mirror
scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x)

# y-mirror
scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y)

################ setting up QCoDeS measurement #######################

galvo_meas_3 = Measurement(name= "082322_scan", exp = room_temp_NV_exp_control_experiment)

galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao0)
galvo_meas_3.register_parameter(scan_galvo.voltage_cdaq1mod2ao1)
galvo_meas_3.register_parameter(scan_counter.Scan_Counter_Read, setpoints = (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao1))

################ looping over grid (scanning) ############################

# print(data_array)

start_time = datetime.datetime.now()

with galvo_meas_3.run() as datasaver:
    
    for i in trange(grid_size): #
        # print("i = %d" % i)
        
        # i_timing_start = datetime.datetime.now()                                                        # timing line
        
        for k in range(grid_size): #
            # k_timing_start = datetime.datetime.now()                                                                    # timing line
            # print("k = %d" % k)
            
            result = scan_counter.Scan_Counter_Read() # read counter (w/ delay)
            if i % 2 != 0:
                data_array[i][-(k + 1)] = result # add counter result to data array
            else:
                data_array[i][k] = result # add counter result to data array
            
            datasaver.add_result(
                (scan_galvo.voltage_cdaq1mod2ao0, scan_galvo.voltage_cdaq1mod2ao0()),
                (scan_galvo.voltage_cdaq1mod2ao1, scan_galvo.voltage_cdaq1mod2ao1()),
                (scan_counter.Scan_Counter_Read, scan_counter.Scan_Counter_Read())
                )
            
            if i % 2 == 0: # if i is 0 or even
                if k < (grid_size - 1):
                    drive_voltage_x += drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
            else:
                if k < (grid_size - 1):
                    drive_voltage_x -= drive_voltage_step # increment drive voltage
                    scan_galvo.voltage_cdaq1mod2ao0(drive_voltage_x) # step x motor
                else:
                    break
            
            # k_timing_end = datetime.datetime.now()                                                                    # timing line
            # print("k loop timing: %s" % (k_timing_end - k_timing_start))                                              # timing line
            
        # print("end of k loop")
        if i < (grid_size - 1):
            drive_voltage_y += drive_voltage_step # increment drive voltage
            scan_galvo.voltage_cdaq1mod2ao1(drive_voltage_y) # step y motor
        else:
            break
        
        # i_timing_end = datetime.datetime.now()                                                            # timing line
        # print("i loop timing: %s" % (i_timing_end - i_timing_start))                                              # timing line
        # print("end of i loop")

    dataset_galvo_meas_3 = datasaver.dataset

end_time = datetime.datetime.now()

##################################################################### visualizing scan data ############################################################################

scanning_time = end_time - start_time
print("scanning info:\n")
print("total scanning time: %s" % scanning_time)
print("counter acquisition time: %s s" % read_acquisition_time)
print("grid_size = %s" % (grid_size))

# print(data_array)

fig, axs = plt.subplots(figsize = (6, 6), layout = "constrained")
plot1 = axs.pcolormesh(data_array)
fig.colorbar(plot1, ax = axs)
axs.set_title("scan_082322");

plot_dataset(dataset_galvo_meas_3) # QCoDeS plotting
"""

082622

old timing cell from speeding up scanning program
"""python:
# timing info. try

import time

scan_counter.close()

read_acquisition_time = 0.003
print("entered apd_read_time = %s s" % (read_acquisition_time))

scan_counter = Scan_Counter(
    "name_for_inst",
    scan_counter_device_name = "cDAQ1Mod1",
    scan_counter_counter_channel = "cDAQ1Mod1/ctr0",
    scan_counter_clock_channel = "cDAQ1Mod1/ctr1",
    scan_counter_source_channel = "/cDAQ1/Ctr1InternalOutput",
    scan_counter_sampling_rate = 1000,
    scan_counter_samples_per_channel = 1,
    scan_counter_duty_cycle = 0.5,
    scan_counter_acquisition_time = read_acquisition_time # this is in seconds. As long as sampling_rate is 1000. If not, math must change for acquisition time
    )

# this will "read data for one pixel"
timing_start = datetime.datetime.now()
# print("timing_start = %s" % (timing_start))
scan_counter.Scan_Counter_Read()
timing_end = datetime.datetime.now()
# difference =

# print("\n")

print("(this cell) fnc call total time: %s" % (timing_end - timing_start))
# print("differ by factor of: %d" % (difference))
"""
