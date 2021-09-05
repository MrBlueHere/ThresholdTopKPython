import pandas as pd


# Should be instantiated in app startup, it is responsible for loading the data from
# csv to memory and pre-sorting it by the available attributes
class UniversityDataSource:
    def __init__(self, src_name):
        self.data_frame = UniversityDataSource.load_from_csv(src_name)

        self.unis_count = len(self.data_frame.index)

        # Sort data
        self.unis_sorted_by = {
            'national_rank': list(self.data_frame["national_rank"].sort_values().iteritems()),
            'quality_of_education': list(self.data_frame["quality_of_education"].sort_values().iteritems()),
            'alumni_employment': list(self.data_frame["alumni_employment"].sort_values().iteritems()),
            'quality_of_faculty': list(self.data_frame["quality_of_faculty"].sort_values().iteritems()),
            'publications': list(self.data_frame["publications"].sort_values().iteritems()),
            'influence': list(self.data_frame["influence"].sort_values().iteritems()),
            'citations': list(self.data_frame["citations"].sort_values().iteritems()),
            'broad_impact': list(self.data_frame["broad_impact"].sort_values().iteritems()),
            'patents': list(self.data_frame["patents"].sort_values().iteritems()),
        }

        # Round values
        for attr in self.unis_sorted_by:
            self.data_frame = self.data_frame.round({attr: 4})

    def get_data_frame(self):
        return self.data_frame

    def get_count(self):
        return self.unis_count

    @staticmethod
    def load_from_csv(src_name):
        df = pd.read_csv(src_name)

        if 'country' in df.columns:
            df.drop('country', axis=1, inplace=True)
        if 'year' in df.columns:
            df.drop('year', axis=1, inplace=True)
        if 'score' in df.columns:
            df.drop('score', axis=1, inplace=True)

        df.set_index("world_rank", inplace=True)
        return df

