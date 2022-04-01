
global isRunning
global numdevices
global devicenumber
global inputdeviceindex
global CHANNELS

global Ch1DirPath
global Ch2DirPath
global Ch3DirPath
global Ch4DirPath
global Ch1fileName
global Ch2fileName
global Ch3fileName
global Ch4fileName

global threshold1
global threshold2
global threshold3
global threshold4

global Ch1On
global Ch2On
global Ch3On
global Ch4On

global Ch1isPlaying
global Ch2isPlaying
global Ch3isPlaying
global Ch4isPlaying

global Ch1audioDirPath
global Ch2audioDirPath
global Ch3audioDirPath
global Ch4audioDirPath

global Ch1AudioFiles
global Ch2AudioFiles
global Ch3AudioFiles
global Ch4AudioFiles

global outputsamplerate
#global outputrateindex
global outputdeviceindex
global AudioDeviceName;
global OutputAudioDeviceName

global wf1
global wf2
global wf3
global wf4

global Pin1
global Pin2
global Pin3
global Pin4

global inputSampleRateIDX
global outputSampleIDX

global COM_PORT


def loadConfig(loadfilename,ui):
    from configparser import SafeConfigParser
    import os
    import GlobalVars
    import serial
    from numpy import arange,array
    import pdb;

    parser = SafeConfigParser()
    loadfilename=loadfilename.replace('/','\\')

    if not parser.read(str(loadfilename)): #.replace('/','\\')):
        raise(IOError, 'cannot load')
    
    GlobalVars.buffertime=int(parser.get('main','GlobalVars.buffertime'))
    
        
    GlobalVars.Ch1DirPath=(parser.get('main','GlobalVars.Ch1DirPath'))
    GlobalVars.Ch2DirPath=(parser.get('main','GlobalVars.Ch2DirPath'))
    GlobalVars.Ch3DirPath=(parser.get('main','GlobalVars.Ch3DirPath'))
    GlobalVars.Ch4DirPath=(parser.get('main','GlobalVars.Ch4DirPath'))
    
    GlobalVars.Ch1fileName=(parser.get('main','GlobalVars.Ch1fileName'))
    GlobalVars.Ch2fileName=(parser.get('main','GlobalVars.Ch2fileName'))
    GlobalVars.Ch3fileName=(parser.get('main','GlobalVars.Ch3fileName'))
    GlobalVars.Ch4fileName=(parser.get('main','GlobalVars.Ch4fileName'))
    
    GlobalVars.threshold1=float(parser.get('main','GlobalVars.threshold1'))
    GlobalVars.threshold2=float(parser.get('main','GlobalVars.threshold2'))
    GlobalVars.threshold3=float(parser.get('main','GlobalVars.threshold3'))
    GlobalVars.threshold4=float(parser.get('main','GlobalVars.threshold4'))
    GlobalVars.SampleRate=int(parser.get('main','GlobalVars.SampleRate'))
    GlobalVars.Ch1AudioFiles=(parser.get('main','GlobalVars.Ch1AudioFiles'))
    GlobalVars.Ch2AudioFiles=(parser.get('main','GlobalVars.Ch2AudioFiles'))
    GlobalVars.Ch3AudioFiles=(parser.get('main','GlobalVars.Ch3AudioFiles'))
    GlobalVars.Ch4AudioFiles=(parser.get('main','GlobalVars.Ch4AudioFiles'))

    GlobalVars.AudioDeviceName=str(parser.get('main','GlobalVars.AudioDeviceName'))
    GlobalVars.OutputAudioDeviceName=str(parser.get('main','GlobalVars.OutputAudioDeviceName'))
    
    GlobalVars.AudioDeviceName=GlobalVars.AudioDeviceName.replace('"','');
    GlobalVars.OutputAudioDeviceName=GlobalVars.OutputAudioDeviceName.replace('"','');
    
    
    GlobalVars.Ch1AudioFiles=GlobalVars.Ch1AudioFiles.split(',');
    GlobalVars.Ch2AudioFiles=GlobalVars.Ch2AudioFiles.split(',');
    GlobalVars.Ch3AudioFiles=GlobalVars.Ch3AudioFiles.split(',');
    GlobalVars.Ch4AudioFiles=GlobalVars.Ch4AudioFiles.split(',');
    
    
    
    GlobalVars.inputdeviceindex=int(parser.get('main','GlobalVars.inputdeviceindex'))
    GlobalVars.outputdeviceindex=int(parser.get('main','GlobalVars.outputdeviceindex'))
    GlobalVars.outputsamplerate=int(parser.get('main','GlobalVars.outputsamplerate'))       

    GlobalVars.Pin1=int(parser.get('main','GlobalVars.Pin1'))
    GlobalVars.Pin2=int(parser.get('main','GlobalVars.Pin2'))
    GlobalVars.Pin3=int(parser.get('main','GlobalVars.Pin3'))
    GlobalVars.Pin4=int(parser.get('main','GlobalVars.Pin4'))
    
    ui.InputSelectioncomboBox.setCurrentText(GlobalVars.AudioDeviceName)
    ui.OutputSelectionComboBox.setCurrentText(GlobalVars.OutputAudioDeviceName)

    ui.Ch1FileNameLabel.setText(GlobalVars.Ch1fileName)
    ui.Ch1FileDirectoryLabel.setText(GlobalVars.Ch1DirPath);        

    ui.Ch2FileNameLabel.setText(GlobalVars.Ch2fileName)
    ui.Ch2FileDirectoryLabel.setText(GlobalVars.Ch2DirPath);        

    ui.Ch3FileNameLabel.setText(GlobalVars.Ch3fileName)
    ui.Ch3FileDirectoryLabel.setText(GlobalVars.Ch3DirPath);        
    ui.Ch4FileNameLabel.setText(GlobalVars.Ch4fileName)
    ui.Ch4FileDirectoryLabel.setText(GlobalVars.Ch4DirPath);
    ui.BufferTimeSpinBox.setValue(GlobalVars.buffertime)
    
    ui.ThresholdLineEdit1.setText(str(GlobalVars.threshold1))
    ui.ThresholdLineEdit2.setText(str(GlobalVars.threshold2))
    ui.ThresholdLineEdit3.setText(str(GlobalVars.threshold3))
    ui.ThresholdLineEdit4.setText(str(GlobalVars.threshold4))


    ui.OutputSampleRatecomboBox.setCurrentText(str(GlobalVars.outputsamplerate))
    ui.SampleRatecomboBox.setCurrentText(str(GlobalVars.SampleRate))        
    
    
    
    ui.Box1LevercomboBox.setCurrentIndex(GlobalVars.Pin1-2)
    ui.Box2LevercomboBox.setCurrentIndex(GlobalVars.Pin2-2)
    ui.Box3LevercomboBox.setCurrentIndex(GlobalVars.Pin3-2)
    ui.Box4LevercomboBox.setCurrentIndex(GlobalVars.Pin4-2)
    
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
        if (GlobalVars.Ch1fileName!=''):
            ui.Ch1checkBox.setEnabled(True);

    if (GlobalVars.CHANNELS >1):
        ui.Ch2SaveDirPushButton.setEnabled(True);
        if (GlobalVars.Ch2fileName!=''):
            ui.Ch2checkBox.setEnabled(True);
    if (GlobalVars.CHANNELS >2):
        ui.Ch3SaveDirPushButton.setEnabled(True);
        if (GlobalVars.Ch3fileName!=''):
            ui.Ch3checkBox.setEnabled(True);
            
    if (GlobalVars.CHANNELS >3):
        ui.Ch4SaveDirPushButton.setEnabled(True);
        if (GlobalVars.Ch4fileName!=''):
            ui.Ch4checkBox.setEnabled(True);         
   # pdb.set_trace();

def saveConfig(savefilename):
    from configparser import SafeConfigParser
    import os
    import GlobalVars
    from numpy import array
    import pdb
    


   
    SaveFile= open((savefilename),'w')
    
    parser = SafeConfigParser()
    
    parser.add_section('main')
    
    parser.set('main','GlobalVars.buffertime',str(GlobalVars.buffertime))
    
    parser.set('main','GlobalVars.Ch1DirPath',str(GlobalVars.Ch1DirPath))
    parser.set('main','GlobalVars.Ch2DirPath',str(GlobalVars.Ch2DirPath))
    parser.set('main','GlobalVars.Ch3DirPath',str(GlobalVars.Ch3DirPath))
    parser.set('main','GlobalVars.Ch4DirPath',str(GlobalVars.Ch4DirPath))

    parser.set('main','GlobalVars.Ch1fileName',str(GlobalVars.Ch1fileName))
    parser.set('main','GlobalVars.Ch2fileName',str(GlobalVars.Ch2fileName))
    parser.set('main','GlobalVars.Ch3fileName',str(GlobalVars.Ch3fileName))
    parser.set('main','GlobalVars.Ch4fileName',str(GlobalVars.Ch4fileName))
    
    parser.set('main','GlobalVars.threshold1',str(GlobalVars.threshold1))
    parser.set('main','GlobalVars.threshold2',str(GlobalVars.threshold2))
    parser.set('main','GlobalVars.threshold3',str(GlobalVars.threshold3))
    parser.set('main','GlobalVars.threshold4',str(GlobalVars.threshold4))
    
    parser.set('main','GlobalVars.SampleRate',str(GlobalVars.SampleRate))    
    str1 = ','.join(GlobalVars.Ch1AudioFiles)
    parser.set('main','GlobalVars.Ch1AudioFiles',str(str1))
    str1 = ','.join(GlobalVars.Ch2AudioFiles)
    parser.set('main','GlobalVars.Ch2AudioFiles',str(str1))
    str1 = ','.join(GlobalVars.Ch3AudioFiles)
    parser.set('main','GlobalVars.Ch3AudioFiles',str(str1))
    str1 = ','.join(GlobalVars.Ch4AudioFiles)
    parser.set('main','GlobalVars.Ch4AudioFiles',str(str1))   


    parser.set('main','GlobalVars.inputdeviceindex',str(GlobalVars.inputdeviceindex))
    parser.set('main','GlobalVars.outputdeviceindex',str(GlobalVars.outputdeviceindex))    

    parser.set('main','GlobalVars.AudioDeviceName',str('"'+GlobalVars.AudioDeviceName+'"'))
    parser.set('main','GlobalVars.OutputAudioDeviceName',str('"'+GlobalVars.OutputAudioDeviceName+'"'))

    
    parser.set('main','GlobalVars.outputsamplerate',str(GlobalVars.outputsamplerate))

    parser.set('main','GlobalVars.Pin1',str(GlobalVars.Pin1))
    parser.set('main','GlobalVars.Pin2',str(GlobalVars.Pin2))
    parser.set('main','GlobalVars.Pin3',str(GlobalVars.Pin3))
    parser.set('main','GlobalVars.Pin4',str(GlobalVars.Pin4))        
         

    
    parser.write(SaveFile)    
    SaveFile.close()
