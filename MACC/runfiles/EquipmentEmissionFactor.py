import numpy as np
import pandas as pd
from MACC.runfiles.clearstone_data import (facility_to_equip,PG_equip_to_component,LL_equip_to_component,
                             HL_equip_to_component,componentEF, facility_to_pneumatics)
from MACC.runfiles.emissions_ef_combined import (PG_component_ef_matching, equipment_component_matching,LL_component_ef_matching, pneumatics_equipment_matching)

def facility_equipment_EF(GD_equipment_count_across_AB):
    # Facility Subtype Equipment Count
    fac_to_equip_df = facility_to_equip()
    fac_to_equip_df.reset_index(names=['FacilitySubType']).to_csv('fac_to_equip.csv')

    # Component count by equipment type, sorted into fluid type
    PG_components_df = PG_equip_to_component()
    LL_components_df = LL_equip_to_component()
    HL_components_df = HL_equip_to_component()

    # Gas and oil sector component emission factors
    gas_components, oil_components = componentEF()  # kgTHC/hr/source

    # unique facility subtypes list
    unique_facility_type_list = list(fac_to_equip_df.index.values)

    # PG Fluid Prod Facility EF/Components/Equipments
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

    # Equipment summed emission factors from individual components
    PG_equip_comp_ef_df = new_PG_component_ef_df.sum(axis=1)

    for unique_PGequipment in unique_PGequipment_type_list:
        try:
            new_PG_equipment_type_df[unique_PGequipment] = \
                fac_to_equip_df[unique_PGequipment].apply(equipment_component_matching,
                                                          args=[unique_PGequipment, PG_equip_comp_ef_df])
        except:
            new_PG_equipment_type_df[unique_PGequipment] = 0

    # Facility subtype summed emission factors from individual equipment
    new_PG_equipment_type_df = new_PG_equipment_type_df.astype(float, errors='ignore')

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

    new_PG_equipment_type_df.to_csv('gasfacilityemissions_ef.csv')
    new_LL_equipment_type_df.to_csv('oilfacilityemissions_ef.csv')

    #glycol dehydrator emissions
    GD_emissions_AB = GD_equipment_count_across_AB * (PG_equip_comp_ef_df['Dehydrator - Glycol'] + LL_equip_comp_ef_df['Dehydrator - Glycol'])

    return new_PG_equipment_type_df, new_LL_equipment_type_df, GD_emissions_AB, PG_equip_comp_ef_df # kgTHC/hr/ source except for GD

def facility_pneumatics_EF():
    #nocomponents within pneumatics, only calculating for pneumatics count of each facility

    NG_pneumatics_facility_subtype_count, IA_pneumatics_facility_subtype_count = facility_to_pneumatics()

    datafile_pneumatics_ef = pd.read_csv(
       './data/PneumaticsEF.csv').set_index('Device Type')
    # unique facility subtypes list
    fac_to_equip_df = facility_to_equip()
    unique_facility_type_list = list(fac_to_equip_df.index.values)

    # Pneumatics Facility EF/Components/Equipments
    unique_pneumatics_type_list = list(datafile_pneumatics_ef.index.values)
    new_pneumatics_facilitysubtype_df = pd.DataFrame(index=unique_facility_type_list)
    for unique_pneumatics_components in unique_pneumatics_type_list:
        try:
            new_pneumatics_facilitysubtype_df[unique_pneumatics_components] = \
                NG_pneumatics_facility_subtype_count[unique_pneumatics_components].apply(pneumatics_equipment_matching,
                                                            args=[unique_pneumatics_components, datafile_pneumatics_ef])
        except:
            new_pneumatics_facilitysubtype_df[unique_pneumatics_components] = 0
    new_pneumatics_facilitysubtype_df = new_pneumatics_facilitysubtype_df.astype(float, errors='ignore')

    return new_pneumatics_facilitysubtype_df

if __name__ == '__main__':
    GD_equipment_count_across_AB = 1300
    gas_facility_EF, oil_facility_EF, GD_totalemissions_AB, PG_equip_EF_summed = facility_equipment_EF(GD_equipment_count_across_AB) # kgTHC/hr/source except for GD
    all_pneumatics_facility_EF = facility_pneumatics_EF() # m^3 NG/hour

    print(gas_facility_EF)
    print(oil_facility_EF)
    print(GD_totalemissions_AB)
    print(all_pneumatics_facility_EF)