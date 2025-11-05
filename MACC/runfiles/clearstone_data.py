import pandas as pd

def facility_to_equip():
    datafile_equip_df = pd.read_csv('C:/Users/jyuan/OneDrive - University of Calgary/PTAC/CE_methane_facilitysubtype_to_equipment.csv')

    equipment_list = datafile_equip_df['Process_Equipment_Type'].unique().tolist()
    facility_list = datafile_equip_df['Facility_SubType_Code'].unique().tolist()

    flattened_equip_list_df = pd.DataFrame(index= facility_list)

    for equipment in equipment_list:
        filtered_df = datafile_equip_df[datafile_equip_df['Process_Equipment_Type'] == equipment].set_index('Facility_SubType_Code')
        # this requires the same index
        flattened_equip_list_df[equipment] = filtered_df['Average_Equipment_Count']

    flattened_equip_list_df = flattened_equip_list_df.fillna(0)

    return flattened_equip_list_df

def PG_equip_to_component():
    datafile_component_df = pd.read_csv(
        'C:/Users/jyuan/OneDrive - University of Calgary/PTAC/CE_methane_equipment_to_component.csv')
    filtered_by_process_gas_df = datafile_component_df[datafile_component_df['ServiceType'] == 'Process Gas']

    equipment_list_PG = filtered_by_process_gas_df['Process_Equipment_Type'].unique().tolist()
    component_list_PG = filtered_by_process_gas_df['ComponentType'].unique().tolist()

    flattened_PG_component_list = pd.DataFrame(index= equipment_list_PG)

    for component in component_list_PG:
        filtered_df = filtered_by_process_gas_df[filtered_by_process_gas_df['ComponentType'] == component].set_index('Process_Equipment_Type')
        flattened_PG_component_list[component] = filtered_df['AverageComponentCount']

    flattened_PG_component_list = flattened_PG_component_list.fillna(0)
    return flattened_PG_component_list


def LL_equip_to_component():
    datafile_component_df = pd.read_csv(
        'C:/Users/jyuan/OneDrive - University of Calgary/PTAC/CE_methane_equipment_to_component.csv')
    filtered_by_light_liquid_df = datafile_component_df[datafile_component_df['ServiceType'] == 'Light Liquid']

    equipment_list_LL = filtered_by_light_liquid_df['Process_Equipment_Type'].unique().tolist()
    component_list_LL = filtered_by_light_liquid_df['ComponentType'].unique().tolist()

    flattened_LL_component_list = pd.DataFrame(index= equipment_list_LL)

    for component in component_list_LL:
        filtered_df = filtered_by_light_liquid_df[filtered_by_light_liquid_df['ComponentType'] == component].set_index('Process_Equipment_Type')
        flattened_LL_component_list[component] = filtered_df['AverageComponentCount']

    flattened_LL_component_list = flattened_LL_component_list.fillna(0)

    return flattened_LL_component_list

def HL_equip_to_component():
    datafile_component_df = pd.read_csv(
        'C:/Users/jyuan/OneDrive - University of Calgary/PTAC/CE_methane_equipment_to_component.csv')
    filtered_by_heavy_liquid_df = datafile_component_df[datafile_component_df['ServiceType'] == 'Heavy Liquid']

    equipment_list_HL = filtered_by_heavy_liquid_df['Process_Equipment_Type'].unique().tolist()
    component_list_HL = filtered_by_heavy_liquid_df['ComponentType'].unique().tolist()

    flattened_HL_component_list = pd.DataFrame(index= equipment_list_HL)

    for component in component_list_HL:
        filtered_df = filtered_by_heavy_liquid_df[filtered_by_heavy_liquid_df['ComponentType'] == component].set_index('Process_Equipment_Type')
        flattened_HL_component_list[component] = filtered_df['AverageComponentCount']

    flattened_HL_component_list = flattened_HL_component_list.fillna(0)

    return flattened_HL_component_list

def facility_to_pneumatics():
    datafile_component_df = pd.read_csv(
        'C:/Users/jyuan/OneDrive - University of Calgary/PTAC/FacilitytoPneumatics.csv')
    filtered_by_NG_df = datafile_component_df[datafile_component_df['Driver'] == 'Natural Gas']

    pneu_list_NG = filtered_by_NG_df['PneumaticDeviceType'].unique().tolist()
    facility_list_NG = filtered_by_NG_df['FacilitySubtype'].unique().tolist()

    flattened_NGPneu_list_df = pd.DataFrame(index= facility_list_NG)

    for pneumatic in pneu_list_NG:
        filtered_df_NG = filtered_by_NG_df[filtered_by_NG_df['PneumaticDeviceType'] == pneumatic].set_index('FacilitySubtype')
        # this requires the same index
        flattened_NGPneu_list_df[pneumatic] = filtered_df_NG['AveragePneumaticCount']

    flattened_NGPneu_list_df = flattened_NGPneu_list_df.fillna(0)

    filtered_by_IA_df = datafile_component_df[datafile_component_df['Driver'] == 'Instrument Air']

    pneu_list_IA = filtered_by_IA_df['PneumaticDeviceType'].unique().tolist()
    facility_list_IA = filtered_by_IA_df['FacilitySubtype'].unique().tolist()

    flattened_IAPneu_list_df = pd.DataFrame(index= facility_list_IA)

    for pneumatic in pneu_list_IA:
        filtered_df_IA = filtered_by_IA_df[filtered_by_IA_df['PneumaticDeviceType'] == pneumatic].set_index('FacilitySubtype')
        # this requires the same index
        flattened_IAPneu_list_df[pneumatic] = filtered_df_IA['AveragePneumaticCount']

    flattened_IAPneu_list_df = flattened_IAPneu_list_df.fillna(0)

    return flattened_NGPneu_list_df, flattened_IAPneu_list_df
def componentEF():
    datafile_component_df = pd.read_csv(
        'C:/Users/jyuan/OneDrive - University of Calgary/PTAC/CE_methane_component_EF.csv')
    filterbygas_df = datafile_component_df[datafile_component_df['Sector'] == 'Gas'].set_index('Component Type')
    filterbyoil_df = datafile_component_df[datafile_component_df['Sector'] == 'Oil'].set_index('Component Type')

    return filterbygas_df, filterbyoil_df

if __name__ == '__main__':
    PG_components_df = PG_equip_to_component()
    LL_components_df = LL_equip_to_component()
    HL_components_df = HL_equip_to_component()
    print(HL_components_df)

