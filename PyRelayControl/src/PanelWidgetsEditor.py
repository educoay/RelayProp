#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PanelWidgetsEditor.py
MIT License (c) Faure Systems <dev at faure dot systems>

Dialog to edit caption and indicators.
"""

from constants import *
from PropPanel import PropPanel
from PanelRelaunchSettingsDialog import PanelRelaunchSettingsDialog

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDialog, QComboBox, QGroupBox, QPushButton
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFrame, QCheckBox
from PyQt5.QtGui import QIcon


class PanelWidgetsEditor(QDialog):
    rebuild = pyqtSignal()
    reorder = pyqtSignal()

    # __________________________________________________________________
    def __init__(self, prop_variables, prop_settings,
                 widget_groups, widget_titles,
                 widget_variables, widget_images, widget_buttons,
                 widget_hiddens, relaunch_command, ssh_credentials, logger):

        self._logger = logger
        self._propSettings = prop_settings
        self._propVariables = prop_variables
        self._groupBoxes = {}
        self._widgetGroups = widget_groups
        self._widgetTitles = widget_titles
        self._widgetVariables = widget_variables
        self._widgetImages = widget_images
        self._widgetButtons = widget_buttons
        self._widgetHiddens = widget_hiddens
        self._relaunchCommand = relaunch_command
        self._sshCredentials = ssh_credentials

        self._imageSelections = {}
        self._labelInputs = {}
        self._titleInputs = {}
        self._moveUpButtons = {}
        self._moveDownButtons = {}
        self._groupButtons = {}
        self._hideChecks = {}

        self._propBox = None

        super(PanelWidgetsEditor, self).__init__()

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(self.tr("Edit captions and indicators"))

        self.setWindowIcon(QIcon('./x-settings.png'))

        self.buildUi()

        self.reorder.connect(self.buildGroups)

    # __________________________________________________________________
    def _buttonEditor(self, action, variable):

        ew = QWidget()
        layout = QHBoxLayout(ew)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        action_widget = QLineEdit(action)
        action_widget.setFrame(QFrame.NoFrame)
        action_widget.setReadOnly(True)

        caption_input = QLineEdit(variable.capitalize())

        hide_check = QCheckBox()
        hide_check.setToolTip(self.tr("Hide widget"))

        layout.addWidget(QLabel(self.tr("Button")))
        layout.addWidget(action_widget)
        layout.addWidget(caption_input)
        layout.addWidget(hide_check)

        return (ew, caption_input, hide_check)

    # __________________________________________________________________
    def _groupEditor(self, group):

        ew = QWidget()
        layout = QHBoxLayout(ew)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        if group is not None:
            action_widget = QLineEdit('{}/'.format(group))
            action_widget.setFrame(QFrame.NoFrame)
            action_widget.setReadOnly(True)
            caption_input = QLineEdit(group.capitalize())
        else:
            caption_input = QLineEdit()

        layout.addWidget(QLabel(self.tr("Group")))
        if group is not None:layout.addWidget(action_widget)
        layout.addWidget(caption_input)

        move_up_button = QPushButton()
        move_up_button.setFlat(True)
        move_up_button.setToolTip(self.tr("Move group up"))
        move_up_button.setIconSize(QSize(10, 10))
        move_up_button.setFixedSize(QSize(14, 14))
        move_up_button.setIcon(QIcon('./images/caret-top'))

        move_down_button = QPushButton()
        move_down_button.setFlat(True)
        move_down_button.setToolTip(self.tr("Move group down"))
        move_down_button.setIconSize(QSize(20, 20))
        move_down_button.setFixedSize(QSize(28, 28))
        move_down_button.setIcon(QIcon('./images/caret-bottom'))

        hide_check = QCheckBox()
        hide_check.setToolTip(self.tr("Hide group"))

        layout.addWidget(move_up_button)
        layout.addWidget(move_down_button)
        layout.addWidget(hide_check)

        return (ew, caption_input, move_up_button, move_down_button, hide_check)

    # __________________________________________________________________
    def _switchEditor(self, action, variable):

        ew = QWidget()
        layout = QHBoxLayout(ew)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        action_widget = QLineEdit(action)
        action_widget.setFrame(QFrame.NoFrame)
        action_widget.setReadOnly(True)
        label_input = QLineEdit(variable.capitalize())
        image_selector = QComboBox()

        image_selector.addItem(self.tr("Light"), 'light')
        image_selector.addItem(self.tr("Door"), 'door')
        image_selector.addItem(self.tr("Smoke"), 'smoke')
        image_selector.addItem(self.tr("Plug"), 'plug')
        image_selector.addItem(self.tr("Relay"), 'relay')

        hide_check = QCheckBox()
        hide_check.setToolTip(self.tr("Hide widget"))

        layout.addWidget(QLabel(self.tr("Switch")))
        layout.addWidget(action_widget)
        layout.addWidget(label_input)
        layout.addWidget(image_selector)
        layout.addWidget(hide_check)

        return (ew, label_input, image_selector, hide_check)

    # __________________________________________________________________
    @pyqtSlot()
    def buildGroups(self):

        main_layout = self.layout()

        for group in list(self._groupBoxes.keys()):
            widgets = self._groupBoxes[group].findChildren(QWidget, '', options=Qt.FindChildrenRecursively)
            for w in widgets:
                try:
                    self._groupBoxes[group].layout().removeWidget(w)
                    w.deleteLater()
                except Exception as e:
                    print(e)
            del (widgets)
            main_layout.removeWidget(self._groupBoxes[group])
            self._groupBoxes[group].deleteLater()
            del (self._groupBoxes[group])

        if self._propBox is not None:
            widgets = self._propBox.findChildren(QWidget, '', options=Qt.FindChildrenRecursively)
            for w in widgets:
                try:
                    self._propBox.layout().removeWidget(w)
                    w.deleteLater()
                except Exception as e:
                    print(e)
            del (widgets)
            main_layout.removeWidget(self._propBox)
            self._propBox.deleteLater()
            del (self._propBox)

        top_group = None
        bottom_group = None

        for group in self._widgetGroups:
            if top_group is None:
                top_group = group
            bottom_group = group
            box = QGroupBox()
            box_layout = QVBoxLayout(box)
            box_layout.setSpacing(12)
            self._groupBoxes[group] = box
            main_layout.addWidget(box)

        for v, pin in self._propVariables.items():
            if '/' in v:
                group, variable = v.split('/', 1)
            else:
                group = None
                variable = v
            switch, label_input, image_selector, hide_check = self._switchEditor(pin.getVariable(), variable)
            self._labelInputs[label_input] = v
            self._imageSelections[image_selector] = v
            self._hideChecks[hide_check] = v
            if v in self._widgetVariables:
                label_input.setText(self._widgetVariables[v])
            if v in self._widgetImages:
                idx = image_selector.findData(self._widgetImages[v])
                if idx > 0:
                    image_selector.setCurrentIndex(idx)
            if v in self._widgetHiddens and self._widgetHiddens[v]:
                hide_check.setChecked(True)
            label_input.editingFinished.connect(self.onLabelEdition)
            image_selector.currentIndexChanged.connect(self.onImageSelection)
            hide_check.released.connect(self.onHideCheck)

            if group in self._groupBoxes:
                self._groupBoxes[group].layout().addWidget(switch)
            else:
                box = QGroupBox()
                box_layout = QVBoxLayout(box)
                box_layout.setSpacing(12)
                self._groupBoxes[group] = box
                main_layout.addWidget(box)
                box_layout.addWidget(switch)
                self._widgetGroups.append(group)

        for group in list(self._groupBoxes.keys()):
            title, title_input, move_up_button, move_down_button, hide_check = self._groupEditor(group)
            self._groupBoxes[group].layout().insertWidget(0, title)

            if group == top_group:
                move_up_button.setEnabled(False)
                move_up_button.setToolTip('')
            if group == bottom_group:
                move_down_button.setEnabled(False)
                move_down_button.setToolTip('')

            self._titleInputs[title_input] = group + '/' if group is not None else None
            self._moveUpButtons[move_up_button] = group
            self._moveDownButtons[move_down_button] = group
            self._hideChecks[hide_check] = group

            if group in self._widgetHiddens and self._widgetHiddens[group]:
                hide_check.setChecked(True)

            title_input.editingFinished.connect(self.onTitleEdition)
            move_up_button.released.connect(self.onMoveGroupUp)
            move_down_button.released.connect(self.onMoveGroupDown)
            hide_check.released.connect(self.onHideCheck)

            variable = group + '/' if group is not None else ''
            if variable in self._widgetTitles:
                title_input.setText(self._widgetTitles[variable])

            if group is None: continue

            v_high = '{}/*:{}'.format(group, str(GPIO_HIGH))
            button_on, button_on_input, hide_check_on = self._buttonEditor(v_high, group)
            self._groupBoxes[group].layout().addWidget(button_on)

            v_low = '{}/*:{}'.format(group, str(GPIO_LOW))
            button_off, button_off_input, hide_check_off = self._buttonEditor(v_low, group)
            self._groupBoxes[group].layout().addWidget(button_off)

            if v_high in self._widgetButtons:
                button_on_input.setText(self._widgetButtons[v_high])
            if v_low in self._widgetButtons:
                button_off_input.setText(self._widgetButtons[v_low])

            if v_high in self._widgetHiddens and self._widgetHiddens[v_high]:
                hide_check_on.setChecked(True)
            if v_low in self._widgetHiddens and self._widgetHiddens[v_low]:
                hide_check_off.setChecked(True)

            button_on_input.editingFinished.connect(self.onButtonEdition)
            button_off_input.editingFinished.connect(self.onButtonEdition)
            hide_check_on.released.connect(self.onHideCheck)
            hide_check_off.released.connect(self.onHideCheck)

            self._groupButtons[button_on_input] = v_high
            self._groupButtons[button_off_input] = v_low

            self._hideChecks[hide_check_on] = v_high
            self._hideChecks[hide_check_off] = v_low

            if v_high in self._widgetButtons:
                button_on_input.setText(self._widgetButtons[v_high])
            if v_low in self._widgetButtons:
                button_off_input.setText(self._widgetButtons[v_low])

        self._propBox = QGroupBox(self.tr("Prop board control"))
        box_layout = QVBoxLayout(self._propBox)
        box_layout.setSpacing(12)
        main_layout.addWidget(self._propBox)

        relaunch_button = QPushButton(self.tr("Relaunch"))
        hide_relaunch = QCheckBox()
        hide_relaunch.setToolTip(self.tr("Hide widget"))
        relaunch_layout = QHBoxLayout()
        relaunch_layout.setContentsMargins(0, 0, 0, 0)
        relaunch_layout.setSpacing(8)
        relaunch_layout.addWidget(relaunch_button, 1)
        relaunch_layout.addWidget(hide_relaunch, 0, Qt.AlignRight)
        box_layout.addLayout(relaunch_layout)

        if '__RELAUNCH__' in self._widgetHiddens and self._widgetHiddens['__RELAUNCH__']:
            hide_relaunch.setChecked(True)

        reboot_button = QPushButton(self.tr("Reboot"))
        hide_reboot = QCheckBox()
        hide_reboot.setToolTip(self.tr("Hide widget"))
        reboot_layout = QHBoxLayout()
        reboot_layout.setContentsMargins(0, 0, 0, 0)
        reboot_layout.setSpacing(8)
        reboot_layout.addWidget(reboot_button, 1)
        reboot_layout.addWidget(hide_reboot, 0, Qt.AlignRight)
        box_layout.addLayout(reboot_layout)

        if '__REBOOT__' in self._widgetHiddens and self._widgetHiddens['__REBOOT__']:
            hide_reboot.setChecked(True)

        if self._propSettings['prop']['board'] == 'mega':
            relaunch_button.setDisabled(True)
            reboot_button.setDisabled(True)

        if self._propSettings['prop']['board'] == 'nucleo':
            relaunch_button.setVisible(False)
            reboot_button.setVisible(False)
            self._propBox.setVisible(False)

        relaunch_button.released.connect(self.onRelaunch)
        reboot_button.setDisabled(True)

        self._hideChecks[hide_relaunch] = '__RELAUNCH__'
        self._hideChecks[hide_reboot] = '__REBOOT__'
        hide_relaunch.released.connect(self.onHideCheck)
        hide_reboot.released.connect(self.onHideCheck)

    # __________________________________________________________________
    def buildUi(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(6)

        self.setLayout(main_layout)

        self.buildGroups()

    # __________________________________________________________________
    @pyqtSlot()
    def onButtonEdition(self):

        input = self.sender()
        if input not in self._groupButtons:
            self._logger.warning("Label input not found")
            return

        variable = self._groupButtons[input]
        self._widgetButtons[variable] = input.text().strip()
        PropPanel.savePanelJson(self._widgetGroups, self._widgetTitles, self._widgetVariables,
                                self._widgetImages, self._widgetButtons, self._widgetHiddens,
                                self._relaunchCommand, self._sshCredentials)
        self.rebuild.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def onHideCheck(self):

        checkbox = self.sender()
        if checkbox not in self._hideChecks:
            self._logger.warning("Hide checkbox not found")
            return

        variable = self._hideChecks[checkbox]
        self._widgetHiddens[variable] = checkbox.isChecked()
        PropPanel.savePanelJson(self._widgetGroups, self._widgetTitles, self._widgetVariables,
                                self._widgetImages, self._widgetButtons, self._widgetHiddens,
                                self._relaunchCommand, self._sshCredentials)
        self.rebuild.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def onImageSelection(self):

        combobox = self.sender()
        if combobox not in self._imageSelections:
            self._logger.warning("Image selection not found")
            return

        variable = self._imageSelections[combobox]
        self._widgetImages[variable] = combobox.currentData()
        PropPanel.savePanelJson(self._widgetGroups, self._widgetTitles, self._widgetVariables,
                                self._widgetImages, self._widgetButtons, self._widgetHiddens,
                                self._relaunchCommand, self._sshCredentials)
        self.rebuild.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def onLabelEdition(self):

        input = self.sender()
        if input not in self._labelInputs:
            self._logger.warning("Label input not found")
            return

        variable = self._labelInputs[input]
        self._widgetVariables[variable] = input.text().strip()
        PropPanel.savePanelJson(self._widgetGroups, self._widgetTitles, self._widgetVariables,
                                self._widgetImages, self._widgetButtons, self._widgetHiddens,
                                self._relaunchCommand, self._sshCredentials)
        self.rebuild.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def onMoveGroupDown(self):

        button = self.sender()
        if button not in self._moveDownButtons:
            self._logger.warning("Button not found : {}".format(button.toolTip()))
            return

        group = self._moveDownButtons[button]

        try:
            i = self._widgetGroups.index(group)
        except ValueError:
            return

        if i < len(self._widgetGroups) - 1:
            self._widgetGroups.pop(i)
            self._widgetGroups.insert(i+1, group)
            PropPanel.savePanelJson(self._widgetGroups, self._widgetTitles, self._widgetVariables,
                                    self._widgetImages, self._widgetButtons, self._widgetHiddens,
                                    self._relaunchCommand, self._sshCredentials)
            self.rebuild.emit()
            self.reorder.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def onMoveGroupUp(self):

        button = self.sender()
        if button not in self._moveUpButtons:
            self._logger.warning("Button not found : {}".format(button.toolTip()))
            return

        group = self._moveUpButtons[button]

        try:
            i = self._widgetGroups.index(group)
        except ValueError:
            return

        if i > 0:
            self._widgetGroups.pop(i)
            self._widgetGroups.insert(i-1, group)
            self.rebuild.emit()
            self.reorder.emit()
            PropPanel.savePanelJson(self._widgetGroups, self._widgetTitles, self._widgetVariables,
                                    self._widgetImages, self._widgetButtons, self._widgetHiddens,
                                    self._relaunchCommand, self._sshCredentials)

    # __________________________________________________________________
    @pyqtSlot()
    def onRelaunch(self):

        dlg = PanelRelaunchSettingsDialog(self.tr("Relaunch command"),
                                     self._relaunchCommand,
                                     self._propSettings, self._logger)
        dlg.setModal(True)
        if dlg.exec() == QDialog.Accepted:
            self.rebuild.emit()
            PropPanel.savePanelJson(self._widgetGroups, self._widgetTitles, self._widgetVariables,
                                    self._widgetImages, self._widgetButtons, self._widgetHiddens,
                                    self._relaunchCommand, self._sshCredentials)

    # __________________________________________________________________
    @pyqtSlot()
    def onTitleEdition(self):

        input = self.sender()
        if input not in self._titleInputs:
            self._logger.warning("Title input not found")
            return

        variable = self._titleInputs[input]
        if variable is None: variable = ''
        self._widgetTitles[variable] = input.text().strip()
        self.rebuild.emit()
        PropPanel.savePanelJson(self._widgetGroups, self._widgetTitles, self._widgetVariables,
                                self._widgetImages, self._widgetButtons, self._widgetHiddens,
                                self._relaunchCommand, self._sshCredentials)

