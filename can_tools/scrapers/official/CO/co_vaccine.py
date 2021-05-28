import us
import pandas as pd
import requests
import json
import io
import re

from can_tools.scrapers.official.base import CountyDashboard
from can_tools.scrapers import variables as v


class ColoradoVaccineDemographics(CountyDashboard):
    has_location = False
    state_fips = us.states.lookup("Colorado").fips
    location_type = "county"
    source = "https://covid19.colorado.gov/vaccine-data-dashboard"
    source_name = ""

    folder = "1r095ofG8YvNj_dMWEq4XKkfhDaF8-I0n"
    # key taken from google network request
    key = "AIzaSyC1qbk75NzWBvSaDh6KnsjjA9pIrP4lYIE"

    def fetch(self) -> requests.models.Response:
        # download the contents of the drive folder
        url = "https://www.googleapis.com/drive/v3/files?q='{folder}'+in+parents&key={key}"
        header = {"Referer": "https://drive.google.com/"}
        r = requests.get(url.format(folder=self.folder, key=self.key), headers=header)
        return r

    def normalize(self, data: requests.models.Response) -> pd.DataFrame:
        # get list of all files in the folder
        files = json.loads(data.content.decode("utf-8"))["files"]

        # extract newest file by date (search for matching date in list of files)
        date = self._retrieve_dtm1d("US/Mountain")
        search = "covid19_vaccine_" + date.strftime("%Y-%m-%d")
        file = [f for f in files if re.search(search, f["name"])][0]

        # fetch data from matching file and load into df
        params = {"id": file["id"]}
        response = requests.get("https://docs.google.com/uc", params=params)
        df = pd.read_csv(io.BytesIO(response.content), encoding="utf8")

        # wrangle df
        df = (
            df.query(
                "section == 'County-level Data' and category == 'Percent of Cumulative Vaccines by Demographics'"
            )
            .assign(dt=date)
            .drop(columns={"date"})
        )
        return df
