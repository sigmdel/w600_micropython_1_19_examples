# w600_micropython_1_19_examples
MicroPython 1.19 Example Scripts on W600-PICO Board

## Description
Source code to accompany 
[A Second Look at the W600-PICO Development Board](https://sigmdel.ca/michel/ha/w600/second_look_w600_en.html).

**This repository is meant to replace the older [w600_micropython_examples](https://github.com/sigmdel/w600_micropython_examples) repository which used MicroPython version 1.10 
that comes preinstalled on the board.**

## Usage

1. Flash the most recent W60X MicroPython port [wm_w600_lfs.fls](https://github.com/robert-hh/Shared-Stuff) onto the W600-PICO.


2. Copy all the MicroPython scripts (`*.py`) in the  [src](src) to the W600-PICO flash memory.  

3. Modify `lib/secrets_template.py` as required to connect to the local Wi-Fi network and save the modified file as `lib/secrets.py`.

4. Modify `lib/mqtttdata_template.py` as required to use a local MQTT broker and save the modified file as `lib/mqttdata.py`.

5. Edit `demo.py` to remove scripts if wanted. For example, if a connection to a Wi-Fi network is not possible, then remove the `import customboot`, and then the last three scripts `import webserver`, `import mqtttest` and `import wifiswitch`. If there is no local MQTT broker available, then remove the last two scripts.

6. Restart the W600-PICO. The scripts in `demo.py` should all be executed one after the other. It will be necessary to click on the `Quit` button in the default web page of the `webserver` to continue on to the last two modules.

Detailed instructions on how to update firmware of the W600-PICO and how to copy files to and from the development board's flash memory are available in [A Second Look at the W600-PICO Development Board](https://sigmdel.ca/michel/ha/w600/second_look_w600_en.html).

## Credits and Thanks

Thanks to the [MicroPython](https://micropython.org) team for porting Python 3 to microcontrollers. 

Thanks to Robert Mammelrath ([robert-hh](https://github.com/robert-hh)) *et al.* for keeping the initial port of MicroPython to the W60X by @wdyichen current and for making the image file available.

Thanks to [LexxM3](https://github.com/LexxM3) for [information](https://github.com/sigmdel/w600_micropython_examples/issues/1) about the newest version of MicroPython of the W60X.

## Licence

The **BSD Zero Clause** ([SPDX](https://spdx.dev/): [0BSD](https://spdx.org/licenses/0BSD.html)) licence applies to the original code in this repository. 

Please respect the licence of each of the libraries used 
  - micropython-lib/umqtt.simple: [MIT](https://github.com/micropython/micropython-lib/blob/master/LICENSE)
  - MicroPython-Button: [not defined](https://github.com/ubidefeo/MicroPython-Button)
