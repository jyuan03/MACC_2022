import numpy as np
import pandas as pd
from clearstone_data import (facility_to_equip,PG_equip_to_component,LL_equip_to_component,
                             HL_equip_to_component,facility_to_pneumatics,componentEF)
from emissions_ef_combined import (PG_component_ef_matching, equipment_component_matching,LL_component_ef_matching)

def facility_subtype_breakdown():
    facilityfile_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\AER\Vol_2022-01-AB.csv"
    datafile_facility_df = pd.read_csv(facilityfile_path)

    groupby_sum_facilityactivity = datafile_facility_df.groupby(['ReportingFacilitySubType', 'ActivityID']).count()

    filter_by_prod_df = datafile_facility_df[datafile_facility_df['ActivityID'] == 'PROD']
    groupby_sum_facility = filter_by_prod_df.groupby(['ReportingFacilitySubType']).count()

    # facility_list = datafile_facility_df['ReportingFacilitySubType'].unique().tolist()
    # for facility in facility_list:
    #     filtered_by_subtype_df = datafile_facility_df[datafile_facility_df['ReportingFacilitySubType'] == facility & datafile_facility_df['ReportingFacilitySubType'] == facility]
    return groupby_sum_facility

def componentemissionscalcs(facility_counts, new_PG_equipment_type_df,new_LL_equipment_type_df):
    #grab facilities that have equipment data

    # gas_facility_emissions = new_PG_equipment_type_df.mul(facility_counts, axis=0).dropna(axis=0).loc[[361, 362, 363, 364]]
    gas_facility_emissions = new_PG_equipment_type_df
    # oil_facility_emissions = new_LL_equipment_type_df.mul(facility_counts, axis=0).dropna(axis=0).loc[[311, 321, 322, 341, 342]]
    oil_facility_emissions = new_LL_equipment_type_df

    return gas_facility_emissions, oil_facility_emissions
# pd.merge(fac_to_equip_df,PC_components_df,left_index=True, right_index=True)


if __name__ == '__main__':
    fac_to_equip_df = facility_to_equip()
    PG_components_df = PG_equip_to_component()
    LL_components_df = LL_equip_to_component()
    HL_components_df = HL_equip_to_component()
    gas_components, oil_components = componentEF() # kgTHC/hr/source
    fac_to_pneuNG_df, fac_to_pneuIA_df = facility_to_pneumatics()

    unique_facility_type_list = list(fac_to_equip_df.index.values)

    facility_numbers_df = facility_subtype_breakdown()
    facility_counts = facility_numbers_df['ProductionMonth']

#PG Fluid Prod Facility EF/Components/Equipments
    unique_PGcomponent_type_list = list(gas_components.index.values)
    unique_PGequipment_type_list = list(PG_components_df.index.values)
    new_PG_component_ef_df = pd.DataFrame(index=unique_PGequipment_type_list)
    new_PG_equipment_type_df = pd.DataFrame(index=unique_facility_type_list)
    for unique_PGcomponents in unique_PGcomponent_type_list:
        try:
            new_PG_component_ef_df[unique_PGcomponents] = \
                PG_components_df[unique_PGcomponents].apply(PG_component_ef_matching,
                                                          args=[unique_PGcomponents, gas_components])
        except:
            PG_components_df[unique_PGcomponents] = 0
    PG_equip_comp_ef_df = new_PG_component_ef_df.sum(axis=1)

    for unique_PGequipment in unique_PGequipment_type_list:
        try:
            new_PG_equipment_type_df[unique_PGequipment] = \
                fac_to_equip_df[unique_PGequipment].apply(equipment_component_matching,
                                                          args=[unique_PGequipment, PG_equip_comp_ef_df])
        except:
            new_PG_equipment_type_df[unique_PGequipment] = 0
    new_PG_equipment_type_df= new_PG_equipment_type_df.astype(float, errors='ignore')

# LL Fluid Prod Facility EF/Components/Equipments
    unique_LLcomponent_type_list = list(oil_components.index.values)
    unique_LLequipment_type_list = list(LL_components_df.index.values)
    new_LL_component_ef_df = pd.DataFrame(index=unique_LLequipment_type_list)
    new_LL_equipment_type_df = pd.DataFrame(index=unique_facility_type_list)
    for unique_LLcomponents in unique_LLcomponent_type_list:
        try:
            new_LL_component_ef_df[unique_LLcomponents] = \
                LL_components_df[unique_LLcomponents].apply(LL_component_ef_matching,
                                                            args=[unique_LLcomponents, oil_components])
        except:
            LL_components_df[unique_LLcomponents] = 0
    LL_equip_comp_ef_df = new_LL_component_ef_df.sum(axis=1)

    for unique_LLequipment in unique_LLequipment_type_list:
        try:
            new_LL_equipment_type_df[unique_LLequipment] = \
                fac_to_equip_df[unique_LLequipment].apply(equipment_component_matching,
                                                          args=[unique_LLequipment, LL_equip_comp_ef_df])
        except:
            new_LL_equipment_type_df[unique_LLequipment] = 0
    new_LL_equipment_type_df = new_LL_equipment_type_df.astype(float, errors='ignore')

    gas_facility_emissions, oil_facility_emissions = componentemissionscalcs(facility_counts, new_PG_equipment_type_df,new_LL_equipment_type_df)
    print(gas_facility_emissions, oil_facility_emissions)
    gas_facility_emissions.to_csv('gasfacilityemissions_ef.csv')
    oil_facility_emissions.to_csv('oilfacilityemissions_ef.csv')




    # datafile_comp_df = pd.read_csv('C:/Users/jyuan/OneDrive - University of Calgary/PTAC/CE_methane_equipment_to_component.csv')
    # equipment_list = datafile_comp_df['Process_Equipment_Type'].unique().tolist()


