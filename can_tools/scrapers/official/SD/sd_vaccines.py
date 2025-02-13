import json

from typing import Any

import pandas as pd
import us
import os.path

from can_tools.scrapers import CMU, variables
from can_tools.scrapers.util import flatten_dict
from can_tools.scrapers.official.base import MicrosoftBIDashboard


class SDVaccineCounty(MicrosoftBIDashboard):

    has_location = False
    location_type = "county"
    state_fips = int(us.states.lookup("South Dakota").fips)

    source = "https://doh.sd.gov/COVID/Dashboard.aspx"
    source_name = "South Dakota Department of Health"
    powerbi_url = "https://wabi-us-gov-iowa-api.analysis.usgovcloudapi.net"

    variables = {
        "total_vaccine_initiated": variables.INITIATING_VACCINATIONS_ALL,
        "total_vaccine_completed": variables.FULLY_VACCINATED_ALL,
    }

    def construct_body(self, resource_key, ds_id, model_id, report_id, counties):
        "Build body request"
        body = {}

        # Set version
        body["version"] = "1.0.0"
        body["cancelQueries"] = []
        body["modelId"] = model_id

        from_variables = [
            # From
            ("c", "County", 0),
            ("v", "Vaccines", 0),
            ("m", " Measures", 0),
        ]

        select_variables = [
            [
                # Selects
                ("c", "County", "county"),
                ("v", "Manufacturer - Dose # (spelled out)", "doses"),
            ],
            [],
            [
                # Measures
                ("m", "Number of Recipients", "recipients")
            ],
        ]

        where_query = [
            {
                "Condition": {
                    "In": {
                        "Expressions": [
                            {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c"}},
                                    "Property": "County",
                                }
                            }
                        ],
                        "Values": [
                            [{"Literal": {"Value": f"'{counties[0]}'"}}],
                            [{"Literal": {"Value": f"'{counties[1]}'"}}],
                            [{"Literal": {"Value": f"'{counties[2]}'"}}],
                            [{"Literal": {"Value": f"'{counties[3]}'"}}],
                            [{"Literal": {"Value": f"'{counties[4]}'"}}],
                            [{"Literal": {"Value": f"'{counties[5]}'"}}],
                            [{"Literal": {"Value": f"'{counties[6]}'"}}],
                            [{"Literal": {"Value": f"'{counties[7]}'"}}],
                            [{"Literal": {"Value": f"'{counties[8]}'"}}],
                            [{"Literal": {"Value": f"'{counties[9]}'"}}],
                            [{"Literal": {"Value": f"'{counties[10]}'"}}],
                        ],
                    }
                }
            },
            {
                "Condition": {
                    "In": {
                        "Expressions": [
                            {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "v"}},
                                    "Property": "IsMostRecentDose",
                                }
                            }
                        ],
                        "Values": [[{"Literal": {"Value": "true"}}]],
                    }
                }
            },
        ]

        body["queries"] = [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": self.construct_from(from_variables),
                                    "Select": self.construct_select(*select_variables),
                                    "Where": where_query,
                                }
                            }
                        }
                    ]
                },
                "QueryId": "",
                "ApplicationContext": self.construct_application_context(
                    ds_id, report_id
                ),
            }
        ]

        return body

    def fetch(self):
        # Get general information
        self._setup_sess()
        dashboard_frame = self.get_dashboard_iframe()
        resource_key = self.get_resource_key(dashboard_frame)
        ds_id, model_id, report_id = self.get_model_data(resource_key)

        # Get the post url
        url = self.powerbi_query_url()

        # Build post headers
        headers = self.construct_headers(resource_key)

        # get list of counties
        counties = self._retrieve_counties()

        jsons = []
        """
        --The max # of counties that the service will return at one time is 13--
        So, to get all counties make multiple requests.
        There are 66 counties, so we make 6 queries of 11 counties each (11*6 = 66).
        store the results of each in a list then return a list of lists.
        """
        for i in range(0, len(counties), 11):
            body = self.construct_body(
                resource_key, ds_id, model_id, report_id, counties[i : i + 11]
            )
            res = self.sess.post(url, json=body, headers=headers)
            jsons.append(res.json())
        return jsons

    def normalize(self, resjson):
        # extract the data we want from each response
        data = []
        for chunk in resjson:
            foo = chunk["results"][0]["result"]["data"]
            d = foo["dsr"]["DS"][0]["PH"][1]["DM1"]
            data.extend(d)

        # make the mappings manually
        col_mapping = {
            "G0": "county",
            "M_1_DM3_1_C_1": "janssen_series",
            "M_1_DM3_2_C_1": "janssen_booster",
            "M_1_DM3_3_C_1": "moderna_1_dose",
            "M_1_DM3_4_C_1": "moderna_complete",
            "M_1_DM3_5_C_1": "moderna_booster",
            "M_1_DM3_6_C_1": "pfizer_1_dose",
            "M_1_DM3_7_C_1": "pfizer_complete",
            "M_1_DM3_8_C_1": "pfizer_booster",
        }
        data_rows = []
        for record in data:
            flat_record = flatten_dict(record)

            row = {}
            for k in list(col_mapping.keys()):
                flat_record_key = [frk for frk in flat_record.keys() if k in frk]

                if len(flat_record_key) > 0:
                    row[col_mapping[k]] = flat_record[flat_record_key[0]]
            data_rows.append(row)

        # Dump records into a DataFrame and transform
        df = pd.DataFrame.from_records(data_rows)

        # Calculate metrics to match our definitions:
        # SD moves individuals between buckets when they receive shots. E.g when someone gets their second dose of Moderna,
        # they are removed from the 1-dose bucket and placed into the 2-dose bucket. So, we need to combine all the buckets.
        df["total_vaccine_completed"] = (
            df["janssen_series"]
            + df["janssen_booster"]
            + df["moderna_complete"]
            + df["pfizer_complete"]
            + df["moderna_booster"]
            + df["pfizer_booster"]
        )

        df["total_vaccine_initiated"] = (
            df["moderna_1_dose"] + df["pfizer_1_dose"] + df["total_vaccine_completed"]
        )

        out = self._rename_or_add_date_and_location(
            df,
            location_name_column="county",
            timezone="US/Central",
            location_names_to_drop=["Other"],
        )
        out = self._reshape_variables(out, self.variables).dropna()
        return out.replace(
            {"location_name": {"Mccook": "McCook", "Mcpherson": "McPherson"}}
        )
