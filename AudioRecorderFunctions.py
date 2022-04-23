
from PyQt5 import QtGui, QtCore, QtWidgets

import pyaudio 
import wave
from collections import deque
import os
import time
import math
import GlobalVars
import copy
global graph_win
import pyqtgraph as pg
from math import ceil

CHUNK = 8192 #*4

FORMAT = pyaudio.paInt16 #this is the standard wav data format (16bit little endian)s

MAX_DUR=60 #max dur in seconds

def output_callback(in_data, CHUNK, time_info, status):    
    
    import GlobalVars
    from pydub import AudioSegment
    import pdb;
    
    RATE=44100;
    SAMPLES=2;
  
    if (GlobalVars.Ch1On & GlobalVars.Ch1isPlaying):        
        data1 = GlobalVars.wf1.readframes(CHUNK)                
        if (len(data1)<(CHUNK*SAMPLES)):
            data1 = bytearray(CHUNK*SAMPLES);
            GlobalVars.Ch1isPlaying=False
    else:
        data1 = bytearray(CHUNK*SAMPLES);    
    ch1=AudioSegment(data1,sample_width=SAMPLES,frame_rate=RATE,channels=1);

    if (GlobalVars.Ch2On & GlobalVars.Ch2isPlaying):
        data2 = GlobalVars.wf2.readframes(CHUNK)
        if (len(data2)<(CHUNK*SAMPLES)):
            data2 = bytearray(CHUNK*SAMPLES);
            GlobalVars.Ch2isPlaying=False
    else:
        data2 = bytearray(CHUNK*SAMPLES);
    ch2=AudioSegment(data2,sample_width=SAMPLES,frame_rate=RATE,channels=1);        

    if (GlobalVars.Ch3On & GlobalVars.Ch3isPlaying):
        data3 = GlobalVars.wf3.readframes(CHUNK)
        if (len(data3)<(CHUNK*SAMPLES)):
            data3 = bytearray(CHUNK*SAMPLES);
            GlobalVars.Ch3isPlaying=False
    else:
        data3 = bytearray(CHUNK*SAMPLES);
    ch3=AudioSegment(data3,sample_width=SAMPLES,frame_rate=RATE,channels=1);       

    if (GlobalVars.Ch4On & GlobalVars.Ch4isPlaying):
        data4 = GlobalVars.wf4.readframes(CHUNK)
        if (len(data4)<(CHUNK*SAMPLES)):
            data4 = bytearray(CHUNK*SAMPLES);
            GlobalVars.Ch4isPlaying=False
    else:
        data4 = bytearray(CHUNK*SAMPLES);
    ch4=AudioSegment(data4,sample_width=SAMPLES,frame_rate=RATE,channels=1);       

    if (GlobalVars.CHANNELS>0):
        temp=ch1; #data=ch1.raw_data;
    if (GlobalVars.CHANNELS>1):
        temp=AudioSegment.from_mono_audiosegments(ch1,ch2)
      #  data=temp.raw_data;
    if (GlobalVars.CHANNELS>2):
        temp=AudioSegment.from_mono_audiosegments(ch1,ch2,ch3)
     #   data=temp.raw_data;
    if (GlobalVars.CHANNELS>3):
        temp=AudioSegment.from_mono_audiosegments(ch1,ch2,ch3,ch4)
    #    data=temp.raw_data;    
    data=temp.raw_data;
    #pdb.set_trace();
    return (data, pyaudio.paContinue)

def TriggeredRecordAudio(ui):

 import GlobalVars
 import pyfirmata
 import random
 global graph_win1
 global graph_win2
 global graph_win3
 global graph_win4


 from pydub import AudioSegment
 import array
 import pdb
 import audioop


 
 board = pyfirmata.Arduino(GlobalVars.COM_PORT)
 it = pyfirmata.util.Iterator(board)
 it.start()

 RATE = int(ui.SampleRatecomboBox.currentText());# sampling frequency
 MIN_DUR=GlobalVars.buffertime+0.1;#

 SILENCE_LIMIT = GlobalVars.buffertime;
 PREV_AUDIO = GlobalVars.buffertime;

 pya = pyaudio.PyAudio()
 
 CHANNELS=GlobalVars.CHANNELS;
 rel = int(RATE/(CHUNK))
 last_val_high = [0] * CHANNELS
 last_val_low = [0] * CHANNELS
 last_data = [0] * CHANNELS

 #fails here if no board. 
 board.digital[GlobalVars.Pin1].mode = pyfirmata.INPUT
 board.digital[GlobalVars.Pin2].mode = pyfirmata.INPUT
 board.digital[GlobalVars.Pin3].mode = pyfirmata.INPUT
 board.digital[GlobalVars.Pin4].mode = pyfirmata.INPUT 
 
 stream=pya.open(format=FORMAT,input_device_index=GlobalVars.inputdeviceindex,channels=GlobalVars.CHANNELS,rate=RATE,input=True, frames_per_buffer=CHUNK)
 
 streamout=pya.open(format=FORMAT,output_device_index=GlobalVars.outputdeviceindex,channels=GlobalVars.CHANNELS,rate=GlobalVars.outputsamplerate,output=True,frames_per_buffer=CHUNK, stream_callback=output_callback)
 
 ui.ListeningTextBox_1.setText('<span style="color:green">quiet</span>')
 ui.ListeningTextBox_2.setText('<span style="color:green">quiet</span>')
 ui.ListeningTextBox_3.setText('<span style="color:green">quiet</span>')
 ui.ListeningTextBox_4.setText('<span style="color:green">quiet</span>')
 
 audio2send1 = [] 
 audio2send2 = []
 audio2send3 = []
 audio2send4 = []
 
 #GlobalVars.wf1=wave.open('test.wav', 'rb')
# GlobalVars.wf1.setpos(GlobalVars.wf1.getnframes()); # Set to EOF 

 prev_audio1 = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 prev_audio2 = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 prev_audio3 = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 prev_audio4 = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 
 perm_win1 = deque(maxlen=PREV_AUDIO*rel)
 perm_win2 = deque(maxlen=PREV_AUDIO*rel)
 perm_win3 = deque(maxlen=PREV_AUDIO*rel)
 perm_win4 = deque(maxlen=PREV_AUDIO*rel)

 plot_win1 = deque(maxlen=ceil(0.5*rel))
 plot_win2 = deque(maxlen=ceil(0.5*rel))
 plot_win3 = deque(maxlen=ceil(0.5*rel))
 plot_win4 = deque(maxlen=ceil(0.5*rel))
 
 started1 = False
 started2 = False
 started3 = False
 started4 = False

 def updateGraph():
     if (ui.Ch1checkBox.isChecked()):
         ui.GraphWidgetCh1.plot(plotarray1, width=1, clear=True)
     if (ui.Ch2checkBox.isChecked()):            
         ui.GraphWidgetCh2.plot(plotarray2, width=1, clear=True)
     if (ui.Ch3checkBox.isChecked()):
         ui.GraphWidgetCh3.plot(plotarray3, width=1, clear=True)
     if (ui.Ch4checkBox.isChecked()):
         ui.GraphWidgetCh4.plot(plotarray4, width=1, clear=True)
 
 timer = pg.QtCore.QTimer()
 timer.timeout.connect(updateGraph)
 timer.start(500)
 
 HopCounter1=0;
 HopCounter2=0;
 HopCounter3=0;
 HopCounter4=0;
 CurrHour=0;

 streamout.start_stream();
     
 sw1=False; # Switch variables. 
 sw2=False;
 sw3=False;
 sw4=False;
 


 if (GlobalVars.Ch1AudioFiles[0]!=''):
     idx=random.randint(0,int(len(GlobalVars.Ch1AudioFiles)-1))    
     GlobalVars.wf1=wave.open(GlobalVars.Ch1AudioFiles[idx], 'rb')
     GlobalVars.wf1.setpos(GlobalVars.wf1.getnframes());
     
 if (GlobalVars.Ch2AudioFiles[0]!=''):
     idx=random.randint(0,int(len(GlobalVars.Ch2AudioFiles)-1))    
     GlobalVars.wf2=wave.open(GlobalVars.Ch2AudioFiles[idx], 'rb')
     GlobalVars.wf2.setpos(GlobalVars.wf2.getnframes());

 if (GlobalVars.Ch3AudioFiles[0]!=''):
     idx=random.randint(0,int(len(GlobalVars.Ch3AudioFiles)-1))    
     GlobalVars.wf3=wave.open(GlobalVars.Ch3AudioFiles[idx], 'rb')
     GlobalVars.wf3.setpos(GlobalVars.wf3.getnframes());

 if (GlobalVars.Ch4AudioFiles[0]!=''):
     idx=random.randint(0,int(len(GlobalVars.Ch4AudioFiles)-1))    
     GlobalVars.wf4=wave.open(GlobalVars.Ch4AudioFiles[idx], 'rb')
     GlobalVars.wf4.setpos(GlobalVars.wf4.getnframes());
     
 Ch1TrigFileMarker='NoTrig'
 Ch2TrigFileMarker='NoTrig'
 Ch3TrigFileMarker='NoTrig'
 Ch4TrigFileMarker='NoTrig'        

 
 while (GlobalVars.isRunning==1):
     
  QtWidgets.qApp.processEvents()
       
  cur_data = stream.read(CHUNK)
  sound = AudioSegment(cur_data, sample_width=2, channels=CHANNELS, frame_rate=RATE)
  #sound, last_val_low=low_pass_filter_by_chunk(sound, 15000, last_val_low)
  #sound2, last_val_high, last_data=high_pass_filter_by_chunk(sound, int(ui.HighPassspinBox.value()), last_val_high, last_data)
  
  
  channels = sound.split_to_mono();
  #trigchannels = sound.split_to_mono();
  
  alltime=time.localtime();
  OldHour=CurrHour;
  CurrHour=time.localtime().tm_hour;

  if (newHopperEpoch(OldHour,CurrHour)==True): # Turns over at 9am, 1pm, and 5pm, 10 hops per time;
      HopCounter1=0;
      HopCounter2=0;
      HopCounter3=0;
      HopCounter4=0;
      print('Reset '+str(CurrHour))
      ui.Stim1TextBox.setText('<span style="color:green">NoHop</span>')
      ui.Stim2TextBox.setText('<span style="color:green">NoHop</span>')
      ui.Stim3TextBox.setText('<span style="color:green">NoHop</span>')
      ui.Stim4TextBox.setText('<span style="color:green">NoHop</span>')
  
  #soundout = AudioSegment(out_data, sample_width=2, channels=CHANNELS, frame_rate=RATE)
  if (ui.Ch1checkBox.isChecked()):        
      if (HopCounter1 < 20):
                if (GlobalVars.Ch1isPlaying==False):
                        ui.Stim1TextBox.setText('<span style="color:green">NoHop</span>')
                        oldsw1=sw1;
                        sw1 = board.digital[GlobalVars.Pin1].read()                            
                        
                        if (sw1 and (not oldsw1)):  #If not, are we triggering?
                            GlobalVars.wf1.close()                            
                            idx=random.randint(0,int(len(GlobalVars.Ch1AudioFiles)-1))
                            fobject=open(GlobalVars.Ch1DirPath+'/Ch1LogFile.log','a+');                            
                            T=time.localtime()
                            outtime=str("%02d"%T[0])+','+str("%02d"%T[1])+','+str("%02d"%T[2])+','+str("%02d"%T[3])+','+str("%02d"%T[4])+','+str("%02d"%T[5])
                            fobject.write(outtime+',Ch1,'+GlobalVars.Ch1AudioFiles[idx]+'\n');
                            fobject.close();                            
                            GlobalVars.wf1=wave.open(GlobalVars.Ch1AudioFiles[idx], 'rb')
                            GlobalVars.Ch1isPlaying=True;
                            HopCounter1=HopCounter1+1;
                            Ch1TrigFileMarker='Triggered'
                            ui.Stim1TextBox.setText('<span style="color:red">Hopped!</span>')
      else:
            ui.Stim1TextBox.setText('<span style="color:yellow">Hops Maxed</span>')
                      
      ch1=channels[0].raw_data;
    
      perm_win1.append(ch1)
      plot_win1.append(ch1)
      data = b''.join(list(plot_win1))
      plotarray1 = array.array("h",data);
      
      data = b''.join(list(perm_win1))
      currmax=audioop.max(data,2)
      
      if (currmax > GlobalVars.threshold1) and (len(audio2send1)<MAX_DUR*rel):
       if(not started1):
          ui.ListeningTextBox_1.setText('<span style="color:red">singing</span>')
          started1 = True
       audio2send1.append(ch1)
      elif (started1 is True and len(audio2send1)>MIN_DUR*rel):
       print("Ch1 Finished")
      
       filename = save_audio(list(prev_audio1) + audio2send1,GlobalVars.Ch1DirPath,GlobalVars.Ch1fileName+Ch1TrigFileMarker)
       started1 = False      
       prev_audio1 = copy.copy(perm_win1)
       Ch1TrigFileMarker='NoTrig'                   
       ui.ListeningTextBox_1.setText('<span style="color:green">quiet</span>')
       audio2send1=[]
      elif (started1 is True):     
       print('Ch1 too short')
       started1 = False       
       prev_audio1 = copy.copy(perm_win1)
       audio2send1=[]
       Ch1TrigFileMarker='NoTrig'                   
       ui.ListeningTextBox_1.setText('<span style="color:green">quiet</span>')
      else:  
       prev_audio1.append(ch1)

       
       
  if (ui.Ch2checkBox.isChecked()):

      if (HopCounter2 < 20):
                if (GlobalVars.Ch2isPlaying==False):
                        ui.Stim2TextBox.setText('<span style="color:green">NoHop</span>')
                        oldsw2=sw2;
                        sw2 = board.digital[GlobalVars.Pin2].read()                                                
                        if (sw2 and (not oldsw2)): #s & oldsw==False): #If not, are we triggering?
                            GlobalVars.wf2.close()                           
                            idx=random.randint(0,int(len(GlobalVars.Ch2AudioFiles)-1))
                            fobject=open(GlobalVars.Ch2DirPath+'/Ch2LogFile.log','a+');                            
                            T=time.localtime()
                            outtime=str("%02d"%T[0])+','+str("%02d"%T[1])+','+str("%02d"%T[2])+','+str("%02d"%T[3])+','+str("%02d"%T[4])+','+str("%02d"%T[5])
                            fobject.write(outtime+',Ch2,'+GlobalVars.Ch2AudioFiles[idx]+'\n');
                            fobject.close();
                            Ch2TrigFileMarker='Triggered'                            
                            GlobalVars.wf2=wave.open(GlobalVars.Ch2AudioFiles[idx], 'rb')
                            GlobalVars.Ch2isPlaying=True;
                            HopCounter2=HopCounter2+1;
                            ui.Stim2TextBox.setText('<span style="color:red">Hopped!</span>')
      else:
            ui.Stim2TextBox.setText('<span style="color:yellow">Hops Maxed</span>')              

      ch2=channels[1].raw_data;    
      plot_win2.append(ch2)
      data = b''.join(list(plot_win2))
      plotarray2 = array.array("h",data);  
      
      data = b''.join(list(perm_win2))
      currmax=audioop.max(data,2)      
     
      if (currmax >  GlobalVars.threshold2) and (len(audio2send2)<MAX_DUR*rel):          
       if(not started2):
          ui.ListeningTextBox_2.setText('<span style="color:red">singing</span>')
          started2 = True
       audio2send2.append(ch2)
      elif (started2 is True and len(audio2send2)>MIN_DUR*rel):
       print("Ch2 Finished")
       filename = save_audio(list(prev_audio2) + audio2send2,GlobalVars.Ch2DirPath,GlobalVars.Ch2fileName+Ch2TrigFileMarker)
       started2 = False       
       prev_audio2 = copy.copy(perm_win2)
       ui.ListeningTextBox_2.setText('<span style="color:green">quiet</span>')
       audio2send2=[]
       Ch2TrigFileMarker='NoTrig'            
      elif (started2 is True):
       ui.ListeningTextBox_2.setText('Ch2 too short')
       started2 = False    
       prev_audio2 = copy.copy(perm_win2)
       audio2send2=[]
       Ch2TrigFileMarker='NoTrig'            
       ui.ListeningTextBox_2.setText('<span style="color:green">quiet</span>')
      else:
       prev_audio2.append(ch2)
    
  if (ui.Ch3checkBox.isChecked()):
      if (HopCounter3 < 20):
                if (GlobalVars.Ch3isPlaying==False):
                        ui.Stim3TextBox.setText('<span style="color:green">NoHop</span>')
                        oldsw3=sw3;
                        sw3 = board.digital[GlobalVars.Pin3].read()                        
                                           
                        if (sw3 and (not oldsw3)): #s & oldsw==False): #If not, are we triggering?
                            GlobalVars.wf3.close()
                            #GlobalVars.wf1=wave.open('test.wav', 'rb')
                            idx=random.randint(0,int(len(GlobalVars.Ch3AudioFiles)-1))
                            fobject=open(GlobalVars.Ch3DirPath+'/Ch3LogFile.log','a+');                            
                            T=time.localtime()
                            outtime=str("%02d"%T[0])+','+str("%02d"%T[1])+','+str("%02d"%T[2])+','+str("%02d"%T[3])+','+str("%02d"%T[4])+','+str("%02d"%T[5])
                            fobject.write(outtime+',Ch3,'+GlobalVars.Ch3AudioFiles[idx]+'\n');
                            fobject.close();
                            Ch3TrigFileMarker='Triggered'                                                        
                            GlobalVars.wf3=wave.open(GlobalVars.Ch3AudioFiles[idx], 'rb')
                            GlobalVars.Ch3isPlaying=True;
                            HopCounter3=HopCounter3+1;
                            
                            ui.Stim3TextBox.setText('<span style="color:red">Hopped!</span>')
      else:
            ui.Stim3TextBox.setText('<span style="color:yellow">Hops Maxed</span>')              

      ch3=channels[2].raw_data;      
      plot_win3.append(ch3)       
      perm_win3.append(ch3)
      data = b''.join(list(plot_win3))
      plotarray3 = array.array("h",data);                
      currmax=audioop.max(data,2)
      
      data = b''.join(list(perm_win3))
      currmax=audioop.max(data,2)

      
      if (currmax > GlobalVars.threshold3) and (len(audio2send3)<MAX_DUR*rel):  
       if(not started3):
          ui.ListeningTextBox_3.setText('<span style="color:red">singing</span>')
          started3 = True
       audio2send3.append(ch3)
      elif (started3 is True and len(audio2send3)>MIN_DUR*rel):
       print("Ch3 Finished")
       filename = save_audio(list(prev_audio3) + audio2send3,GlobalVars.Ch3DirPath,GlobalVars.Ch3fileName+Ch3TrigFileMarker)
       started3 = False
       slid_win3 = deque(maxlen=SILENCE_LIMIT * rel)
       prev_audio13= copy.copy(perm_win3)
       ui.ListeningTextBox_3.setText('<span style="color:green">quiet</span>')
       audio2send3=[]
       Ch3TrigFileMarker='NoTrig'            
      elif (started3 is True):
       ui.ListeningTextBox_3.setText('Ch3 too short')
       started3 = False
       slid_win3 = deque(maxlen=SILENCE_LIMIT * rel)
       prev_audio3 = copy.copy(perm_win3)
       audio2send3=[]
       Ch3TrigFileMarker='NoTrig'            
       ui.ListeningTextBox_3.setText('<span style="color:green">quiet</span>')
      else:
       prev_audio3.append(ch3)

  if (ui.Ch4checkBox.isChecked()):
      if (HopCounter4 < 20):
                if (GlobalVars.Ch4isPlaying==False):
                        ui.Stim4TextBox.setText('<span style="color:green">NoHop</span>')
                        oldsw4=sw4;
                        sw4 = board.digital[GlobalVars.Pin4].read()

                        if (sw4 and (not oldsw4)): #s & oldsw==False): #If not, are we triggering?
                            GlobalVars.wf4.close()
                            #GlobalVars.wf1=wave.open('test.wav', 'rb')
                            idx=random.randint(0,int(len(GlobalVars.Ch4AudioFiles)-1))
                            fobject=open(GlobalVars.Ch4DirPath+'/Ch4LogFile.log','a+');                            
                            T=time.localtime()
                            outtime=str("%02d"%T[0])+','+str("%02d"%T[1])+','+str("%02d"%T[2])+','+str("%02d"%T[3])+','+str("%02d"%T[4])+','+str("%02d"%T[5])
                            fobject.write(outtime+',Ch4,'+GlobalVars.Ch4AudioFiles[idx]+'\n');
                            fobject.close();                    
                            #GlobalVars.Ch4DirPath
                            GlobalVars.wf4=wave.open(GlobalVars.Ch4AudioFiles[idx], 'rb')
                            Ch4TrigFileMarker='Triggered'                                                                                    
                            GlobalVars.Ch4isPlaying=True;
                            HopCounter4=HopCounter1+1;
                            ui.Stim4TextBox.setText('<span style="color:red">Hopped!</span>')
      else:
            ui.Stim1TextBox.setText('<span style="color:yellow">Hops Maxed</span>')
            
      ch4=channels[3].raw_data;
      perm_win4.append(ch4)
      plot_win4.append(ch4)       
      data = b''.join(list(plot_win4))
      plotarray4 = array.array("h",data);          
      data = b''.join(list(perm_win4))
      currmax=audioop.max(data,2)
      
      if (currmax > GlobalVars.threshold4) and (len(audio2send4)<MAX_DUR*rel):     
       if(not started4):
          ui.ListeningTextBox_4.setText('<span style="color:red">singing</span>')
          started4 = True
       audio2send4.append(ch4)
      elif (started4 is True and len(audio2send4)>MIN_DUR*rel):
       print("Ch4 Finished")
       filename = save_audio(list(prev_audio4) + audio2send4,GlobalVars.Ch4DirPath,GlobalVars.Ch4fileName+Ch4TrigFileMarker)
       Ch4TrigFileMarker='NoTrig'                                                                                           
       started4 = False       
       prev_audio4 = copy.copy(perm_win1)
       ui.ListeningTextBox_4.setText('<span style="color:green">quiet</span>')
       audio2send4=[]
      elif (started4 is True):
       ui.ListeningTextBox_4.setText('Ch4 too short')
       started4 = False
       Ch4TrigFileMarker='NoTrig'            
       prev_audio4 = copy.copy(perm_win4)
       audio2send4=[]
       ui.ListeningTextBox_4.setText('<span style="color:green">quiet</span>')
      else:
       prev_audio4.append(ch4)
          
 print("done recording")
 stream.close()
 streamout.close();
 board.exit();
 pya.terminate()

def save_audio(data,rootdir,filename):
 import GlobalVars
 import pdb
 import os
 """ Saves mic data to  WAV file. Returns filename of saved
 file """

 # writes data to WAV file

 T=time.localtime()
 RATE=int(GlobalVars.SampleRate);
 
 outtime=str("%02d"%T[0])+str("%02d"%T[1])+str("%02d"%T[2])+str("%02d"%T[3])+str("%02d"%T[4])+str("%02d"%T[5])
 DatePath='/'+str("%02d"%T[0])+'_'+str("%02d"%T[1])+'_'+str("%02d"%T[2])+'/'
 filename = rootdir+DatePath+filename+'_'+outtime

 
 
 if not os.path.exists(os.path.dirname(rootdir+DatePath)):
    try:
        os.makedirs(os.path.dirname(rootdir+DatePath))
    except:
        print('File error- bad directory?')

 
 data = b''.join(data)
        
 wf = wave.open(filename + '.wav', 'wb')
 wf.setnchannels(1);
 wf.setsampwidth(2)
 wf.setframerate(RATE) 
 wf.writeframes(data)
 wf.close()
 return filename + '.wav'
 

##
##if(__name__ == '__main__'):
## audio_int()
## record_song()

def newHopperEpoch(OldHour,CurrHour):
        
      newEpoch=False;
      if ((OldHour==8) & (CurrHour==9)):
              newEpoch=True;
      if ((OldHour==12) & (CurrHour==13)):
              newEpoch=True;
      if ((OldHour==17) & (CurrHour==18)):
              newEpoch=True;

      return newEpoch;
