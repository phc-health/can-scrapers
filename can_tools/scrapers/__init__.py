from can_tools.scrapers import util
from can_tools.scrapers.base import CMU, DatasetBase
from can_tools.scrapers.nytimes.nyt_cases_deaths import NYTimesCasesDeaths

from can_tools.scrapers.official.AL.al_vaccine import (
    ALCountyVaccine,
    ALCountyVaccineSex,
    ALCountyVaccineRace,
    ALCountyVaccineAge,
)
from can_tools.scrapers.official.AK.ak_vaccine import (
    AlaskaCountyVaccine,
)
from can_tools.scrapers.official.AZ.az_vaccine import (
    ArizonaVaccineCounty,
)
from can_tools.scrapers.official.AZ.az_demographics import ArizonaVaccineRace

from can_tools.scrapers.official.AZ.counties.maricopa_vaccine import (
    ArizonaMaricopaVaccine,
)
from can_tools.scrapers.official.AZ.counties.maricopa_race import MaricopaVaccineRace
from can_tools.scrapers.official.CA.ca_vaccine import (
    CaliforniaVaccineCounty,
    CaliforniaVaccineDemographics,
)
from can_tools.scrapers.official.CT.ct_vaccine import CTCountyVaccine
from can_tools.scrapers.official.DC.dc_cases import DCCases
from can_tools.scrapers.official.DC.dc_deaths import DCDeaths

from can_tools.scrapers.official.DE.de_vaccine import (
    DelawareCountyVaccine,
    DelawareVaccineDemographics,
)

from can_tools.scrapers.official.DC.dc_vaccines import (
    DCVaccine,
    DCVaccineDemographics,
)

from can_tools.scrapers.official.federal.CDC.cdc_testing_cases import (
    CDCHistoricalTestingDataset,
    CDCOriginallyPostedTestingDataset,
    CDCTestingBase,
)

from can_tools.scrapers.official.federal.CDC.cdc_community_level import (
    CDCCommunityLevelMetrics,
)

from can_tools.scrapers.official.federal.CDC.cdc_vaccines import (
    CDCStateVaccine,
    CDCUSAVaccine,
)
from can_tools.scrapers.official.federal.CDC.cdc_county_vaccines import CDCCountyVaccine

from can_tools.scrapers.official.federal.CDC.cdc_historical_vaccine import (
    CDCHistoricalCountyVaccine,
)
from can_tools.scrapers.official.federal.CDC.cdc_variant_tracker import (
    CDCVariantTracker,
)
from can_tools.scrapers.official.federal.HHS.facility import (
    HHSReportedPatientImpactHospitalCapacityFacility,
)

from can_tools.scrapers.official.federal.HHS.hhs_state_testing import HHSTestingState

from can_tools.scrapers.official.federal.HHS.hhs_state import (
    HHSReportedPatientImpactHospitalCapacityState,
)

from can_tools.scrapers.official.GA.ga_vaccines import (
    GeorgiaCountyVaccine,
    GeorgiaCountyVaccineAge,
    GeorgiaCountyVaccineRace,
    GeorgiaCountyVaccineSex,
    GeorgiaCountyVaccineEthnicity,
)
from can_tools.scrapers.official.HI.hi_county import HawaiiVaccineCounty
from can_tools.scrapers.official.HI.hi_demographics import (
    HawaiiVaccineRace,
    HawaiiVaccineAge,
)

from can_tools.scrapers.official.ID.id_county import IdahoCountyVaccine

from can_tools.scrapers.official.IA.ia_vaccine_county import IowaCountyVaccine
from can_tools.scrapers.official.ID.id_county import IdahoCountyVaccine
from can_tools.scrapers.official.IL.il_vaccine import (
    IllinoisVaccineCounty,
)
from can_tools.scrapers.official.IL.il_vaccine_demographics import (
    ILVaccineRace,
)
from can_tools.scrapers.official.IN.in_vaccines import IndianaCountyVaccinations
from can_tools.scrapers.official.LA.la_county import (
    LAVaccineCounty,
    LAVaccineCountyDemographics,
)
from can_tools.scrapers.official.MD.md_vaccine import MarylandCountyVaccines
from can_tools.scrapers.official.ME.me_vaccines import MaineCountyVaccines
from can_tools.scrapers.official.MI.mi_vaccine import (
    MichiganVaccineCounty,
)
from can_tools.scrapers.official.MI.mi_vaccine_demographics import MIVaccineRaceAge
from can_tools.scrapers.official.ME.me_vaccines import (
    MaineCountyVaccines,
    MaineRaceVaccines,
    MaineGenderVaccines,
    MaineAgeVaccines,
)
from can_tools.scrapers.official.MN.mn_vaccine import (
    MinnesotaCountyVaccines,
    MinnesotaCountyAgeVaccines,
    MinnesotaCountySexVaccines,
)
from can_tools.scrapers.official.MO.mo_vaccine import MissouriVaccineCounty
from can_tools.scrapers.official.MS.ms_vaccine import MSCountyVaccine
from can_tools.scrapers.official.MT.mt_vaccinations import (
    MontanaCountyVaccine,
    MontanaStateVaccine,
)

from can_tools.scrapers.official.MA.ma_vaccines import MassachusettsVaccineDemographics
from can_tools.scrapers.official.NC.nc_vaccine import NCVaccine, NCVaccineState
from can_tools.scrapers.official.ND.nd_vaccines import NDVaccineCounty

# 12/02/21: NE has made their server private, so we can no longer access the data driving the NebraskaCases scraper
# I'm leaving the code intact in case they begin to publish data publicly again at some point. Commenting this out removes
# the scraper from list that drives the Prefect tasks, so this scraper will not be included in any flows (because it isn't functional)
# from can_tools.scrapers.official.NE.ne_cases import NebraskaCases

from can_tools.scrapers.official.NH.nh_demographics import NHVaccineRace

from can_tools.scrapers.official.NJ.nj_vaccine import NewJerseyVaccineCounty
from can_tools.scrapers.official.NM.nm_vaccine import NewMexicoVaccineCounty
from can_tools.scrapers.official.NV.nv_vaccines import NevadaCountyVaccines
from can_tools.scrapers.official.NY.ny_vaccine import (
    NewYorkVaccineCounty,
    NewYorkVaccineCountyAge,
    NewYorkVaccineCountySex,
)
from can_tools.scrapers.official.OH.oh_vaccine import OhioVaccineCounty
from can_tools.scrapers.official.OH.oh_vaccine_demographics import (
    OHVaccineCountyRace,
    OHVaccineCountySex,
    OHVaccineCountyAge,
    OHVaccineCountyEthnicity,
)
from can_tools.scrapers.official.OR.or_vaccine import OregonVaccineCounty
from can_tools.scrapers.official.OR.or_vaccine_demographics import (
    OregonVaccineRace,
    OregonVaccineAge,
    OregonVaccineSex,
)
from can_tools.scrapers.official.PA.pa_vaccines import (
    PennsylvaniaCountyVaccines,
    PennsylvaniaVaccineAge,
    PennsylvaniaVaccineEthnicity,
    PennsylvaniaVaccineRace,
    PennsylvaniaVaccineSex,
)

from can_tools.scrapers.official.PA.philadelhpia_vaccine import PhiladelphiaVaccine

from can_tools.scrapers.official.SC.sc_demographics import (
    SCVaccineRace,
    SCVaccineEthnicity,
)

from can_tools.scrapers.official.SD.sd_vaccines import SDVaccineCounty
from can_tools.scrapers.official.SD.sd_vaccine_demographics import (
    SDVaccineRace,
    SDVaccineSex,
    SDVaccineEthnicity,
    SDVaccineAge,
)

from can_tools.scrapers.official.TN.tn_vaccine import TennesseeVaccineCounty
from can_tools.scrapers.official.TX.texas_vaccine import (
    TexasCountyVaccine,
    TexasStateVaccine,
    TXVaccineCountyAge,
    TXVaccineCountyRace,
)
from can_tools.scrapers.official.VA.va_vaccine import (
    VirginiaVaccine,
    VirginiaCountyVaccineDemographics,
)
from can_tools.scrapers.official.VT.vt_vaccinations import (
    VermontCountyVaccine,
)
from can_tools.scrapers.official.WA.wa_vaccine import (
    WashingtonVaccine,
    WashingtonVaccineCountyRace,
)
from can_tools.scrapers.official.WI.wi_county_vaccine import WisconsinVaccineCounty
from can_tools.scrapers.official.WI.wi_demographic_vaccine import (
    WisconsinVaccineCountyRace,
    WisconsinVaccineCountySex,
    WisconsinVaccineCountyAge,
    WisconsinVaccineCountyEthnicity,
)
from can_tools.scrapers.official.WV.wv_vaccine import (
    WVCountyVaccine,
    WVCountyVaccineRace,
    WVCountyVaccineAge,
    WVCountyVaccineSex,
)

from can_tools.scrapers.usafacts import USAFactsCases, USAFactsDeaths
