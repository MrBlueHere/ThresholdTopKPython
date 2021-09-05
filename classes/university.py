

# Class which represents the university object and its data
class University:
    def __init__(self, world_rank, name, national_rank, education_quality, alumni_employment, faculty_quality,
                 publications, influence, citations, impact, patents, aggregate_rank):
        self.id = world_rank
        self.name = name
        self.national_rank = national_rank
        self.education_quality = education_quality
        self.alumni_employment = alumni_employment
        self.faculty_quality = faculty_quality
        self.publications = publications
        self.influence = influence
        self.citations = citations
        self.impact = impact
        self.patents = patents
        self.aggregate_rank = aggregate_rank

    def __gt__(self, uni):
        return self.id < uni.id
