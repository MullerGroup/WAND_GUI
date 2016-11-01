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

datalen = 200
ecglen = 8

# CM register addresses
class Reg(Enum):
    ctrl = 0x00
    rst = 0x04
    n0d1 = 0x10
    n0d2 = 0x14
    n1d1 = 0x20
    n1d2 = 0x24
    req = 0xff

class stream_data(IsDescription):
    # crc = UInt8Col()
    # data = UInt16Col(shape=(96))
    # ramp = UInt16Col()
    # time = FloatCol()
    out = UInt16Col(int((ecglen-2)/2))
    time = FloatCol()

class stream_info(IsDescription):
    channels = UInt16Col(shape=(8))

# data queue used to read out FTDI fifo data and store it locally by readFTDIFifoThread class
dataQueue = Queue()

# another queue used to store the "time stamps" for the data pulled from FTDI fifo
# this ensures we record the time the sample arrived at the PC instead of the time it was written to file
timeQueue = Queue()

class readFTDIFifoThread(QThread):

    fail = 0
    misalignment_flag = 0
    temp1 = 0
    temp2 = 0
    # binaryFile = open('streams/' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.txt', mode='wb')

    def __init__(self):
        QThread.__init__(self)
        self._running = True
        self.stimFlag = False

    def __del__(self):
        self.wait()

    def stop(self):
        self._running = False

    def stim(self):
        # print('FIFO Thread Pulse Stim')
        self.stimFlag = True

    def run(self):
        # make sure serial device is open
        if not CMWorker.ser._opened:
            return

        # reset
        if not self._running:
            CMWorker.ser.flush()
            self._running = True

        t_0 = time.time()
        while self._running:
            if self.misalignment_flag == 0:
                data = []
            self.misalignment_flag = 0
            count1 = 0
            while (len(data) != ecglen):
                temp = CMWorker.ser.read(ecglen - len(data), timeout=0)
                data.extend(temp)
                count1 += 1
                if count1 == 200:
                    print('Stream dead')
                    self._running = False
                    CMWorker()._regWr(Reg.req, 0x0000)
                    break
            # self.binaryFile.write(bytearray(data))

            if len(data)==ecglen and ((data[0]==0xAA)) and data[len(data)-1]==0x55:
                # pass
                dataQueue.put(data)
                timeQueue.put(time.time() - t_0)
            else:
                # keep reading from serial until we reach end-of-packet byte (flush until next packet)
                # print("missed at least one sample")
                # self.fail += 1
                # temp = 0
                # tries = 0
                # while (temp != b'U'): # b'U' is 0x55 (end of packet byte)
                #     temp = CMWorker.ser.read(1, timeout=0)
                #     tries += 1
                # print("Misalignment! length of data = {}, header = {}, footer = {}".format(len(data),data[0], data[len(data)-1]))
                # print("Number of bytes flushed to fix misalignment: {}".format(tries))

                self.fail += 1
                tries = 0
                self.temp1 = CMWorker.ser.read(1, timeout=0)
                self.temp2 = CMWorker.ser.read(1, timeout=0)
                while self.temp1 != b'U' and self.temp2!= b'\xAA':
                    self.temp1 = self.temp2
                    self.temp2 = CMWorker.ser.read(1, timeout=0)
                    tries += 1
                self.misalignment_flag = 1
                data = []
                data.extend(self.temp2)
                # print("Misalignment! length of data = {}, header = {}, footer = {}".format(len(data),data[0], data[len(data)-1]))
                # print("Number of bytes flushed to fix misalignment: {}".format(tries))
            if self.stimFlag:
                self.stimFlag = False
                CMWorker()._sendCmd(0, 0x09)


class streamAdcThread(QThread):

    stim = pyqtSignal()

    streamAdcData = pyqtSignal(list)
    streamChunkSize = 1
    plotChunkSize = 100
    read_count = 0



    def __init__(self):
        QThread.__init__(self)
        # print("turned ON streaming mode")
        self._running = True
        self.stim = False

    def __del__(self):
        # if CMWorker.ser._opened:
            # CMWorker()._regWr(Reg.req, 0x0000) # turn off streaming mode
        # print("turned OFF streaming mode")
        self.wait()

    def stop(self):
        # self.terminate()
        self._running = False
        CMWorker()._regWr(Reg.req, 0x0000)

    @pyqtSlot()
    def pulseStim(self):
        if self._running:
            # print('Stream Thread Pulse Stim')
            self.stim = True


    def run(self):
        # make sure serial device is open
        if not CMWorker.ser._opened:
            return

        # reset
        if not self._running:
            CMWorker.ser.flush()
            self._running = True


        # # # get file for saving using datetime
        # self.file = 'streams/' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.csv'
        #
        # self.fn = open(self.file, 'w')
        # self.csvfile = csv.writer(self.fn)
        #
        # self.csvfile.writerow(CMWorker.enabledChannels)
        #
        # start = datetime.datetime.now()
        # print("Stream started at: {}".format(start))
        # self.csvfile.writerow([start])

        # self.saveFile = tables.open_file('streams/' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.hdf', mode="w", title="Stream")
        # self.dataGroup = self.saveFile.create_group("/", name='dataGroup', title='Recorded Data Group')
        # self.dataTable = self.saveFile.create_table(self.dataGroup, name='dataTable', title='Recorded Data Table', description=stream_data, expectedrows=60000*5*1)
        # self.infoGroup = self.saveFile.create_group("/", name='infoGroup', title='Recording Information Group')
        # self.infoTable = self.saveFile.create_table(self.infoGroup, name='infoTable', title='Recording Information Table', description=stream_info)

        start = datetime.datetime.now()
        print("Stream started at: {}".format(start))
        # data_point = self.infoTable.row
        # data_point['channels'] = CMWorker.enabledChannels
        # data_point.append()
        # self.infoTable.flush()

        CMWorker()._regWr(Reg.req, 0x0030 | self.streamChunkSize<<16) # put CM into streaming mode for both NMs

        out = []
        self.read_count = 0
        success = 0
        crcs = 0
        # fail = 0
        samples = 0
        misalignments = []
        t_0 = time.time()
        count = 0

        # initialize ftdiFIFO thread and start it
        ftdiFIFO = readFTDIFifoThread()
        ftdiFIFO.start()


        while self._running:
            if self.stim:
                ftdiFIFO.stim()
                self.stim = False
            # changed the number of bytes to read to 200: this includes 96 channels + 6 bytes of accelerometer data
            samples += 1
            count += 1
            # data = []
            # count1 = 0
            # while (len(data) != 200):
            #     temp = CMWorker.ser.read(200 - len(data), timeout=0)
            #     data.extend(temp)
            #     count1 += 1
            #     if count1 == 200:
            #         print('Stream dead')
            #         self._running = False
            #         CMWorker()._regWr(Reg.req, 0x0000)
            #         break
            data = dataQueue.get()
            data_time = timeQueue.get()


            # data = []
            # data_time = 0
            if data[0]==0xAA:
                out.append([(data[i + 1] << 8 | data[i]) & 0x7FFF if i > 9 else (data[i + 1] << 8 | data[i]) for i in list(range(1, 7, 2))])
                if count == 20:
                    count = 0
                    self.streamAdcData.emit(out)
                    out = []

                # success += 1
                # #out.append([(((data[i+1] << 8 | data[i]) & 0xFFFF) + 2**15) % 2**16 - 2**15 if i > 192 else (-((data[i+1] << 8 | data[i]) & 0x7FFF) if (data[i+1] & 2**7) else (data[i+1] << 8 | data[i]) & 0x7FFF )for i in list(range(1,199,2))])
                # # neural data (i<192) is unsigned 15-bit (16th bit is stim info)
                # # accelerometer data is 2's complement
                # #out.append([(((data[i+1] << 8 | data[i]) & 0xFFFF) + 2**15) % 2**16 - 2**15 if i > 192 else (data[i+1] << 8 | data[i]) & 0x7FFF for i in list(range(1,199,2))])
                # # out = [data[0] if i == -1 else ((data[i + 1] << 8 | data[i]) & 0x7FFF if i < 193 else (time.time() - t_0 if i > 193 else (data[i + 1] << 8 | data[i]))) for i in list(range(-1, 197, 2))]
                # data_point = self.dataTable.row
                # data_point['out'] = [(data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(1,5,2))]
                # # data_point['out'] = [data[0] if i == -1 else ((data[i + 1] << 8 | data[i]) & 0x7FFF if i < datalen - 7 else (data[i + 1] << 8 | data[i])) for i in list(range(-1, datalen - 5, 2))]
                # # data_point['crc'] = data[0]
                # # data_point['data'] = [(data[i + 1] << 8 | data[i]) for i in list(range(1, 193, 2))]
                # # data_point['ramp'] = (data[194] << 8 | data[193])
                # # data_point['time'] = time.time() - t_0
                # data_point['time'] = data_time
                # data_point.append()
                # # self.dataTable.flush()
                #
                # # self.csvfile.writerow(out[45:-1])
                # # self.csvfile.writerow([out[97]])
                # # self.csvfile.writerow(out)

            # else:
            #     crcs += 1
            #     success += 1
            #     # out.append([(((data[i+1] << 8 | data[i]) & 0xFFFF) + 2**15) % 2**16 - 2**15 if i > 192 else (-((data[i+1] << 8 | data[i]) & 0x7FFF) if (data[i+1] & 2**7) else (data[i+1] << 8 | data[i]) & 0x7FFF )for i in list(range(1,199,2))])
            #     # neural data (i<192) is unsigned 15-bit (16th bit is stim info)
            #     # accelerometer data is 2's complement
            #     # out.append([(((data[i+1] << 8 | data[i]) & 0xFFFF) + 2**15) % 2**16 - 2**15 if i > 192 else (data[i+1] << 8 | data[i]) & 0x7FFF for i in list(range(1,199,2))])
            #     # out = [data[0] if i == -1 else ((data[i + 1] << 8 | data[i]) & 0x7FFF if i < 193 else (time.time() - t_0 if i > 193 else (data[i + 1] << 8 | data[i]))) for i in list(range(-1, 197, 2))]
            #     data_point = self.dataTable.row
            #     data_point['out'] = [(data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(1, 5, 2))]
            #     # data_point['out'] = [data[0] if i == -1 else ((data[i + 1] << 8 | data[i]) & 0x7FFF if i < datalen - 7 else (data[i + 1] << 8 | data[i])) for i in list(range(-1, datalen - 5, 2))]
            #     # data_point['crc'] = data[0]
            #     # data_point['data'] = [(data[i + 1] << 8 | data[i]) for i in list(range(1, 193, 2))]
            #     # data_point['ramp'] = (data[194]<<8 | data[193])
            #     data_point['time'] = data_time
            #     data_point.append()
            #     # self.dataTable.flush()
            #
            #     # self.csvfile.writerow([out[45:-1]])
            #     # self.csvfile.writerow([out[97]])
            #     # self.csvfile.writerow(out)

            # else:
            #     fail += 1
            #     # misalignments.append(samples)
            #     # print("misalignment!")
            #     # keep reading from serial until we reach end-of-packet byte (flush until next packet)
            #     temp = 0
            #     # TODO: should actually check that we have 0x55 followed by 0xAA in order to be sure we're at the end of one packet and start of another
            #     while (temp != b'U'): # b'U' is 0x55 (end of packet byte)
            #         temp = CMWorker.ser.read(1, timeout=0)

            # flush the tables every 1000 samples (any speed up?)
            # if samples%1000 == 0:
            #     self.dataTable.flush()

        ftdiFIFO.stop()  # turn off FTDI fifo reading thread
        # only get here if we've called stop(), so turn off streaming mode
        # print("success: {}. fail: {}. %: {}".format(success, ftdiFIFO.fail, 100*success/(success+ftdiFIFO.fail)))
        # print("success: {}. fail: {}. %: {}".format(success, fail, 100*success/(success+fail)))
        # print("Misalignments:")
        # print(str(misalignments).strip('[]'))
        # print("Number of bytes read to sync up after each failure: ")
        # print(str(misalignments).strip('[]'))
        # print("CRCs: {}".format(crcs))
        time.sleep(0.5)

        CMWorker()._regWr(Reg.req, 0x0000) # turn off streaming mode
        print("End of Stream")
        CMWorker.ser.flush()
        print("Fifos Flushed")

        # self.saveFile.close()

class CMWorker(QThread):
    connStateChanged = pyqtSignal(bool)
    boardsChanged = pyqtSignal(list)
    regReadData = pyqtSignal(int, int, int)
    adcData = pyqtSignal(list)
    updateChannels = pyqtSignal(list)

    enabledChannels = [65535,65535,65535,65535,65535,65535,0,0]

    ser = Device(lazy_open=True)

    def __init__(self, parent=None):
        super().__init__(parent)

    def __del__(self):
        # wait for the thread to finish before destroying object
        self.wait()

    def _regWr(self, reg, value):
        s = struct.pack(">cI", bytes([reg.value]), value)
        # print("reg wr: {}".format(s))
        # print("reg wr: {:04x} {:04x}".format(reg.value, value))
        self.ser.write(s)

    def _resetIF(self):
        # reset AM
        self._regWr(Reg.ctrl, 0x103)
        # reset all NMs
        self._regWr(Reg.rst, 0xFFFF)
        self._regWr(Reg.ctrl, 0x102)

    def _sendCmd(self, nm, cmd):
        if nm==0:
            self._regWr(Reg.n0d2, 1<<10 | (cmd & 0x3FF))
            self._regWr(Reg.ctrl, 0x1010)
        if nm==1:
            self._regWr(Reg.n1d2, 1<<10 | (cmd & 0x3FF))
            self._regWr(Reg.ctrl, 0x2020)

    def _regOp(self, nm, addr, data, write):
        if nm==0:
            self._regWr(Reg.n0d1, 1 if write else 0)
            self._regWr(Reg.n0d2, addr << 16 | data)
            self._regWr(Reg.ctrl, 0x1000)
            if not write:
                # self.ser.setTimeout(3)
                self._regWr(Reg.req, 0x0100)
                try:
                    d = self.ser.read(4, timeout=0.3)
                except:
                    return [False, 0]
                # self.ser.setTimeout(1)
                if len(d) != 4:
                    raise Exception("Reg read failed: {}/4 bytes, {}".format(len(d), d))
                if (d[1] << 8 | d[0]) != addr:
                    raise Exception("Reg read failed - wrong register value: {}".format(d))
                return [True, d[3] << 8 | d[2]]

        if nm==1:
            self._regWr(Reg.n1d1, 1 if write else 0)
            self._regWr(Reg.n1d2, addr << 16 | data)
            self._regWr(Reg.ctrl, 0x2000)
            if not write:
                # self.ser.setTimeout(3)
                self._regWr(Reg.req, 0x0200)
                try:
                    d = self.ser.read(4, timeout=0.3)
                except:
                    return [False, 0]
                # self.ser.setTimeout(1)
                if len(d) != 4:
                    raise Exception("Reg read failed: {}/4 bytes, {}".format(len(d), d))
                if (d[1] << 8 | d[0]) != addr:
                    raise Exception("Reg read failed - wrong register value: {}".format(d))
                return [True, d[3] << 8 | d[2]]

    def _getAdc(self, N):

        out = []
        self._regWr(Reg.req, 0x0003 | (N-1)<<16) # request N samples from both NMs
        badlengths = 0
        misalignments = []
        emptylengths = 0
        crcs = 0
        samples = 0
        # time.sleep(1)
        # return out
        for loop in range(0,N):
            data = []
            count1 = 0
            while (len(data) != datalen):
                temp = self.ser.read(datalen-len(data), timeout=0)
                data.extend(temp)
                count1 += 1
                if count1 == 20:
                    #print("break while reading 200 bytes of data")
                    break

            if len(data) == datalen:
                if data[0] == 0xAA and data[len(data) - 1] == 0x55:
                    samples += 1
                    # neural data (i<192) is unsigned 15-bit (16th bit is stim info)
                    # accelerometer data is 2's complement
                    #out.append([(((data[i + 1] << 8 | data[i]) & 0xFFFF) + 2 ** 15) % 2 ** 16 - 2 ** 15 if i > 192 else (data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(1, 199, 2))])
                    out.append([((data[i + 1] << 8 | data[i]) & 0xFFFF) if i > datalen - 8 else (data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(1, datalen - 1, 2))])

                elif data[0] == 0xFF and data[len(data) - 1] == 0x55:
                    samples += 1
                    crcs += 1
                    # neural data (i<192) is unsigned 15-bit (16th bit is stim info)
                    # accelerometer data is 2's complement
                    #out.append([(((data[i + 1] << 8 | data[i]) & 0xFFFF) + 2 ** 15) % 2 ** 16 - 2 ** 15 if i > 192 else (data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(1, 199, 2))])
                    out.append([((data[i + 1] << 8 | data[i]) & 0xFFFF) if i > datalen - 8 else (data[i + 1] << 8 | data[i]) & 0x7FFF for i in list(range(1, datalen - 1, 2))])
                else:
                    misalignments.append(loop)
                    count2 = 0
                    temp = 0
                    # keep reading from serial until we reach end-of-packet byte (flush until next packet)
                    while (temp != b'U'):
                        temp = self.ser.read(1, timeout=0)
                        count2 += 1
                        if count2 == 500:
                            break

            else:
                if len(data) == 0:
                    emptylengths += 1
                else:
                    badlengths += 1

            if emptylengths > 2:
                break
        print("Samples: {}".format(samples))
        print("Read {} bad lengths".format(badlengths))
        print("Misalignments:")
        print(str(misalignments).strip('[]'))
        print("CRCs: {}".format(crcs))
        time.sleep(0.1)
        self.ser.flush()
        return out

    @pyqtSlot(int)
    def readAdc(self, ns):
        if not self.ser._opened:
            return
        self.adcData.emit(self._getAdc(ns))

    @pyqtSlot()
    def refreshBoards(self):
        dev_list = []
        for device in Driver().list_devices():
            vendor, product, serial = map(lambda x: x.decode('latin1'), device)
            dev_list.append(serial)
        self.boardsChanged.emit(dev_list)


    @pyqtSlot(str)
    def connectToBoard(self, board):
        self.ser.open()
        self.ser.flush()
        print("Connected to FTDI and flushed FIFOs")
        self.connStateChanged.emit(self.ser._opened)

    @pyqtSlot()
    def flushCommandFifo(self):
        if not self.ser._opened:
            return
        self.ser.flush_input()
        print("Flushed FTDI input (command) FIFO")

    @pyqtSlot()
    def flushDataFifo(self):
        if not self.ser._opened:
            return
        self.ser.flush_output()
        print("Flushed FTDI output (data) FIFO")

    @pyqtSlot()
    def resetSerial(self):
        if not self.ser._opened:
            return
        self._resetIF()

    @pyqtSlot()
    def disconnectBoard(self):
        self.ser.close()
        self.connStateChanged.emit(self.ser._opened)

    @pyqtSlot(bool, bool)
    def setPwrEn(self, en1v, en3v):
        pass

    @pyqtSlot(int, int)
    def nmicCommand(self, nm, cmd):
        if not self.ser._opened:
            return
        #if cmd == 0x04 or cmd == 0x09: # imp_start or stim start command
        #    # if recording is disabled, don't abort on timeout
        #    prev = None
        #    try:
        #        prev = self._getAdc(400)
        #    except Exception:
        #        pass
        self._sendCmd(nm, cmd)
        # if (cmd == 0x04 or cmd == 0x09):
        #     self.adcData.emit(self._getAdc(1000))

    @pyqtSlot(float)
    def setPwr3V(self, voltage):
        pass

    @pyqtSlot(float)
    def setPwr1V(self, voltage):
        pass

    @pyqtSlot(float)
    def setPwrHV(self, voltage):
        pass

    @pyqtSlot(int, int, int)
    def writeReg(self, nm, addr, value):
        if not self.ser._opened:
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
        if not self.ser._opened:
            return
        ret = self._regOp(nm, addr, 0, False)
        if not ret[0]:
            ret = self._regOp(nm, addr, 0, False)
        if not ret[0]:
            print('Timeout reading register {}'.format(addr))
        else:
            print("Read register from NM {}: {:04x} {:04x}".format(nm, addr, ret[1]))
            if addr == 0x04:
                if nm == 0:
                    self.enabledChannels[0] = ret[1]
                else:
                    self.enabledChannels[4] = ret[1]
            elif addr == 0x05:
                if nm == 0:
                    self.enabledChannels[1] = ret[1]
                else:
                    self.enabledChannels[5] = ret[1]
            elif addr == 0x06:
                if nm == 0:
                    self.enabledChannels[2] = ret[1]
                else:
                    self.enabledChannels[6] = ret[1]
            elif addr == 0x07:
                if nm == 0:
                    self.enabledChannels[3] = ret[1]
                else:
                    self.enabledChannels[7] = ret[1]
            self.updateChannels.emit(self.enabledChannels)
            self.regReadData.emit(nm, addr, ret[1])
        # time.sleep(0.1)
        self.ser.flush()

    @pyqtSlot()
    def testCommOn(self):
        print("Test Comm On")
        self._regWr(Reg.req, 0x00000080) # enable test

    @pyqtSlot()
    def testCommOff(self):
        print("Test Comm Off")
        self._regWr(Reg.req, 0x00000040)  # disable test
