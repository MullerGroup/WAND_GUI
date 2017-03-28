from PyQt4.QtCore import *
from PyQt4 import QtGui
import serial
import serial.tools.list_ports # _osx ?
from bitarray import *
import struct
import time
# from binascii import hexlify
from pylibftdi import Driver, Device
import ui.ui_DataVisualizer as ui_DataVisualizer
import DataVisualizer
import datetime
import csv
import tables
from tables import *
from enum import Enum
import numpy as np
from queue import Queue
import libusb1
from ctypes import byref, create_string_buffer, c_int, sizeof, POINTER, \
    cast, c_uint8, c_uint16, c_ubyte, string_at, c_void_p, cdll, addressof, \
    c_char
import os
import math
from numpy import arange


datalen = 12

# CM register addresses
class Reg(Enum):
    ctrl = 0x00
    rst = 0x04
    n0d1 = 0x10
    n0d2 = 0x14
    n1d1 = 0x20
    n1d2 = 0x24
    req = 0xff
    cl1 = 0xDD
    cl2 = 0xEE
    cl3 = 0xCC
    cl4 = 0xBB
    cl5 = 0xAB
    cl6 = 0xCD

class stream_data(IsDescription):
    # crc = UInt8Col()
    # data = UInt16Col(shape=(96))
    # ramp = UInt16Col()
    # time = FloatCol()
    out = UInt16Col(int(datalen/2))
    time = FloatCol()

class stream_info(IsDescription):
    deadlen = UInt16Col()
    fakestim = UInt16Col()
    fftsize = UInt16Col()
    randmode = UInt16Col()
    en1 = UInt16Col()
    en0 = UInt16Col()
    enA = UInt16Col()
    chctrl = UInt16Col()
    dirA = UInt16Col()
    threshA = UInt16Col()
    chorder = UInt16Col()
    chstim = UInt16Col()
    freqmaxA = UInt16Col()
    freqminA = UInt16Col()
    randMax = UInt16Col()
    randMin = UInt16Col()
    freqmaxB = UInt16Col()
    freqminB = UInt16Col()
    enB = UInt16Col()
    dirB = UInt16Col()
    threshB = UInt16Col()
    andor = UInt16Col()
    derivative = UInt16Col()
    derivativeB = UInt16Col()
    signA = UInt16Col()
    signB = UInt16Col()

dataQueue = Queue()
timeQueue = Queue()

# CP2130 functions for reading, writing, and setting various SPI parameters

# change device to read priority
def cp2130_libusb_set_usb_config(handle):
	buf = c_ubyte * 10
	control_buf_out = buf(0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80)
	usbTimeout = 500

	error_code = libusb1.libusb_control_transfer(handle, 0x40, 0x61, 0xA5F1, 0x000A, control_buf_out, sizeof(control_buf_out), usbTimeout)
	if error_code != sizeof(control_buf_out):
		print('Error in bulk transfer')
		return False
	# print('Successfully set value of spi_word on chip:')
	# for i in control_buf_out:
	# 	print(i)
	return True

# this function always writes 5 bytes. if you want to write more than that, have to parametrize it
def cp2130_libusb_write(handle, value): # value should be a list of 5 bytes to write
    buf = c_ubyte * 13
    write_command_buf = buf(
    	0x00, 0x00,
    	0x01,
    	0x00,
    	0x01, 0x00, 0x00, 0x00)
    # populate command buffer with value to write
    write_command_buf[8:13] = value
    bytesWritten = c_int()
    usbTimeout = 500

    # print(write_command_buf[8:13])

    error_code = libusb1.libusb_bulk_transfer(handle, 0x02, write_command_buf, sizeof(write_command_buf), byref(bytesWritten), usbTimeout)
    if error_code:
        print('Error in bulk transfer (write command)! Error # {}'.format(error_code))
        return False
    return True

def cp2130_libusb_readRTR(handle):
    buf = c_ubyte * 8
    read_command_buf = buf(
        0x00, 0x00,
        0x04,
        0x00,
        datalen, 0x00, 0x00, 0x00)
    bytesWritten = c_int()
    buf = c_ubyte * datalen
    read_input_buf = buf()
    bytesRead = c_int()
    usbTimeout = 500

    error_code = libusb1.libusb_bulk_transfer(handle, 0x02, read_command_buf, sizeof(read_command_buf), byref(bytesWritten), usbTimeout)
    if error_code:
        print('Error in bulk transfer (read command). Error # {}'.format(error_code))
        return False
    if bytesWritten.value != sizeof(read_command_buf):
        print('Error in bulk transfer write size')
        print(bytesWritten.value)
        return False
    # time.sleep(0.05)
    # while(1):
    #     pass
    error_code = libusb1.libusb_bulk_transfer(handle, 0x81, read_input_buf, sizeof(read_input_buf), byref(bytesRead), usbTimeout)
    if error_code:
        print('Error in bulk transfer (read buffer). Error # {}'.format(error_code))
        return False
    # for i in read_input_buf:
    #     print('{} '.format(i), end="")
    return read_input_buf

def cp2130_libusb_read(handle):
    buf = c_ubyte * 8
    read_command_buf = buf(
        0x00, 0x00,
        0x00,
        0x00,
        datalen, 0x00, 0x00, 0x00)
    bytesWritten = c_int()
    buf = c_ubyte * datalen
    read_input_buf = buf()
    bytesRead = c_int()
    usbTimeout = 500

    error_code = libusb1.libusb_bulk_transfer(handle, 0x02, read_command_buf, sizeof(read_command_buf), byref(bytesWritten), usbTimeout)
    if error_code:
        print('Error in bulk transfer (read command). Error # {}'.format(error_code))
        return False
    if bytesWritten.value != sizeof(read_command_buf):
        print('Error in bulk transfer write size')
        print(bytesWritten.value)
        return False
    # time.sleep(0.05)
    # while(1):
    #     pass
    error_code = libusb1.libusb_bulk_transfer(handle, 0x81, read_input_buf, sizeof(read_input_buf), byref(bytesRead), usbTimeout)
    if error_code:
        print('Error in bulk transfer (read buffer). Error # {}'.format(error_code))
        return False
    if bytesRead.value != sizeof(read_input_buf):
        print('Error in bulk transfer - returned {} out of {} bytes'.format(bytesRead.value, sizeof(read_input_buf)))
        return False
    # for i in read_input_buf:
    #     print('{} '.format(i), end="")
    return read_input_buf

def cp2130_libusb_set_spi_word(handle):
    buf = c_ubyte * 2
    control_buf_out = buf(0x00, 0x09)
    usbTimeout = 500

    error_code = libusb1.libusb_control_transfer(handle, 0x40, 0x31, 0x0000, 0x0000, control_buf_out, sizeof(control_buf_out), usbTimeout)
    if error_code != sizeof(control_buf_out):
        print('Error in bulk transfer')
        return False
    # for i in control_buf_out:
    # 	print(i)
    return True

def cp2130_libusb_get_rtr_state(handle):
    buf = c_ubyte * 1
    control_buf_in = buf()
    usbTimeout = 500

    error_code = libusb1.libusb_control_transfer(handle, 0xC0, 0x36, 0x0000, 0x0000, control_buf_in, sizeof(control_buf_in), usbTimeout)
    if error_code != sizeof(control_buf_in):
        print('Error in bulk transfer')
        return False
    # print('RTR_state: ')
    # for i in control_buf_in:
    # 	print(i)
    return True


class readFTDIFifoThread(QThread):

    stim = False
    count = 1000
    rep = 1
    art = False
    interp = False
    artcount = 1000

    def __init__(self):
        QThread.__init__(self)
        self._running = True

    def __del__(self):
        self.wait()

    def stop(self):
        self._running = False

    def setup(self, stim, rep, delay, art, interp, artdelay, stimOnNM, imp, impdelay):
        self.rep = rep
        self.stim = stim
        self.count = delay
        self.art = art
        self.interp = interp
        self.artcount = artdelay + self.count
        self.stimOnNM = stimOnNM
        self.imp = imp
        self.impcount = impdelay

    def run(self):
        # make sure serial device is open
        if not CMWorker.cp2130Handle:
            return

        # reset
        if not self._running:
            # CMWorker.ser.flush()
            self._running = True

        t_0 = time.time()
        while self._running:
            # time.sleep(0.0001)
            data = cp2130_libusb_read(CMWorker.cp2130Handle)
            if data == False:
                pass
            elif (data[1] == datalen - 2) or (data[1] == 198):
                dataQueue.put(data)
                timeQueue.put(time.time() - t_0)
                if self.count > 0 and self.stim:
                    self.count = self.count - 1
                    if self.count == 0:
                        print("stimming")
                        # CMWorker().nmicCommand(0, 0x09)
                        if self.stimOnNM == 0:
                            # print("stim on 0")
                            CMWorker()._regWr(Reg.req, (self.rep << 16) | (1 << 13) | (1 << 11))
                        if self.stimOnNM == 1:
                            # print("stim on 1")
                            CMWorker()._regWr(Reg.req, (self.rep << 16) | (1 << 13) | (1 << 12))
                if self.artcount > 0:
                    self.artcount = self.artcount - 1
                    if self.artcount == 0:
                        print("artifact enable")
                        if self.art:
                            CMWorker().enableArtifact()
                        elif self.interp:
                            CMWorker().enableInterpolate()
                if self.impcount > 0 and self.imp and not self.stim:
                    self.impcount = self.impcount - 1
                    if self.impcount == 0:
                            print("impedance measure")
                            CMWorker().nmicCommand(0, 0x04)
                            CMWorker().nmicCommand(1, 0x04)

        CMWorker().disableArtifact()
        CMWorker().disableInterpolate()
        dataQueue.queue.clear()
        timeQueue.queue.clear()

class streamAdcThread(QThread):

    streamAdcData = pyqtSignal(list)
    plotfft = pyqtSignal(list)
    plotmag = pyqtSignal(list)
    display = True
    ch0 = 0
    ch1 = 0
    ch2 = 0
    ch3 = 0
    stim = True
    rep = 1
    delay = 1000
    art = False
    interp = False
    artdelay = 1000
    deadlen = (0 >> 16) & 0xFFFF
    fakestim = (0 >> 8) & 0x01
    fftsize = (0 >> 5) & 0x07
    randmode = (0 >> 4) & 0x01
    en1 = (0 >> 2) & 0x01
    en0 = 0 & 0x01
    enA = (0 >> 31) & 0x01
    chctrl = (0 >> 24) & 0x7F
    dirA = (0>>23) & 0x01
    threshA = (0 >> 8) & 0x7FFF
    chorder = (0 >> 7) & 0x01
    chstim = 0 & 0x7F
    freqmaxA = (0 >> 16) & 0x3FF
    freqminA = 0 & 0x3FF
    randMax = (0 >> 16) & 0xFF
    randMin = 0 & 0xFF
    freqmaxB = (0 >> 16) & 0x3FF
    freqminB = 0 & 0x3FF
    enB = (0 >> 31) & 0x01
    dirB = (0 >> 23) & 0x01
    threshB = (0 >> 8) & 0x7FFF
    andor = (0 >> 7) & 0x01
    derivative = 0;
    derivativeB = 0;
    signA = 0;
    signB = 0;

    filename = ''

    def __init__(self):
        QThread.__init__(self)
        self._running = True
        self.ftdiFIFO = readFTDIFifoThread()

    def __del__(self):
        self.wait()

    def stop(self):
        self._running = False
        return self.filename + '.txt'

    def setup(self, disp, stim, ch0, ch1, ch2, ch3, rep, delay, art, interp, artdelay, stimOnNM, imp, impdelay):
        self.ch0 = ch0
        self.ch1 = ch1
        self.ch2 = ch2
        self.ch3 = ch3
        self.display = disp
        self.stim = stim
        self.rep = rep
        self.delay = delay
        self.art = art
        self.interp = interp
        self.artdelay = artdelay
        self.stimOnNM = stimOnNM
        self.imp = imp
        self.impdelay = impdelay
        self.fft_data = []
        self.mag_data = []
        if stim:
            print("Streaming with stim")
        elif imp:
            print("Streaming with impedance measurement")
        # print(art)
        # print(interp)
        # print(artdelay)

    def writeCLInfo(self, deadlen, fakestim, fftsize, randmode, en1, en0,
                    enA, chctrl, dirA, threshA, chorder, chstim,
                    freqmaxA, freqminA, randMax, randMin, freqmaxB, freqminB,
                    enB, dirB, threshB, andor, derivative, signA, signB, derivativeB):
        self.deadlen = deadlen
        self.fakestim = fakestim
        self.fftsize = fftsize
        self.randmode = randmode
        self.en1 = en1
        self.en0 = en0
        self.enA = enA
        self.chctrl = chctrl
        self.dirA = dirA
        self.threshA = threshA
        self.chorder = chorder
        self.chstim = chstim
        self.freqmaxA = freqmaxA
        self.freqminA = freqminA
        self.randMax = randMax
        self.randMin = randMin
        self.freqmaxB = freqmaxB
        self.freqminB = freqminB
        self.enB = enB
        self.dirB = dirB
        self.threshB = threshB
        self.andor = andor
        self.derivative = derivative
        self.derivativeB = derivativeB
        self.signA = signA
        self.signB = signB


    def run(self):
        # make sure serial device is open
        if not CMWorker.cp2130Handle:
            return

        # reset
        if not self._running:
            self._running = True

        os.makedirs('streams', exist_ok=True)
        self.filename = 'streams/' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.saveFile = tables.open_file(self.filename + '.hdf', mode="w", title="Stream")
        self.dataGroup = self.saveFile.create_group("/", name='dataGroup', title='Recorded Data Group')
        self.dataTable = self.saveFile.create_table(self.dataGroup, name='dataTable', title='Recorded Data Table', description=stream_data, expectedrows=60000*5*1)
        self.infoGroup = self.saveFile.create_group("/", name='infoGroup', title='Recording Information Group')
        self.infoTable = self.saveFile.create_table(self.infoGroup, name='infoTable', title='Recording Information Table', description=stream_info)

        start = datetime.datetime.now()
        print("Stream started at: {}".format(start))
        data_point = self.infoTable.row

        data_point['deadlen'] = self.deadlen
        data_point['fakestim'] = self.fakestim
        data_point['fftsize'] = self.fftsize
        data_point['randmode'] = self.randmode
        data_point['en1'] = self.en1
        data_point['en0'] = self.en0
        data_point['enA'] = self.enA
        data_point['chctrl'] = self.chctrl
        data_point['dirA'] = self.dirA
        data_point['threshA'] = self.threshA
        data_point['chorder'] = self.chorder
        data_point['chstim'] = self.chstim
        data_point['freqmaxA'] = self.freqmaxA
        data_point['freqminA'] = self.freqminA
        data_point['randMax'] = self.randMax
        data_point['randMin'] = self.randMin
        data_point['freqmaxB'] = self.freqmaxB
        data_point['freqminB'] = self.freqminB
        data_point['enB'] = self.enB
        data_point['dirB'] = self.dirB
        data_point['threshB'] = self.threshB
        data_point['andor'] = self.andor
        data_point['derivative'] = self.derivative
        data_point['signA'] = self.signA
        data_point['signB'] = self.signB
        data_point['derivativeB'] = self.derivativeB

        data_point.append()
        self.infoTable.flush()

        CMWorker().startStream() # put CM into streaming mode for both NMs
        time.sleep(0.07)

        out = []
        success = 0
        crcs = 0
        fail = 0
        samples = 0
        t_0 = time.time()

        # initialize ftdiFIFO thread and start it
        self.ftdiFIFO.setup(self.stim, self.rep, self.delay, self.art, self.interp, self.artdelay, self.stimOnNM, self.imp, self.impdelay)
        self.ftdiFIFO.start()
        timeout = False
        while self._running:
            try:
                data = dataQueue.get(timeout=5)
            except:
                timeout = True
                print('timeout reading from data queue at sample {}'.format(samples))
                self.streamAdcData.emit(out)
                out = []
            if not timeout:
                try:
                    data_time = timeQueue.get(timeout=5)
                except:
                    timeout = True
                    print('timeout reading from time queue at sample {}'.format(samples))
            if not timeout:
                samples = samples + 1
                if data[0]==0x00: # no CRC
                    success += 1
                    data_point = self.dataTable.row
                    data_point['out'] = [data[0] if i == 0 else (data[i + 1] << 8 | data[i]) for i in list(range(0, datalen - 1, 2))]
                    if self.display:
                        # out.append([(data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(2*(self.chStart + 1), 2*(self.chStart + 5), 2))])
                        out.append([(data[i + 1] << 8 | data[i]) & 0xFFFF for i in [2, 4, 10]])
                        
                        # real = (data[7] << 8 | data[6]) 
                        # if real >= 0x8000:
                        #     real -= 0x10000
                        # imag = (data[9] << 8 | data[8])
                        # if imag >= 0x8000:
                        #     imag -= 0x10000
                        mag = ((data[9] << 24) | (data[8] << 16) | (data[7] << 8) | data[6])
                        # self.fft_data.append(real**2 + imag**2)
                        # self.mag_data.append(mag)

                        # real = (data[13] << 8 | data[12]) 
                        # if real >= 0x8000:
                        #     real -= 0x10000
                        # imag = (data[15] << 8 | data[14])
                        # if imag >= 0x8000:
                        #     imag -= 0x10000
                        # mag = (data[9] << 8 | data[8])
                        # self.fft_data.append(real**2 + imag**2)
                        self.mag_data.append(mag)

                        if (data[3] & 0x80 == 0x80 and self.chorder == 1):
                            if (len(self.mag_data) & (len(self.mag_data) - 1) == 0):
                                # self.plotfft.emit(self.fft_data)
                                self.plotmag.emit(self.mag_data)
                            # self.fft_data = []
                            self.mag_data = []
                        if (data[5] & 0x80 == 0x80 and self.chorder == 0):
                            if (len(self.mag_data) & (len(self.mag_data) - 1) == 0):
                                # self.plotfft.emit(self.fft_data)
                                self.plotmag.emit(self.mag_data)
                            # self.fft_data = []
                            self.mag_data = []
                        # real = - ((data[7] << 8 | data[6]) & 0x8000) | ((data[7] << 8 | data[6]) & 0x7FFF)
                        # imag = - ((data[9] << 8 | data[8]) & 0x8000) | ((data[9] << 8 | data[8]) & 0x7FFF)
                        
                        # if len(self.fft_data) == 1024:
                        #     # self.plotfft.emit(self.fft_data)
                        #     self.plotfft.emit(list(range(0,1024)))
                    data_point['time'] = data_time
                    data_point.append()

                elif data[0] == 0xFF: # CRC
                    crcs += 1
                    success += 1
                    data_point = self.dataTable.row
                    data_point['out'] = [data[0] if i == 0 else (data[i + 1] << 8 | data[i]) for i in list(range(0, datalen - 1, 2))]
                    # if self.display:
                    #     # out.append([(data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(2*(self.chStart + 1), 2*(self.chStart + 5), 2))])
                    #     out.append([(data[i + 1] << 8 | data[i]) & 0x7FFF for i in [2*(self.ch0 + 1), 2*(self.ch1 + 1), 2*(self.ch2 + 1), 2*(self.ch3 + 1)]])
                    # if self.display:
                    #     # out.append([(data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(2*(self.chStart + 1), 2*(self.chStart + 5), 2))])
                    #     # out.append([(data[i + 1] << 8 | data[i]) & 0xFFFF for i in [2*(0 + 1), 2*(1 + 1), 2*(2 + 1), 2*(3 + 1), 2*(4 + 1)]])
                        
                    #     if data[3] & 0x80:
                    #         self.fft_data = []
                    #     # real = - ((data[7] << 8 | data[6]) & 0x8000) | ((data[7] << 8 | data[6]) & 0x7FFF)
                    #     # imag = - ((data[9] << 8 | data[8]) & 0x8000) | ((data[9] << 8 | data[8]) & 0x7FFF)
                    #     real = (data[7] << 8 | data[6]) 
                    #     if real >= 0x8000:
                    #         real -= 0x10000
                    #     imag = (data[9] << 8 | data[8])
                    #     if imag >= 0x8000:
                    #         imag -= 0x10000
                    #     self.fft_data.append(real**2 + imag**2)
                    #     if len(self.fft_data) == 1024:
                    #         self.plotfft.emit(self.fft_data)
                    data_point['time'] = data_time
                    data_point.append()

                else: # should never get here?
                    fail += 1

                # flush the tables every 1000 samples (any speed up?)
                if samples%1000 == 0:
                    self.dataTable.flush()
                if samples%50 == 0 and self.display:
                    self.streamAdcData.emit(out)
                    out = []
            timeout = False
            #TODO: add plotting during streaming (activated via checkbox) only on displayed channels

        self.ftdiFIFO.stop() # turn off FTDI fifo reading thread
        print("Stream ended at: {}".format(datetime.datetime.now()))
        print("CRCs: {}".format(crcs))
        print("Received Samples: {}".format(samples))
        time.sleep(0.5)

        CMWorker().stopStream() # turn off streaming mode
        print("End of Stream")
        print("Fifos Flushed")

        self.saveFile.close()

class CMWorker(QThread):
    connStateChanged = pyqtSignal(bool)
    boardsChanged = pyqtSignal(list)
    regReadData = pyqtSignal(int, int, int)
    updateChannels = pyqtSignal(list)
    writeCLInfo = pyqtSignal(int, int)
    saveRegs = pyqtSignal(str, int)

    enabledChannels = [65535,65535,65535,65535,65535,65535,0,0]

    # ser = Device(lazy_open=True)

    # initializing libusb and device things
    context = libusb1.libusb_context_p()
    deviceList = libusb1.libusb_device_p_p()
    deviceCount = 0
    deviceDescriptor = libusb1.libusb_device_descriptor()
    device = libusb1.libusb_device_p()
    cp2130Handle = libusb1.libusb_device_handle_p()
    kernelAttached = 0
    if libusb1.libusb_init(byref(context)) != 0:
        print('Could not initialize libusb!')

    def __init__(self, parent=None):
        super().__init__(parent)

    def __del__(self):
        # wait for the thread to finish before destroying object
        self.wait()

    def _flushRadio(self):
        cp2130_libusb_write(CMWorker.cp2130Handle, [0xAA, *struct.pack('>I',0x00)])

    def _regWr(self, reg, value):
        cp2130_libusb_write(CMWorker.cp2130Handle, [reg.value, *struct.pack('>I', value)])

    def _resetIF(self):
        # reset AM
        self._regWr(Reg.ctrl, 0x103)
        # reset all NMs
        self._regWr(Reg.rst, 0xFFFF)
        self._regWr(Reg.ctrl, 0x102)

    def _sendCmd(self, nm, cmd):
        print('Send Command')
        if nm==0:
            self._regWr(Reg.n0d2, 1<<10 | (cmd & 0x3FF))
            self._regWr(Reg.ctrl, 0x1010)
        if nm==1:
            self._regWr(Reg.n1d2, 1<<10 | (cmd & 0x3FF))
            self._regWr(Reg.ctrl, 0x2020)

    def _regOp(self, nm, addr, data, write):
        buf = c_ubyte*200
        d = buf()
        count = 0
        if nm==0:
            self._regWr(Reg.n0d1, 1 if write else 0)
            time.sleep(0.005)
            self._regWr(Reg.n0d2, addr << 16 | data)
            time.sleep(0.005)
            self._regWr(Reg.ctrl, 0x1000)
            time.sleep(0.005)
            if not write:
                self._flushRadio()
                self._regWr(Reg.req, 0x0100)
                time.sleep(0.05)
                while d[1] != 4 and count < 20:
                    d = cp2130_libusb_read(CMWorker.cp2130Handle)
                    count = count + 1
                    time.sleep(0.0008)
                success = (d[1] == 4)
                add = d[2] + 256*d[3]
                val = d[4] + 256*d[5]
                return [success, add, val]

        if nm==1:
            self._regWr(Reg.n1d1, 1 if write else 0)
            time.sleep(0.001)
            self._regWr(Reg.n1d2, addr << 16 | data)
            time.sleep(0.001)
            self._regWr(Reg.ctrl, 0x2000)
            time.sleep(0.001)
            if not write:
                self._flushRadio()
                self._regWr(Reg.req, 0x0200)
                time.sleep(0.05)
                while d[1] != 4 and count < 150:
                    d = cp2130_libusb_read(CMWorker.cp2130Handle)
                    count = count + 1
                    time.sleep(0.0008)
                success = (d[1] == 4)
                add = d[2] + 256 * d[3]
                val = d[4] + 256 * d[5]
                return [success, add, val]

    def exit_cp2130(self):
        if self.cp2130Handle:
            libusb1.libusb_release_interface(self.cp2130Handle, 0)
        if self.kernelAttached:
            libusb1.libusb_attach_kernel_driver(self.cp2130Handle,0)
            if self.cp2130Handle:
                libusb1.libusb_close(self.cp2130Handle)
            if self.deviceList:
                libusb1.libusb_free_device_list(self.deviceList, 1)
            if self.context:
                libusb1.libusb_exit(self.context)

    @pyqtSlot()
    def refreshBoards(self):
        dev_list = []
        deviceCount = libusb1.libusb_get_device_list(self.context, byref(self.deviceList))
        if deviceCount <= 0:
            print('No devices found!')
        for i in range(0, deviceCount):
            if libusb1.libusb_get_device_descriptor(self.deviceList[i], byref(self.deviceDescriptor)) == 0:
                if (self.deviceDescriptor.idVendor == 0x10C4) and (self.deviceDescriptor.idProduct == 0x87A0):
                    dev_list.append(self.deviceList[i])
                    self.device = self.deviceList[i]
        # TODO: how to get device desciptor from libusb1?
        if dev_list:
            self.boardsChanged.emit(["cp2130"])
        else:
            self.boardsChanged.emit([])

    @pyqtSlot(str)
    def connectToBoard(self, board):
        # open device
        if libusb1.libusb_open(self.device, byref(self.cp2130Handle)) != 0:
            print('Could not open device!')
            return
        # See if a kernel driver is active already, if so detach it and store a flag so we can reattach when we are done
        if libusb1.libusb_kernel_driver_active(self.cp2130Handle, 0) != 0:
            libusb1.libusb_detach_kernel_driver(self.cp2130Handle, 0)
            self.kernelAttached = 1
        # claim the device
        if libusb1.libusb_claim_interface(self.cp2130Handle, 0) != 0:
            print('Could not claim interface!')
            return
        print("Connected to {}".format(board))
        cp2130_libusb_set_spi_word(self.cp2130Handle)
        cp2130_libusb_set_usb_config(self.cp2130Handle)
        self.connStateChanged.emit(True)

    @pyqtSlot(str)
    def disconnectBoard(self, board):
        self.exit_cp2130()
        print("Disconnected from {}".format(board))
        self.connStateChanged.emit(False)
        self.refreshBoards()

    @pyqtSlot(int, int)
    def nmicCommand(self, nm, cmd):
        if not self.cp2130Handle:
            return
        self._sendCmd(nm, cmd)

    @pyqtSlot(int, int, int)
    def writeReg(self, nm, addr, value):
        if not self.cp2130Handle:
            return
        self._regOp(nm, addr, value, True)
        #print("Write register: {:04x} {:04x}".format(addr, value))
        self.regReadData.emit(nm, addr, value)
        if addr == 0x04:
            if nm == 0:
                self.enabledChannels[0] = value
            else:
                self.enabledChannels[4] = value
        elif addr == 0x05:
            if nm == 0:
                self.enabledChannels[1] = value
            else:
                self.enabledChannels[5] = value
        elif addr == 0x06:
            if nm == 0:
                self.enabledChannels[2] = value
            else:
                self.enabledChannels[6] = value
        elif addr == 0x07:
            if nm == 0:
                self.enabledChannels[3] = value
            else:
                self.enabledChannels[7] = value
        self.updateChannels.emit(self.enabledChannels)

    @pyqtSlot(int, int)
    def readReg(self, nm, addr):
        if not self.cp2130Handle:
            return
        ret = [False, 0, 0]
        tries = 0
        while (tries < 20) and not(ret[0] and addr == ret[1]):
            ret = self._regOp(nm, addr, 0, False)
            tries = tries + 1
            # time.sleep(0.001)
        if tries < 10:
            print("Read register from NM {}: {:04x} {:04x}".format(nm, addr, ret[2]))
            if addr == 0x04:
                if nm == 0:
                    self.enabledChannels[0] = ret[2]
                else:
                    self.enabledChannels[4] = ret[2]
            elif addr == 0x05:
                if nm == 0:
                    self.enabledChannels[1] = ret[2]
                else:
                    self.enabledChannels[5] = ret[2]
            elif addr == 0x06:
                if nm == 0:
                    self.enabledChannels[2] = ret[2]
                else:
                    self.enabledChannels[6] = ret[2]
            elif addr == 0x07:
                if nm == 0:
                    self.enabledChannels[3] = ret[2]
                else:
                    self.enabledChannels[7] = ret[2]
            self.updateChannels.emit(self.enabledChannels)
            self.regReadData.emit(nm, addr, ret[2])
        else:
            print("Failed to read register{:04x}".format(addr))
        return ret

    @pyqtSlot(str)
    def regFile(self, fn):
        self.saveRegs.emit(fn, 0)
        self.saveRegs.emit(fn, 1)

    @pyqtSlot()
    def testCommOn(self):
        if not self.cp2130Handle:
            return
        print("Test Comm On")
        self._regWr(Reg.req, 0x00000080) # enable test

    @pyqtSlot()
    def testCommOff(self):
        if not self.cp2130Handle:
            return
        print("Test Comm Off")
        self._regWr(Reg.req, 0x00000040)  # disable test

    @pyqtSlot()
    def setupRecording(self):
        if not self.cp2130Handle:
            return
        self.writeReg(0, 0x11, 0x4000)
        time.sleep(0.01)
        self._sendCmd(0, 0x0a)
        self.writeReg(1, 0x11, 0x4000)
        time.sleep(0.01)
        self._sendCmd(1, 0x0a)

        time.sleep(0.05)
        ret0 = self.readReg(0, 0x11)
        if not ret0[0]:
            print("Register readback failed for NM0 - try again")
            return
        if ret0[2] != 0x4000:
            print("Register write failed for NM0 - try again")
            return
        ret1 = self.readReg(1, 0x11)
        if not ret1[0]:
            print("Register write failed for NM1 - try again")
            return
        if ret1[2] != 0x4000:
            print("Register write failed for NM1 - try again")
            return
        print("Recording setup successfully. You may begin stream.")

    @pyqtSlot()
    def setupStim(self):
        if not self.cp2130Handle:
            return
        # write stim registers for NM0
        self.writeReg(0, 16, 0x82)
        time.sleep(0.01)
        self.writeReg(0, 17, 0x1082)
        time.sleep(0.01)
        self.writeReg(0, 18, 0x7)
        time.sleep(0.01)
        self.writeReg(0, 19, 0x7)
        time.sleep(0.01)
        self.writeReg(0, 20, 0x7)
        time.sleep(0.01)
        self.writeReg(0, 21, 0x7)
        time.sleep(0.01)
        self.writeReg(0, 22, 0x0)
        time.sleep(0.01)
        self.writeReg(0, 23, 0x260)
        time.sleep(0.01)
        self.writeReg(0, 24, 0x64)
        time.sleep(0.01)
        self.writeReg(0, 25, 0x0)
        time.sleep(0.01)
        self.writeReg(0, 26, 0x275C)
        time.sleep(0.01)
        self.writeReg(0, 27, 0x0)
        time.sleep(0.01)
        self.writeReg(0, 28, 0x0)
        time.sleep(0.01)
        self.writeReg(0, 29, 0x0)
        time.sleep(0.01)
        self.writeReg(0, 30, 0x62)
        time.sleep(0.01)

        self.writeReg(1, 16, 0x82)
        time.sleep(0.01)
        self.writeReg(1, 17, 0x1082)
        time.sleep(0.01)
        self.writeReg(1, 18, 0x7)
        time.sleep(0.01)
        self.writeReg(1, 19, 0x7)
        time.sleep(0.01)
        self.writeReg(1, 20, 0x7)
        time.sleep(0.01)
        self.writeReg(1, 21, 0x7)
        time.sleep(0.01)
        self.writeReg(1, 22, 0x0)
        time.sleep(0.01)
        self.writeReg(1, 23, 0x260)
        time.sleep(0.01)
        self.writeReg(1, 24, 0x64)
        time.sleep(0.01)
        self.writeReg(1, 25, 0x0)
        time.sleep(0.01)
        self.writeReg(1, 26, 0x275C)
        time.sleep(0.01)
        self.writeReg(1, 27, 0x0)
        time.sleep(0.01)
        self.writeReg(1, 28, 0x0)
        time.sleep(0.01)
        self.writeReg(1, 29, 0x0)
        time.sleep(0.01)
        self.writeReg(1, 30, 0x102)
        time.sleep(0.01)

        # clear error
        self.nmicCommand(0, 0x02)
        time.sleep(0.01)
        self.nmicCommand(1, 0x02)
        time.sleep(0.01)

        # HV load
        self.nmicCommand(0, 0x03)
        time.sleep(0.01)
        self.nmicCommand(1, 0x03)
        time.sleep(0.01)

        # stim transfer
        self.nmicCommand(0, 0x0a)
        time.sleep(0.01)
        self.nmicCommand(1, 0x0a)
        time.sleep(0.01)

        # clear error again
        self.nmicCommand(0, 0x02)
        time.sleep(0.01)
        self.nmicCommand(1, 0x02)
        time.sleep(0.01)

    @pyqtSlot(Reg, int)
    def writeCL(self, addr, val):
        # print(hex(addr.value))
        # print(bin(value))
        if not self.cp2130Handle:
            return
        self._regWr(addr, val & 0xFFFFFFFF)
        self.writeCLInfo.emit(addr.value ,val & 0xFFFFFFFF)

    @pyqtSlot(int, int)
    def writeCLCh(self, ctrl, stim):
        rec0_0 = 0;
        if ctrl <= 15:
            rec0_0 |= 0x01 << ctrl
        if stim <= 15:
            rec0_0 |= 0x01 << stim

        rec0_1 = 0;
        if ctrl > 15 and ctrl <= 31:
            rec0_1 |= 0x01 << (ctrl - 16)
        if stim > 15 and stim <= 31:
            rec0_1|= 0x01 << (stim - 16)

        rec0_2 = 0;
        if ctrl > 31 and ctrl <= 47:
            rec0_2 |= 0x01 << (ctrl - 32)
        if stim > 31 and stim <= 47:
            rec0_2 |= 0x01 << (stim - 32)

        rec0_3 = 0;
        if ctrl > 47 and ctrl <= 63:
            rec0_3 |= 0x01 << (ctrl - 48)
        if stim > 47 and stim <= 63:
            rec0_3 |= 0x01 << (stim - 48)

        rec1_0 = 0;
        if ctrl > 63 and ctrl <= 79:
            rec1_0 |= 0x01 << (ctrl - 64)
        if stim > 63 and stim <= 79:
            rec1_0 |= 0x01 << (stim - 64)

        rec1_1 = 0;
        if ctrl > 79 and ctrl <= 95:
            rec1_1 |= 0x01 << (ctrl - 80)
        if stim > 79 and stim <= 95:
            rec1_1 |= 0x01 << (stim - 80)

        rec1_2 = 0;
        if ctrl > 95 and ctrl <= 111:
            rec1_2 |= 0x01 << (ctrl - 96)
        if stim > 95 and stim <= 111:
            rec1_2 |= 0x01 << (stim - 96)

        rec1_3 = 0;
        if ctrl > 111 and ctrl <= 127:
            rec1_3 |= 0x01 << (ctrl - 112)
        if stim > 111 and stim <= 127:
            rec1_3 |= 0x01 << (stim - 112)

        self.writeReg(0,0x04, rec0_0)
        time.sleep(0.01)
        self.writeReg(0,0x05, rec0_1)
        time.sleep(0.01)
        self.writeReg(0,0x06, rec0_2)
        time.sleep(0.01)
        self.writeReg(0,0x07, rec0_3)
        time.sleep(0.01)
        self.writeReg(1,0x04, rec1_0)
        time.sleep(0.01)
        self.writeReg(1,0x05, rec1_1)
        time.sleep(0.01)
        self.writeReg(1,0x06, rec1_2)
        time.sleep(0.01)
        self.writeReg(1,0x07, rec1_3)
        time.sleep(0.01)


    # @pyqtSlot()
    def enableArtifact(self):
        if not self.cp2130Handle:
            return
        self._regWr(Reg.req, 0x0080)
        print("Enabled Artifact Removal")

    # @pyqtSlot()
    def disableArtifact(self):
        if not self.cp2130Handle:
            return
        self._regWr(Reg.req, 0x0040)
        print("Disabled Artifact Removal")

    # @pyqtSlot()
    def enableInterpolate(self):
        if not self.cp2130Handle:
            return
        self._regWr(Reg.req, 0x8000)
        print("Enabled Artifact Interpolation")

    # @pyqtSlot()
    def disableInterpolate(self):
        if not self.cp2130Handle:
            return
        self._regWr(Reg.req, 0x4000)
        print("Disabled Artifact Interpolation")

    def startStream(self):
        if not self.cp2130Handle:
            return
        self._regWr(Reg.req, 0x0020)

    def stopStream(self):
        if not self.cp2130Handle:
            return
        self._regWr(Reg.req, 0x0010)
        # self._regWr(Reg.req, 0x0000)