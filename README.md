# Dygma Layer Switcher
Simple tool to switch between layer of the dygma defy base on the currently active window. It currently only works for Microsoft Windows.

The layers won't switch while another program (like Bazecor) is occupying the com port, but will continue function once other application is closed.

----
To switch automatically switch between layers, edit the config.yaml file.

'base_layer' refers to the layer to switch to, when the currently focussed program is not in any of the layer lists

'layers' is a dictionary matching the layer number (-1) to different programs. Simply add the exe-name as shown in task manager and a layer switch will be made when focussing the program.

'refresh_interval' refers to how often the currently active window is checked

'PORT' is the com port the keyboards neuron is connected to.
