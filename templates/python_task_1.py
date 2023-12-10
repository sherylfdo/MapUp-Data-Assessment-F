import pandas as pd

def generate_car_matrix(df)->pd.DataFrame:
    car_matrix=df.pivot(columns='id_1', index='id_2', values='car').fillna(0)
    for i in car_matrix.index.intersection(car_matrix.columns):
        car_matrix.loc[i, i] = 0    
    return car_matrix


def get_type_count(df)->dict:
    dict_car_types={'low':0,'medium':0,'high':0}
    for i in df['car']:
        if i<=15:
            dict_car_types['low']+=1
        elif 15<i<=25:
            dict_car_types['medium']+=1
        else:
            dict_car_types['high]+=1
    return dict_car_types


def get_bus_indexes(df)->list:
    mean_val_bus=df['bus'].mean()
    indices=df[df['bus']>2*mean_val_bus].index.tolist()
    sorted_list=sorted(indices)
    return sorted_list


def filter_routes(df)->list:
    truck_routes = df['route'].unique()
    f = []
    for route in truck_routes:
        mean_val_truck = df[df['route'] == route]['truck'].mean()
        if mean_val_truck > 7:
            f.append(route)
    filter_route_truck=sorted(f)
    return filter_route_truck


def multiply_matrix(car_matrix)->pd.DataFrame:
    multiply_matrix = car_matrix.copy() 
    for row, rows in multiply_matrix.iterrows():
        for col in rows.index:
            value = multiply_matrix.at[row, col]
            if value > 20:
                multiply_matrix.at[row, col] *= 0.75
            else:
                multiply_matrix.at[row, col] *= 1.25
            multiply_matrix.at[row, col] = round(multiply_matrix.at[row, col], 1)
    return multiply_matrix
    

def time_check(df)->pd.Series:
    result1 = []
    df['startTime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['endTime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    grouped = df.groupby(['id', 'id_2'])
    for (_, _), group_df in grouped:
        dur_check = (group_df['endTime'].min() - group_df['startTime'].max()) >= pd.Timedelta(days=1)
        days_check = group_df['startTime'].dt.dayofweek.nunique() == 7
        result1.append(dur_check and days_check)
    unique_pairs = df[['id', 'id_2']].drop_duplicates()
    result = pd.Series(result1, index=unique_pairs.index)
    return result
