# Deep Self _Dev @ Transient Hypofrontality toolkit 

INDICE:

1. [Extracción de datos](https://github.com/interspecifics/Deep_Self_dev#1-extracción-de-datos-eeg)
2. [Procesamiento de datos](https://github.com/interspecifics/Deep_Self_dev#1-extracción-de-datos-eeg)
3. [EEG a Emociones](https://github.com/interspecifics/Deep_Self_dev#1-extracción-de-datos-eeg)
4. [Data Server](https://github.com/interspecifics/Deep_Self_dev#1-extracción-de-datos-eeg)
5. [Visualizaciones](https://github.com/interspecifics/Deep_Self_dev#1-extracción-de-datos-eeg)
6. [Patches de composición](https://github.com/interspecifics/Deep_Self_dev#1-extracción-de-datos-eeg)


Deep Self_Dev es un toolkit desarrollado para el proyecto Trasient Hypofrontality apoyado por el Sistema Nacional de Creadores de Arte del FONCA. 

En este repositorio se alojan los desarrollos software / hardware utilizados para: extraer señales biometricas EEG, anlizar las señales por medio de un algortimo de detección de emociones. 

![This is an image](https://github.com/interspecifics/Deep_Self_dev/blob/main/sistema.png?raw=true)

Estos datos son despues transmitidos por un servidor que tiene la capacidad de sencuenciar set de datos pregrabados en un formato para creación audivisual estandar Open Sound Control. 

## 1. Extracción de datos EEG
Para el levantamieno de datos EEG decidimos trabajar con la diadema EMOTIV Insight con capacidad de 5 electrodos. 

![This is an image](https://www.mindtecstore.com/media/image/product/2163/md/emotiv-insight-5-kanal-eeg-headset~4.jpg)

Para la tarea de extracción estamos utilizando un versión modificada del CyKit-reverse_engineering 
Para utilizar el sistema es necesario seguir los siguientes pasos. 

###### a. Servidor OSC para transmitir la lectura de electroencefalograma (EEG) raw de la diadema EMOTIV

insight_osc.py

Este scrpit crea dos servidores OSC para transmitir las señales de lectura de EEG creadas por la diadema EMOTIV Insight. La idea es que se crea 1) un servidor que comunica a un cliente para el monitoreo de la data en tiempo real (que hicimos en TouchDesigner) y 2) un servidor que comunica a un cliente que escribe la lectura línea por línea a un archivo de CSV (este cliente se crea con el script csv_out.py).
Está pensado para ser ejecutado desde linea de comandos y recibe los parámetros:

--ip - valor de texto con la ip del cliente 'osc' --port - valor con el puerto del cliente'osc --omit - indica si debe omitir la creación del servidor 'csv' o el servidor 'osc'.

###### b. Cliente OSC para escribir la lectura de EEG en un archivo CSV

insight_osc.py

Este script crea un cliente que recibe las señales de lectura de EEG de la diadema y las escribe línea por línea (para minimizar memoria RAM) en un archivo csv.

Está pensado para ser ejecutado desde linea de comandos y opcionalmente recibe el parámetro --user que agrega la cadena de texto especificada al nombre del archivo csv resultante.

![This is an image](https://github.com/interspecifics/Deep_Self_dev/blob/main/CyKit-reverse_engineering/deep-self/eegcapture.jpg?raw=true)

## 2. Procesamientos de datos


![This is an image](https://github.com/interspecifics/Deep_Self_dev/blob/main/raw_icad.png?raw=true)

![This is an image](https://github.com/interspecifics/Deep_Self_dev/blob/main/frec_clusters.png?raw=true)



___________________________________________

## 3. EEG a Emociones

Para poder diferenciar entre estados de ánimo durante las sesión de 10 minutos se caracterizaron las emociones.
Para ello procesamos las señales para obtener nivel de energía en las bandas alpha y beta.
Con ello obtener valores de "valence", "arousal", "dominance" de acuerdo a lo que la literatura sugiere.
Con esos 3 valores normalizados pasarlos a un clasificador de reglas difuso.
Los resultados son el nivel de activación de las emociones en el tiempo.

![This is an image](https://github.com/interspecifics/Deep_Self_dev/blob/main/EEG2Emotions/resultados/graficas/alf_audio_EEG_2022-04-20_155442.PNG?raw=true)

## 4. Data Server

Proporciona un flujo de datos sin procesar y transformados, y permite reproducir los datos en segmentos de 128 muestras (2 segundos) que se pueden organizar de forma personalizada en secuencias y bucles. Hay tres tipos de datos en la secuencia:

###### - Raw Data: 

• EEG-Electrodos de actividad bioelectrica [5 canales]: Medición de la actividad electroencefalográfica para cada una de las 5 posiciones del auricular Muse: AF3, T7 Pz, T8, AF4. La frecuencia de muestreo es de 64 muestras/s, las unidades son microvoltios.

###### - Transformed data:

• Componentes Independientes [4 canales]: Representaciones paralelas de la actividad cerebral. Cada canal corresponde a un tipo de comportamiento periódico como eventos incidentales, frecuentes, únicos, etc. La frecuencia de muestreo es de 64 muestras/seg.

• Bandas de frecuencia: representación de datos de EEG como componentes espectrales para bandas de EEG comunes: alfa (a, 8-12 Hz), beta_low (bl, 13-21 Hz), beta_high (bh, 21-30 Hz), delta (d, 1) -3 Hz), gamma (g, 30-100 Hz), theta (th, 4-7 Hz). La frecuencia de muestreo es de 64 muestras/seg.

###### - Metadata 

• Índices del modelo de valencia/excitación/dominancia: la valencia es el nivel de felicidad, varía de positivo a negativo y expresa el sentimiento agradable o desagradable acerca de algo. La excitación es el nivel de activación afectiva, que va desde el sueño hasta la excitación. La dominancia refleja el nivel de control del estado emocional, de sumiso a dominante.

• Predicción del Estado de Emoción sobre Ventanas de Tiempo: La emoción predicha por los índices del modelo VAD, requiere las muestras en un periodo de 2 segundos, por lo que genera una muestra cada vez que se completa un segmento. Las emociones reconocibles son: Aburrido, Soñoliento, Desprecio, Tristeza, Alegría, RelajaciónNeutral, Amor, Ira, Tensión, Estrés, Miedo, Sorpresa.
Confianza de predicción: Cuanta confianza hay en las predicciones.

![This is an image](https://github.com/interspecifics/Deep_Self_dev/blob/main/deepself_server_v1.0/Selection_078.jpg?raw=true)



## 5. Visualizaciones

## 6. Patches de composición 
