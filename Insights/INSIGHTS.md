# CAPSTON ANALISIS E INSIGHTS

## 1. Introducción

### 1.1 Definición del problema
El objetivo inicial de este análisis fue determinar las rutas entre estaciones para que la reposición de las bicis fuera más rápida y efectiva.
Responder a esta pregunta requiere más tiempo del disponible para este proyecto, por lo que hemos dividido esa pregunta en pequeños análisis que ayudarán a, si alguien quiere seguir con esta propuesta, responder a esa gran pregunta. 

1. Identificar los patrones que existen durante un día entero en una estación del bincing.
2. Identificar los patrones que existen en una estación durante un mes cogiendo siempre el mismo día (ex:martes)
3. Extrapolarlo a tres estaciones con alturas diferentes. Una parte alta de Barcelona, otra por la parte del Eixample y otra por la zona costera.

### 1.2 Áreas de Enfoque
El análisis se ha centrado en las siguientes variables clave: station_id, name, lat, lon, altitude, post_code, capacity, last_reported, num_bikes_available, num_docks_available,
 minute, hour, day, month, year.
Como datos externos se han considerado si es fin de semana o no (is_weekend) y si es un día de fiesta o no

### 1.3 Alcance Temporal
El análisis cubre datos recolectados de Marzo de 2023 con una frecuencia por minutos.

### 1.4 Limitaciones
Se ha asumido que las tendencias observadas en los datos estudiados son representativas de los comportamientos futuros.

### 1.5 Exclusiones
Para este análisis no se consideró estaciones sin info


## 2. Metodología

### 2.1 Fuentes de datos
#### 2.1.1 Descripción de las Fuentes de Datos

- **Internas**: Se utilizaron datos del sistema del Bicing de Barcelona.
- **Externas**: También se incluyeron datos de los barrios de Barcelona, calendario de fiestas y de fines de semana. 

#### 2.1.2 Tipos de Datos

- Datos de geolocalización: latitud, logitud, código postal, altura.
- Datos temporales: fecha, año, mes, día, minutos, horas.
- Datos cuantitativos: capacidad de las estaciones, bicis disponibles
- Datos nominales: nombre de las estaciones y su id.

### 2.2 Herramientas y Técnicas
Para llevar a cabo este análisis hemos utilizado el editor Google Colaboratory para programar en Python.
En concreto nos hemos apoyado en estas librerias:
- Pandas 
- Geopandas 
- Numpy
- Os
- Datetime
- Matplotlib lines
- Plotly graph objects
- Matplotlib pyplot
- Seaborn

#### 2.2.1 Técnicas y pasos realizados

Primero, nos hemos preguntábamos cual era la ocupación media de las estaciones. Queríamos comprobar qué era lo normal (a grosso modo) para cada estación, si estar más vacía, más llena o un término medio y si tenía algo que ver con su localización. 
Y también qué capacidad tienen exactamente porque a lo mejor sí que tenía algo que ver también con su localización. 
Para comprobar esto, hemos visualizado en el mapa de Barcelona todas las estaciones.
Para representar su estado usual se ha utilizado un círculo rojo/salmón en el caso de que suelan estar más llenas, 
gris para las medio llenas y azul para las vacías. Ha quedado así: 

![newplot.png](imagenes%2Fnewplot.png)

Podemos comprobar a simple vista que usualmente las estaciones con una mayor altura son las que están más vacías, 
sin embargo, donde suele haber llenas es cerca de la costa, que coincide que tienen una altura menor,
por lo que ambos casos tendrían sentido.


