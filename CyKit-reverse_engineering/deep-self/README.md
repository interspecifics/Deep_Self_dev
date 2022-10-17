## 1. Servidor OSC para transmitir la lectura de electroencefalograma (EEG) de la diadema EMOTIV

`insight_osc.py`  
  
Este scrpit crea dos servidores OSC para transmitir las señales de lectura de EEG creadas por la diadema EMOTIV Insight. La idea es que se crea 1) un servidor que comunica a un cliente para el monitoreo de la data en tiempo real (que hicimos en TouchDesigner) y 2) un servidor que comunica a un cliente que escribe la lectura línea por línea a un archivo de CSV (este cliente se crea con el script `csv_out.py`).  
Está pensado para ser ejecutado desde linea de comandos y recibe los parámetros:

**--ip** - valor de texto con la ip del cliente 'osc'
**--port** - valor con el puerto del cliente'osc
**--omit** - indica si debe omitir la creación del servidor 'csv' o el servidor 'osc'.

## 2. Cliente OSC para escribir la lectura de EEG en un archivo CSV

`insight_osc.py`  
  
Este script crea un cliente que recibe las señales de lectura de EEG de la diadema y las escribe línea por línea (para minimizar memoria RAM) en un archivo csv. 

Está pensado para ser ejecutado desde linea de comandos y opcionalmente recibe el parámetro **--user** que agrega la cadena de texto especificada al nombre del archivo csv resultante.