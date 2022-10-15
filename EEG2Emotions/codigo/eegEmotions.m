clear;

path = 'C:\Users\eobey\Desktop\EEG2Emotions\EEG-procesadas\';
file = 'alf_audio_EEG_2022-04-20_155442';
importData16;
eegCAR = applyCAR(eeg);
calcValAroDom;