import pandas as pd
import json
from pathlib import Path
from .utils import span


def rename_cols(s):
    new_name = (s
        .lower()
        .replace(' ', '_')
        .replace('[', '')
        .replace(']', '')
        .replace('/', '_')
        .replace('relative_humidity_%', 'hum')
        .replace('_kw', '_kW')
        .replace('_w', '_W')
        .replace('prediction', 'pred')
        .replace('temperature_c', 'temp')
        .replace('radiation_', '')
        .replace('drybulb_', '')
        .replace('_status', '')
        .replace('6h_pred', 'pred_6h')
        .replace('12h_pred', 'pred_12h')
        .replace('24h_pred', 'pred_24h')
        .replace('average_unmet_cooling_setpoint_difference_c', 'avg_unmet_cooling_temp') #do we even need this column?
    )
    return new_name


def preprocess_building(nr, data_dir="../data", raw_data_dir=None, output_dir=None):
    #TODO: create importer for format of CityLearn1.0.0 to get buildings from different climate zones.

    #0. parse all path parameters and make them pathlib Paths
    data_dir = Path(data_dir)

    if raw_data_dir is None:
        raw_data_dir = data_dir / "citylearn_challenge_2021"
    else:
        raw_data_dir = Path(raw_data_dir)

    if output_dir is None:
        output_dir = data_dir / "preprocessed"
    else:
        output_dir = Path(output_dir)

    outputfile_stem = output_dir / f"Building_{nr}"

    #1. load json for this building
    schema_json_file = raw_data_dir / "schema.json"
    with open(schema_json_file, 'r') as schema_file:
        schema = json.load(schema_file)

    #2. save building attributes to json file
    building_properties = schema['buildings'][f'Building_{nr}']
    output_json_file = outputfile_stem.with_suffix(".json")
    output_csv_file = outputfile_stem.with_suffix(".csv")
    with open(output_json_file, 'w') as output_json_fh:
        json.dump(building_properties, output_json_fh)
    
    #pv power us needed for assigning the total values to the solar_generation_kW column.
    pv_nominal_power_kW = building_properties['pv']['attributes']['nominal_power']

    #3. load csv files to combine them to dataframe.
    weather = pd.read_csv(raw_data_dir / "weather.csv")
    building_only = pd.read_csv(raw_data_dir / f"Building_{nr}.csv")

    building = pd.concat([building_only, weather], axis=1)
    assert len(building) == len(weather) == len(building_only)

    building = (building
        .drop(columns=["Heating Load [kWh]"])
        .assign(
                datetime = span('2008-01-02', '2011-12-31'),
                holiday = lambda x: x["Day Type"] == 8)
        .assign(workday = lambda x: (x.datetime.dt.weekday >= 1) & (x.datetime.dt.weekday <= 5) & (x["Day Type"] != 8) )
        .drop(columns=["Month", "Hour", "Day Type"])
        .set_index("datetime")
        .rename(columns=rename_cols)
        .assign(solar_generation_kW = lambda x: x.solar_generation_W_kW * pv_nominal_power_kW/1000)
    )

    building['net_load_kWh'] = building['equipment_electric_power_kWh'] + building['dhw_heating_kWh'] + building['cooling_load_kWh'] - building['solar_generation_kW']

    #4. finally save result to csv.
    building.to_csv(outputfile_stem.with_suffix(".csv"))


def load_building(nr = 4, climate_zone = 5, data_dir = "../data"):
    if climate_zone != 5:
        print("[WARNING: Currently only climate zone 5 is supported.]")
        return None
    stem_path = Path(data_dir) / f"preprocessed/Building_{nr}"
    csv_file = stem_path.with_suffix(".csv")
    json_file = stem_path.with_suffix(".json")

    df = pd.read_csv(csv_file).astype({'datetime': 'datetime64'}).set_index('datetime')

    if json_file.is_file():
        with open(json_file, 'r') as json_fh:
            metadata = json.load(json_fh)
        df.attrs = metadata

    return df


if __name__ == "__main__":
    import sys
    print(sys.argv)
    print("name: main:", len(span('2020-01-03')))