#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py

Contains all the control applet constants.
"""

# __________________________________________________________________
# Required by MqttApplet
ORGANIZATIONDOMAIN = "xcape.io"
ORGANIZATIONNAME = "xcape.io"

CONFIG_FILE = '.config.yml'

APPLICATION = "Control"

PYPROPS_CORELIBPATH = '../core' # however ./core is preferred if present

MQTT_DEFAULT_HOST = 'localhost'  # replace localhost with your broker IP address
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

# __________________________________________________________________
# Required by ControlApplet
APPDISPLAYNAME = APPLICATION

# __________________________________________________________________
# Required by the widgets
LAYOUT_FILE = '.layout.yml'

# __________________________________________________________________
# Required by the application
DATALED_IMAGE_ON = './images/led-circle-yellow.svg'
DATALED_IMAGE_OFF = './images/led-circle-generic.svg'

SWITCH_IMAGES = {}
SWITCH_IMAGES['default'] = ('./images/led-circle-yellow.svg', './images/led-circle-generic.svg')
SWITCH_IMAGES['door'] = ('./images/door-closed.svg', './images/door-opened.svg')
SWITCH_IMAGES['smoke'] = ('./images/smoke_on.svg', './images/smoke_off.svg')
SWITCH_IMAGES['plug'] = ('./images/plug.svg', './images/unplugged.svg')
SWITCH_IMAGES['relay'] = ('./images/relay_closed.svg', './images/relay_opened.svg')


GPIO_LOW = 0
GPIO_HIGH = 1
