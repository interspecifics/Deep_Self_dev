[`deep_self_feature_ext.ipynb`](https://github.com/interspecifics/Deep_Self_dev/blob/main/notebooks/deep_self_feature_ext.ipynb) **-** Esta notebook está dedicada a la construcción de variables a partir de la data de EEG. Toma un archivo 'csv' con la lectura de EEG de un experimento y le agrega columnas con las variables correspondientes a:  
1. componentes independientes [ICA](https://en.wikipedia.org/wiki/Independent_component_analysis) de la lectura de los 5 electrodos
2. bandas de frecuencia (sobre la componente $IC_1$):  $\delta, \theta, \alpha, \beta_l, \beta_h, \gamma$
3. estadísticos de las bandas de frecuencia: media y varianza móvil 
4. clustering (con k-means) de los momentos en el tiempo (donde $k$ maximiza el silouhette score)

[`reporte_EEG_data.ipynb`](https://github.com/interspecifics/Deep_Self_dev/blob/main/notebooks/reporte_EEG_data.ipynb) **-** Este notebook genera reportes (en pdf) con visualizaciones de la data de EEG y del proceso de EEG2EMOTIONS para un conjunto de archivos. Cada reporte coniene tres páginas con:  
1. metadata de la lectura: ID, fecha, duración en segundos
2. visualizaciones: data raw de los electrodos (RAW_EEG), componentes independientes (ICA), bandas de frecuencia ($\delta, \theta, \alpha, \beta_l, \beta_h, \gamma$), cluster de cada entrada en la lectura.
3. visualización de la 'constelación afectiva' cálculada a partir del la data generada por el proceso de `EEG2EMOTIONS`. Una 'constelación afectiva' es un grafo —en el cubo de las tres dimensiones para los valores de valence, arousal y dominance— en donde los *vertices* son los centroides de cada emoción capturada por el proceso de `EEG2EMOTIONS` y el grosor de las *aristas* representa la proporción de saltos entre dos estados emocionales a lo largo del tiempo. 