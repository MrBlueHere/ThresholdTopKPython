from top_k import *
from flask import Flask, render_template, request
import time


App = Flask(__name__)
data_source = UniversityDataSource('./datasets/cwur_data_normalized.csv')


# Handles the app startup
def main():
    App.run()


@App.route('/')
def homepage():
    req = RequestParams()
    req.parse_request(request)

    # At least one param
    if True not in req.get_filter().values():
        req.attributes_filter['national_rank'] = True

    start = time.time()
    if req.get_query_method() == QUERY_SEQUENTIAL:
        print("Running query with {} ...".format(QUERY_SEQUENTIAL))
        top_k_result, counter = top_k_sequential(data_source, req)
    else:
        print("Running query with {} ...".format(QUERY_TOP_K_THRESHOLD))
        top_k_result, counter = top_k_threshold(data_source, req)
    end = time.time()

    columns = ['world_rank']
    columns.extend(data_source.get_data_frame().columns)
    columns.append('aggregate')

    return render_template('main.html', columns=columns, data=top_k_result, k_amount=len(top_k_result),
                           time_elapsed=(end - start), data_access_counter=counter)


if __name__ == '__main__':
    main()
