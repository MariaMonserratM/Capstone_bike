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

El código para la generación del dataset inicial con todos los datos para los años 2020 a 2023 se puede explorar en el archivo _Load_concatenate_data_code.py_ del directorio _datasets and models_.
El código para la generación del dataset de entrenamiento inicial anteriormente descrito se puede explorar en el archivo _Bike_preprocesed_code.py_ del directorio _datasets and models_.

#### Primer modelo simple
Para realizar la primera submisión al Kaggle, se ha hecho un split temporal del dataset de entrenamiento, de manera que se ha usado el 80% de los datos como entrenamiento y el 20% como datos de validación. A continaución se ha entrenado un modelo de regresión lineal obteniéndose un RMSE de 0.110990656 y un R2 de 0.820732338.
Para hacer la predicción con los datos de test, se ha entrenado el modelo de nuevo con el dataset completo de training.

### Segunda parte: Enriquecimiento del dataset y resultado de otros modelos
#### Variables extras añadidas al dataset
El código con las funciones y la extracción de la última versión del dataset de training y test se puede explorar en el documento _Extra_variables_dataset.py_ del directorio _datasets and models_

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

Por último, al hacer el análisis de predictores en los diferentes modelos, se ha visto que la variable que mejor predice el target es la disponibilidad de huecos en la hora anterior (ctx-1), así que se ha añadido la **media de la disponibilidad de huecos en las estaciones adyacentes en la hora anterior** para explorar también su capacidad predictiva.

Se ha valorado la inclusión de otras variables que finalmente no han sido incluídas en el dataset para su testeado:
Climatología: se desechó la idea de incluir variables relativas a la climatología por dos razones, 1) los datos abiertos de la AEMET solo proporcionan datos medios diarios y no por hora. Asignar el dato medio del día a todas las horas, podría penalizar el poder predictivo del modelo; y b) la ciudad de Barcelona se caracteriza por tener un clima no muy extremo durante todo el año y las precipitaciones son excasas, lo que una hipotética variable precipitación si/no, sería demasiado desbalanceada y no beneficiaría al modelo.
Distancia a la playa y a la montaña: como estas características están muy correlacionadas con la altitud, se decidió no inclirlas para su testeado.


## 3. Exploración de los Datos, Selección de Variables y Modelización

### Exploración de los datos

#### Año 2020 y COVID-19
El año 2020 se caracterizó por ser muy atípico debido a la pandemia mundial de COVID-19 que alteró drásticamente los patrones habituales de actividad humana, incluyendo el uso del transporte. Incorporar datos de este año en nuestros modelos de aprendizaje automático podría conducir a interpretaciones inexactas y a la identificación de patrones que no reflejan las condiciones normales.

* **Comportamiento No Representativo de los Usuarios**: Confinamientos y Restricciones.

* **Patrones de Datos Anómalos**: Eventos específicos relacionados con la pandemia, como fases de reapertura o nuevos confinamientos, crearon cambios bruscos y no recurrentes en los patrones de uso.

* **Impacto en la Precisión del Modelo**: Incluir datos de 2020 podría introducir anomalías y ruido, llevando al modelo a aprender patrones que no se generalizan bien a otros años.

![covid](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/52b8c6ec-e1d2-4b8a-8bc5-9b57459f4b63)

En 2020, observamos una clara diferencia en el porcentaje de disponibilidad de docks en comparación con los años 2021, 2022 y 2023, que muestran patrones similares entre ellos. El porcentaje promedio de docks disponibles por mes es relativamente constante a lo largo de estos años, excepto en 2020 (especialmente en marzo, abril, mayo y junio).

Hemos decidido excluir 2020, nos aseguramos de que los datos de entrenamiento reflejen patrones regulares y predecibles de uso de bicicletas, lo que mejora la robustez y la fiabilidad de nuestras predicciones. Los modelos entrenados con datos de años más representativos (por ejemplo, 2021, 2022, 2023) tienen más probabilidades de generalizarse bien a las condiciones futuras, proporcionando insights más precisos y útiles. Por estas razones, hemos decidido excluir los datos de 2020 en nuestros modelos predictivos.

#### Estaciones del año

Durante el invierno y la primavera, el porcentaje medio de docks disponibles por hora es menor que en verano y otoño. Esto se puede explicar por el hecho de que durante los meses más cálidos, la gente tiende a usar más el Bicing y por eso se puede encontrar un mayor porcentaje de docks disponibles.

![season](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/d3f46d8d-e737-499a-9565-73636a466de8)

#### Días de la semana

Hay una diferencia entre el porcentaje medio de docks disponibles según si es día laborable o fin de semana.

![day_of_week](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/730e878b-066c-4cd5-b47e-9a278e051e8d)

#### Momento del día

Observamos cómo durante la mañana y la tarde es cuando generalmente hay menos docks disponibles. Y durante la noche y la madrugada es cuando hay más docks disponibles. Tiene sentido porque durante la noche menos personas usan las bicicletas y, por lo tanto, las estaciones están más llenas.

![time_of_day](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/9e63057c-2c81-4ca7-b9b5-0d14cc9503bb)

#### Altitud

La disponibilidad de docks en las diferentes estaciones de Barcelona está significativamente influenciada por la altitud en la que se encuentran.

* **Preferencia por las pendientes**: Las estaciones situadas a mayor altitud generalmente tienen más docks disponibles. Esto se debe a que los usuarios prefieren montar en bicicleta cuesta abajo, lo que requiere menos esfuerzo físico. En consecuencia, las bicicletas se coger con frecuencia de estaciones en altitudes más altas y se conducen a áreas de menor altitud.

* **Acumulación en altitudes bajas**: La tendencia de ir cuesta abajo provoca una acumulación de bicicletas en las estaciones de menor altitud, donde los usuarios terminan sus viajes. Como resultado, estas estaciones a menudo tienen menos docks disponibles.

Para abordar estos desequilibrios, los operadores del Bicing a menudo necesitan realizar tareas de reequilibrio, donde las bicicletas se transportan de estaciones de menor a mayor altitud. Sin embargo, estas tareas solo pueden mitigar parcialmente los patrones de flujo natural dictados por la altitud.

![altitude](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/7d49174b-0068-4c45-af1a-f33c80b61f54)

#### Nearby Stations y Nearby Colleges ( y otras variables "near")

Algunas variables muestran diferencias aparentemente significativas cuando hacemos boxplots, como son la variable nearby_stations y nearby_colleges. Sin embargo, será tras la evaluación de los modelos y la importancia de sus características finales que se decidirá qué variables añadir al modelo predictivo.

<img width="580" alt="nearby_stations" src="https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/07874c6e-01fd-457e-ae27-d14116d2908a">

<img width="578" alt="nearby_colleges" src="https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/f7ff2615-37cf-4316-bdee-e12deeb2d401">

#### Fin de semana y festivos

Hemos decidido unir en una sola variable las variables is_weekend y is_holiday. Al final, solo nos interesa saber si estamos tratando con días de tipología festivo (fines de semana y días festivos adicionales) ya que el comportamiento es muy similar. Así que hemos creado la variable is_not_workday para reflejarlo.

<img width="592" alt="is_not_workday" src="https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/68ebf6e1-3bc3-42d6-a5a9-ea624bfc4a73">

#### Barrio y postcode

Si estás familiarizado con Barcelona, puedes ver claramente cómo la altitud de cada barrio afecta la disponibilidad de docks. Por lo tanto, la variable de altitud está, en cierta medida, implícita en la variable de barrio. Sin embargo, otras características del barrio también pueden ser importantes para la disponibilidad de docks, lo que indica que esta variable puede añadir información adicional a nuestro conjunto de datos.

![neighborhood](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/29306882-f466-43fb-909d-20ffea1bcb11)


El código postal y el barrio están altamente correlacionados. Sin embargo, algunos códigos postales pueden pertenecer a más de un barrio. Al final, solo utilizaremos una de estas dos variables en nuestro modelo, si es el caso.

![post_code](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/e190a10b-9475-45da-9717-87dba2290267)

#### Correlaciones entre variables numéricas

![heat_map](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/4313158f-3081-41da-986c-ff2340b5e3e5)

Las variables numéricas más correlacionadas con la variable target son: ctx-1, ctx-2, ctx-3, ctx-4, altitude y nearby_stations. Además, las variables contexto están correlacionadas entre ellas, lo cual tiene sentido. Variables como la hora y el mes, si las analizamos como variables numéricas no parecen tener correlación. Sin embargo, si tratamos la variable hora como categórica (o usamos la variable hour_info) si que posiblemente pueda aportar un valor añadido a nuestros modelos.

### Entrenamiento y evaluación de los modelos predictivos

Para dividir nuestro dataframe (df) en conjuntos de datos de entrenamiento y validación debemos tener en cuenta que estamos manejando datos temporales, por lo que durante el proceso de división, debemos respetar el orden temporal. Por ejemplo, no podemos tener datos de diciembre de 2023 en nuestro conjunto de datos de entrenamiento y datos de 2021 en nuestro conjunto de datos de validación. Además, es importante tener en cuenta la variable station_id durante este paso.

Se han explorado distintos tipos de modelos predictivos, empezando por el más simple:

#### Linear Regression

Para escoger las variables que queremos usar en nuestro modelo de regresion lineal nos hemos basado en el estudio previo de correlación de variables con nuestra variable target y también en las limitaciones y ventajas que presenta un modelo como este.

Las variables escogidas han sido: ['ctx-1', 'ctx-2', 'ctx-3', 'ctx-4', 'hour', 'altitude', 'is_weekend']

Por un lado, hemos escogido las variables que más correlación lineal tienen con la variable target así como aquellas, aunque sean categoricas (binarias) pueden ser facilmente interpretables por un modelo simple de regresion lineal. No hemos querido añadir variables categoricas con un gran número de opciones dentro de ellas ya que este tipo de modelos no son los más adecuados para tratar con variables de esas caracteristicas ni tampoco hemos querido añadir muchísimas variables ya que para ello disponemos de modelos más potentes y complejos capaces de encontrar relaciones no lineales entre variables.

Los resultados han sido:
* **Root Mean Squared Error**: 0.10308152279128933
* **Validation R^2 Score**: 0.8484644676948296

La variable que más peso tiene en el modelo es ctx-1, seguida de la ctx-2. La variable altitude está en quinta posición de importancia y is_weekend la última.

**Regresión Lineal**:
* Simplicidad: Fácil de implementar e interpretar. Sirve como un buen modelo de referencia.
* Relaciones Lineales: Asume una relación lineal entre las características y la variable objetivo, lo cual puede no captar las complejidades en los datos.
* Independencia de Características: Asume la independencia de las características, lo cual puede no ser cierto en escenarios del mundo real.
* Manejo Limitado de Variables Categóricas: Requiere un procesamiento extensivo de variables categóricas. También puede manejar características binarias, pero las trata de manera lineal, lo cual puede no capturar todas las complejidades.

#### XGBoost

XGBoost generalmente tiene una mayor capacidad para manejar datos categóricos codificados (onehot encoder) y características binarias debido a su habilidad para capturar relaciones no lineales, manejar eficientemente datos dispersos y modelar automáticamente interacciones entre características. Mientras que la regresión lineal puede trabajar con estos tipos de datos, frecuentemente no logra capturar las complejidades y las interacciones que XGBoost puede modelar de manera efectiva, lo que puede llevar a un mejor rendimiento predictivo potencialmente con XGBoost.

Aprovechando los benficios de un modelo como XGBoost, en este caso hemos decidido añadir más variables a nuestro modelo, para probar si éstas realmente aportan algún beneficio a la predicción.

Las variables escogidas han sido:
['ctx-1', 'ctx-2', 'ctx-3', 'ctx-4', 'hour', 'altitude', 'is_weekend', 'hour_info', 'season_info', 'post_code', 'nearby_stations', 'near_transport', 'near_college', 'nearby_colleges', 'near_museum']

Los resultados de la predicción:
* **Root Mean Squared Error**: 0.09632863965409555
* **Validation R^2 Score**: 0.8676683638545032

Vemos que el resultado ha mejorado respecto al modelo anterior. Sin embargo, también hemos añadido complejidad al modelo con la suma de nuevas variables.

**Feature Importance**:

En este caso volvemos a observar como las variables más importances son ctx-1 (con mucha diferencia), ctx-2, hour_info_early_morning, post_code_8002, ...otras variables que nacen de post_code..., altitude (en 10a posición de importancia), etc.
Vemos como la variable altitud pierde peso en nuestor modelo: probablemente se deba a que hemos añadido la variable post_code que de alguna manera tiene implícita también la altitud.

#### Neural Networks

A continuación hemos querido probar un modelo de red neuronal para ver si aporta alguna mejora dadas sus características:

* **Relaciones no lineales**: Las redes neuronales pueden capturar relaciones complejas y no lineales entre las características y la variable objetivo. Variables que parecen menos importantes en modelos lineales o basados en árboles (como XGBoost) pueden contribuir de manera más significativa en las redes neuronales si influyen en el resultado a través de interacciones no lineales.

* **Feature Engineering**: Las redes neuronales aprenden automáticamente las interacciones y representaciones de las características a partir de los datos, mientras que en XGBoost y Regresión Lineal, el proceso de feature engineering (crear nuevas características o transformaciones) puede ser más crítica.

Hemos utilizado las mismas variables que en el modelo anterior (XGBoost) y hemos codificado las variables categóricas usando OneHotEncoder y hemos escalado los datos numéricos usando MinMaxScaler [0, 1], tal y como hemos hecho también con XGBoost.

Evaluación del modelo:
* **Mean Squared Error**: 0.009247507075219633
* **Root Mean Squared Error**: 0.09616395933622758
* **Validation R^2 Score**: 0.8681204368450266

Ha mejorado el modelo respecto el XGBoost anterior, sin embargo también ha aumentado la complejidad del modelo y el tiempo de computación.

Feature Importance:

![feature_imp_nn](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/3f1260d3-4cae-45ef-bbfd-3471f83dfa32)

Resulta curioso observar como variables que en los otros modelos no aparecían como impportances, en este modelo de NN sí que aparecen: nearby_stations es un ejemplo, esto puede deberse a que las redes neuronales pueden captar relaciones más sutiles que otros modelos (relaciones no lineales en contextos distintos).

#### Light GBM

Hemos decidido probar este tipo de modelo, similar al XGBoost pero con algunas peculiaridades:

* **Soporte para Características Categóricas**: LightGBM cuenta con soporte incorporado para características categóricas, las cuales pueden ser utilizadas sin necesidad de hacer OneHotEncoder. Esto puede ahorrar tiempo de preprocesamiento y memoria, especialmente al tratar con conjuntos de datos que contienen variables categóricas con alta cardinalidad, como es el caso de post_code.
* **Ajuste de Parámetros**: LightGBM ofrece parámetros adicionales para ajustar finamente el rendimiento del modelo, como manejar el sobreajuste mediante regularización y controlar el crecimiento del árbol con parámetros como num_leaves y min_data_in_leaf. Esta flexibilidad nos permite optimizar el rendimiento del modelo de manera más efectiva.

Las variables que hemos seleccionado para probar este modelo han sido:
['ctx-1', 'ctx-2', 'post_code', 'hour', 'altitude', 'is_not_workday']

En este caso, vamos a tratar la variable "hour" y "post_code" como categóricas.

<img width="336" alt="vairables_lgbm" src="https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/ac9ab516-5fa8-4038-845e-e3f9b2410aa4">

Resultado del modelo:

* **Mean Squared Error**: 0.009171869657551976

* **R^2 Score**: 0.8691991091314109

Observamos como el modelo vuelve a mejorar respecto al anterior, aunque ligeramente. Este modelo es más sencillo a nivel de selección de variables y con un coste computacional inferior.

**Feature Importance**

<img width="282" alt="feature_imp_values_lgbm" src="https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/f698a473-eeb6-4bb1-9885-1186d106461c">

![feature_imp_lgbm](https://github.com/MariaMonserratM/Capstone_bike/assets/66376420/f412fbc8-cd48-47e6-b9aa-f7b279bc59e6)

De nuevo, la variable más importante para la predicción es ctx-1. En este caso, la tercera variable más importante es post_code.

#### Conclusiones y selección de modelo final

Todos los modelos destacan ctx-1 y ctx-2 como variables cruciales, lo cual es lógico dado su relevancia contextual. Otras variables añadidas a nuestro modelo proporcionan mejoras modestas en el rendimiento. Su importancia no es tan alta como en ctx-1, pero ayudan a explicar las predicciones en casos específicos: donde la altitud es relevante, también el código postal, etc.

A lo largo de este proyecto, otras variables evaluadas no beneficiaron sustancialmente nuestro modelo. Por lo tanto, optamos por la simplicidad al incluir solo las variables más relevantes para la predicción, como lo hicimos con el modelo Light GBM.

Es destacable que la variable nearby_stations muestra una importancia significativa en el modelo de Neural Network, lo cual no se observa en los otros modelos.

Además, destacar que la influencia de la altitud se ve mitigada en cierta medida por los esfuerzos de los operadores de las estaciones de Bicing para reequilibrar las bicicletas. Aunque nuestros datos capturan este efecto, su impacto es menos pronunciado.

Las variables bajo consideración podrían ser mejoradas potencialmente recalculando las distancias de manera diferente (nearby_stations, nearby_colleges, etc.). Además, la creación de una nueva variable que indicase el tipo de estación basada en la ubicación, altitud, código postal, etc., y clusterizar las estaciones según sus patrones de uso (por ejemplo, estaciones con frecuentes excesos o déficits de bicicletas) podría mejorar aún más el rendimiento de nuestro modelo.

En conclusión, hemos optado por el modelo Light GBM con un conjunto mínimo de características para predecir el porcentaje de docks disponibles. Si bien el modelo de Red Neuronal muestra un rendimiento comparable, introduce complejidad adicional. Es importante señalar que, a pesar de su rendimiento ligeramente inferior, la simplicidad del modelo de regresión lineal ofrece un buen resultado.

#### Limitaciones del modelo y mejoras
Como se ha demostrado, las variables adicionales añadidas al dataset no tienen un peso relativo muy alto comparadas con la variable predictiva principal que es la ctx-1.

El momento del día, si es un día de trabajo o no, y la altitud son otras de las variables que usa el modelo, aunque tengan un peso menor.

Para mejorar el valor predictivo de las variables relacionadas con los elementos de interés de la ciudad podríamos reducir el número de elementos y dejár únicamente los más importantes. También podríamos variar la distancia. Es posible que las distancias elegidas (entre 200-300 según el elemento) sea demasiado grande para generar diferencias entre estaciones.
Creemos que la media de la disponibilidad de estaciones adyacentes en la hora anterior puede tener un valor predictivo mayor si se usaran todas las estaciones del servicio, y no únicamente las 399 que hay en el dataset de test. Además, esta medida es poco representativa, ya que por la naturaleza del dataset, cuyo target es únicamente 1 de cada 5 horas, hace complicado encontrar el dato para las estaciones adyacentes para la hora exacta de la estación sobre la que estamos haciendo el cálculo.

