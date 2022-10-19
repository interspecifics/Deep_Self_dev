# Deep_Self_Dev _ Transient Hypofrontality toolkit 

Deep Self_Dev es un toolkit desarrollado para el proyecto Trasient Hypofrontality apoyado por el Sistema Nacional de Creadores de Arte del FONCA. 

En este repositorio se alojan los desarrollos software / hardware utilizados para extraer señales biometricas EEG, anlizar las señales por medio de un algortimo 
de detección de emociones. 

Estos datos son despues transmitidos por un servidor que tiene la capacidad de sencuenciar set de datos pregrabados en un formato para creación audivisual estandar Open Sound Control. 

## 1. Extracción de datos EEG
Para la tarea de extracción estamos utilizando un versión modificada del CyKit-reverse_engineering dentro de esta carpeta se encuentra una carpeta deep self. Para utilizar el sistema es necesario seguir los siguientes pasos. 

###### a. Servidor OSC para transmitir la lectura de electroencefalograma (EEG) de la diadema EMOTIV

insight_osc.py

Este scrpit crea dos servidores OSC para transmitir las señales de lectura de EEG creadas por la diadema EMOTIV Insight. La idea es que se crea 1) un servidor que comunica a un cliente para el monitoreo de la data en tiempo real (que hicimos en TouchDesigner) y 2) un servidor que comunica a un cliente que escribe la lectura línea por línea a un archivo de CSV (este cliente se crea con el script csv_out.py).
Está pensado para ser ejecutado desde linea de comandos y recibe los parámetros:

--ip - valor de texto con la ip del cliente 'osc' --port - valor con el puerto del cliente'osc --omit - indica si debe omitir la creación del servidor 'csv' o el servidor 'osc'.

###### b. Cliente OSC para escribir la lectura de EEG en un archivo CSV

insight_osc.py

Este script crea un cliente que recibe las señales de lectura de EEG de la diadema y las escribe línea por línea (para minimizar memoria RAM) en un archivo csv.

Está pensado para ser ejecutado desde linea de comandos y opcionalmente recibe el parámetro --user que agrega la cadena de texto especificada al nombre del archivo csv resultante.

___________________________________________

## 2. Analisis de EEG a Emociones

Para poder diferenciar entre estados de ánimo durante las sesión de 10 minutos se caracterizaron las emociones.
Para ello procesamos las señales para obtener nivel de energía en las bandas alpha y beta.
Con ello obtener valores de "valence", "arousal", "dominance" de acuerdo a lo que la literatura sugiere.
Con esos 3 valores normalizados pasarlos a un clasificador de reglas difuso.
Los resultados son el nivel de activación de las emociones en el tiempo.

![This is an image](https://github.com/interspecifics/Deep_Self_dev/blob/main/EEG2Emotions/resultados/graficas/alf_audio_EEG_2022-04-20_155442.PNG?raw=true)

## 3. Servidor de EEG a OSC

## 4. Visualizaciones

## 5. Patches de composición 
