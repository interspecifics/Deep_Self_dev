clear;

path = '/home/fred/Desktop/EEG2Emotions/archivos/';
files = {'EEG_2022-04-11_150103'}
% files = {'EEG_2022-04-11_150103' 'alf5m_EEG_2022-04-11_122813' 'EEG_2022-04-11_150155' 'alfEEG_2022-04-11_120136' 'EEG_2022-04-11_114703' 'EEG_2022-04-11_170212' 'alf_EEG_2022-04-11_120250' 'EEG_2022-04-11_115012' 'EEG_2022-04-11_170235' 'alf_audio_EEG_2022-04-20_155442' 'EEG_2022-04-11_115104' 'EEG_2022-04-12_121634' 'amigo_emotiv_EEG_2022-05-04_183959' 'EEG_2022-04-11_144642' 'EEG_2022-04-12_121731' 'emme_audio_EEG_2022-04-28_145148' 'EEG_2022-04-11_144734' 'EEG_2022-04-12_122008' 'feli_audio_EEG_2022-04-28_174706' 'EEG_2022-04-11_144807' 'EEG_2022-04-12_122322' 'les_audio_EEG_2022-04-20_153820' 'EEG_2022-04-11_144831' 'EEG_2022-04-12_123107' 'quetzalli_EEG_2022-04-30_134611' 'EEG_2022-04-11_145126' 'EEG_2022-04-12_145307' 'visitaLUIS_EEG_2022-05-12_155743' 'EEG_2022-04-11_145221' 'EEG_2022-04-12_145341' 'visita_nom_metzli_EEG_2022-05-12_150718' 'EEG_2022-04-11_145722' 'EEG_2022-04-12_145430' 'visitanta_1_EEG_2022-05-04_125549' 'EEG_2022-04-11_150016' 'EEG_2022-04-28_191254'}
for filenum = 1:length(files) 
    file = string(files{filenum}) 
    importData16;
    eegCAR = applyCAR(eeg);
    calcValAroDom;
end 