# WAND_GUI
GUI for WAND, as published in Nature Biomedical Engineering. 

03/25/19 - Updated for "mini" version of WAND with single NMIC. 

&nbsp;&nbsp;&nbsp;&nbsp;***For GUI compatible with dual-NMIC version of WAND, checkout tag "v1.0"***

## Python setup
The WAND GUI requires Python 3. For easy package installation, an Anaconda environment has been provided in "wand_env.yml". This file lists package requirements.


## GUI windows

The GUI consists of 7 main windows:
1. Receiver connection setup (Connection)
1. Command window (Command Window)
1. Data visualizer and streaming setup (Data Visualizer)
1. NMIC common settings configuration (NM0 Configuration)
1. NMIC stimulation settings configuration (NM0 Stim Config)
1. NMIC commands (NM0 Commands)
1. NMIC register read/write (NM0 Registers)

The different windows are described below in order of a typical workflow.


## Receiver connection setup (Connection)

In this window, a spinbox displays the list of currently connected receiver devices for communicating wirelessly with the WAND board. To refresh the list of devices, click the "Refresh" button.

After selecting the desired receiver in the spinbox, click "Connect" ("Disconnect") to connect (disconnect) to the receiver. Upon returning to the Command Window, the logtext will indicate successful/unsuccessful connection.


## Command window (Command Window)

The command window should mostly be used to display messages and warnings from WAND control. The log can be saved to a text file using the "Save Log" button, and can be cleared with the "Clear Log" button.


## Data visualizer and streaming setup (Data Visualizer)

The data visualizer window is used to view real-time streamed data, and to configure stimulation, artifact cancellation, and impedance measurements to be performed during a stream.

The top portion of this window consists of four plots used to visualize four channels of streamed data. Plots can be zoomed using the mouse wheel, as well as by clicking and dragging a rectagle over the data traces.

The first two rows of controls are used to start and stop streaming, as well as to configure plotting. Clicking the "Stream data" button will begin a stream (if a WAND board is enabled and a receiver is connected), and clicking again will stop the stream. "Clear plots" will clear the previously buffered data shown in the plots. Y-axis autoranging can be enabled or disabled with the "Autorange Y" checkbox. The length of the X-axis can be set by changing the "X-axis range (ms)" value.

Displaying streamed data can be enabled or disabled using the checkbox on the second row of controls. When enabled, the channel being displayed for each of the four plots can be set using the four spinboxes. The left-most box configures the top plot, and the right-most box configures the bottom plot.

The bottom three rows are for configuring stimulation, artifact cancellation, and impedance measurement during streams.

If you wish to enable stimulation during a stream, check the "Stimulate in stream" box. The configured stimulation pulse train will then be repeated a number of times as specified by the spinbox to the right. The "Stim delay" value determines the delay (in ms) between the start of the stream and the start of the first stimulation trigger.

If you wish to enable on-board artifact cancellation, check the "Interpolate artifacts" box. The "Artifact delay" is counted relative to the "Stim delay". An "Artifact delay" value of 0 will enable artifact cancellation immediately with the stimulation trigger. Values greater than 0 will result in artifact cancellation being enabled after the stimulation has been triggered.

If you wish to enable impedance measurements, check the "Measure impedance w/ delay" box. The "Impdeance delay" value determines the delay (in ms) between the start of the stream and the start of the impedance measurement trigger.


## NMIC common settings configuration (NM0 Configuration)

Some common settings can be configured from this window:

1. Wide-input mode (where the input range is increased to 400mV) can be enabled by checking the "Wide-input mode" checkbox. 
1. The high-voltage (12 V) stimulation compliance mode can be enabled by clicking the "Enable 12V stim compliance" button. By default the stimulation compliance voltage is 3V.
1. Impedance measurement pulses can be configured by selecting the current pulse amplitue ("Z-measure current") and the number of impedance measurement cycles ("Z-measure # cycles"). Once settings are chosen, they can be written to the board by clicking the "Set Z-measure" button.


## NMIC stimulation settings configuration (NM0 Stim Config)

This window contains all settings to configure the four on-chip stimulators. 

Click the "Waveform Configuration" buttons to create different waveforms that will be saved between sessions. Once a waveform has been created, it can be selected for each of the stimulators ("A-D") in the left most spinbox. 
For each stimulator, the user can also select source/sink channels, as well as enable/disable.

The bottom checkboxes and right-hand-side spin boxes contain various stimulation setup parameters common to all stimulators. 

Once stimulation has been configured, click the "Write Stim Registers" button in the bottom right-hand corner to buffer them to the chip. To enable the buffered settings, a "Transfer stimulation settings" command must be sent fromt he NMIC command window. 


## NMIC commands (NM0 Commands)

Common commands for the NMIC can be sent from this window. They are:
1. Resetting the chip
1. Clearing chip errors (as shown in chip register 0x01)
1. Loading the charge pumps for the high compliance voltage rails
1. Triggering an impedance measurement
1. Resetting stimulation parameters
1. Triggering a preset stimulation pulse train
1. Transferring buffered stimulation settings.

The most commonly used of these commands will be transferring stimulation settings. This is because stimulation settings are double-buffered on chip: while one set of stimulation parameters are actively being used, another set can be buffered up. The buffered settings will only be used once they are "transfered" by sending the "transfer stimulation settings" command. This must be done every time the user wants to update stimulation settings.


## NMIC register read/write (NM0 Registers)

Individual registers can be read and written to from this window. Checkboxes will populate with the current values after pressing the "Read" button. Checkboxes can also be manually configured. Once registers are configured to the desired value, the "Write" checkbox in the right-most column will be set. When pressing the "Write" button, only registers with the "Write" checkbox set will actually be written to. To force a write to all registers with the current selected values, click the "Write All" button.

Register values can be written to and read from configuration text files using the "Read from File" and "Write to File" buttons. 
