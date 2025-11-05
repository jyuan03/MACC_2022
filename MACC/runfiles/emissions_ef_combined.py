def PG_component_ef_matching(component_count, component_type,filterbygas_comp_ef_df):
    # filterbygas_PG_comp_ef_df = filterbygas_comp_ef_df[filterbygas_comp_ef_df['Service'] == 'PG']
    PG_component_EF_value = filterbygas_comp_ef_df.loc[component_type, '2017EF']
    component_count_emissions = PG_component_EF_value * component_count
    return component_count_emissions

def LL_component_ef_matching(component_count, component_type,filterbyoil_comp_ef_df):
    # filterbyoil_LL_comp_ef_df = filterbyoil_comp_ef_df[filterbyoil_comp_ef_df['Service'] == 'LL']
    PG_component_EF_value = filterbyoil_comp_ef_df.loc[component_type, '2017EF']
    component_count_emissions = PG_component_EF_value * component_count
    return component_count_emissions

def equipment_component_matching(equipment_count, equipment_type,equipment_sum_comp_df):
    equipment_facility_ef = equipment_sum_comp_df.loc[[equipment_type]].values[0]
    facility_count_emissions = equipment_count*equipment_facility_ef
    return facility_count_emissions

def pneumatics_equipment_matching(pneumatics_count, pneumatics_type, datafile_pneumatics_ef):
    pneumatics_EF_value = datafile_pneumatics_ef.loc[pneumatics_type, 'Average Vent Rate'] #(m^{3} natural gas/hour)
    pneumatics_count_emissions = pneumatics_EF_value * pneumatics_count
    return pneumatics_count_emissions