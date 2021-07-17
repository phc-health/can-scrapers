import us
import pandas as pd
from can_tools.scrapers import variables
from can_tools.scrapers.official.base import TableauDashboard


class IdahoCountyVaccine(TableauDashboard):
    has_location = False
    location_type = "county"
    source = "https://coronavirus.idaho.gov/"
    source_name = "Idaho Official Government Website"
    data_tableau_table = "Vax Rate / County Chart (2)"
    baseurl = "https://public.tableau.com"
    viewPath = "COVID-19VaccineDataDashboard/VaccineUptakeIdahoIIS"
    filterFunctionName = "[Parameters].[Map (copy)]"  # set to county level
    secondaryFilterFunctionName = (
        "[federated.1kzfta61gthwho1b6d51b1t54x4v].[none:dose_number:nk]"  # dose type
    )
    filterFunctionValue = "County"
    state_fips = int(us.states.lookup("Idaho").fips)

    variables = {
        "1": variables.INITIATING_VACCINATIONS_ALL,
        "2": variables.FULLY_VACCINATED_ALL,
    }

    def fetch(self):
        # get both 1 dose and complete data
        self.secondaryFilterValue = "1"
        one_dose = super().fetch()
        self.secondaryFilterValue = "2"
        complete = super().fetch()

        return pd.concat([one_dose, complete])

    def normalize(self, data):
        df = data.rename(
            columns={
                "SUM(Doses_Unique)-alias": "doses",
                "PHD or County Bar Chart-value": "county",
                "dose_number-value": "dose_number",
            }
        )
        keep = df[["county", "doses", "dose_number"]].drop_duplicates()
        out = (
            keep.pivot(index="county", columns="dose_number", values="doses")
            .reset_index()
            .rename_axis(None, axis=1)
        )
        # It seems like people who are fully vaccinated are no longer counted in the
        # "people who have received one dose" category. Summing these two together to
        # match our definition
        out["1"] = out["1"] + out["2"]

        out = self._rename_or_add_date_and_location(
            out, location_name_column="county", timezone="US/Mountain"
        )
        out = self._reshape_variables(out, self.variables)

        return out
