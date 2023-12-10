import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    unique_ids = sorted(set(data['id_start'].unique()) | set(data['id_end'].unique()))
    distances = {(start, end): data[(data['id_start'] == start) & (data['id_end'] == end)]['distance'].sum()
                  for start in unique_ids
                  for end in unique_ids}
    distance_matrix = pd.DataFrame([[distances.get((i, j), 0) for j in unique_ids] for i in unique_ids], index=unique_ids, columns=unique_ids)
    return distance_matrix


def unroll_distance_matrix(distance_matrix):
    unrolled_matrix = distance_matrix.shape[0]
    unrolled_distances = [[distance_matrix.index[i], distance_matrix.columns[j], distance_matrix.iloc[i, j]]
                          for i in range(unrolled_matrix) for j in range(i + 1, unrolled_matrix) if distance_matrix.iloc[i, j] != 0]
    unrolled_df = pd.DataFrame(unrolled_distances, columns=['id_start', 'id_end', 'distance'])
    return unrolled_df


def find_ids_within_ten_percentage_threshold(unrolled_df, ref_val):
    ref_avg = unrolled_df[unrolled_df['id_start'] == ref_val]['distance'].mean()
    thresh_min = ref_avg - (ref_avg*0.1)
    thresh_max = ref_avg + (ref_avg*0.1)
    within = unrolled_df[(unrolled_df['id_start'] != ref_val) & 
                                 (unrolled_df['distance'].between(thresh_min, thresh_max))]
    ten_percent_threshold=sorted(within['id_start'].unique())
    return ten_percent_threshold


def calculate_toll_rate(unrolled_df):
    rate_coeff = {'moto': 0.8, 'car': 1.2, 
                'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_types, rate in rate_coeff.items():
        unrolled_df[vehicle_types] = unrolled_df['distance'] * rate
    return unrolled_df


def calculate_time_based_toll_rates(find_ids_within_ten_percentage_threshold):
    intervals = [
        (datetime.strptime('00:00:00', '%H:%M:%S').time(), datetime.strptime('10:00:00', '%H:%M:%S').time(), 0.8),
        (datetime.strptime('10:00:00', '%H:%M:%S').time(), datetime.strptime('18:00:00', '%H:%M:%S').time(), 1.2),
        (datetime.strptime('18:00:00', '%H:%M:%S').time(), datetime.strptime('23:59:59', '%H:%M:%S').time(), 0.8),
        (datetime.strptime('00:00:00', '%H:%M:%S').time(), datetime.strptime('23:59:59', '%H:%M:%S').time(), 0.7)]
    rows = []
    for id_start, id_end in df[['id_start', 'id_end']].drop_duplicates().itertuples(index=False):
        for day in range(7):
            for start_time, end_time, rate in intervals:
                rows.append([id_start, id_end, datetime(2023, 1, 1) + timedelta(days=day), start_time, datetime(2023, 1, 1) + timedelta(days=day), end_time, rate])

    time_toll=pd.DataFrame(rows, columns=['id_start', 'id_end', 'start_day', 'start_time', 'end_day', 'end_time', 'rate_factor'])
    return time_toll
