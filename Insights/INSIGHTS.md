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
El análisis cubre datos recolectados de Enero, Febrero y Marzo de 2023 con una frecuencia por minutos.

### 1.4 Limitaciones
Se ha asumido que las tendencias observadas en los datos estudiados son representativas de los comportamientos futuros.

### 1.5 Exclusiones
Al extraer la información y empezar a analizarla, nos dimos cuenta de que las estaciones [ 48, 188, 429, 487, 520] no tenían información de ningún tipo. 
Para nuestro estudio no eran relevantes, por lo que decimos excluirlas del análisis. 

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

##### Análisis de la ocupación usual de las estaciones y su comportamiento

Primero, nos hemos preguntado cuál era la ocupación media de las estaciones. Queríamos comprobar qué era lo normal (a grosso modo) para cada estación, si estar más vacía, más llena o un término medio y si tenía algo que ver con su localización. 
Y también qué capacidad tienen exactamente porque a lo mejor sí que tenía algo que ver también con su localización. 
Para comprobar esto, hemos visualizado en el mapa de Barcelona todas las estaciones.
Para representar su estado usual se ha utilizado un círculo rojo/salmón en el caso de que suelan estar más llenas, 
gris para las medio llenas y azul para las vacías. Ha quedado así: 

![newplot.png](imagenes%2Fnewplot.png)

Podemos comprobar a simple vista que usualmente las estaciones con una mayor altura son las que están más vacías, 
sin embargo, donde suele haber llenas es cerca de la costa, que coincide que tienen una altura menor,
por lo que ambos casos tendrían sentido.

Otro aspecto interesante que hemos detectado es que la capacidad de las estaciones no parece tener ninguna relación con 
la localización de esta. En un primer momento, creímos que esto podría tener relación debido a que las más cercanas al 
mar siempre suelen estar más llenas y, por lo tanto, si tuvieran más capacidad podrían acoger más bicis y el usuario no 
tendría que dar muchas vueltas buscando donde aparcarla.

##### Análisis de los patrones durante un día de una sola estación

Segundo, ayudándonos con el mapa, escogimos una estación, la número 371, para empezar a ver los patrones que sigue durante el día.
Escogimos esta porque está en medio de la ciudad y sospechábamos que veríamos mucho movimiento o al menos varios picos interesantes. Además, es una de las que, con el
análisis anterior, su estado usual era other.

Para conseguir visualizar el patrón, hemos creado una clase "Visualization" para agrupar todos los tipos de visualizaciones que 
que hemos hecho. Hay variables que son comunes y se registran dentro del _self._ Estas son la fecha, las estaciones, los 
barrios, y los tres estados de las estaciones, llena (full_stations), vacías (empty_stations) y el resto (other_stations).

Para este caso en concreto hemos hecho una función llamada _def plot_occupancy_stats(self, station_ids, occu_type, n_week_of_year, day_of_week, n_month_of_year)_ para visualizar cómo varía la
ocupación durante el período que se le indique. Como se ve en la definición de la función se le pueden pasar las siguientes 
variables:
- self: las variables propias de la clase
- station_ids: los identificadores de cada estación que se quiere evaluar
- occu_type: tipo de estación según su ocupación
- n_week_of_year: número de la semana según el año
- day_of_week: número del día según la semana
- n_month_of_year: número del mes según el año

La frecuencia temporal es por minutos.

En el caso de la estación número 371, en el Carrer dels Enamorats, que tiene como ocupación usual "other" y el día 09-03-2023, visualizamos el siguiente gráfico:

**XXXXXXX -VISUALIZACIÓN DE UN DÍA DE ESTACION 371- XXXXXXXX**

analisis

##### Análisis de los patrones durante un mes de una sola estación

Detectar los patrones durante un día aislado no es suficiente para detectar patrones reales de una estación. Como primer
enfoque para empezar a detectar factores está muy bien, pero nosotros queríamos ir más allá. 
¿Pasaría lo mismo el mismo día durante todo el mes?

Para analizarlo, escogimos los miércoles del mes de Marzo de la misma estación, la 371.  

![img.png](imagenes/img_273.png)

Es superinteresante observar varias tendencias:

- **Madrugada (00:00 - 06:00):** Generalmente, la capacidad es baja durante las primeras horas de la madrugada, con un pequeño incremento justo antes del amanecer en algunos días.
- **Mañana (06:00 - 12:00):** Hay un aumento significativo en la ocupación durante las primeras horas de la mañana, alcanzando un pico entre las 08:00 y 09:00, lo cual es típico del inicio de la jornada laboral.
- **Tarde (12:00 - 18:00):** La ocupación disminuye gradualmente después del pico matutino y muestra fluctuaciones, posiblemente debido a la hora del almuerzo y la variabilidad en las rutinas de las personas.
- **Noche (18:00 - 24:00):** Se observa otro aumento en la ocupación durante la tarde y la noche, alcanzando otro pico significativo alrededor de las 18:00-20:00 horas, seguido de una disminución hacia el final del día.

En conclusión, parece que si se cumplen los mismos patrones, por lo que quizá nos pueda ayudar a determinar las horas clave 
para hacer reposición de bicis y si se comparara con las estaciones de alrededor, quizá hasta de donde sería más óptimo
cogerlas. (pregunta original)

##### Análisis de los patrones durante tres meses de una sola estación





##### Análisis extrapolado a 3 estaciones de sus patrones durante un día





##### Análisis extrapolado a 3 estaciones de sus patrones durante un mes





##### Análisis extrapolado a 3 estaciones de sus patrones durante tres meses