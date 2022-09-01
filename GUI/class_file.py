"""
comments

dates: 081922 -> 082322
"""

from typing import Dict, Union
import numpy as np

import nidaqmx
import datetime
from nidaqmx.constants import AcquisitionType
from qcodes.instrument.base import Instrument
from qcodes.instrument.parameter import ParameterWithSetpoints, Parameter
from nidaqmx.constants import(
    Edge,
    CountDirection,
    AcquisitionType,
    FrequencyUnits
)

# TODO: remove unused imports

#########################################################################################################################################

# Scan_Counter
class Scan_Counter(Instrument):
    """
    comments

    Notes:
    1. this could eventually work for a list (using a Dict) of possible channels to use. Selection would then be different
    """

    #
    def __init__(self, name: str, scan_counter_device_name: str, scan_counter_counter_channel: str,
        scan_counter_clock_channel: str, scan_counter_source_channel: str, scan_counter_sampling_rate: int,
        scan_counter_samples_per_channel: int, scan_counter_duty_cycle: int, scan_counter_acquisition_time = float, **kwargs) -> None:
        super().__init__(name, **kwargs)

        #
        self.metadata.update({
            # "name": name,
            "scan_counter_device_name": scan_counter_device_name,
            "scan_counter_counter_channel": scan_counter_counter_channel,
            "scan_counter_clock_channel": scan_counter_clock_channel,
            "scan_counter_source_channel": scan_counter_source_channel,
            "scan_counter_sampling_rate": scan_counter_sampling_rate,
            "scan_counter_samples_per_channel": scan_counter_samples_per_channel,
            "scan_counter_duty_cycle": scan_counter_duty_cycle,
            "scan_counter_acquisition_time": scan_counter_acquisition_time
            })

        #
        self.add_parameter(
            name = "Scan_Counter_Read",
            scan_counter_device_name = scan_counter_device_name,
            scan_counter_counter_channel = scan_counter_counter_channel,
            scan_counter_clock_channel = scan_counter_clock_channel,
            scan_counter_source_channel = scan_counter_source_channel,
            scan_counter_sampling_rate = scan_counter_sampling_rate,
            scan_counter_samples_per_channel = scan_counter_samples_per_channel,
            scan_counter_duty_cycle = scan_counter_duty_cycle,
            scan_counter_acquisition_time = scan_counter_acquisition_time,
            parameter_class = Scan_Read_Counter, # commment
            label = "scan_counter_read_parameter",
            unit = "#"
            # set_cmd = ""
        )

# Scan_Read_Counter
class Scan_Read_Counter(Parameter):
    """
    comments
    """

    #
    def __init__(self, name: str, scan_counter_device_name: str, scan_counter_counter_channel: str,
        scan_counter_clock_channel: str, scan_counter_source_channel: str, scan_counter_sampling_rate: int,
        scan_counter_samples_per_channel: int, scan_counter_duty_cycle: int, scan_counter_acquisition_time: float, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.scan_counter_device_name = scan_counter_device_name
        self.scan_counter_counter_channel = scan_counter_counter_channel,
        self.scan_counter_clock_channel = scan_counter_clock_channel,
        self.scan_counter_source_channel = scan_counter_source_channel,
        self.scan_counter_sampling_rate = scan_counter_sampling_rate,
        self.scan_counter_samples_per_channel = scan_counter_samples_per_channel,
        self.scan_counter_duty_cycle = scan_counter_duty_cycle,
        self.scan_counter_acquisition_time = scan_counter_acquisition_time
    
    # #
    # def set_raw(self, arg_1: int):
    #     """
    #     comments
    #     """
        
    #     print("Hello World! This is Scan_Read_Counter set_method Arg: %s." % arg_1)

    #
    def get_raw(self):
        """
        comments
        """

        start_fnc_call_time = datetime.datetime.now()
        
        # print("Hello World! This is Scan_Read_Counter get_method.")

        from tqdm.notebook import trange, tqdm

        output_value = 0

        with nidaqmx.Task() as task1, nidaqmx.Task() as counter_output_task:

            # adding dig pulse train chan
            counter_output_task.co_channels.add_co_pulse_chan_freq(
                counter = "cDAQ1Mod1/ctr1", # this line works
                # counter = self.scan_counter_counter_channel,                  # this line makes an error I cannot fix now
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
                # samps_per_chan = self.scan_counter_samples_per_channel,                  # this line makes an error I cannot fix now
                samps_per_chan = 1
                )

            # adding count egdes chan
            task1.ci_channels.add_ci_count_edges_chan(
                # counter = self.scan_counter_counter_channel,                  # this line makes an error I cannot fix now
                counter = "cDAQ1Mod1/ctr0",
                name_to_assign_to_channel = "",
                edge = Edge.RISING,
                initial_count = 0,
                count_direction = CountDirection.COUNT_UP
                )

            # cfg sample clk timing
            task1.timing.cfg_samp_clk_timing(
                # rate = self.scan_counter_sampling_rate,                  # this line makes an error I cannot fix now
                rate = 1000,
                # source = self.scan_counter_source_channel,                  # this line makes an error I cannot fix now
                source = "/cDAQ1/Ctr1InternalOutput",
                active_edge = Edge.RISING,
                sample_mode = AcquisitionType.CONTINUOUS,
                # samps_per_chan = self.scan_counter_samples_per_channel                  # this line makes an error I cannot fix now
                samps_per_chan = 1
                )
                
            counter_output_task.start()
            task1.start()

            start_time = datetime.datetime.now()
            for i in range(int(self.scan_counter_acquisition_time * 1000)):
                counter_value = task1.read()
                output_value += counter_value
            end_time = datetime.datetime.now()
        
        # print("hello")
        # print(float(str(counter_value)[1]))
        # return float(str(counter_value)[1])
        # return counter_value

        # print("(in fnc) loop_time (physical reading time): " + str(end_time - start_time))                                     # timing line

        end_fnc_call_time = datetime.datetime.now()
        # print("(in fnc) total called fnc time: " + str(end_fnc_call_time - start_fnc_call_time))                                     # timing line

        return output_value

#####################################################

################################################################ AO ###################################################################

# AO
class DAQAnalogOutputs(Instrument):
    """Instrument to write DAQ analog output data in a qcodes Loop or measurement.

    Args:
        name: Name of instrument (usually 'daq_ao').
        dev_name: NI DAQ device name (e.g. 'Dev1').
        channels: Dict of analog output channel configuration.
        **kwargs: Keyword arguments to be passed to Instrument constructor.
    """
    def __init__(self, name: str, dev_name: str, channels: Dict[str, int], **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.metadata.update({
            'dev_name': dev_name,
            'channels': channels})
        # We need parameters in order to write voltages in a qcodes Loop or Measurement
        for ch, idx in channels.items():
            self.add_parameter(
                name=f'voltage_{"".join(c for c in ch.lower() if c.isalnum())}',
                # name = f'voltage_{ch.lower}',
                dev_name=dev_name,
                idx=idx,
                parameter_class=DAQAnalogOutputVoltage,
                label='Voltage',
                unit='V'
            )
        #print("name: "+name)

# AO extra
class DAQAnalogOutputVoltage(Parameter):
    """Writes data to one or several DAQ analog outputs. This only writes one channel at a time,
    since Qcodes ArrayParameters are not settable.

    Args:
        name: Name of parameter (usually 'voltage').
        dev_name: DAQ device name (e.g. 'Dev1').
        idx: AO channel index.
        kwargs: Keyword arguments to be passed to ArrayParameter constructor.
    """
    def __init__(self, name: str, dev_name: str, idx: int, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.dev_name = dev_name
        self.idx = idx
        self._voltage = np.nan
     
    def set_raw(self, voltage: Union[int, float]) -> None:
        with nidaqmx.Task('daq_ao_task') as ao_task:
            channel = f'{self.dev_name}/ao{self.idx}'
            ao_task.ao_channels.add_ao_voltage_chan(channel, self.name)
            ao_task.write(voltage, auto_start=True)
        self._voltage = voltage

    def get_raw(self):
        """Returns last voltage array written to outputs.
        """
        return self._voltage


######################################################################################################################################

# # Scan_Motor_X
# class Scan_Motor_X(Instrument):
#     """
#     comments
#     """

#     #
#     def __init__(self, name: str, scan_motor_device_name: str, **kwargs) -> None:
#         super().__init__(name, **kwargs)

#         #
#         self.metadata.update({
#             "name": name,
#             "scan_motor_device_name": scan_motor_device_name,
#             })

#         #
#         self.add_parameter(
#             name = "Scan_Motor_Drive_X",
#             scan_motor_device_name = scan_motor_device_name,
#             parameter_class = Scan_Motor_Drive,
#         )

# # Scan_Motor_Y
# class Scan_Motor_Y(Instrument):
#     """
#     comments
#     """

#     #
#     def __init__(self, name: str, scan_motor_device_name: str, **kwargs) -> None:
#         super().__init__(name, **kwargs)

#         #
#         self.metadata.update({
#             "name": name,
#             "scan_motor_device_name": scan_motor_device_name,
#             })

#         #
#         self.add_parameter(
#             name = "Scan_Motor_Drive_Y",
#             scan_motor_device_name = scan_motor_device_name,
#             parameter_class = Scan_Motor_Drive,
#         )

# #
# class Scan_Motor_Drive(Parameter):
#     """
#     comments
#     """

#     #
#     def __init__(self, name: str, scan_motor_device_name: str, **kwargs) -> None:
#         super().__init__(name, **kwargs)
#         self.scan_motor_device_name = scan_motor_device_name
    
#     #
#     def set_raw(self, arg_1: int):
#         """
#         comments
#         """
        
#         print("Hello World! This is Scan_Motor_Drive set_method Arg: %s." % arg_1)

#     #
#     def get_raw(self):
#         """
#         comments
#         """
        
#         print("Hello World! This is Scan_Motor_Drive get_method.")
