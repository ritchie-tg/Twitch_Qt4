####################################################
# Author: datguy-dev                               #
# Version: 0.2                                     #
# Git: https://github.com/datguy-dev/Twitch_Qt4    #
####################################################
#to use chatty: oauth must be - user_read chat_login

import os, sys, re, time, gi, ConfigParser, streamLib
gi.require_version('Notify', '0.7')

from PyQt4 import QtCore, QtGui
from functools import partial
from gi.repository import Notify

#Global variables
assetsPath = os.path.dirname(os.path.realpath(__file__)) + '/assets/' #for images
configPath = os.path.dirname(os.path.realpath(__file__)) + '/config.ini' #for configs

def ConfigCtrl(flag, which, data):
	parser = ConfigParser.SafeConfigParser()
	parser.read(configPath)
	if flag == 'get':
		if which == 'all':
			clientid = parser.get('settings', 'clientid')
			oauth = parser.get('settings', 'oauth')
			notifications = parser.getint('settings', 'notifications')
			chatty = parser.getint('settings', 'chatty')
			clientheight = parser.getint('settings', 'clientheight')
			quality = parser.get('settings', 'quality')
			cache = parser.getint('settings', 'cache') * 1000 #ms to seconds
			return True, clientid, oauth, notifications, chatty, clientheight, quality, cache
		elif which == 'clientid':
			clientid = parser.get('settings', 'clientid')
			return True, clientid
		elif which == 'oauth':
			oauth = parser.get('settings', 'oauth')
			return True, oauth
		elif which == 'notifications':
			notifications = parser.getint('settings', 'notifications')
			return True, notifications
		elif which == 'chatty':
			chatty = parser.getint('settings', 'chatty')
			return True, chatty
		elif which == 'clientheight':
			clientheight = parser.getint('settings', 'clientheight')
			return True, clientheight
		elif which == 'quality':
			quality = parser.get('settings', 'quality')
			return True, quality
		elif which == 'cache':
			cache = parser.getint('settings', 'cache') * 1000 #ms to seconds
			return True, cache
		else:
			return False
	elif flag == 'set':
		if which == 'all':
			data = data.split(',')
			parser.set('settings', 'clientid', data[0])
			parser.set('settings', 'oauth', data[1])
			parser.set('settings', 'notifications', data[2])
			parser.set('settings', 'chatty', data[3])
			parser.set('settings', 'clientheight', data[4])
			parser.set('settings', 'quality', data[5])
			parser.set('settings', 'cache', data[6])
		elif which == 'clientid':
			parser.set('settings', 'clientid', data)
		elif which == 'oauth':
			parser.set('settings', 'oauth', data)
		elif which == 'notifications':
			parser.set('settings', 'notifications', data)
		elif which == 'chatty':
			parser.set('settings', 'chatty', data)
		elif which == 'clientheight':
			parser.set('settings', 'clientheight', data)
		elif which == 'quality':
			parser.set('settings', 'quality', data)
		elif which == 'cache':
			parser.set('settings', 'cache', data)
		else:
			return False

		with open(configPath, 'wb') as f:
			parser.write(f)
		f.close()
		return True

def ShowDialogInfo(flag, shortErr, fullErr):
	#flag { NoIcon, Question, Information, Warning, Critical }
	msg = QtGui.QMessageBox()
	if flag == 'information':
		msg.setIcon(QtGui.QMessageBox.Information)
	elif flag == 'warning':
		msg.setIcon(QtGui.QMessageBox.Warning)
	elif flag == 'critical':
		msg.setIcon(QtGui.QMessageBox.Critical)
	else:
		msg.setIcon(QtGui.QMessageBox.NoIcon)

	msg.setWindowTitle("Twitch_Qt")
	msg.setText("An error has occured!")
	msg.setInformativeText('{0}'.format(shortErr))
	msg.setDetailedText("{0}".format(fullErr))
	msg.setStandardButtons(QtGui.QMessageBox.Ok)
	#msg.buttonClicked.connect(msgbtn)
	retval = msg.exec_()

class Ui_OptionsWindow(object):
	def MainWindow(self, MainWindow):
		#pressing cancel switch back to main window
		ui = Ui_MainWindow()
		ui.setupUi(MainWindow)
		MainWindow.show()

	def SaveConfigs(self, MainWindow):
		clientid = self.lineEdit_ClientID.text()
		oauth =  self.lineEdit_Oauth.text()
		if self.checkBox_1.isChecked():
			notifications = 1
		else:
			notifications = 0
		if self.checkBox_2.isChecked():
			chatty = 1
		else:
			chatty = 0
		heightAdjust = self.lineEdit_5.text()
		quality = self.comboBox_Quality.currentText()
		cache = self.lineEdit_4.text()
		ConfigCtrl('set', 'all', '{0},{1},{2},{3},{4},{5},{6}'.format(clientid,oauth,notifications,chatty,heightAdjust,quality,cache))
		#return to mainwindow
		self.MainWindow(MainWindow)

	def setupOptionUi(self, OptionsWindow):
		OptionsWindow.setObjectName(_fromUtf8("OptionsWindow"))
		OptionsWindow.resize(429, 429)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OptionsWindow.sizePolicy().hasHeightForWidth())
		OptionsWindow.setSizePolicy(sizePolicy)
		OptionsWindow.setMinimumSize(QtCore.QSize(430, 475))
		OptionsWindow.setMaximumSize(QtCore.QSize(430, 475))
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("Twitch_Qt/assets/glitch.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		OptionsWindow.setWindowIcon(icon)
		OptionsWindow.setAutoFillBackground(False)
		self.centralWidget = QtGui.QWidget(OptionsWindow)
		self.centralWidget.setMinimumSize(QtCore.QSize(0, 0))
		self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 999999))
		self.centralWidget.setStyleSheet(_fromUtf8("background-color: rgb(100, 65, 164);"))
		self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
		self.verticalLayoutWidget = QtGui.QWidget(self.centralWidget)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 411, 181))
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
		self.vLayout_AccSettings = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.vLayout_AccSettings.setMargin(5)
		self.vLayout_AccSettings.setSpacing(0)
		self.vLayout_AccSettings.setObjectName(_fromUtf8("vLayout_AccSettings"))
		self.label_MainOptions = QtGui.QLabel(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_MainOptions.sizePolicy().hasHeightForWidth())
		self.label_MainOptions.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(21)
		self.label_MainOptions.setFont(font)
		self.label_MainOptions.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_MainOptions.setObjectName(_fromUtf8("label_MainOptions"))
		self.vLayout_AccSettings.addWidget(self.label_MainOptions, QtCore.Qt.AlignHCenter)
		self.label_AccSettings = QtGui.QLabel(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_AccSettings.sizePolicy().hasHeightForWidth())
		self.label_AccSettings.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(14)
		self.label_AccSettings.setFont(font)
		self.label_AccSettings.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_AccSettings.setObjectName(_fromUtf8("label_AccSettings"))
		self.vLayout_AccSettings.addWidget(self.label_AccSettings)
		self.hLayout_ClientID = QtGui.QHBoxLayout()
		self.hLayout_ClientID.setContentsMargins(11, 11, 11, 0)
		self.hLayout_ClientID.setSpacing(0)
		self.hLayout_ClientID.setObjectName(_fromUtf8("hLayout_ClientID"))
		self.label_ClientID = QtGui.QLabel(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_ClientID.sizePolicy().hasHeightForWidth())
		self.label_ClientID.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(11)
		self.label_ClientID.setFont(font)
		self.label_ClientID.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_ClientID.setObjectName(_fromUtf8("label_ClientID"))
		self.hLayout_ClientID.addWidget(self.label_ClientID)

		self.lineEdit_ClientID = QtGui.QLineEdit(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lineEdit_ClientID.sizePolicy().hasHeightForWidth())
		self.lineEdit_ClientID.setSizePolicy(sizePolicy)
		self.lineEdit_ClientID.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);\n"
"background-color: rgb(46, 52, 54);"))
		self.lineEdit_ClientID.setInputMask(_fromUtf8(""))
		self.lineEdit_ClientID.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
		self.lineEdit_ClientID.setObjectName(_fromUtf8("lineEdit_ClientID"))
		self.lineEdit_ClientID.setText(_translate("OptionsWindow", 'c', None))
		self.hLayout_ClientID.addWidget(self.lineEdit_ClientID)

		self.vLayout_AccSettings.addLayout(self.hLayout_ClientID)
		self.hLayout_Oauth = QtGui.QHBoxLayout()
		self.hLayout_Oauth.setContentsMargins(11, 11, 11, 0)
		self.hLayout_Oauth.setSpacing(0)
		self.hLayout_Oauth.setObjectName(_fromUtf8("hLayout_Oauth"))
		self.label_Oauth = QtGui.QLabel(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Oauth.sizePolicy().hasHeightForWidth())
		self.label_Oauth.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(11)
		self.label_Oauth.setFont(font)
		self.label_Oauth.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_Oauth.setObjectName(_fromUtf8("label_Oauth"))
		self.hLayout_Oauth.addWidget(self.label_Oauth)

		self.lineEdit_Oauth = QtGui.QLineEdit(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lineEdit_Oauth.sizePolicy().hasHeightForWidth())
		self.lineEdit_Oauth.setSizePolicy(sizePolicy)
		self.lineEdit_Oauth.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236); background-color: rgb(46, 52, 54);"))
		self.lineEdit_Oauth.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
		self.lineEdit_Oauth.setObjectName(_fromUtf8("lineEdit_Oauth"))
		self.hLayout_Oauth.addWidget(self.lineEdit_Oauth)

		self.vLayout_AccSettings.addLayout(self.hLayout_Oauth)
		self.label_fieldsReq = QtGui.QLabel(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_fieldsReq.sizePolicy().hasHeightForWidth())
		self.label_fieldsReq.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setItalic(True)
		self.label_fieldsReq.setFont(font)
		self.label_fieldsReq.setStyleSheet(_fromUtf8("color: rgb(211, 215, 207);"))
		self.label_fieldsReq.setObjectName(_fromUtf8("label_fieldsReq"))
		self.vLayout_AccSettings.addWidget(self.label_fieldsReq, QtCore.Qt.AlignRight)
		self.verticalLayoutWidget_2 = QtGui.QWidget(self.centralWidget)
		self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 258, 411, 211))
		self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
		self.vLayout_PlaybkSettings = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
		self.vLayout_PlaybkSettings.setContentsMargins(11, 0, 11, 0)
		self.vLayout_PlaybkSettings.setSpacing(6)
		self.vLayout_PlaybkSettings.setObjectName(_fromUtf8("vLayout_PlaybkSettings"))
		self.label_PlaybkSettings = QtGui.QLabel(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_PlaybkSettings.sizePolicy().hasHeightForWidth())
		self.label_PlaybkSettings.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(14)
		self.label_PlaybkSettings.setFont(font)
		self.label_PlaybkSettings.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_PlaybkSettings.setObjectName(_fromUtf8("label_PlaybkSettings"))
		self.vLayout_PlaybkSettings.addWidget(self.label_PlaybkSettings)
		self.hLayout_Quality = QtGui.QHBoxLayout()
		self.hLayout_Quality.setMargin(11)
		self.hLayout_Quality.setSpacing(6)
		self.hLayout_Quality.setObjectName(_fromUtf8("hLayout_Quality"))
		self.label_filler_4 = QtGui.QLabel(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_filler_4.sizePolicy().hasHeightForWidth())
		self.label_filler_4.setSizePolicy(sizePolicy)
		self.label_filler_4.setText(_fromUtf8(""))
		self.label_filler_4.setObjectName(_fromUtf8("label_filler_4"))
		self.hLayout_Quality.addWidget(self.label_filler_4)
		self.label_Quality = QtGui.QLabel(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Quality.sizePolicy().hasHeightForWidth())
		self.label_Quality.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(11)
		self.label_Quality.setFont(font)
		self.label_Quality.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_Quality.setObjectName(_fromUtf8("label_Quality"))
		self.hLayout_Quality.addWidget(self.label_Quality)

		self.comboBox_Quality = QtGui.QComboBox(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.comboBox_Quality.sizePolicy().hasHeightForWidth())
		self.comboBox_Quality.setSizePolicy(sizePolicy)
		self.comboBox_Quality.setMinimumSize(QtCore.QSize(0, 24))
		self.comboBox_Quality.setMaximumSize(QtCore.QSize(16777215, 24))
		self.comboBox_Quality.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);\n"
"background-color: rgb(46, 52, 54);"))
		self.comboBox_Quality.setObjectName(_fromUtf8("comboBox_Quality"))

		self.comboBox_Quality.addItem(_fromUtf8(""))
		self.comboBox_Quality.addItem(_fromUtf8(""))
		self.comboBox_Quality.addItem(_fromUtf8(""))
		self.comboBox_Quality.addItem(_fromUtf8(""))
		self.comboBox_Quality.addItem(_fromUtf8(""))
		self.comboBox_Quality.addItem(_fromUtf8(""))
		self.comboBox_Quality.addItem(_fromUtf8(""))
		self.hLayout_Quality.addWidget(self.comboBox_Quality)

		self.vLayout_PlaybkSettings.addLayout(self.hLayout_Quality)
		self.hLayout_Cache = QtGui.QHBoxLayout()
		self.hLayout_Cache.setMargin(11)
		self.hLayout_Cache.setSpacing(0)
		self.hLayout_Cache.setObjectName(_fromUtf8("hLayout_Cache"))
		self.label_Cache = QtGui.QLabel(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Cache.sizePolicy().hasHeightForWidth())
		self.label_Cache.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(11)
		self.label_Cache.setFont(font)
		self.label_Cache.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_Cache.setObjectName(_fromUtf8("label_Cache"))
		self.hLayout_Cache.addWidget(self.label_Cache)

		self.lineEdit_4 = QtGui.QLineEdit(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
		self.lineEdit_4.setSizePolicy(sizePolicy)
		self.lineEdit_4.setMinimumSize(QtCore.QSize(0, 24))
		self.lineEdit_4.setMaximumSize(QtCore.QSize(16777215, 24))
		self.lineEdit_4.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);\n"
"background-color: rgb(46, 52, 54);"))
		self.lineEdit_4.setInputMask(_fromUtf8(""))
		self.lineEdit_4.setEchoMode(QtGui.QLineEdit.Normal)
		self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
		self.hLayout_Cache.addWidget(self.lineEdit_4)

		self.label_inSecs = QtGui.QLabel(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_inSecs.sizePolicy().hasHeightForWidth())
		self.label_inSecs.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setItalic(True)
		self.label_inSecs.setFont(font)
		self.label_inSecs.setStyleSheet(_fromUtf8("color: rgb(211, 215, 207);"))
		self.label_inSecs.setObjectName(_fromUtf8("label_inSecs"))
		self.hLayout_Cache.addWidget(self.label_inSecs)
		self.label_filler_5 = QtGui.QLabel(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_filler_5.sizePolicy().hasHeightForWidth())
		self.label_filler_5.setSizePolicy(sizePolicy)
		self.label_filler_5.setText(_fromUtf8(""))
		self.label_filler_5.setObjectName(_fromUtf8("label_filler_5"))
		self.hLayout_Cache.addWidget(self.label_filler_5)
		self.vLayout_PlaybkSettings.addLayout(self.hLayout_Cache)
		self.label_AboutInfo = QtGui.QLabel(self.verticalLayoutWidget_2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_AboutInfo.sizePolicy().hasHeightForWidth())
		self.label_AboutInfo.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setItalic(True)
		self.label_AboutInfo.setFont(font)
		self.label_AboutInfo.setStyleSheet(_fromUtf8("color: rgb(211, 215, 207);"))
		self.label_AboutInfo.setObjectName(_fromUtf8("label_AboutInfo"))
		self.vLayout_PlaybkSettings.addWidget(self.label_AboutInfo)
		self.hLayout_MainButtons = QtGui.QHBoxLayout()
		self.hLayout_MainButtons.setMargin(11)
		self.hLayout_MainButtons.setSpacing(0)
		self.hLayout_MainButtons.setObjectName(_fromUtf8("hLayout_MainButtons"))

		self.pButton_SaveClose = QtGui.QPushButton(self.verticalLayoutWidget_2)
		self.pButton_SaveClose.setMinimumSize(QtCore.QSize(0, 16))
		self.pButton_SaveClose.setMaximumSize(QtCore.QSize(16777215, 24))
		self.pButton_SaveClose.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.pButton_SaveClose.setObjectName(_fromUtf8("pButton_SaveClose"))
		self.pButton_SaveClose.clicked.connect(partial(self.SaveConfigs, MainWindow))
		self.hLayout_MainButtons.addWidget(self.pButton_SaveClose)

		self.pButton_Cancel = QtGui.QPushButton(self.verticalLayoutWidget_2)
		self.pButton_Cancel.setMinimumSize(QtCore.QSize(0, 16))
		self.pButton_Cancel.setMaximumSize(QtCore.QSize(16777215, 24))
		self.pButton_Cancel.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.pButton_Cancel.setObjectName(_fromUtf8("pButton_Cancel"))
		self.pButton_Cancel.clicked.connect(partial(self.MainWindow, MainWindow))
		self.hLayout_MainButtons.addWidget(self.pButton_Cancel)

		self.vLayout_PlaybkSettings.addLayout(self.hLayout_MainButtons)
		self.verticalLayoutWidget_3 = QtGui.QWidget(self.centralWidget)
		self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(9, 179, 411, 81))
		self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
		self.vLayout_ProgSettings = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
		self.vLayout_ProgSettings.setContentsMargins(11, 0, 11, 0)
		self.vLayout_ProgSettings.setSpacing(0)
		self.vLayout_ProgSettings.setObjectName(_fromUtf8("vLayout_ProgSettings"))
		self.label_ProgSettings = QtGui.QLabel(self.verticalLayoutWidget_3)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_ProgSettings.sizePolicy().hasHeightForWidth())
		self.label_ProgSettings.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(14)
		self.label_ProgSettings.setFont(font)
		self.label_ProgSettings.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_ProgSettings.setObjectName(_fromUtf8("label_ProgSettings"))
		self.vLayout_ProgSettings.addWidget(self.label_ProgSettings)
###############
################
################
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setMargin(0)
		self.horizontalLayout.setSpacing(0)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		#notifications
		self.checkBox_1 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.checkBox_1.setFont(font)
		self.checkBox_1.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.checkBox_1.setObjectName(_fromUtf8("checkBox_1"))
		state, enabled = ConfigCtrl('get', 'notifications', '')
		if state and enabled:
			self.checkBox_1.setChecked(True)
		else:
			self.checkBox_1.setChecked(False)
		self.horizontalLayout.addWidget(self.checkBox_1)
		#chatty
		self.checkBox_2 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
		self.checkBox_2.setFont(font)
		self.checkBox_2.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
		state, enabled = ConfigCtrl('get', 'chatty', '')
		if state and enabled:
			self.checkBox_2.setChecked(True)
		else:
			self.checkBox_2.setChecked(False)
		self.horizontalLayout.addWidget(self.checkBox_2)
		self.vLayout_ProgSettings.addLayout(self.horizontalLayout)
################
################
################
		self.hLayout_HeightAdjust = QtGui.QHBoxLayout()
		self.hLayout_HeightAdjust.setMargin(11)
		self.hLayout_HeightAdjust.setSpacing(0)
		self.hLayout_HeightAdjust.setObjectName(_fromUtf8("hLayout_HeightAdjust"))

		self.label_HeightAdjust = QtGui.QLabel(self.verticalLayoutWidget_3)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_HeightAdjust.sizePolicy().hasHeightForWidth())
		self.label_HeightAdjust.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(11)
		self.label_HeightAdjust.setFont(font)
		self.label_HeightAdjust.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);"))
		self.label_HeightAdjust.setObjectName(_fromUtf8("label_HeightAdjust"))
		self.hLayout_HeightAdjust.addWidget(self.label_HeightAdjust)

		self.lineEdit_5 = QtGui.QLineEdit(self.verticalLayoutWidget_3)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
		self.lineEdit_5.setSizePolicy(sizePolicy)
		self.lineEdit_5.setMinimumSize(QtCore.QSize(0, 24))
		self.lineEdit_5.setMaximumSize(QtCore.QSize(16777215, 24))
		self.lineEdit_5.setStyleSheet(_fromUtf8("color: rgb(238, 238, 236);\n"
"background-color: rgb(46, 52, 54);"))
		self.lineEdit_5.setInputMask(_fromUtf8(""))
		self.lineEdit_5.setEchoMode(QtGui.QLineEdit.Normal)
		self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
		self.hLayout_HeightAdjust.addWidget(self.lineEdit_5)

		self.label_pixels = QtGui.QLabel(self.verticalLayoutWidget_3)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_pixels.sizePolicy().hasHeightForWidth())
		self.label_pixels.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setItalic(True)
		self.label_pixels.setFont(font)
		self.label_pixels.setStyleSheet(_fromUtf8("color: rgb(211, 215, 207);"))
		self.label_pixels.setObjectName(_fromUtf8("label_pixels"))
		self.hLayout_HeightAdjust.addWidget(self.label_pixels)
		self.label_filler_3 = QtGui.QLabel(self.verticalLayoutWidget_3)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_filler_3.sizePolicy().hasHeightForWidth())
		self.label_filler_3.setSizePolicy(sizePolicy)
		self.label_filler_3.setText(_fromUtf8(""))
		self.label_filler_3.setObjectName(_fromUtf8("label_filler_3"))
		self.hLayout_HeightAdjust.addWidget(self.label_filler_3)

		self.vLayout_ProgSettings.addLayout(self.hLayout_HeightAdjust)

		OptionsWindow.setCentralWidget(self.centralWidget)

		self.retranslateUi(OptionsWindow)
		QtCore.QMetaObject.connectSlotsByName(OptionsWindow)


	def retranslateUi(self, OptionsWindow):
		state, clientid, oauth, notifications, chatty, clientheight, quality, cache = ConfigCtrl('get', 'all', '')
		OptionsWindow.setWindowTitle(_translate("OptionsWindow", "Options", None))

		self.checkBox_1.setText(_translate("MainWindow", "Notifications", None))
		self.checkBox_2.setText(_translate("MainWindow", "Chatty IRC", None))

		self.label_MainOptions.setText(_translate("OptionsWindow", "Options", None))
		self.label_AccSettings.setText(_translate("OptionsWindow", "Account Settings", None))
		self.label_ClientID.setText(_translate("OptionsWindow", "Client ID:  ", None))
		self.label_Oauth.setText(_translate("OptionsWindow", "OAuth:      ", None))
		self.label_fieldsReq.setText(_translate("OptionsWindow", "Both fields are required*", None))
		self.label_PlaybkSettings.setText(_translate("OptionsWindow", "Playback Settings", None))
		self.label_Quality.setText(_translate("OptionsWindow", "Quality:", None))

		#audio_only, 160p , 360p, 480p, 720p, 720p60, 1080p60
		if quality == '1080p60':
			self.comboBox_Quality.setItemText(0, _translate("OptionsWindow", "1080p60", None))
			self.comboBox_Quality.setItemText(1, _translate("OptionsWindow", "720p60", None))
			self.comboBox_Quality.setItemText(2, _translate("OptionsWindow", "720p", None))
			self.comboBox_Quality.setItemText(3, _translate("OptionsWindow", "480p", None))
			self.comboBox_Quality.setItemText(4, _translate("OptionsWindow", "360p", None))
			self.comboBox_Quality.setItemText(5, _translate("OptionsWindow", "160p", None))
			self.comboBox_Quality.setItemText(6, _translate("OptionsWindow", "audio only", None))
		elif quality == '720p60':
			self.comboBox_Quality.setItemText(1, _translate("OptionsWindow", "1080p60", None))
			self.comboBox_Quality.setItemText(0, _translate("OptionsWindow", "720p60", None))
			self.comboBox_Quality.setItemText(2, _translate("OptionsWindow", "720p", None))
			self.comboBox_Quality.setItemText(3, _translate("OptionsWindow", "480p", None))
			self.comboBox_Quality.setItemText(4, _translate("OptionsWindow", "360p", None))
			self.comboBox_Quality.setItemText(5, _translate("OptionsWindow", "160p", None))
			self.comboBox_Quality.setItemText(6, _translate("OptionsWindow", "audio only", None))
		elif quality == '720p':
			self.comboBox_Quality.setItemText(1, _translate("OptionsWindow", "1080p60", None))
			self.comboBox_Quality.setItemText(2, _translate("OptionsWindow", "720p60", None))
			self.comboBox_Quality.setItemText(0, _translate("OptionsWindow", "720p", None))
			self.comboBox_Quality.setItemText(3, _translate("OptionsWindow", "480p", None))
			self.comboBox_Quality.setItemText(4, _translate("OptionsWindow", "360p", None))
			self.comboBox_Quality.setItemText(5, _translate("OptionsWindow", "160p", None))
			self.comboBox_Quality.setItemText(6, _translate("OptionsWindow", "audio only", None))
		elif quality == '480p':
			self.comboBox_Quality.setItemText(1, _translate("OptionsWindow", "1080p60", None))
			self.comboBox_Quality.setItemText(2, _translate("OptionsWindow", "720p60", None))
			self.comboBox_Quality.setItemText(3, _translate("OptionsWindow", "720p", None))
			self.comboBox_Quality.setItemText(0, _translate("OptionsWindow", "480p", None))
			self.comboBox_Quality.setItemText(4, _translate("OptionsWindow", "360p", None))
			self.comboBox_Quality.setItemText(5, _translate("OptionsWindow", "160p", None))
			self.comboBox_Quality.setItemText(6, _translate("OptionsWindow", "audio only", None))
		elif quality == '360p':
			self.comboBox_Quality.setItemText(1, _translate("OptionsWindow", "1080p60", None))
			self.comboBox_Quality.setItemText(2, _translate("OptionsWindow", "720p60", None))
			self.comboBox_Quality.setItemText(3, _translate("OptionsWindow", "720p", None))
			self.comboBox_Quality.setItemText(4, _translate("OptionsWindow", "480p", None))
			self.comboBox_Quality.setItemText(0, _translate("OptionsWindow", "360p", None))
			self.comboBox_Quality.setItemText(5, _translate("OptionsWindow", "160p", None))
			self.comboBox_Quality.setItemText(6, _translate("OptionsWindow", "audio only", None))
		elif quality == '160p':
			self.comboBox_Quality.setItemText(1, _translate("OptionsWindow", "1080p60", None))
			self.comboBox_Quality.setItemText(2, _translate("OptionsWindow", "720p60", None))
			self.comboBox_Quality.setItemText(3, _translate("OptionsWindow", "720p", None))
			self.comboBox_Quality.setItemText(4, _translate("OptionsWindow", "480p", None))
			self.comboBox_Quality.setItemText(5, _translate("OptionsWindow", "360p", None))
			self.comboBox_Quality.setItemText(0, _translate("OptionsWindow", "160p", None))
			self.comboBox_Quality.setItemText(6, _translate("OptionsWindow", "audio only", None))
		elif quality == 'audio_only':
			self.comboBox_Quality.setItemText(1, _translate("OptionsWindow", "1080p60", None))
			self.comboBox_Quality.setItemText(2, _translate("OptionsWindow", "720p60", None))
			self.comboBox_Quality.setItemText(3, _translate("OptionsWindow", "720p", None))
			self.comboBox_Quality.setItemText(4, _translate("OptionsWindow", "480p", None))
			self.comboBox_Quality.setItemText(5, _translate("OptionsWindow", "360p", None))
			self.comboBox_Quality.setItemText(6, _translate("OptionsWindow", "160p", None))
			self.comboBox_Quality.setItemText(0, _translate("OptionsWindow", "audio only", None))
		else:
			self.comboBox_Quality.setItemText(1, _translate("OptionsWindow", "there", None))
			self.comboBox_Quality.setItemText(2, _translate("OptionsWindow", "was an", None))
			self.comboBox_Quality.setItemText(3, _translate("OptionsWindow", "error", None))
			self.comboBox_Quality.setItemText(4, _translate("OptionsWindow", "with", None))
			self.comboBox_Quality.setItemText(5, _translate("OptionsWindow", "the", None))
			self.comboBox_Quality.setItemText(0, _translate("OptionsWindow", "quality", None))
			ShowDialogInfo('warning', 'Reason: The quality string is not valid for Twitch.',
				'The current combobox value is: ({0}).'.format(quality))

		self.label_Cache.setText(_translate("OptionsWindow", "Cache:", None))
		self.label_inSecs.setText(_translate("OptionsWindow", "  (in seconds)", None))
		self.label_AboutInfo.setText(_translate("OptionsWindow", " See the \'About\' button on the main window for detailed instructions...", None))
		self.pButton_SaveClose.setText(_translate("OptionsWindow", "Save / Close", None))
		self.pButton_Cancel.setText(_translate("OptionsWindow", "Cancel", None))
		self.label_ProgSettings.setText(_translate("OptionsWindow", "Program Settings", None))
		self.label_HeightAdjust.setText(_translate("OptionsWindow", "Height Adjust: ", None))
		self.label_pixels.setText(_translate("OptionsWindow", "  (in pixels)", None))
		
		self.lineEdit_ClientID.setText(_translate("OptionsWindow", clientid, None))
		self.lineEdit_Oauth.setText(_translate("OptionsWindow", oauth, None))
		self.lineEdit_4.setText(_translate("OptionsWindow", str(cache/1000), None))
		self.lineEdit_5.setText(_translate("OptionsWindow", str(clientheight), None))

###
####
###
#GLOBAL
def Notification(who):
	state, enabled = ConfigCtrl('get', 'notifications', '')
	if state and enabled:
		Notify.init("Twitch_Qt4")
		desiredLength = 4
		#small bursts notifications because newlines dont work?
		if len(who) >= desiredLength:
			notifyArray = []
			for i in who:
				notifyArray.append(str(i))
				if len(notifyArray) >= 4:
					note=Notify.Notification.new(
						"Twitch_Qt4", "{0}".format(', '.join([str(x) for x in notifyArray])),
						assetsPath+'glitch.png'
						)
					note.show()
					notifyArray = []
		else:
			#input list less than desiredLength
			note=Notify.Notification.new("Twitch_Qt4",
				"{0}".format(', '.join([str(x) for x in who])),
				assetsPath+'glitch.png'
				)
		note.show()		

###################################################################################################
###############################################################MAIN-WINDOW-FUNCTIONS###############
###################################################################################################
buttonPos = 0 #used to keeptrack of how many buttons and put labels after each
strStore1 = []
class Ui_MainWindow(object):

	def AddLabels(self, MainWindow, labelName, labelGame):
		#data uses delimiter 'streamer':''game'
		global buttonPos
		labelPos = buttonPos + 1

		self.streamerLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.streamerLabel.sizePolicy().hasHeightForWidth())
		self.streamerLabel.setSizePolicy(sizePolicy)
		self.streamerLabel.setMinimumSize(QtCore.QSize(161, 64))
		self.streamerLabel.setMaximumSize(QtCore.QSize(128, 64))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Ubuntu"))
		font.setPointSize(10)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(50)
		self.streamerLabel.setFont(font)
		self.streamerLabel.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255); background-color: rgb(95, 60, 159);"))
		self.streamerLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.streamerLabel.setWordWrap(True)
		self.streamerLabel.setObjectName(_fromUtf8(labelName))
		self.streamerLabel.setText(_translate("MainWindow", '{0}\n{1}'.format(labelName, labelGame), None))
		#				           							 #r #c
		self.gridLayout.addWidget(self.streamerLabel, labelPos, 0, 1, 1)

	def DeleteButtons(self, MainWindow):
		#remove all widgets in the scroll area
		while self.gridLayout.count():
			child = self.gridLayout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())
			else:
				continue
		#not resetting
		global buttonPos
		buttonPos = 0

	def ButtonImage(self, streamerName):
		# searches for streamer name in the image cache folder
		# and returns a result to be shown in the GUI
		path = os.path.dirname(os.path.realpath(__file__))
		if streamerName != 'null':
			imgPath = path + r'/img_cache/'
			for imgFile in os.listdir(imgPath):
				isFile = re.search(streamerName, imgFile)
				if isFile:
					return str(imgPath + imgFile)
		else:
			#no match or is null -> return placeholder.jpg in assets
			phPath = path + r'/assets/placeholder.jpg'
			return phPath

	def AddButtons(self, MainWindow, data):
		#buttonpos for label alignment
		global buttonPos
		data = data.split('~')
		if len(data) == 2:
			labelName = str(data[0])
			labelGame = str(data[1])
		else:
			labelName = 'null'
			labelGame = 'null'

		#image for button
		picPath = self.ButtonImage(labelName)

		class button(object):
			def __init__(self, ident, name, game, picPath):
				self.id = ident
				self.name = name
				self.game = game
				self.pic = picPath
		btn_object = button(buttonPos, labelName, labelGame, picPath)

		self.streamerBtn = QtGui.QToolButton(self.scrollAreaWidgetContents)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.streamerBtn.sizePolicy().hasHeightForWidth())
		self.streamerBtn.setSizePolicy(sizePolicy)
		self.streamerBtn.setMinimumSize(QtCore.QSize(161, 64))
		self.streamerBtn.setMaximumSize(QtCore.QSize(161, 64))
		self.streamerBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(_fromUtf8(btn_object.pic)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.streamerBtn.setIcon(icon1)
		self.streamerBtn.setIconSize(QtCore.QSize(64, 64))
		self.streamerBtn.setPopupMode(QtGui.QToolButton.DelayedPopup)
		self.streamerBtn.setAutoRaise(True)
		self.streamerBtn.setObjectName(_fromUtf8(str(btn_object.id)))

		self.streamerBtn.clicked.connect(partial(self.StreamCall, btn_object.name))
		
		self.gridLayout.addWidget(self.streamerBtn, buttonPos, 0, 1, 1)
		self.AddLabels(self, btn_object.name, btn_object.game)
		buttonPos += 2

	def Chatty(self, oauth, stream):
		state, chattyEnabled = ConfigCtrl('get', 'chatty', '')
		if state and chattyEnabled:
			from subprocess import Popen,PIPE,STDOUT
			chattyPath = os.path.dirname(os.path.realpath(__file__)) + '/chatty/Chatty.jar' #for images
			if os.path.exists(chattyPath):
				try:
					call = 'java -jar {0} -connect -single -token {1} -channel {2}'.format(chattyPath, oauth, stream)
					proc = Popen(call, shell=True, stderr=STDOUT, stdout=PIPE)
				except Exception as e:
					ShowDialogInfo('critical', 'Error executing Chatty!','{0}'.format(e))
			else:
				ShowDialogInfo('warning', 'Error opening Chatty because the file is not present.','I see: {0}'.format(os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/chatty/')))

	def StreamCall(self, stream, quality):
		state, oauth = ConfigCtrl('get', 'oauth', '')
		state, cache = ConfigCtrl('get', 'cache', '')
		#sometimes passed a quality when not supported
		if not quality:
			state, quality = ConfigCtrl('get', 'quality', '')

		call, errorCode, errorComment = streamLib.Livestreamer(stream,oauth,cache,quality)
		if not call and errorCode:
			if errorCode == 1:
				self.ShowDialogQuality(stream, errorComment, quality)
			else:
				errorComment = errorComment.split('~')
				ShowDialogInfo('warning', '{0}'.format(errorComment[0]),'{0}.'.format(errorComment[1]))
		else:
			self.Chatty(oauth, stream)

##########################MENU-BUTTONS#####################################

	def EnableReset(self):
		#enable reset button after timer and set icon
		self.menuBtn_Refresh.setEnabled(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8(assetsPath + "refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.menuBtn_Refresh.setIcon(icon)

	def Refresh(self, MainWindow):
		#progstate to not show notifications on startup being first run
		#streamerStore an array to compare to notify
		global strStore1
		strStore2 = []
		#disable reset button and remove icon
		self.menuBtn_Refresh.setEnabled(False)
		self.menuBtn_Refresh.setIcon(QtGui.QIcon())
		QtCore.QTimer.singleShot(3000, self.EnableReset)

		call, errorCode, resultList = streamLib.GetStreams(ConfigCtrl('get', 'clientid', '')[1], ConfigCtrl('get', 'oauth', '')[1])
		if call and errorCode == 0:
			self.DeleteButtons(MainWindow)
			for s in resultList:
				name = s.name
				game = s.game
				self.AddButtons(self, '{0}~{1}'.format(name.encode('utf8'), game.encode('utf8')))
#  File "/home/dev/Documents/scripts/Twitch_Qt4_edit/Twitch_Qt4.py", line 828, in Refresh
#    self.AddButtons(self, '{0}~{1}'.format(name, game))
#UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' in position 3: ordinal not in range(128)				
				###NOTIFY
				if name not in strStore1:
					strStore1.append(name)
					strStore2.append(name)

			if len(strStore2) > 0:
				Notification(strStore2)
		else:
			error = resultList.split('~')
			if len(error) == 2:
				ShowDialogInfo('warning', 'Reason: {0}.'.format(error[0]),
					'{0}.'.format(error[1]))

	def OptionsWindow(self, MainWindow):
		#opens options window
		Oui = Ui_OptionsWindow()
		Oui.setupOptionUi(MainWindow)
		MainWindow.show()

	def OpenAbout(self):
		import webbrowser
		url = 'https://github.com/datguy-dev/Twitch_Qt4'
		#opens options window
		webbrowser.open_new(url)
		return

	def ShowDialogQuality(self, stream, comment, quality):
		#when streamlib cannot use the quality in config. ask to use next best quality.
		msg = QtGui.QMessageBox()
		msg.setWindowTitle('Twitch_Qt')
		msg.setIcon(QtGui.QMessageBox.Question)
		msg.setText('{0} does not support the quality {1}'.format(stream, quality))
		msg.setInformativeText('Try the next best quality of {0}?'.format(comment))
		msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		btnValue = msg.exec_()

		if btnValue == QtGui.QMessageBox.Yes:
			self.StreamCall(stream, comment)
		else:
			pass
		return

	def ShowDialogCustom(self):
		#custom menu button. enter a streamer name to open stream.
		stream, state = QtGui.QInputDialog().getText(None, "Custom", "Enter a stream name:")
		response = str(stream).lower()
		if state and len(response) > 0:
			self.StreamCall(response, '')
			#streamLib.Livestreamer(response, ConfigCtrl('get', 'oauth', ''), ConfigCtrl('get', 'cache', '') * 1000, ConfigCtrl('get', 'quality', ''))

###################################################################################################
###############################################################MAIN-WINDOW-FUNCTIONS###############
###################################################################################################

	def setupUi(self, MainWindow):
		#reload config.py and use height adjustment value
		state, heightAdjust = ConfigCtrl('get', 'clientheight', '')


		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.setEnabled(True)
		MainWindow.resize(161, 416 + heightAdjust) #416
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
		MainWindow.setSizePolicy(sizePolicy)
		MainWindow.setMinimumSize(QtCore.QSize(161, 416 + heightAdjust))
		MainWindow.setMaximumSize(QtCore.QSize(161, 416 + heightAdjust))
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8(assetsPath + "glitch.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)
		MainWindow.setAutoFillBackground(False)
		MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
		MainWindow.setWindowTitle(_translate("MainWindow", "Twitch_Qt", None))

		self.centralWidget = QtGui.QWidget(MainWindow)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
		self.centralWidget.setSizePolicy(sizePolicy)
		self.centralWidget.setMinimumSize(QtCore.QSize(161, 416 + heightAdjust))
		self.centralWidget.setMaximumSize(QtCore.QSize(161, 416 + heightAdjust))
		self.centralWidget.setObjectName(_fromUtf8("centralWidget"))

		self.scrollArea = QtGui.QScrollArea(self.centralWidget)
		self.scrollArea.setGeometry(QtCore.QRect(0, 0, 161, 381 + heightAdjust))
		self.scrollArea.setStyleSheet(_fromUtf8("background-color: rgb(100, 65, 164);"))
		self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
		self.scrollArea.setLineWidth(3)
		self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName(_fromUtf8("scrollArea"))

		self.scrollAreaWidgetContents = QtGui.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 161, 381))
		self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))

		self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
		self.gridLayout.setMargin(0)
		self.gridLayout.setSpacing(0)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)

		self.horizontalLayoutWidget = QtGui.QWidget(self.centralWidget)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 380 + heightAdjust, 161, 34)) #x,y,width,height
		self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))

		self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
		self.horizontalLayout_2.setMargin(5)
		self.horizontalLayout_2.setSpacing(5)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

		self.menuBtn_Refresh = QtGui.QToolButton(self.horizontalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.menuBtn_Refresh.sizePolicy().hasHeightForWidth())
		self.menuBtn_Refresh.setEnabled(True)
		self.menuBtn_Refresh.setSizePolicy(sizePolicy)
		self.menuBtn_Refresh.setMinimumSize(QtCore.QSize(24, 24))
		self.menuBtn_Refresh.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8(assetsPath + "refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.menuBtn_Refresh.setIcon(icon)
		self.menuBtn_Refresh.setObjectName(_fromUtf8("menuBtn_Refresh"))
		self.menuBtn_Refresh.clicked.connect(partial(self.Refresh, MainWindow))
		self.horizontalLayout_2.addWidget(self.menuBtn_Refresh)

		self.menuBtn_Custom = QtGui.QToolButton(self.horizontalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.menuBtn_Custom.sizePolicy().hasHeightForWidth())
		self.menuBtn_Custom.setSizePolicy(sizePolicy)
		self.menuBtn_Custom.setMinimumSize(QtCore.QSize(24, 24))
		self.menuBtn_Custom.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))

		icon.addPixmap(QtGui.QPixmap(_fromUtf8(assetsPath + "custom.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.menuBtn_Custom.setIcon(icon)
		self.menuBtn_Custom.setObjectName(_fromUtf8("menuBtn_Custom"))

		self.menuBtn_Custom.clicked.connect(partial(self.ShowDialogCustom))

		self.horizontalLayout_2.addWidget(self.menuBtn_Custom)

		self.menuBtn_About = QtGui.QToolButton(self.horizontalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.menuBtn_About.sizePolicy().hasHeightForWidth())
		self.menuBtn_About.setSizePolicy(sizePolicy)
		self.menuBtn_About.setMinimumSize(QtCore.QSize(24, 24))
		self.menuBtn_About.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(_fromUtf8(assetsPath + "about.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.menuBtn_About.setIcon(icon3)
		self.menuBtn_About.setPopupMode(QtGui.QToolButton.DelayedPopup)
		self.menuBtn_About.setObjectName(_fromUtf8("menuBtn_About"))
		self.menuBtn_About.clicked.connect(self.OpenAbout)
		self.horizontalLayout_2.addWidget(self.menuBtn_About)

		
		self.menuBtn_Config = QtGui.QToolButton(self.horizontalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.menuBtn_Config.sizePolicy().hasHeightForWidth())
		self.menuBtn_Config.setSizePolicy(sizePolicy)
		self.menuBtn_Config.setMinimumSize(QtCore.QSize(24, 24))

		icon.addPixmap(QtGui.QPixmap(_fromUtf8(assetsPath + "config.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.menuBtn_Config.setIcon(icon)
		self.menuBtn_Config.setObjectName(_fromUtf8("menuBtn_Config"))
		self.menuBtn_Config.clicked.connect(partial(self.OptionsWindow, MainWindow))
		self.horizontalLayout_2.addWidget(self.menuBtn_Config)
		MainWindow.setCentralWidget(self.centralWidget)

		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.Refresh(MainWindow)

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s
try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

