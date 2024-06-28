## CAPSTON ANALISIS E INSIGHTS

# 1. Introducción

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


# 2. Metodología

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

Primero nos hemos preguntado qué capacidad tienen exactamente las estaciones. Y si siguen una norma concreta dependiendo de su localización. Para comprobar esto, hemos 
visualizado el mapa de Barcelona, por barrios, de todas las estaciones
y las capacidades de cada una.

Los datos los hemos tenido que complimentar y preprocesar antes, porque había variables que no venían en el DataFrame, como los barrios, y eran muy importantes para la visualización. Además, 
utilizamos la columna "last_reported" para extraer el minuto, la hora, el día, el mes, y el año que le correspondía a cada entrada. El día exacto de la semana y del año para también lo hemos extraido porque necesitábamos ver si era un día de fiesta, entre semana o fin de semana. 



Con esto hemos visto que XXXXXXXXXX




