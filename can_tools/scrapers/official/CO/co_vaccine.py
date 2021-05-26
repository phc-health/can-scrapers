import us
import pandas as pd
import requests 

from can_tools.scrapers.official.base import CountyDashboard
from can_tools.scrapers import variables as v

class ColoradoVaccineDemographics(CountyDashboard):
    has_location = False
    state_fips = us.states.lookup("Colorado").fips
    location_type = "county"
    source = "https://covid19.colorado.gov/vaccine-data-dashboard"
    source_name = ""

    def fetch(self):
        return requests.get("https://drive.google.com/file/d/1pksECDG9mkLKNlBZpT4fzFBvo9isSE_p/edit")

    def normalize(self, data):
        return data.content