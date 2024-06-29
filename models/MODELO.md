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

Como características de la estación que pudieran tener un valor predictivo se han añadido las siguientes variables:
* Capacidad de la estación
* Altitud:
* Latitud y Longitud
* Código postal y barrio
* Número de otras estaciones de bicing cercanas
* Cercanía a estaciones de transporte público
* Cercanía a alguna facultad
* Número de facultades cercanas
* Cercanía a bibliotecas
* Cercanía a museos
* Cercanía a cines y teatros
* Cercanía a bares y clubes
* Número de bares cercanos

Como características relacionadas con la temporalidad se han añadido las siguientes variables:
* Momento del día
* Estación
* Si es fin de semana o fiesta

El hacer en análisis de predictores en los diferentes modelos, se ha visto que la variable que mejor predice el target es la disponibilidad de huecos en la hora anterior (ctx-1), así que se ha añadido la media de la disponibilidad de huevos en las estaciones adyacentes en la hora anterior para explorar también su capacidad predictiva.

#### Entrenamiento de diferentes modelos

#### Selección de variables y modelofinal