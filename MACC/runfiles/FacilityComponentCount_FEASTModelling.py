import pandas as pd
from MACC.runfiles.clearstone_data import (facility_to_equip, PG_equip_to_component, LL_equip_to_component,
                                           HL_equip_to_component)


def facilitytype_to_component_counts():
    PG_components_df = PG_equip_to_component()
    PG_components_df['totalcomponentcount'] = PG_components_df.sum(axis=1)
    LL_components_df = LL_equip_to_component()
    LL_components_df['totalcomponentcount'] = LL_components_df.sum(axis=1)
    HL_components_df = HL_equip_to_component()
    HL_components_df['totalcomponentcount'] = HL_components_df.sum(axis=1)

    facility_to_equip_df = facility_to_equip()
    facility_to_equip_df = facility_to_equip_df.reset_index(names='facilitysubtype')

    gasfacilities = [351, 361, 362, 363, 364, 365, 366, 367]
    oilfacilitites = [311, 321, 322]
    bitumenfacilties = [331, 341, 342, 343]

    gasfacilities_df = facility_to_equip_df[facility_to_equip_df['facilitysubtype'].isin(gasfacilities)]
    gasfacilities_df = gasfacilities_df.set_index('facilitysubtype').transpose().join(
        PG_components_df[['totalcomponentcount']])
    gasfacilities_compcountdf = gasfacilities_df[[351, 361, 362, 363, 364]].multiply(
        gasfacilities_df['totalcomponentcount'].astype(float),
        axis='index')

    oilfacilities_df = facility_to_equip_df[facility_to_equip_df['facilitysubtype'].isin(oilfacilitites)]
    oilfacilities_df = oilfacilities_df.set_index('facilitysubtype').transpose().join(
        LL_components_df[['totalcomponentcount']])
    oilfacilities_compcountdf = oilfacilities_df[[311, 321, 322]].multiply(
        oilfacilities_df['totalcomponentcount'].astype(float),
        axis='index')

    oil_gas_facilities_compcountdf = pd.concat([gasfacilities_compcountdf, oilfacilities_compcountdf])
    oil_gas_facilities_compcountdf = oil_gas_facilities_compcountdf.transpose()
    oil_gas_facilities_compcountdf['facility_componentcount_total'] = oil_gas_facilities_compcountdf.sum(axis=1)
    oil_gas_facilities_compcountdf['facility_componentcount_total'].to_csv('FacilityComponentCount_FEASTModelling.csv')

    return oil_gas_facilities_compcountdf

def regional_wellandcomponent_count(oil_gas_facilities_compcountdf):
    abdata_path = r"C:\Users\jyuan\OneDrive - University of Calgary\Methane\MonteCarlo_uncertainty\runfiles\Well Infrastructure-AB_regionareas.csv"
    abdata_df = pd.read_csv(abdata_path)
    abdata_df = abdata_df.loc[abdata_df['WellStatusMode'].isin(['FLOW', 'PUMP'])]

    abdata_df = abdata_df[['WellID', 'WellIdentifier', 'LinkedFacilityID', 'LinkedFacilitySubType', 'area']]

    componentcount = oil_gas_facilities_compcountdf[['facility_componentcount_total']].reset_index(names='LinkedFacilitySubType')
    componentcount.to_csv('well_componentcount.csv')

    #determine how many components in each facility type
    well_componentcount = abdata_df.dropna(subset=['LinkedFacilityID']).astype({'LinkedFacilitySubType':float})
    well_componentcount = well_componentcount.merge(componentcount, how='left', on='LinkedFacilitySubType')

    #determine how many facility types per region
    facilities_2022 = pd.read_csv(r'C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\2022v10_oilgasfacilityvol.csv')
    facilities_2022_regionalwelltype_count = facilities_2022.set_index('ReportingFacilityID').join(well_componentcount[['area', 'LinkedFacilitySubType', 'LinkedFacilityID']].set_index('LinkedFacilityID'), how='left')
    facilities_2022_regionalwelltype_count = facilities_2022_regionalwelltype_count.dropna(subset='area')
    facilities_2022_regionalwelltype_count = facilities_2022_regionalwelltype_count[~facilities_2022_regionalwelltype_count.index.duplicated(keep='first')]

    facilities_2022_subtypecount = facilities_2022_regionalwelltype_count.reset_index(names='LinkedFacilityID')[['area', 'LinkedFacilitySubType', 'LinkedFacilityID']].groupby(['area', 'LinkedFacilitySubType']).count()
    facilities_2022_subtypecount = facilities_2022_subtypecount.reset_index(names=['area', 'LinkedFacilitySubType']).astype({'LinkedFacilitySubType': 'int32'})
    facilities_2022_subtypecount = facilities_2022_subtypecount.pivot(index= 'area', columns='LinkedFacilitySubType', values ='LinkedFacilityID')
    facilities_2022_subtypecount = facilities_2022_subtypecount[[351, 361, 362, 363, 364, 311, 321, 322]]
    facilities_2022_subtypecount.to_csv('2022_regional_welltype_count.csv')

    # regional_welltype_count = well_componentcount[['area', 'LinkedFacilitySubType', 'LinkedFacilityID']].groupby(['area', 'LinkedFacilitySubType']).count()
    # regional_welltype_count = regional_welltype_count.reset_index(names=['area', 'LinkedFacilitySubType']).astype({'LinkedFacilitySubType': 'int32'})
    # regional_welltype_count = regional_welltype_count.pivot(index= 'area', columns='LinkedFacilitySubType', values ='LinkedFacilityID')
    # regional_welltype_count = regional_welltype_count[[351, 361, 362, 363, 364, 365, 366, 367, 311, 321, 322]]
    #
    # regional_welltype_count.to_csv('regional_welltype_count.csv')

    return


if __name__ == '__main__':
    oil_gas_facilities_compcountdf = facilitytype_to_component_counts()
    regional_wellandcomponent_count(oil_gas_facilities_compcountdf)
