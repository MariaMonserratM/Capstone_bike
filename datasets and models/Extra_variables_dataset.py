import pandas as pd
import numpy as np
from geopy.distance import distance
from geopy.distance import geodesic

# Taken from the metadata_sample_submission_2024
RELEVANT_STATION_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                        29, 30, 31, 33, 34, 35, 36, 39, 40, 41, 42, 44, 45, 46, 47, 49, 50, 51, 53, 54, 55, 56, 57, 58,
                        60, 61, 62, 63, 64, 65, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 85,
                        86, 87, 88, 89, 90, 92, 94, 95, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                        110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
                        129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147,
                        148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 161, 162, 163, 164, 165, 166, 167,
                        168, 170, 171, 173, 174, 175, 176, 177, 178, 179, 180, 182, 183, 184, 185, 186, 187, 189, 190,
                        192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
                        212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230,
                        231, 232, 233, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 246, 247, 248, 249, 250, 251,
                        252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270,
                        271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 288, 289, 290,
                        291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309,
                        310, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329,
                        331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349,
                        350, 351, 352, 353, 354, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 367, 368, 369, 370,
                        371, 372, 373, 374, 375, 376, 377, 378, 380, 381, 382, 384, 385, 386, 387, 388, 389, 390, 391,
                        392, 393, 394, 395, 396, 397, 398, 400, 401, 402, 404, 405, 406, 408, 409, 410, 412, 413, 414,
                        415, 416, 418, 419, 421, 423, 424, 425, 426, 427, 428, 469, 471, 472, 474, 492, 494, 495, 496]


# ----- FUNCTIONS TO READ ALL FILES NEDDED ------

# FUNCTION TO READ DATASET WITH CONTEXT VARIABLES
def read_ctx_df(filename: str):
    dtype = {
        'station_id': 'Int16',
        'Year': 'Int16',
        'Month': 'Int16',
        'Day': 'Int16',
        'Hour': 'Int16',
        'availability_percentage': 'Float32',
        'ctx-1': 'Float32',
        'ctx-2': 'Float32',
        'ctx-3': 'Float32',
        'ctx-4': 'Float32'
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )
    # Equal column names with test names
    new_column_names = ['station_id', 'year', 'month', 'day', 'hour', 'percentage_docks_available', 'ctx-1', 'ctx-2',
                        'ctx-3', 'ctx-4']
    df.columns = new_column_names
    # Drop year 2020 as it is not representative of our target year (because of the pandemics)
    df = df[df['year'] != 2020]

    return df


# FUNCTION TO READ TEST FILE AND GET IT READY (metadata_sample_submission_2024)
def read_test_df(filename: str):
    dtype = {
        'index': 'Int16',
        'station_id': 'Int16',
        'month': 'Int16',
        'day': 'Int16',
        'hour': 'Int16',
        'ctx-4': 'Float32',
        'ctx-3': 'Float32',
        'ctx-2': 'Float32',
        'ctx-1': 'Float32'
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    df['year'] = 2024
    df['year'] = df['year'].astype('int16')
    new_column_order = ['index', 'station_id', 'year', 'month', 'day', 'hour', 'ctx-1', 'ctx-2', 'ctx-3', 'ctx-4']
    # Apply the new column order
    df = df[new_column_order]
    features = ['station_id', 'year', 'month', 'day', 'hour', 'ctx-1', 'ctx-2', 'ctx-3', 'ctx-4']
    df = df[features]
    return df


# FUNCTION TO READ BARCELONA HOLIDAYS FOR YEARS 2020-2024
def read_bcn_holidays_df(filename: str):
    dtype = {
        'year': 'Int16',
        'month': 'Int16',
        'day': 'Int16',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    df = df['date']

    return df


# FUNCTION TO READ DATASET WITH THE NECESSARY STATION INFO
def read_stations_geocodes(filename: str):
    dtype = {
        'station_id': 'Int16',
        'lat': 'float64',
        'lon': 'float64',
        'altitude': 'Int16',
        'post_code': 'string',
        'capacity': 'Int16',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    # Correct errors in dataset
    df.loc[df['station_id'] == 35, 'post_code'] = '08019'
    df.loc[df['station_id'] == 381, 'post_code'] = '08001'

    return df


# FUNCTION TO READ DATASET WITH INFORMATION ABOUT POSTAL CODES AND NEIGHBORHOODS
def read_postcodes_neighborhood(filename: str):
    dtype = {
        'post_code': 'string',
        'neighborhood': 'string',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
        encoding='unicode_escape',  # for escape some special characters
        sep=';',
    )

    return df




# FUNCTION TO READ DATASET WITH COLLEGE LOCATION INFO
def read_college_info(filename: str):
    dtype = {
        'name': 'string',
        'shortname': 'string',
        'latitud': 'float64',
        'longitud': 'float64',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    return df


#FUNCTION TO READ DATASET WITH LIBRARY LOCATION INFO
def read_library_info(filename: str):
    dtype = {
        'register_id': 'int32',
        'lat': 'float64',
        'lon': 'float64',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    return df


# FUNCTION TO READ DATASET WITH MUSEUM LOCATION INFO
def read_museum_info(filename: str):
    dtype = {
        'register_id': 'int32',
        'lat': 'float64',
        'lon': 'float64',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    return df


# FUNCTION TO READ DATASET WITH THEATER AND CINEMA LOCATION INFO
def read_theater_cinema_info(filename: str):
    dtype = {
        'register_id': 'int32',
        'lat': 'float64',
        'lon': 'float64',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    return df


# FUNCTION TO READ DATASET WITH BARS AND CLUBS LOCATION INFO
def read_bar_club_info(filename: str):
    dtype = {
        'register_id': 'int32',
        'lat': 'float64',
        'lon': 'float64',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    return df


# FUNCTION TO READ TRANSPORT STATIONS LOCACION INFO
def read_transport_info(filename: str):
    dtype = {
        'lat': 'float64',
        'lon': 'float64',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        encoding='unicode_escape',  # for escape some special characters
        dtype=dtype,
    )

    return df


# FUNCTION TO CATEGORIZE PERIODS DURING THE DAY
def categorize_hour(hour):
    if hour in [0, 1, 2, 3, 4, 5]:
        return 'night'
    elif hour in [6, 7, 8, 9]:
        return 'early_morning'
    elif hour in [10, 11, 12, 13, 14]:
        return 'morning'
    elif hour in [15, 16, 17, 18, 19]:
        return 'afternoon'
    elif hour in [20, 21, 22, 23]:
        return 'evening'


# FUNCTION TO GET SEASON
def create_season_info(month):
    if month in (3, 4, 5):
        return 'spring'

    elif month in (6, 7, 8):
        return 'summer'

    elif month in (9, 10, 11):
        return 'autumn'

    elif month in (12, 1, 2):
        return 'winter'


# FUNCTION TO ADD DATE AND DATETIME
def add_day_info_1(df):
    # re-create datetime info
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    # re-create datetime (hour) info
    df['date_hour'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

    return df


# FUNCTION TO ADD OTHER INFO ABOUT DAY (DAY OF THE WEEK, WEEKEND, NON-WORKING DAY, ETC.)
def add_day_info(df):
    # get day of week info
    df['day_info'] = df['date'].dt.day_name()
    # define whether date is weekend or not
    weekend_days = ['Saturday', 'Sunday']
    df['is_weekend'] = np.where(df['day_info'].isin(weekend_days), 1, 0)
    # define whether date is a holiday
    holidays = read_bcn_holidays_df('data/bcn_holidays_2020_2024.csv').tolist()
    df['is_holiday'] = np.where(df['date'].isin(holidays), 1, 0)
    # add column is_not_workday
    df['is_not_workday'] = df.apply(lambda row: 1 if row['is_weekend'] == 1 or row['is_holiday'] == 1 else 0, axis=1)
    # Add cathegories by hours of the day: night, early_morning, morning, afternoon, evening
    df['hour_info'] = df['hour'].apply(categorize_hour)
    # Add sesason cathegories by months
    df['season_info'] = df['month'].apply(create_season_info)

    return df


# FUNCTION TO COUNT NUMBER OF NEARBY BICING STATIONS
def count_nearby_stations(lat, lon, station_info, max_distance=300):
    point = (lat, lon)
    count = 0
    for _, station in station_info.iterrows():
        station_coords = (station['lat'], station['lon'])
        distance = geodesic(point, station_coords).meters
        if distance <= max_distance:
            count += 1
    return count


# FUNCTION TO LIST NEARBY BICING STATIONS
def list_nearby_stations(lat, lon, station_info, max_distance=300):
    point = (lat, lon)
    near_stations = []
    for _, station in station_info.iterrows():
        station_coords = (station['lat'], station['lon'])
        station_id = station['station_id']
        distance = geodesic(point, station_coords).meters
        if distance <= max_distance:
            near_stations.append(station_id)
    return near_stations


# FUNCTION TO GET INFO ON NEARBY BICING STATIONS
def get_info_nearby_stations():
    # Cargar df de estaciones con sus geocodes
    nearby_stations_info = read_stations_geocodes('data/informacio_Estacions_Bicing.csv')
    station_info = read_stations_geocodes('data/informacio_Estacions_Bicing.csv')

    # Add number of nearby stations
    nearby_stations_info['nearby_stations'] = nearby_stations_info.apply(
        lambda row: count_nearby_stations(row['lat'], row['lon'], station_info), axis=1)

    station_info_filetered = station_info[station_info['station_id'].isin(RELEVANT_STATION_IDS)] #####
    nearby_stations_info['nearby_stations_list'] = nearby_stations_info.apply(
        lambda row: list_nearby_stations(row['lat'], row['lon'], station_info_filetered), axis=1) #####

    return nearby_stations_info


# FUNCTION TO ADD NEARBY BICING STATION INFO
def add_info_nearby_stations(df):
    nearby_stations_info = get_info_nearby_stations()
    df_with_nearby_stations_info = df.merge(nearby_stations_info, on='station_id', how='inner')
    return df_with_nearby_stations_info


# FUNCTION TO ADD NEIGHBORHOOD
def add_neighborhood_info(df):
    # stations = read_stations_geocodes('data/informacio_Estacions_Bicing.csv')
    postcodes = read_postcodes_neighborhood('data/postcode_neighborhood.csv')
    neighborhood_info = df.merge(postcodes, on='post_code', how='inner')

    return neighborhood_info


# FUNCTIONS TO CALCULATE IF ELEMENT OF INTEREST IS NEAR THE STATION
def is_near_college(station_lat, station_lon, uni_lat, uni_lon, max_distance=0.3):
    return distance((station_lat, station_lon), (uni_lat, uni_lon)).km < max_distance


def is_near_library(station_lat, station_lon, lib_lat, lib_lon, max_distance=0.2):
    return distance((station_lat, station_lon), (lib_lat, lib_lon)).km < max_distance


def is_near_museum(station_lat, station_lon, mus_lat, mus_lon, max_distance=0.2):
    return distance((station_lat, station_lon), (mus_lat, mus_lon)).km < max_distance


def is_near_theater_cinema(station_lat, station_lon, mus_lat, mus_lon, max_distance=0.2):
    return distance((station_lat, station_lon), (mus_lat, mus_lon)).km < max_distance


def is_near_bar_club(station_lat, station_lon, mus_lat, mus_lon, max_distance=0.2):
    return distance((station_lat, station_lon), (mus_lat, mus_lon)).km < max_distance


def is_near_transport(station_lat, station_lon, transport_lat, transport_lon, max_distance=0.2):
    return distance((station_lat, station_lon), (transport_lat, transport_lon)).km < max_distance


# FUNCTIONS TO COUNT NEARBY ELEMENTS OF INTERESTS (BARS AND COLLEGES)
def count_nearby_bars(lat, lon, bar_info, max_distance=200):
    point = (lat, lon)
    count = 0
    for _, bar in bar_info.iterrows():
        bar_coords = (bar['lat'], bar['lon'])
        distance = geodesic(point, bar_coords).meters
        if distance <= max_distance:
            count += 1
    return count


def count_nearby_colleges(lat, lon, college_info, max_distance=300):
    point = (lat, lon)
    count = 0
    for _, uni in college_info.iterrows():
        uni_coords = (uni['latitud'], uni['longitud'])
        distance = geodesic(point, uni_coords).meters
        if distance <= max_distance:
            count += 1
    return count


# def merge_station_postocode_info():
#     stations = read_stations_geocodes('data/informacio_Estacions_Bicing.csv')
#     postcodes = read_postcodes_neighborhood('data/postcode_neighborhood.csv')
#     geocodes_info = stations.merge(postcodes, on='post_code', how='inner')
#     # geocodes_info = geocodes_info[['station_id', 'neighborhood']]
#
#     return geocodes_info


# FUNCTION TO GET INFORMATION ABOUT NEAR DISTANCE TO ELEMENTS OF INTEREST
def get_geocodes_and_distance_info():
    # Cargar df de estaciones con sus geocodes
    geocodes_info = read_stations_geocodes('data/informacio_Estacions_Bicing.csv')
    transport_info = read_transport_info('data/transport_info.csv')
    college_info = read_college_info('data/college_info.csv')
    library_info = read_library_info('data/library_info.csv')
    museum_info = read_museum_info('data/museum_info.csv')
    theater_info = read_museum_info('data/theater_cinema_info.csv')
    bar_info = read_museum_info('data/bar_club_info.csv')

    # Near to public transport station
    # inicialize column to 0
    geocodes_info['near_transport'] = 0

    # Iterate over each row of the dataframe
    for idx, station in geocodes_info.iterrows():
        station_coords = (station['lat'], station['lon'])

        # Check if bicing station is near to a public transport station
        for _, transport in transport_info.iterrows():
            transport_coords = (transport['lat'], transport['lon'])
            if is_near_college(*station_coords, *transport_coords):
                geocodes_info.at[idx, 'near_transport'] = 1
                break

    # Near to college
    geocodes_info['near_college'] = 0

    for idx, station in geocodes_info.iterrows():
        station_coords = (station['lat'], station['lon'])

        for _, uni in college_info.iterrows():
            uni_coords = (uni['latitud'], uni['longitud'])
            if is_near_college(*station_coords, *uni_coords):
                geocodes_info.at[idx, 'near_college'] = 1
                break

    # Add number of nearby colleges
    geocodes_info['nearby_colleges'] = geocodes_info.apply(
        lambda row: count_nearby_colleges(row['lat'], row['lon'], college_info), axis=1)

    # Near to library
    geocodes_info['near_library'] = 0

    for idx, station in geocodes_info.iterrows():
        station_coords = (station['lat'], station['lon'])

        for _, lib in library_info.iterrows():
            lib_coords = (lib['lat'], lib['lon'])
            if is_near_library(*station_coords, *lib_coords):
                geocodes_info.at[idx, 'near_library'] = 1
                break

    # # Near to museum
    geocodes_info['near_museum'] = 0

    for idx, station in geocodes_info.iterrows():
        station_coords = (station['lat'], station['lon'])

        for _, mus in museum_info.iterrows():
            mus_coords = (mus['lat'], mus['lon'])
            if is_near_museum(*station_coords, *mus_coords):
                geocodes_info.at[idx, 'near_museum'] = 1
                break

    # # Near to theater or cinema
    geocodes_info['near_theater'] = 0

    for idx, station in geocodes_info.iterrows():
        station_coords = (station['lat'], station['lon'])

        for _, theater in theater_info.iterrows():
            theater_coords = (theater['lat'], theater['lon'])
            if is_near_museum(*station_coords, *theater_coords):
                geocodes_info.at[idx, 'near_theater'] = 1
                break

    # # Near to bar or club
    geocodes_info['near_bar'] = 0

    for idx, station in geocodes_info.iterrows():
        station_coords = (station['lat'], station['lon'])

        for _, bar in bar_info.iterrows():
            bar_coords = (bar['lat'], bar['lon'])
            if is_near_museum(*station_coords, *bar_coords):
                geocodes_info.at[idx, 'near_bar'] = 1
                break

    # Add number of nearby bars or clubs
    geocodes_info['nearby_bars'] = geocodes_info.apply(
        lambda row: count_nearby_bars(row['lat'], row['lon'], bar_info), axis=1)

    return geocodes_info[['station_id', 'near_transport', 'near_college', 'nearby_colleges', 'near_library',
                          'near_museum', 'near_theater', 'near_bar', 'nearby_bars']]



# ADD DISTANCE TO ELEMENTS OF INTEREST INFO
def add_geocodes_and_distance_info(df):
    geocodes_info = get_geocodes_and_distance_info()
    df_with_geocodes_info = df.merge(geocodes_info, on='station_id', how='inner')
    return df_with_geocodes_info


# FUNCTION TO CALCULATE AVERAGE CTX-1 OF NEARBY BICING STATIONS AT THE SAME HOUR
def calculate_nearby_avg(row):
    nearby_stations = row['nearby_stations_list']
    date_hour = row['date_hour']
    row_ctx1 = row['ctx-1']

    # Obtener los valores de 'ctx1' para las estaciones cercanas en la misma fecha y hora
    ctx1_values = df_grouped.loc[(nearby_stations, date_hour), 'ctx-1'].values

    if len(ctx1_values) > 1: # Because there is always 1 station that is the station of the testing row itself
        return np.mean(ctx1_values)
    else:
        return row_ctx1


if __name__ == "__main__":

    # CREATE FULL DATASETS (TRAIN AND TEST) WITH CATEGORICAL VARIABLES
    # TRAIN
    df_train = read_ctx_df('data/all_mean_hour_ctx_2.csv')
    df_train = add_day_info_1(df_train)
    df_train = add_info_nearby_stations(df_train)

    # AVERAGE CTX-1 OF NEARBY BICING STATIONS AT THE SAME HOUR
    df_grouped = df_train.set_index(['station_id', 'date_hour'])
    print(df_grouped[['nearby_stations_list']].head())
    df_train['nearby_avg_ctx1'] = df_train.apply(calculate_nearby_avg, axis=1) ## Añadir resto de estaciones en el dataset (modificar en Bike_preprocesed_code)

    df_train = add_day_info(df_train)
    df_train = add_geocodes_and_distance_info(df_train)
    df_train = add_neighborhood_info(df_train)

    # OUTPUT
    df_train.to_csv('data/df_v3_cat.csv', index=False)

    # TEST
    df_test = read_test_df('data/metadata_sample_submission_2024.csv')
    df_test = add_day_info_1(df_test)
    df_test = add_info_nearby_stations(df_test)

    # AVERAGE CTX-1 OF NEARBY BICING STATIONS AT THE SAME HOUR
    df_grouped = df_test.set_index(['station_id', 'date_hour'])
    print(df_grouped[['nearby_stations_list']].head())
    df_test['nearby_avg_ctx1'] = df_test.apply(calculate_nearby_avg,
                                                 axis=1)  ## Añadir resto de estaciones en el dataset (modificar en Bike_preprocesed_code)

    df_test = add_day_info(df_test)
    df_test = add_geocodes_and_distance_info(df_test)
    df_test = add_neighborhood_info(df_test)

    # OUTPUT
    df_test.to_csv('data/df_test_v3_cat.csv', index=False)

    # CREATE FULL DATASET WITH DUMMY (NOT CATEGORICAL) VARIABLES
    # TRAIN
    # Get dummy variables from categorical variables
    df_train = pd.get_dummies(df_train, columns=['day_info', 'hour_info', 'season_info', 'neighborhood'])
    # convert boolean columns into integers (0,1)
    bool_columns_training = ['day_info_Friday', 'day_info_Monday',
                             'day_info_Saturday', 'day_info_Sunday', 'day_info_Thursday',
                             'day_info_Tuesday', 'day_info_Wednesday', 'hour_info_afternoon',
                             'hour_info_early_morning', 'hour_info_evening', 'hour_info_morning',
                             'hour_info_night', 'season_info_autumn', 'season_info_spring',
                             'season_info_summer', 'season_info_winter',
                             'neighborhood_Diagonal_Mar_i_el_Front_Marítim_del_Poblenou',
                             'neighborhood_Horta', 'neighborhood_Navas', 'neighborhood_Sant_Andreu',
                             'neighborhood_Sant_Antoni', 'neighborhood_Sant_Gervasi_-_Galvany',
                             'neighborhood_Sant_Gervasi_-_la_Bonanova',
                             'neighborhood_Sant_Pere,_Santa_Caterina_i_la_Ribera',
                             'neighborhood_Sants', 'neighborhood_Sarrià', 'neighborhood_Torre_Baró',
                             'neighborhood_Vilapicina_i_la_Torre_Llobeta',
                             'neighborhood_el_Barri_Gòtic', 'neighborhood_el_Besòs_i_el_Maresme',
                             'neighborhood_el_Camp_d_en_Grassot_i_Gràcia_Nova',
                             'neighborhood_el_Camp_de_l_Arpa_del_Clot', 'neighborhood_el_Fort_Pienc',
                             'neighborhood_el_Guinardó',
                             'neighborhood_el_Parc_i_la_Llacuna_del_Poblenou',
                             'neighborhood_el_Poble-sec', 'neighborhood_el_Raval',
                             'neighborhood_el_Turó_de_la_Peira',
                             'neighborhood_l_Antiga_Esquerra_de_l_Eixample',
                             'neighborhood_la_Dreta_de_l_Eixample', 'neighborhood_la_Marina_de_Port',
                             'neighborhood_la_Marina_del_Prat_Vermell',
                             'neighborhood_la_Nova_Esquerra_de_l_Eixample', 'neighborhood_la_Salut',
                             'neighborhood_la_Vall_d_Hebron',
                             'neighborhood_la_Vila_Olímpica_del_Poblenou',
                             'neighborhood_la_Vila_de_Gràcia', 'neighborhood_les_Corts',
                             'neighborhood_les_Tres_Torres']

    df_train[bool_columns_training] = df_train[bool_columns_training].astype(int)
    # OUTPUT
    df_train.to_csv('data/df_v3.csv', index=False)

    # TEST
    df_test = pd.get_dummies(df_test, columns=['day_info', 'hour_info', 'season_info', 'neighborhood'])
    bool_columns_test = ['day_info_Friday', 'day_info_Monday',
                         'day_info_Saturday', 'day_info_Sunday', 'day_info_Thursday',
                         'day_info_Tuesday', 'day_info_Wednesday', 'hour_info_afternoon',
                         'hour_info_early_morning', 'hour_info_evening', 'hour_info_morning',
                         'hour_info_night', 'season_info_spring', 'season_info_winter',
                         'neighborhood_Diagonal_Mar_i_el_Front_Marítim_del_Poblenou',
                         'neighborhood_Horta', 'neighborhood_Navas', 'neighborhood_Sant_Andreu',
                         'neighborhood_Sant_Antoni', 'neighborhood_Sant_Gervasi_-_Galvany',
                         'neighborhood_Sant_Gervasi_-_la_Bonanova',
                         'neighborhood_Sant_Pere,_Santa_Caterina_i_la_Ribera',
                         'neighborhood_Sants', 'neighborhood_Sarrià', 'neighborhood_Torre_Baró',
                         'neighborhood_Vilapicina_i_la_Torre_Llobeta',
                         'neighborhood_el_Barri_Gòtic', 'neighborhood_el_Besòs_i_el_Maresme',
                         'neighborhood_el_Camp_d_en_Grassot_i_Gràcia_Nova',
                         'neighborhood_el_Camp_de_l_Arpa_del_Clot', 'neighborhood_el_Fort_Pienc',
                         'neighborhood_el_Guinardó',
                         'neighborhood_el_Parc_i_la_Llacuna_del_Poblenou',
                         'neighborhood_el_Poble-sec', 'neighborhood_el_Raval',
                         'neighborhood_el_Turó_de_la_Peira',
                         'neighborhood_l_Antiga_Esquerra_de_l_Eixample',
                         'neighborhood_la_Dreta_de_l_Eixample', 'neighborhood_la_Marina_de_Port',
                         'neighborhood_la_Marina_del_Prat_Vermell',
                         'neighborhood_la_Nova_Esquerra_de_l_Eixample', 'neighborhood_la_Salut',
                         'neighborhood_la_Vall_d_Hebron',
                         'neighborhood_la_Vila_Olímpica_del_Poblenou',
                         'neighborhood_la_Vila_de_Gràcia', 'neighborhood_les_Corts',
                         'neighborhood_les_Tres_Torres']

    df_test[bool_columns_test] = df_test[bool_columns_test].astype(int)
    # OUTPUT
    df_test.to_csv('data/df_test_v3.csv', index=False)
