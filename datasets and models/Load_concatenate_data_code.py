from pathlib import Path

import py7zr
import pandas as pd
import os



i2m = list(zip(range(1,13), ['Gener','Febrer','Marc','Abril','Maig','Juny','Juliol','Agost','Setembre','Octubre','Novembre','Desembre']))
def load_data():
    for year in [2023, 2022, 2021, 2020]:
        for month, month_name in i2m:
            file_name = f"{year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z"
            url = f"https://opendata-ajuntament.barcelona.cat/resources/bcn/BicingBCN/{file_name}"

            # Download the 7z file
            os.system(f"curl -o {file_name} {url}")

            # Uncompress the 7z file using the py7zr library:
            with py7zr.SevenZipFile(file_name, mode='r') as z:
                z.extractall()

            # Remove the 7z file
            Path(file_name).unlink()


def join_dataframe():
    # Lista para almacenar los DataFrames de cada archivo CSV
    dataframes = []

    # Iterar sobre los archivos CSV descargados
    for year in [2023, 2022, 2021, 2020]:
        for month, month_name in i2m:
            csv_file = f"data/{year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.csv"
            # Verificar si el archivo CSV existe antes de intentar leerlo
            if not os.path.exists(csv_file):
                raise RuntimeError(f"File {csv_file} does not exist")

            # Leer el archivo CSV y almacenar su contenido en un DataFrame
            df = pd.read_csv(csv_file)
            dataframes.append(df)

    # Concatenar todos los DataFrames en uno solo
    bicing_df = pd.concat(dataframes, ignore_index=True)
    bicing_df.to_csv('data/all-data-concatenated.csv', sep=',', index=False)

    return bicing_df


DOWNSAMPLING_RATIO = 1000  # We'll keep only (approx) 1/DOWNSAMPLING_RATIO of the data

INPUT_FILE = "data/all-data-concatenated.csv"
OUTPUT_FILE = f"data/all-data-concatenated-downsampled-{DOWNSAMPLING_RATIO}.csv"


def sample_data():
    print(f"Downsampling one of every {DOWNSAMPLING_RATIO} lines from {INPUT_FILE} to {OUTPUT_FILE}...")
    with open(INPUT_FILE, 'r') as f, open(OUTPUT_FILE, 'w') as out:
        # Must start with 0 so that the first line (the CSV header) gets picked up and written
        for line_number, line in enumerate(f, start=0):
            if line_number % DOWNSAMPLING_RATIO == 0:
                out.write(line)


if __name__ == "__main__":
    load_data()
    bicing = join_dataframe()
    all_data = pd.read_csv('all-data-concatenated.csv')
    sample_data()








