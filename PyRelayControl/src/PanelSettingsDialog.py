#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PanelSettingsDialog.py
MIT License (c) Marie Faure <dev at faure dot systems>

Dialog to configure control parameters.
"""

from EditPanelWidgets import EditPanelWidgets
from PropPanel import PropPanel

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtWidgets import QDialog, QPushButton, QGroupBox
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
import os


class PanelSettingsDialog(QDialog):
    rebuildWidgets = pyqtSignal()

    # __________________________________________________________________
    def __init__(self, prop_variables, prop_settings,
                 widget_groups, widget_titles,
                 widget_variables, widget_images,
                 widget_buttons, logger):

        super(PanelSettingsDialog, self).__init__()

        self._logger = logger
        self._propSettings = prop_settings
        self._propVariables = prop_variables
        self._widgetGroups = widget_groups
        self._widgetTitles = widget_titles
        self._widgetVariables = widget_variables
        self._widgetImages = widget_images
        self._widgetButtons = widget_buttons

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(self.tr("Panel configuration"))

        self.setWindowIcon(QIcon('./images/cog-black.svg'))

        self.setMinimumWidth(400)
        self.buildUi()

    # __________________________________________________________________
    def buildUi(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(6)

        settings_box = QGroupBox(self.tr("Prop settings"))
        settings_box_layout = QVBoxLayout(settings_box)
        main_layout.addWidget(settings_box)

        json_layout = QHBoxLayout()
        settings_box_layout.addLayout(json_layout)

        self._jsonInput = QLineEdit()
        self._jsonInput.setDisabled(True)

        json_browse_button = QPushButton()
        json_browse_button.setIcon(QIcon('./images/folder.svg'))
        json_browse_button.setFlat(True)
        json_browse_button.setToolTip(self.tr("Browse to select JSON file"))
        json_browse_button.setIconSize(QSize(16, 16))
        json_browse_button.setFixedSize(QSize(20, 20))

        json_layout.addWidget(QLabel(self.tr("JSON file")))
        json_layout.addWidget(self._jsonInput)
        json_layout.addWidget(json_browse_button)

        if self._propVariables:
            button = self.tr("Rebuild widgets from new settings")
        else:
            button = self.tr("Build widgets from new settings")

        build_button = QPushButton(" {} ".format(button))
        build_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        settings_box_layout.addWidget(build_button)

        self._settingsWidget = QWidget()
        self._settingsWidget.setContentsMargins(0, 0, 0, 0)
        settings_layout = QGridLayout(self._settingsWidget)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._settingsWidget)

        close_button = QPushButton(self.tr("Close"))
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        edit_button = QPushButton(' {} '.format(self.tr("Edit captions and indicators")))
        edit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        edit_button.setEnabled(len(self._propVariables))

        button_layout = QHBoxLayout()
        button_layout.addWidget(edit_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        close_button.released.connect(self.accept)
        edit_button.released.connect(self.onEdit)
        build_button.released.connect(self.onBuild)
        json_browse_button.released.connect(self.onBrowse)

        if 'prop' in self._propSettings and 'json' in self._propSettings['prop']:
            self._jsonInput.setText(os.path.basename(self._propSettings['prop']['json']))

    # __________________________________________________________________
    @pyqtSlot()
    def onBuild(self):

        if 'prop' in self._propSettings and 'json' in self._propSettings['prop']:
            prop_variables = PropPanel.getVariablesJson(self._propSettings['prop']['json'], self._logger)
        else:
            msg = QMessageBox()
            msg.setWindowIcon(self.windowIcon())
            msg.setIcon(QMessageBox.Warning)
            msg.setText(self.tr("There is no JSON file from prop settings, select one."))
            msg.setWindowTitle("Missing JSON")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        new_variables = []
        for variable in prop_variables:
            if variable not in self._propVariables:
                new_variables.append(variable)

        lost_variables = []
        for variable in self._propVariables:
            if variable not in prop_variables:
                lost_variables.append(variable)

        while lost_variables:
            del (self._propVariables[lost_variables.pop(0)])

        for variable in new_variables:
            self._propVariables[variable] = prop_variables[variable]

        self.rebuildWidgets.emit()


    # __________________________________________________________________
    @pyqtSlot()
    def onBrowse(self):

        if 'prop' in self._propSettings and 'json' in self._propSettings['prop']:
            json_path = self._propSettings['prop']['json']
            json_dir = os.path.dirname(json_path)
        else:
            json_path = None
            json_dir = os.getcwd()

        dlg = QFileDialog(self,
                          self.tr("Select prop settings JSON file"),
                          json_dir,
                          self.tr("JSON files (*.json);; All files (*.*)"))

        dlg.setViewMode(QFileDialog.Detail)
        dlg.setFileMode(QFileDialog.ExistingFile)

        if json_path:
            dlg.selectFile(os.path.basename(json_path))

        ret = dlg.exec()

        if QDialog.Accepted == ret and len(dlg.selectedFiles()) == 1:
            returned_path = dlg.selectedFiles()[0]

            if os.path.isfile(returned_path):
                self._propSettings['prop']['json'] = returned_path
                self._jsonInput.setText(os.path.basename(returned_path))
                with open('prop.ini', 'w') as configfile:
                    self._propSettings.write(configfile)


    # __________________________________________________________________
    @pyqtSlot()
    def onEdit(self):

        dlg = EditPanelWidgets(self._propVariables, self._propSettings,
                               self._widgetGroups, self._widgetTitles,
                               self._widgetVariables, self._widgetImages,
                               self._widgetButtons, self._logger)
        dlg.setModal(True)

        dlg.rebuild.connect(self.rebuildWidgets)

        dlg.exec()