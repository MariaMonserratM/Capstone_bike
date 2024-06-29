# 🚲 CAPSTONE PROJECT: DOCK AVAILABILITY PREDICTION

## 1. Introducción
Bicing es el servicio público de alquiler de bicis de la ciudad de Barcelona. Cuenta a día de hoy con más de 500 estaciones repartidas por toda la ciudad. El sistema cuenta con una aplicación donde explorar en tiempo real la disponibilidad de bicis y de espacios para dejar la bici en las diferentes estaciones. Sin embargo, no cuenta con un predictor que determine el porcentaje de bicis o sitios probables que habrá en un determinado momento del tiempo para una estación determinada.

### 1.1 Objetivo y evaluación
El presente proyecto tiene como objetivo la generación de un modelo de predicción del porcentaje de sitios libres (docks) en una estación de Bicing determinada y en un momento determinado del tiempo.
La valoración de la exactitud del modelo se ha medido mediante RMSE (Root Mean Squared Error) que cuantifica la diferencia entre los valores predichos y los valores reales, indicando el nivel de dispersión de los datos.
El envío del resultado del modelo y la evaluación se ha realizado a través de una competición con otros equipos en la plataforma Kaggle: https://www.kaggle.com/competitions/2024-online-bike-availability-prediction


## 2. Metodología y resultados
### Primera parte: dataset y modelo simple de regresión lineal
#### Orígen de los datos
El Ayuntamiento de Barcelona, a través de su portal de datos abiertos, opendata-ajuntament.barcelona.cat, pone a disposición de la ciudadanía datos sobre el estado de las estaciones de Bicing. En concreto, los datos sobre la disponibilidad de bicis y de huecos libres se puede descargar para los diferentes meses del año en la siguiente página: https://opendata-ajuntament.barcelona.cat/data/ca/dataset/estat-estacions-bicing.

Para este proyecto se han usado como datos de entrenamiento los comprendidos entre los años 2020 y 2023, y como datos de test los comprendidos entre enero y abril de 2024.

Solo se han usado las estaciones que se encuentran en el dataset de test (399 estaciones diferentes) que se puede bajar del propio kaggle (documento: _metadata_sample_submission_2024_)

#### Primer dataset
El Ayuntamiento de Barcelona recoge el estado de las diferentes estaciones cada 5 minutos aproximadamente. Para disminuir la complejidad de los datos y del modelo, se ha calculado la media de la disponibilidad de huecos por hora para cada estación, y se ha construido un dataset inicial con los datos de la estación, el año, el mes, el día, la hora, y la disponibilidad de huecos en las 4 horas anteriores a la hora diana. A estas últimas variables las hemos denominado _variables contexto_.

El código para la generación del dataset inicial con todos los datos para los años 2020 a 2023 se puede explorar en el archivo _Load_concatenate_data_code.py_ del directorio _Dataset_.
El código para la generación del dataset de entrenamiento inicial anteriormente descrito se puede explorar en el archivo _Bike_preprocesed_code.py_ del directorio _Dataset_.

#### Primer modelo simple
Para realizar la primera submisión al Kaggle, se ha hecho un split temporal del dataset de entrenamiento, de manera que se ha usado el 80% de los datos como entrenamiento y el 20% como datos de validación. A continaución se ha entrenado un modelo de regresión lineal obteniéndose un RMSE de XXXXX y un R2 de XXXX.
Para hacer la predicción con los datos de test, se ha entrenado el modelo de nuevo con el dataset completo de training.

### Segunda parte: Enriquecimiento del dataset y resultado de otros modelos
#### Variables extras añadidas al dataset
Para enriquecer el dataset con variables que pudieran tener un valor predictor nos hemos centrado en características geográficas de la estacion y en caracterísicas temporales.

El listado y la localización de elementos de interés de la ciudad como museos, cines, teatros, bares, etc. han sido obtenido del portal de datos abiertos del Ayuntamiento de Barcelona anteriormente citado.

La localización de las diferentes facultades de las universidades de la ciudad y La correspondencia entre los códigos postales y los barrios mayoritarios a los que pertenecen se han obtenido con la ayuda de ChatGPT basada en la arquitectura GPT-4 de OpenAI.

Como características de la estación que pudieran tener un valor predictivo se han añadido las siguientes variables:
* **Capacidad de la estación**: el tamaño total de la estación puede influir en el porcentaje de disponibilidad.
* **Altitud**: el uso de la bici probablemente tenga una direccionalidad de zonas altas hacia zonas bajas. Estaciones que se encuentran en zonas más altas tendran más disponibilidad de huuecos que zonas las que se encuentran en zonas bajas.
* **Latitud y Longitud**: la localización exacta de la estación podría estar relacionada con los patrones de uso. Necesitamos esta localización para calcular distancias a otros elementos de interés.
* **Código postal y barrio**: la zona en la que se localiza una estación puede marcar el patrón de uso de la misma.
* **Número de otras estaciones de bicing cercanas**: la cercanía de otras estaciones puede generar también patrones de uso en una estación.
* **Cercanía a estaciones de transporte público**: el uso complementario de la bici y el transporte público puede determinar patrones de uso.
* **Cercanía a alguna facultad**: las estaciones cercanas a las facultades se suelen llenar por la mañana y vaciar por la tarde
* **Número de facultades cercanas**: cuanto más grande es el campus, más gente puede podría hacer uso del bicing para llegar a la universidad o para volver a casa.
* **Cercanía a bibliotecas**: elementos de interés
* **Cercanía a museos**: elementos de interés con posible relación con días de fiesta o fin de semana
* **Cercanía a cines y teatros**: elementos de interés con posible relación con días de fiesta o fin de semana
* **Cercanía a bares y clubes**: elementos de interés con posible relación con días de fiesta o fin de semana
* **Número de bares cercanos**: una zona con gran cantidad de bares o clubes puede ser una zona de salir con mayor probabilidad de generar un patrón de uso en las estaciones adyacentes

Como características relacionadas con la temporalidad se han añadido las siguientes variables:
* **Momento del día**: los patrones de uso podrían cambiar entre la noche, las primeras horas de la mañana, las primeras horas de la tarde, etc.
* **Estación**: los patrones de uso podrían variar según sea invierno, primavera, verano u otoño.
* **Si es fin de semana o fiesta**: los patrones de uso podrían variar dependiendo de si es un día de trabajo o no.

Por último, al hacer el análisis de predictores en los diferentes modelos, se ha visto que la variable que mejor predice el target es la disponibilidad de huecos en la hora anterior (ctx-1), así que se ha añadido la **media de la disponibilidad de huevos en las estaciones adyacentes en la hora anterior** para explorar también su capacidad predictiva.

Se ha valorado la inclusión de otras variables que finalmente no han sido incluídas en el dataset para su testeado:
Climatología: se desechó la idea de incluir variables relativas a la climatología por dos razones, 1) los datos abiertos de la AEMET solo proporcionan datos medios diarios y no por hora. Asignar el dato medio del día a todas las horas, podría penalizar el poder predictivo del modelo; y b) la ciudad de Barcelona se caracteriza por tener un clima no muy extremo durante todo el año y las precipitaciones son excasas, lo que una hipotética variable precipitación si/no, sería demasiado desbalanceada y no beneficiaría al modelo.
Distancia a la playa y a la montaña: como estas características están muy correlacionadas con la altitud, se decidió no inclirlas para su testeado.


#### Entrenamiento de diferentes modelos

#### Selección de variables y modelo final

EXPLICAR CORRELACIONES, VARIABLES PREDICTIVAS PRINCIPALES, RAZONES POR LAS QUE EL MODELO NO LAS USA....

#### Limitaciones del modelo y mejoras
Como se ha demostrado, las variables adicionales añadidas al dataset no tienen un peso relativo muy alto comparadas con la variable predictiva principal que es la ctx-1.

El momento del día, si es un día de trabajo o no, y la altitud son otras de las variables que usa el modelo, aunque tengan un peso menor.

Para mejorar el valor predictivo de las variables relacionadas con los elementos de interés de la ciudad podríamos reducir el número de elementos y dejár únicamente los más importantes. También podríamos variar la distancia. Es posible que las distancias elegidas (entre 200-300 según el elemento) sea demasiado grande para generar diferencias entre estaciones.
Creemos que la media de la disponibilidad de estaciones adyacentes en la hora anterior puede tener un valor predictivo mayor si se usaran todas las estaciones del servicio, y no únicamente las 399 que hay en el dataset de test. Además, esta medida es poco representativa, ya que por la naturaleza del dataset, cuyo target es únicamente 1 de cada 5 horas, hace complicado encontrar el dato para las estaciones adyacentes para la hora exacta de la estación sobre la que estamos haciendo el cálculo.

