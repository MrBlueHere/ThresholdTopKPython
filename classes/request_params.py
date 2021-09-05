from flask import request

UNI_FILTER_VALUES = ['national_rank', 'quality_of_education', 'alumni_employment', 'quality_of_faculty',
                     'publications', 'influence', 'citations', 'broad_impact', 'patents']
DEFAULT_K_AMOUNT = 5
QUERY_SEQUENTIAL = 'sequential'
QUERY_TOP_K_THRESHOLD = 'top_k_threshold'
QUERY_METHODS = [QUERY_SEQUENTIAL, QUERY_TOP_K_THRESHOLD]


class RequestParams:
    def __init__(self):
        self.aggr_func_code = ""
        self.attributes_filter = {}
        self.k_amount = DEFAULT_K_AMOUNT
        self.query_method = QUERY_TOP_K_THRESHOLD

    def parse_request(self, req: request):
        self.aggr_func_code = req.args.get('aggregateFuncSelect')
        req_sort_filter = request.args.getlist('sort_by')
        for val in UNI_FILTER_VALUES:
            if val in req_sort_filter:
                self.attributes_filter[val] = True
            else:
                self.attributes_filter[val] = False

        req_k_amount = req.args.get('kAmount')
        self.k_amount = int(DEFAULT_K_AMOUNT if req_k_amount is None else req_k_amount)

        # Validate and used default if invalid
        if req.args.get('queryMethodSelect') in QUERY_METHODS:
            self.query_method = req.args.get('queryMethodSelect')

    def get_filter(self):
        return self.attributes_filter

    def get_aggr_func_code(self):
        return self.aggr_func_code

    def get_k_amount(self):
        return self.k_amount

    def get_query_method(self):
        return self.query_method
