# Capstone Bike Project
El objetivo de este repositorio es incluir todo el código y explicaciones relacionadas con la creación del modelo, los
diferentes análisis y conclusiones.
Además, se pondrá a disposición del usuario la web donde podrá probar en tiempo real las predicciones del modelo.

El proyecto tiene la siguiente estructura:

1. [API](API): directorio donde encontrará todo lo relacionado con la creación de la aplicación.
   - API.md: documento donde se redacta todo el proceso.


2. [datasets and models](datasets%20and%20models): directorio donde encontrará todo lo relacionado con el preprocesado y análisis de variables, y la creación del modelo.
   * Load_concatenate_data_code.py: código que genera el dataset con todos los datos en raw extraidos de la web de datos abiertos del Ayuntamiento de Barcelona https://opendata-ajuntament.barcelona.cat/es/
   * Bike_preprocessed_code.py : código que genera el dataset base con las variables contexto.
   * Extra_variables_dataset.py: código que genera el dataset extendido con las varaibles extras añadidas.
   * Docks_Avaliability_Prediction_Bicing.ipynb: notebook de python explora diferentes modelos predictivos y analiza la importancia de las variables en cada uno, para finalmente hacer la selección del mejor modelo y de sus principales variables.
   * MODELO.md: documento donde se redacta todo el proceso de elección de variables, preprocesado y creación del modelo.
   * requirements.txt: documento anexado a los 3 primeros archivos .py que necesita para instalar todas las librerias necesarias para ejecutar el código.
   
3. [Insights](Insights): directorio donde encontrará todo lo relacionado con la definición y el desarrollo de los diferentes insights.
   * imagenes: directorio dedicado a almacenar las imágenes que se necesitan para apoyar las explicaciones de la memoria.
   * INSIGHTS.mg: documento o memoria donde se redactan todos los análisis y desarrollos hechos apoyados por gráficos.
   * Insights_Capston.ipynb: notebook de python con el código utilizado para el análisis y las visualizaciones.



Proyecto realizado por: Núria Romero, Roger Salvador, Demian Moschin, Sherezade Fuentes y María Monserrat

A cargo de los profesores: Mariona Carós Roca y Pere Gilabert Roca 

![img.png](img.png)

