
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QSizeGrip
from PyQt5 import QtCore, QtGui, uic

qtCreatorFile = "GUI2.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

##from PyRecordMenu import Ui_MainWindow
from AudioRecorderFunctions import *
import GlobalVars



def RescanInputsButtonPushed():
    
    import GlobalVars
    import pyaudio 
    import sys, serial
    

    from serial.tools import list_ports
    import pdb

    #TeensyPort = (list_ports.grep("Arduino"))
    TeensyPort = (list_ports.comports())

    i=0;    
    ui.ArduinoSelectioncomboBox.clear();
    for p in TeensyPort:                              
               temp = p[0]
               #print(temp)
               ui.ArduinoSelectioncomboBox.insertItem(0,str(temp))          


    if (len(temp)>0):
        GlobalVars.COM_PORT=(temp)
    else:
        print("No Teensy Serial Device")   
    
    inputdevices = 0
    outputdevices=0    
    pya = pyaudio.PyAudio()
    info = pya.get_host_api_info_by_index(0)
    DeviceList = info.get('deviceCount')

    ui.InputSelectioncomboBox.disconnect();
    ui.InputSelectioncomboBox.clear();    
    for i in range (0,DeviceList):        
        if pya.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>1:
            # print(pya.get_device_info_by_host_api_device_index(0,i).get('name'))            
             ui.InputSelectioncomboBox.insertItem(20,str(pya.get_device_info_by_host_api_device_index(0,i).get('name')))    
             inputdevices+=1

    ui.InputSelectioncomboBox.currentIndexChanged.connect(InputSelectioncomboBoxChanged)
    InputSelectioncomboBoxChanged(ui.InputSelectioncomboBox.currentIndex())    
    #pdb.set_trace()
    
    ui.OutputSelectionComboBox.disconnect(); 
    ui.OutputSelectionComboBox.clear();
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,DeviceList):
      #  print(pya.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels'))
        if pya.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>1:
          #   print(pya.get_device_info_by_host_api_device_index(0,i).get('name'))            
             ui.OutputSelectionComboBox.insertItem(20,str(pya.get_device_info_by_host_api_device_index(0,i).get('name')))    
             outputdevices+=1
    pya.terminate();        
    
    ui.OutputSelectionComboBox.currentIndexChanged.connect(OutputSelectioncomboBoxChanged);
    OutputSelectioncomboBoxChanged(ui.OutputSelectionComboBox.currentIndex())    
    
def StopPushButton():   
    import GlobalVars
    GlobalVars.isRunning=0    
  
    ui.RescanInputsPushButton.setEnabled(True)
    ui.SampleRatecomboBox.setEnabled(True);

    ui.ArduinoSelectioncomboBox.setEnabled(True);
    ui.OutputSelectionComboBox.setEnabled(True);
    ui.OutputSampleRatecomboBox.setEnabled(True);    
 
    ui.InputSelectioncomboBox.setEnabled(True)
    ui.BufferTimeSpinBox.setEnabled(True)    
    ui.ListeningTextBox.setText('')
    ui.Ch1SaveDirPushButton.setEnabled(True);
    ui.Ch2SaveDirPushButton.setEnabled(True);
    ui.Ch3SaveDirPushButton.setEnabled(True);
    ui.Ch4SaveDirPushButton.setEnabled(True);
    ui.ThresholdLineEdit1.setEnabled(True)
    ui.ThresholdLineEdit2.setEnabled(True)
    ui.ThresholdLineEdit3.setEnabled(True)
    ui.ThresholdLineEdit4.setEnabled(True)

    ui.Box1LevercomboBox.setEnabled(True);
    ui.Box2LevercomboBox.setEnabled(True);
    ui.Box3LevercomboBox.setEnabled(True);
    ui.Box4LevercomboBox.setEnabled(True);    

    ui.Ch1AudioFileSelectButton.setEnabled(True);
    ui.Ch2AudioFileSelectButton.setEnabled(True);
    ui.Ch3AudioFileSelectButton.setEnabled(True);
    ui.Ch4AudioFileSelectButton.setEnabled(True);
    
    ui.StartPushButton.setEnabled(True)
      
def StartPushButton():

    import GlobalVars
    import time;
    
    
    ui.RescanInputsPushButton.setEnabled(False)
    
    ui.ArduinoSelectioncomboBox.setEnabled(False);
    ui.OutputSelectionComboBox.setEnabled(False);
    ui.OutputSampleRatecomboBox.setEnabled(False);    

    ui.SampleRatecomboBox.setEnabled(False);    
  
    ui.InputSelectioncomboBox.setEnabled(False)    
    ui.BufferTimeSpinBox.setEnabled(True)
    ui.Ch1SaveDirPushButton.setEnabled(False);
    ui.Ch2SaveDirPushButton.setEnabled(False);
    ui.Ch3SaveDirPushButton.setEnabled(False);
    ui.Ch4SaveDirPushButton.setEnabled(False);
    
    ui.ThresholdLineEdit1.setEnabled(True)
    ui.ThresholdLineEdit2.setEnabled(True)
    ui.ThresholdLineEdit3.setEnabled(True)
    ui.ThresholdLineEdit4.setEnabled(True)
    
    ui.Ch1AudioFileSelectButton.setEnabled(False);
    ui.Ch2AudioFileSelectButton.setEnabled(False);
    ui.Ch3AudioFileSelectButton.setEnabled(False);    
    ui.Ch4AudioFileSelectButton.setEnabled(False);
    
    ui.Box1LevercomboBox.setEnabled(False);
    ui.Box2LevercomboBox.setEnabled(False);
    ui.Box3LevercomboBox.setEnabled(False);
    ui.Box4LevercomboBox.setEnabled(False);
    
    pya = pyaudio.PyAudio()
    inputdevicename=pya.get_device_info_by_host_api_device_index(0,GlobalVars.inputdeviceindex).get('name')
    outputdevicename=pya.get_device_info_by_host_api_device_index(0,GlobalVars.outputdeviceindex).get('name')
    pya.terminate();
    T=time.localtime()
    outtime=str("%02d"%T[0])+','+str("%02d"%T[1])+','+str("%02d"%T[2])+','+str("%02d"%T[3])+','+str("%02d"%T[4])+','+str("%02d"%T[5])
    
    if (ui.Ch1checkBox.isEnabled()):
        fobject=open(GlobalVars.Ch1DirPath+'/Ch1LogFile.log','a+');                
        fobject.write(outtime+',Ch1,Input:'+inputdevicename+','+ui.SampleRatecomboBox.currentText()+',Output:'+outputdevicename+','+str(GlobalVars.outputsamplerate)+'\n');
    if (ui.Ch2checkBox.isEnabled()):
        fobject=open(GlobalVars.Ch2DirPath+'/Ch2LogFile.log','a+');                
        fobject.write(outtime+',Ch2,Input:'+inputdevicename+','+ui.SampleRatecomboBox.currentText()+',Output:'+outputdevicename+','+str(GlobalVars.outputsamplerate)+'\n');
    if (ui.Ch4checkBox.isEnabled()):
        fobject=open(GlobalVars.Ch4DirPath+'/Ch4LogFile.log','a+');                
        fobject.write(outtime+',Ch4,Input:'+inputdevicename+','+ui.SampleRatecomboBox.currentText()+',Output:'+outputdevicename+','+str(GlobalVars.outputsamplerate)+'\n');        
    if (ui.Ch3checkBox.isEnabled()):
        fobject=open(GlobalVars.Ch3DirPath+'/Ch3LogFile.log','a+');
        fobject.write(outtime+',Ch3,Input:'+inputdevicename+','+ui.SampleRatecomboBox.currentText()+',Output:'+outputdevicename+','+str(GlobalVars.outputsamplerate)+'\n');
        
    pya.terminate();
    GlobalVars.isRunning=1
    ui.StartPushButton.setEnabled(False)
    
    
    try:        
        TriggeredRecordAudio(ui)
    except Exception as e: 
        print(e)

def ThresholdLineEditChanged1(newvalue):
    import GlobalVars
    GlobalVars.threshold1=float(newvalue)        
    
def ThresholdLineEditChanged2(newvalue):
    import GlobalVars
    GlobalVars.threshold2=float(newvalue)

def ThresholdLineEditChanged3(newvalue):
    import GlobalVars
    GlobalVars.threshold3=float(newvalue)

def ThresholdLineEditChanged4(newvalue):
    import GlobalVars
    GlobalVars.threshold4=float(newvalue)    
   
def BufferTimeSpinBoxChanged(newvalue):
    import GlobalVars
    GlobalVars.buffertime=int(newvalue)
    
def InputSelectioncomboBoxChanged(newvalue):
    import GlobalVars
    import pyaudio
    import pdb
    
    
    GlobalVars.inputdeviceindex=int(newvalue)    

    p = pyaudio.PyAudio()
    
    devinfo = p.get_device_info_by_index(int(newvalue))    
    samplerates = 32000, 44100, 48000, 96000, 128000

    
    ui.SampleRatecomboBox.disconnect()
    ui.SampleRatecomboBox.clear();
    
    for fs in samplerates:
        try:        
            p.is_format_supported(fs,  # Sample rate
                         input_device=devinfo['index'],
                         input_channels=devinfo['maxInputChannels'],
                         input_format=pyaudio.paInt16)
            ui.SampleRatecomboBox.insertItem(20,str(fs))                
        except Exception as e:
            print('Failed at')
            print(fs, e)        
         
    ui.SampleRatecomboBox.setCurrentText(str(GlobalVars.SampleRate));
    ui.SampleRatecomboBox.currentIndexChanged.connect(updateSampleRate);
    GlobalVars.CHANNELS=p.get_device_info_by_host_api_device_index(0,ui.SampleRatecomboBox.currentIndex()).get('maxInputChannels')    
    GlobalVars.AudioDeviceName=ui.InputSelectioncomboBox.currentText();
    
    p.terminate
    
    ui.Ch1SaveDirPushButton.setEnabled(False);
    ui.Ch2SaveDirPushButton.setEnabled(False);
    ui.Ch3SaveDirPushButton.setEnabled(False);
    ui.Ch4SaveDirPushButton.setEnabled(False);

    ui.Ch1checkBox.setEnabled(False);
    ui.Ch1checkBox.setEnabled(False);
    ui.Ch1checkBox.setEnabled(False);
    ui.Ch1checkBox.setEnabled(False); 


    if (GlobalVars.CHANNELS >0):
        ui.Ch1SaveDirPushButton.setEnabled(True);
        if (len(GlobalVars.Ch1fileName)>0):
            ui.Ch1checkBox.setEnabled(True);

    if (GlobalVars.CHANNELS >1):
        ui.Ch2SaveDirPushButton.setEnabled(True);
        if (len(GlobalVars.Ch2fileName)>0):
            ui.Ch2checkBox.setEnabled(True);
    if (GlobalVars.CHANNELS >2):
        ui.Ch3SaveDirPushButton.setEnabled(True);
        if (len(GlobalVars.Ch3fileName)>0):
            ui.Ch3checkBox.setEnabled(True);            
    if (GlobalVars.CHANNELS >3):
        ui.Ch4SaveDirPushButton.setEnabled(True);
        if (len(GlobalVars.Ch4fileName)>0):
            ui.Ch4checkBox.setEnabled(True);                   

def OutputSelectioncomboBoxChanged(newvalue):
    import GlobalVars
    import pyaudio
    import pdb        

    p = pyaudio.PyAudio()            
    info = p.get_host_api_info_by_index(0)
    DeviceList = info.get('deviceCount')

    samplerates = 32000, 44100, 48000, 96000, 128000

    ## Search the listings and find the current text for that one, since outputs aren't ordered 0-x like inputs
    
    for i in range (0,DeviceList):        
        if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:            
             if (p.get_device_info_by_host_api_device_index(0,i).get('name').find(ui.OutputSelectionComboBox.currentText())!=-1):
                 GlobalVars.outputdeviceindex=i;                
      
    devinfo = p.get_device_info_by_index(GlobalVars.outputdeviceindex)
    
    ui.OutputSampleRatecomboBox.disconnect()
    ui.OutputSampleRatecomboBox.clear();
    
    for fs in samplerates:
        try:            
            p.is_format_supported(fs,  # Sample rate
                         output_device=devinfo['index'],
                         output_channels=devinfo['maxOutputChannels'],
                         output_format=pyaudio.paInt16)
        except Exception as e:
            print('Failed at')
            print(fs, e)
        else:            
            ui.OutputSampleRatecomboBox.insertItem(20,str(fs))    

    ui.OutputSampleRatecomboBox.setCurrentText(str(GlobalVars.outputsamplerate))
    ui.OutputSampleRatecomboBox.currentIndexChanged.connect(updateOutputSampleRate);
        
    GlobalVars.OutputAudioDeviceName=ui.OutputSelectionComboBox.currentText();    #GlobalVars.outputsamplerate=int(ui.OutputSampleRatecomboBox.currentText())
    #print(GlobalVars.outputsamplerate)
 
    p.terminate

def Ch1SaveDirPushButtonpushButtonClicked():

    import os
    import GlobalVars
    import pdb
    
    savefilename = (QtWidgets.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch1DirPath, ''))
    GlobalVars.Ch1DirPath = QtCore.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch1fileName = QtCore.QFileInfo(savefilename[0]).fileName();
    
    ui.Ch1FileNameLabel.setText("Filename: "+GlobalVars.Ch1fileName)
    ui.Ch1FileDirectoryLabel.setText("Directory: "+GlobalVars.Ch1DirPath)
    ui.Ch1checkBox.setEnabled(True);

    
def Ch2SaveDirPushButtonpushButtonClicked():
    import GlobalVars

    import os
    import GlobalVars
    
    savefilename = (QtWidgets.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch2DirPath, '.wav'))
    GlobalVars.Ch2DirPath = QtCore.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch2fileName = QtCore.QFileInfo(savefilename[0]).fileName();
    
    ui.Ch2FileNameLabel.setText("Filename: "+GlobalVars.Ch2fileName)
    ui.Ch2FileDirectoryLabel.setText("Directory: "+GlobalVars.Ch2DirPath)
    ui.Ch2checkBox.setEnabled(True);
    
def Ch3SaveDirPushButtonpushButtonClicked():        
    import GlobalVars

    import os
    import GlobalVars
    
    savefilename = (QtWidgets.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch3DirPath, '.wav'))
    GlobalVars.Ch3DirPath = QtCore.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch3fileName = QtCore.QFileInfo(savefilename[0]).fileName();

    ui.Ch3FileNameLabel.setText("Filename: "+GlobalVars.Ch3fileName)
    ui.Ch3FileDirectoryLabel.setText("Directory: "+GlobalVars.Ch3DirPath)
    ui.Ch3checkBox.setEnabled(True);
    
def Ch4SaveDirPushButtonpushButtonClicked():
    import os
    import GlobalVars
    
    savefilename = (QtWidgets.QFileDialog.getSaveFileName(ui,'Save Name/Directory', GlobalVars.Ch4DirPath, '.wav'))
    GlobalVars.Ch4DirPath = QtCore.QFileInfo(savefilename[0]).path();
    GlobalVars.Ch4fileName = QtCore.QFileInfo(savefilename[0]).fileName();

    ui.Ch4FileNameLabel.setText(GlobalVars.Ch4fileName)
    ui.Ch4FileDirectoryLabel.setText(GlobalVars.Ch4DirPath);
    ui.Ch4checkBox.setEnabled(True);
    
def loadConfig_ButtonPressed():
    import os
    import GlobalVars       
    import pdb

    
    loadfilename = (QtWidgets.QFileDialog.getOpenFileName(ui,'Open Config File', './','*.TUTcfg'))
    
    GlobalVars.loadConfig(loadfilename[0],ui)

def saveConfig_ButtonPressed():
    import GlobalVars

    
    
    savefilename = (QtWidgets.QFileDialog.getSaveFileName(ui,'Save Config File', './', '.TUTcfg','.TUTcfg'))
    GlobalVars.saveConfig(savefilename[0]+savefilename[1])

def updateSampleRate():
    import GlobalVars

    GlobalVars.inputSampleRateIDX=int(ui.SampleRatecomboBox.currentIndex())
    GlobalVars.SampleRate=int(ui.SampleRatecomboBox.currentText())

def updateOutputSampleRate():
    import GlobalVars

    GlobalVars.outputSampleIDX=int(ui.OutputSampleRatecomboBox.currentIndex())        
    GlobalVars.outputsamplerate=int(ui.OutputSampleRatecomboBox.currentText())
    
def Ch1OnChanged():
    import GlobalVars
    GlobalVars.Ch1On = ui.Ch1checkBox.isChecked();

def Ch2OnChanged():
    import GlobalVars
    GlobalVars.Ch2On = ui.Ch2checkBox.isChecked();

def Ch3OnChanged():
    import GlobalVars
    GlobalVars.Ch3On = ui.Ch3checkBox.isChecked();

def Ch4OnChanged():
    import GlobalVars
    GlobalVars.Ch4On = ui.Ch4checkBox.isChecked();    

def ChangeArduinoCom():
    import GlobalVars
    GlobalVars.COM_PORT=ui.ArduinoSelectioncomboBox.currentText();   

def Ch1TriggerChanged():
    import GlobalVars
    GlobalVars.Pin1 = int(ui.Box1LevercomboBox.currentText());
    
def Ch2TriggerChanged():
    import GlobalVars
    GlobalVars.Pin2 = int(ui.Box2LevercomboBox.currentText());

def Ch3TriggerChanged():
    import GlobalVars
    GlobalVars.Pin3 = int(ui.Box3LevercomboBox.currentText());

def Ch4TriggerChanged():
    import GlobalVars
    GlobalVars.Pin4 = int(ui.Box4LevercomboBox.currentText());

def Ch1SelectAudioFiles():
    import GlobalVars
    import pdb
    import wave;
    import random;
    
    GlobalVars.Ch1AudioFiles = (QtWidgets.QFileDialog.getOpenFileNames(ui,'Audio Files', GlobalVars.Ch1DirPath, ''))
    #pdb.set_trace();
    GlobalVars.Ch1AudioFiles=GlobalVars.Ch1AudioFiles[0]    
    
    idx=random.randint(0,int(len(GlobalVars.Ch1AudioFiles)-1))    
    GlobalVars.wf1=wave.open(GlobalVars.Ch1AudioFiles[idx], 'rb')
    GlobalVars.wf1.setpos(GlobalVars.wf1.getnframes()); 

def Ch2SelectAudioFiles():
    import GlobalVars
    import wave;
    import random;
    
    GlobalVars.Ch2AudioFiles = (QtWidgets.QFileDialog.getOpenFileNames(ui,'Audio Files', GlobalVars.Ch2DirPath, ''))
    GlobalVars.Ch2AudioFiles=GlobalVars.Ch2AudioFiles[0]
    idx=random.randint(0,int(len(GlobalVars.Ch2AudioFiles)-1))    
    GlobalVars.wf2=wave.open(GlobalVars.Ch2AudioFiles[idx], 'rb')
    GlobalVars.wf2.setpos(GlobalVars.wf2.getnframes()); 

    

def Ch3SelectAudioFiles():
    import GlobalVars
    import wave;
    import random;    
    
    GlobalVars.Ch3AudioFiles = (QtWidgets.QFileDialog.getOpenFileNames(ui,'Audio Files', GlobalVars.Ch3DirPath, ''))
    GlobalVars.Ch3AudioFiles=GlobalVars.Ch3AudioFiles[0]
    idx=random.randint(0,int(len(GlobalVars.Ch3AudioFiles)-1))    
    GlobalVars.wf3=wave.open(GlobalVars.Ch3AudioFiles[idx], 'rb')
    GlobalVars.wf3.setpos(GlobalVars.wf3.getnframes()); 

    
    
def Ch4SelectAudioFiles():
    import GlobalVars
    import wave;
    import random;    
    GlobalVars.Ch4AudioFiles = (QtWidgets.QFileDialog.getOpenFileNames(ui,'Audio Files', GlobalVars.Ch4DirPath, ''))
    GlobalVars.Ch4AudioFiles=GlobalVars.Ch4AudioFiles[0]
    idx=random.randint(0,int(len(GlobalVars.Ch4AudioFiles)-1))    
    GlobalVars.wf4=wave.open(GlobalVars.Ch4AudioFiles[idx], 'rb')
    GlobalVars.wf4.setpos(GlobalVars.wf4.getnframes()); 

    
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        from numpy import arange, array, zeros
        import GlobalVars;
        import pyaudio
        
        GlobalVars.buffertime=3
        GlobalVars.threshold1=300
        GlobalVars.threshold2=300
        GlobalVars.threshold3=300
        GlobalVars.threshold4=300
        GlobalVars.SampleRate=44100
        GlobalVars.outputsamplerate=44100
        
        GlobalVars.Ch1DirPath=''
        GlobalVars.Ch2DirPath=''
        GlobalVars.Ch3DirPath=''
        GlobalVars.Ch4DirPath=''
        GlobalVars.Ch1AudioFiles=str('')
        GlobalVars.Ch2AudioFiles=str('')
        GlobalVars.Ch3AudioFiles=str('')
        GlobalVars.Ch4AudioFiles=str('')        
        GlobalVars.Ch1fileName=[]
        GlobalVars.Ch2fileName=[]
        GlobalVars.Ch3fileName=[]
        GlobalVars.Ch4fileName=[]        
        GlobalVars.inputdeviceindex=0
        GlobalVars.CHANNELS=4;
        GlobalVars.isRunning=False;
        GlobalVars.Ch1isPlaying=False;
        GlobalVars.Ch2isPlaying=False;
        GlobalVars.Ch3isPlaying=False;
        GlobalVars.Ch4isPlaying=False;
        GlobalVars.Ch1On=False;
        GlobalVars.Ch2On=False;
        GlobalVars.Ch3On=False;
        GlobalVars.Ch4On=False;

        GlobalVars.Pin1=5;
        GlobalVars.Pin2=6
        GlobalVars.Pin3=7
        GlobalVars.Pin4=8        

        self.Ch1checkBox.setEnabled(False);
        self.Ch2checkBox.setEnabled(False);
        self.Ch3checkBox.setEnabled(False);
        self.Ch4checkBox.setEnabled(False);
        
        self.Ch1SaveDirPushButton.setEnabled(False);
        self.Ch2SaveDirPushButton.setEnabled(False);
        self.Ch3SaveDirPushButton.setEnabled(False);
        self.Ch4SaveDirPushButton.setEnabled(False);      
        self.actionLoad_Config.triggered.connect(loadConfig_ButtonPressed);
        self.actionSave_Config.triggered.connect(saveConfig_ButtonPressed);                

        self.RescanInputsPushButton.clicked.connect(RescanInputsButtonPushed)
        self.StopPushButton.clicked.connect(StopPushButton)
        self.StartPushButton.clicked.connect(StartPushButton)
                                               
        self.BufferTimeSpinBox.valueChanged.connect(BufferTimeSpinBoxChanged) 


        self.Ch1SaveDirPushButton.clicked.connect(Ch1SaveDirPushButtonpushButtonClicked)
        self.Ch2SaveDirPushButton.clicked.connect(Ch2SaveDirPushButtonpushButtonClicked)
        self.Ch3SaveDirPushButton.clicked.connect(Ch3SaveDirPushButtonpushButtonClicked)
        self.Ch4SaveDirPushButton.clicked.connect(Ch4SaveDirPushButtonpushButtonClicked)
        self.Ch4SaveDirPushButton.clicked.connect(Ch4SaveDirPushButtonpushButtonClicked)
        
        self.ArduinoSelectioncomboBox.currentIndexChanged.connect(ChangeArduinoCom);
        self.OutputSelectionComboBox.currentIndexChanged.connect(OutputSelectioncomboBoxChanged);
        self.InputSelectioncomboBox.currentIndexChanged.connect(InputSelectioncomboBoxChanged)
        
        self.Box1LevercomboBox.currentIndexChanged.connect(Ch1TriggerChanged);
        self.Box2LevercomboBox.currentIndexChanged.connect(Ch2TriggerChanged);
        self.Box3LevercomboBox.currentIndexChanged.connect(Ch3TriggerChanged);
        self.Box4LevercomboBox.currentIndexChanged.connect(Ch4TriggerChanged);
        
        self.Ch1checkBox.clicked.connect(Ch1OnChanged);
        self.Ch2checkBox.clicked.connect(Ch2OnChanged);
        self.Ch3checkBox.clicked.connect(Ch3OnChanged);
        self.Ch4checkBox.clicked.connect(Ch4OnChanged);
        
        self.ThresholdLineEdit1.textChanged.connect(ThresholdLineEditChanged1);
        self.ThresholdLineEdit2.textChanged.connect(ThresholdLineEditChanged2);
        self.ThresholdLineEdit3.textChanged.connect(ThresholdLineEditChanged3);
        self.ThresholdLineEdit4.textChanged.connect(ThresholdLineEditChanged4);
        self.SampleRatecomboBox.currentIndexChanged.connect(updateSampleRate);
        
        self.OutputSampleRatecomboBox.currentIndexChanged.connect(updateOutputSampleRate);
            

        self.Ch1AudioFileSelectButton.clicked.connect(Ch1SelectAudioFiles);
        self.Ch2AudioFileSelectButton.clicked.connect(Ch2SelectAudioFiles);
        self.Ch3AudioFileSelectButton.clicked.connect(Ch3SelectAudioFiles);
        self.Ch4AudioFileSelectButton.clicked.connect(Ch4SelectAudioFiles);
        #self.HighPassSpinBox.valueChanged.connect(GlobalVars.HighPass=newvalue);

        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    RescanInputsButtonPushed()
    sys.exit(app.exec_())
    #window.show()
    sys.exit(app.exec_())


