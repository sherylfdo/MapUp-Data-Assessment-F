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
    
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    return pd.Series()


df=pd.read_csv("dataset-1.csv")
