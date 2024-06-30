import gc


USE_DASK = False

if USE_DASK:
    import dask.dataframe as pd
else:
    import pandas as pd

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


# FUNCTION TO PROCESS DATASET WITH STATION INFO
def load_station_info():
    dtype = {
        'station_id': 'UInt16',
        # 'name': 'string',
        # 'physical_configuration': 'string',
        # 'lat': 'Float64',
        # 'lon': 'Float64',
        # 'altitude': 'Float64',  # TODO: int?
        # 'address': 'string',
        # 'post_code': 'string',
        'capacity': 'UInt16',
        # 'is_charging_station': 'boolean',
        # 'nearby_distance': 'Float64',  # TODO This seems useless, and an int
        # '_ride_code_support': 'boolean',
        # 'rental_uris': 'string',  # TODO all nans - remove?
        # 'cross_street': 'string',  # TODO all nans - remove?
    }


    df = pd.read_csv(
        'data/Informacio_Estacions_Bicing.csv',
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    # Filter out non-desired station IDs
    return df[df['station_id'].isin(RELEVANT_STATION_IDS)]


def read_bicing_data(filename: str):
    dtype = {
        'station_id': 'UInt16',
        # 'num_bikes_available': 'UInt16',
        # 'num_bikes_available_types.mechanical': 'UInt16',
        # 'num_bikes_available_types.ebike': 'UInt16',
        'num_docks_available': 'UInt16',
        'last_reported': 'UInt64',
        # 'is_charging_station': 'boolean',
        'status': 'string',
        # 'is_installed': 'boolean',
        # 'is_renting': 'boolean',
        # 'is_returning': 'boolean',
        # 'traffic': 'boolean',
        # 'last_updated': 'UInt64',
        # 'ttl': 'Float32',
        # 'Year': 'UInt16',
        # 'Month': 'UInt16',
        # 'V1': 'boolean',
    }

    df = pd.read_csv(
        filename,
        usecols=list(dtype.keys()),
        dtype=dtype,
    )

    # Filter out non-desired station IDs
    return df[df['station_id'].isin(RELEVANT_STATION_IDS)]


# FUNCTION TO PROCESS MAIN DATASET
def process_data(df):
    # Eliminate NaNs
    df = df.dropna()

    # Remove last_reported = 0 because it ends up being 01/01/1970
    df = df[df['last_reported'] != 0]

    # # Process timestamp and extract Hour, Day, Month_t and Year_t
    df['timestamp'] = pd.to_datetime(df['last_reported'], unit='s')
    df['Year'] = df['timestamp'].dt.year
    df['Month'] = df['timestamp'].dt.month
    df['Day'] = df['timestamp'].dt.day
    df['Hour'] = df['timestamp'].dt.hour
    # Drop any year not in 2020-2023
    df = df[(df['Year'] >= 2020) & (df['Year'] <= 2023)]

    return df


# Function to merge bicing big dataframe with dataframe with station info
def merge_dataframes(sample_data_processed, info_stations):
    merge_dataset = sample_data_processed.merge(info_stations, on='station_id', how='inner')
    return merge_dataset


# Function to get mean capacity % per hour, day, mont, year, id_station
def mean_hour(df):
    df['availability_percentage'] = (df['num_docks_available'] / df['capacity']).clip(upper=1)
    mean_hour_dataset = df.groupby(['station_id', 'Year', 'Month', 'Day', 'Hour'])[
        'availability_percentage'].mean().reset_index()
    # Correct availability_percentage values over 100
    mean_hour_dataset['availability_percentage'] = mean_hour_dataset['availability_percentage']
    return mean_hour_dataset


# Function to calculate dataframe with context variables
def calculate_context_variables(df):
    # Number of shifts
    max_shift = 4

    # List to keep rows with calculated context variables
    context_rows = []

    # Iterate over each unique station
    for station_id in df['station_id'].unique():
        print(f"Processing station ID: {station_id}...")

        # Filter by current station
        station_df = df[df['station_id'] == station_id].copy().reset_index(drop=True)

        # Iterate over each row of the current station
        for i in range(max_shift, len(station_df), max_shift + 1):
            current_row = station_df.iloc[i]
            context_values = []

            # Iterate over shifts to calculate context variables
            for shift in range(1, max_shift + 1):
                context_index = i - shift

                # Verify that the calculated index is within the current station range
                if 0 <= context_index < len(station_df):
                    context_value = station_df.iloc[context_index]['availability_percentage']
                    context_values.append(context_value)
                else:
                    context_values.append(None)

            # Add current row and context variables to the list
            context_row = list(current_row) + context_values
            context_rows.append(context_row)

    # convert listo into df
    df_ctx = pd.DataFrame(context_rows,
                          columns=list(df.columns) + [f'ctx-{shift}' for shift in range(1, max_shift + 1)])

    return df_ctx




if __name__ == "__main__":

    # LOAD DATA
    info_stations = load_station_info()
    df = read_bicing_data('data/all-data-concatenated.csv')
    gc.collect()

    # PROCESS DATA

    df = process_data(df)
    gc.collect()

    # MERGE BICING DATAFRAME WITH STATION INFO DATAFRAME
    df = merge_dataframes(df, info_stations)
    gc.collect()

    # GET DATASET WITH MEAN OF CAPACITY % PER HOUR, DAY, MONTH, YEAR, ID_STATION
    df = mean_hour(df)
    gc.collect()

    df.to_csv('data/all_availability_mean_hour.csv', index=False)
    for station_id in df['station_id'].unique():
        df[df['station_id'] == station_id].to_csv(f'data/all_availability_mean_hour_station_{station_id}.csv',
                                                  index=False)
    gc.collect()

    # GET DATASET WITH CONTEXT VARIABLES
    df = calculate_context_variables(df)
    gc.collect()

    # OUTPUT
    df.to_csv('data/all_mean_hour_ctx_2.csv', index=False)
    gc.collect()

