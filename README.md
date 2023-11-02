# Dygma Layer Switcher
Simple tool to switch between layers of the dygma defy based on the currently active window. It currently only works for Microsoft Windows.

The layers won't switch while another program (like Bazecor) is occupying the com port, but will continue function once other application is closed.

---
## Install
Either use the compiled files in *windows-compiled.zip* or *dist*. If you want to use the uncompiled .py-file, install copy the repository, run 
    
    pip install -r requirements.txt 

and 
    
    py -3 main.py

----
## How to use
To switch automatically switch between layers, edit the *config.yaml* file.

**base_layer** refers to the layer to switch to, when the currently focussed program is not in any of the layer lists

**layers** is a dictionary matching the layer number (-1) to different programs. Simply add the exe-name as shown in task manager and a layer switch will be made when focussing the program.

**refresh_interval** refers to how often the currently active window is checked

**PORT** is the com port the keyboards neuron is connected to.

---
## Limitations
There is a short delay (~1s) while switching layers and while the switch occurs inputs are not available as the com port is used for the layer switching command. 