﻿# Install
*Room Relay Prop applets installation and prop installation.*

Components necessary to create, manage and control a Room Relay Prop:

* prop board, either
    - Arduino Mega 2560 board
    - STM32 Nucleo-144 board
    - Raspberry Pi (3B/3B+/4) board
* settings applet
    - GUI app to configure every pin that controls a relay on the prop
* control applet:
    - GUI control panel app to control the prop relays remotely 
* MQTT broker
    - an MQTT broker must be present in you local network
    

## Arduino, Nucleo or Raspberry ?
First you have to choose what's better for your room Relay prop:

* an Arduino Mega 2560 (with Dragino Yún shield)
* an STM32 Nucleo-144 (F767ZI)
* a Raspberry Pi (3B/3B+/4)

Then configure and upload either:

* **MegaRelayProp** with [`MegaRelayProp.ino` sketch to Arduino Mega 2560](https://github.com/xcape-io/RelayProp/tree/master/MegaRelayProp#megarelayprop)
* **NucleoRelayProp** with [`NucleoRelayProp.ino` sketch to STM32 Nucleo-144](https://github.com/xcape-io/RelayProp/tree/master/NucleoRelayProp#nucleorelayprop)
* **PiPyRelayProp** with [PiPyRelayProp app to Raspberry Pi](https://github.com/xcape-io/RelayProp/tree/master/PiPyRelayProp#pipyrelayprop)


## PyRelayControl
Install the PyQt5 Relay prop control applet and its wiring GUI:

* [PyRelayControl applet](https://github.com/xcape-io/RelayProp/tree/master/PyRelayControl#pyrelaycontrol)


## MQTT broker
You can use any MQTT broker:

* *mosquitto* on Windows
    - broker included in *<a href="https://xcape.io/" target="_blank">xcape.io</a> Room* software
    - <a href="https://mosquitto.org/download/" target="_blank">standalone installation</a> from *mosquitto.org*
* *moquitto* on Raspberry
    - <a href="https://github.com/xcape-io/PyProps/blob/master/RASPBERRY_PI_PROPS.md#5-install-mosquitto-broker" target="_blank">install *mosquitto* on Raspbian</a>
* any broker in your local network

If you choose Raspberry Pi for your prop, you can install *mosquitto* on this Raspberry.


## Author

**Faure Systems** (May 15th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>