import matplotlib.pyplot as plt
import time
from TopK.top_k import *


def get_time_and_access_stats(data_src: UniversityDataSource, req: RequestParams, sizes, is_attr=False):
    time_data = []
    access_data = []
    for i in sizes:
        if is_attr:
            req.attributes_filter[UNI_FILTER_VALUES[i]] = True
        else:
            req.k_amount = i
        start = time.time()
        if req.query_method == QUERY_SEQUENTIAL:
            _, counter = top_k_sequential(data_src, req)
        else:
            _, counter = top_k_threshold(data_src, req)
        end = time.time()
        time_data.append(end - start)
        access_data.append(counter)
    return time_data, access_data


# Compares the naive and threshold implementation based on the aggregate function and site of k-parameter
def compare_query_method(data_src: UniversityDataSource):
    k_sizes = [5]
    k_sizes.extend([x for x in range(20, 100, 20)])

    req = RequestParams()
    req.attributes_filter = {key: False for key in UNI_FILTER_VALUES}
    req.attributes_filter['national_rank'] = True
    req.attributes_filter['quality_of_education'] = True
    req.attributes_filter['alumni_employment'] = True
    req.k_amount = DEFAULT_K_AMOUNT

    # Sequential runs
    req.query_method = QUERY_SEQUENTIAL
    req.aggr_func_code = 'avg'
    seq_avg_time_data, seq_avg_access_data = get_time_and_access_stats(data_src, req, k_sizes)

    req.aggr_func_code = 'max'
    seq_max_time_data, seq_max_access_data = get_time_and_access_stats(data_src, req, k_sizes)

    # Threshold runs
    req.query_method = QUERY_TOP_K_THRESHOLD
    req.aggr_func_code = 'avg'
    threshold_avg_time_data, threshold_avg_access_data = get_time_and_access_stats(data_src, req, k_sizes)

    req.aggr_func_code = 'max'
    threshold_max_time_data, threshold_max_access_data = get_time_and_access_stats(data_src, req, k_sizes)

    # Plotting
    plt.plot(k_sizes, seq_avg_time_data, label='Sequential with average aggregate func')
    plt.plot(k_sizes, seq_max_time_data, label='Sequential with max aggregate func')
    plt.plot(k_sizes, threshold_avg_time_data, label='Threshold with average aggregate func')
    plt.plot(k_sizes, threshold_max_time_data, label='Threshold with max aggregate func')
    plt.title('Comparison of sequential and threshold searches (ranking by 3 attributes over a dataset with 7000 items)')
    plt.xlabel('Size of the k-parameter')
    plt.ylabel('Time in seconds')
    plt.legend()
    plt.show()

    plt.plot(k_sizes, seq_avg_access_data, label='Sequential with average aggregate func')
    plt.plot(k_sizes, seq_max_access_data, label='Sequential with max aggregate func')
    plt.plot(k_sizes, threshold_avg_access_data, label='Threshold with average aggregate func')
    plt.plot(k_sizes, threshold_max_access_data, label='Threshold with max aggregate func')
    plt.title(
        'Comparison of sequential and threshold searches (ranking by 3 attributes over a dataset with 7000 items)')
    plt.xlabel('Size of the k-parameter')
    plt.ylabel('Data source access count')
    plt.legend()
    plt.show()


# Compares the naive and threshold implementation based on the amount of selected attributes
def compare_number_of_attributes(data_src: UniversityDataSource):
    attr_sizes = [x for x in range(len(UNI_FILTER_VALUES))]

    req = RequestParams()
    req.attributes_filter = {key: False for key in UNI_FILTER_VALUES}
    req.k_amount = DEFAULT_K_AMOUNT
    req.aggr_func_code = 'max'

    # Sequential runs
    req.query_method = QUERY_SEQUENTIAL
    seq_time_data, seq_access_data = get_time_and_access_stats(data_src, req, attr_sizes, True)

    # Threshold runs
    req.query_method = QUERY_TOP_K_THRESHOLD
    req.attributes_filter = {key: False for key in UNI_FILTER_VALUES}
    threshold_time_data, threshold_access_data = get_time_and_access_stats(data_src, req, attr_sizes, True)

    # Plotting
    plt.plot(attr_sizes, seq_time_data, label='Sequential with max aggregate func')
    plt.plot(attr_sizes, threshold_time_data, label='Threshold with max aggregate func')
    plt.title(
        'Comparison of sequential and threshold searches based on the amount of attributes to rank by (dataset with 7000 items)')
    plt.xlabel('Number of attributes')
    plt.ylabel('Time in seconds')
    plt.legend()
    plt.show()

    plt.plot(attr_sizes, seq_access_data, label='Sequential with max aggregate func')
    plt.plot(attr_sizes, threshold_access_data, label='Threshold with max aggregate func')
    plt.title(
        'Comparison of sequential and threshold searches based on the amount of attributes to rank by (dataset with 7000 items)')
    plt.xlabel('Number of attributes')
    plt.ylabel('Data source access count')
    plt.legend()
    plt.show()


# Runs performance comparison experiments and plots the results
def run_perf_experiments():
    data_source = UniversityDataSource('../datasets/random.csv')

    #compare_query_method(data_source)
    compare_number_of_attributes(data_source)


run_perf_experiments()
