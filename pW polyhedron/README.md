
# pulseWidth polyhedron
Esta carpeta contiene código utilizado para modelar el mapeo de señal de EEG a modulación de pulso sobre un polihedro de n caras. 

![image](https://github.com/interspecifics/Deep_Self_dev/assets/12953522/13f77d7f-6ac6-44ff-a878-eac70984df04)

## Instalación
\```bash
pip install -r requirements.txt
\```

## Uso
Para correr la simulación ejecuta el script `goldberg_perlin.py`

### goldberg.py

Este script genera un poliedro de Goldberg, que es una forma geométrica construida subdividiendo las caras de un icosaedro regular. El script ofrece la opción de personalizar el número de subdivisiones para crear formas más complejas.

### goldberg_perlin.py

Este script combina el poliedro de Goldberg con el ruido de Perlin para crear un paisaje animado y en evolución. Las caras del poliedro cambian de color según un mapa de ruido de Perlin, que también se visualiza como una "manta de Perlin".

## Características

- Generar poliedro de Goldberg con subdivisiones personalizables.
- Crear un paisaje dinámico usando ruido de Perlin.
- Visualización 3D de ambos, el poliedro y el mapa de ruido de Perlin.
