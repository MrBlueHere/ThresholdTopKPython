from classes.university_data_source import *
from classes.university import *
from classes.request_params import *
import heapq


def get_agr_func_from_code(code: str):
    if code == 'avg':
        return avg_func
    else:
        return max_func


# Aggregate function using average of the aggregated values
def avg_func(data_src, uni_index: int, uni_filter: dict):
    attr_sum = 0
    attr_cnt = 0

    for filter_attr in uni_filter:
        # If the attributes is selected
        if uni_filter[filter_attr]:
            attr_sum += data_src.get_data_frame().loc[uni_index][filter_attr]
            attr_cnt += 1
    return round(attr_sum / attr_cnt, 6)


# Aggregate function using max of the aggregated values
def max_func(data_src, uni_index: int, uni_filter: dict):
    attr_max = 0

    for filter_attr in uni_filter:
        # If the attributes is selected
        if uni_filter[filter_attr]:
            attr_max = max(attr_max, data_src.get_data_frame().loc[uni_index][filter_attr])
    return attr_max


def threshold_max_func(data):
    return max(data)


def threshold_avg_func(data):
    return sum(data) / len(data)


# Returns top k elements by naively iterating through all records in data source
def top_k_sequential(data_src, request_params: RequestParams):
    if request_params.k_amount == 0:
        return [], 0

    agr_func = get_agr_func_from_code(request_params.get_aggr_func_code())

    counter = 0

    result = []
    for row in data_src.get_data_frame().itertuples():
        func_val = agr_func(data_src, row.Index, request_params.get_filter())
        new_uni = University(row.Index, row.institution, row.national_rank, row.quality_of_education,
                             row.alumni_employment, row.quality_of_faculty, row.publications, row.influence,
                             row.citations, row.broad_impact, row.patents, func_val)
        result.append((new_uni, func_val))
        counter += 1

    result = sorted(result, key=lambda x: x[1])
    result = [x[0] for x in result]

    print("Data source hit count: {}".format(counter))
    return result[:request_params.get_k_amount()], counter


# Returns top k elements from the data source using Fagin's Threshold algorithm
def top_k_threshold(data_src, request_params: RequestParams):
    if request_params.k_amount == 0:
        return [], 0

    agr_func = get_agr_func_from_code(request_params.get_aggr_func_code())
    threshold_agr_func = threshold_avg_func if agr_func is avg_func else threshold_max_func
    counter = 0
    uni_filter = request_params.get_filter()

    # Min heap with inverted values because we want to check the amount of elements in it and whether the worst
    # one is below or equal to threshold
    heap_li = []
    heapq.heapify(heap_li)
    seen_unis = set()

    # Iterate over items
    for i in range(data_src.get_count()):
        counter += 1
        for_threshold = []

        # Iterate over ordered attribute values
        for attribute in data_src.unis_sorted_by:
            # If the attribute is selected
            if uni_filter[attribute]:
                index, val = data_src.unis_sorted_by[attribute][i]

                for_threshold.append(val)
                uni = data_src.get_data_frame().loc[index]

                if index not in seen_unis:
                    func_val = agr_func(data_src, index, request_params.get_filter())
                    uni_obj = University(index, uni.institution, uni.national_rank, uni.quality_of_education,
                                         uni.alumni_employment, uni.quality_of_faculty, uni.publications, uni.influence,
                                         uni.citations, uni.broad_impact, uni.patents, func_val)
                    heapq.heappush(heap_li, (-1 * func_val, uni_obj))
                    seen_unis.add(index)

                # Remove the worst elements (we could afford this since the agr. func. is monotonic)
                if len(heap_li) > request_params.k_amount:
                    heapq.heappop(heap_li)

        threshold = threshold_agr_func(for_threshold)

        # Threshold reached, stop the iteration since no better elements can be found
        if len(heap_li) >= request_params.k_amount and (-1 * heap_li[0][0]) <= threshold:
            break

    # Heap has inverted values so get n largest (these are the ones with smallest rank)
    result = [uni_tuple[1] for uni_tuple in heapq.nlargest(request_params.k_amount, heap_li)]

    print("Data source hit count: {}".format(counter))
    return result, counter
