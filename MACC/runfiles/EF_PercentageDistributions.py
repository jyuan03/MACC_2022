import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from MACC.runfiles.EquipmentEmissionFactor import (facility_equipment_EF, facility_pneumatics_EF)
from MACC.runfiles.clearstone_data import (PG_equip_to_component)

def new_DF_percentages_calc_UDF(combined_gas_EF, combined_oil_EF):
    gas_perc_DF = pd.DataFrame()
    gas_perc_DF['Compressor-Recip'] = combined_gas_EF['Reciprocating Compressor'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['Compressor-Screw'] = combined_gas_EF['Screw Compressor'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['PneuLevelControl'] = combined_gas_EF['Level Controller'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['PneuPositioner'] = combined_gas_EF['Positioner'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['PneuPressureControl'] = combined_gas_EF['Pressure Controller'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['PneuTransducer'] = combined_gas_EF['Transducer'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['PneuPump'] = combined_gas_EF['Pump'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['GlycolDehy'] = combined_gas_EF['Glycol Dehydrator'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['PneuIntermittent'] = combined_gas_EF['Intermittent'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['ProdTank'] = combined_gas_EF['Production Tank (fixed roof -Light/Medium Oil)'] / combined_gas_EF['TotalEFs']
    gas_perc_DF['OtherEquip'] = 1 - gas_perc_DF[['Compressor-Recip', 'Compressor-Screw', 'PneuLevelControl', 'PneuPositioner',
                                                 'PneuPressureControl', 'PneuTransducer', 'PneuPump', 'GlycolDehy',
                                                 'ProdTank']].sum(axis=1)

    oil_perc_DF = pd.DataFrame()
    oil_perc_DF['Compressor-Recip'] = combined_oil_EF['Reciprocating Compressor'] / combined_oil_EF['TotalEFs']
    oil_perc_DF['Compressor-Screw'] = combined_oil_EF['Screw Compressor'] / combined_oil_EF['TotalEFs']
    oil_perc_DF['PneuLevelControl'] = combined_oil_EF['Level Controller'] / combined_oil_EF['TotalEFs']
    oil_perc_DF['PneuPositioner'] = combined_oil_EF['Positioner'] / combined_oil_EF['TotalEFs']
    oil_perc_DF['PneuPressureControl'] = combined_oil_EF['Pressure Controller'] / combined_oil_EF['TotalEFs']
    oil_perc_DF['PneuTransducer'] = combined_oil_EF['Transducer'] / combined_oil_EF['TotalEFs']
    oil_perc_DF['PneuPump'] = combined_oil_EF['Pump'] / combined_oil_EF['TotalEFs']
    oil_perc_DF['ProdTank'] = combined_oil_EF['Production Tank (fixed roof -Light/Medium Oil)'] / combined_oil_EF['TotalEFs']
    oil_perc_DF['PneuIntermittent'] = 0 #no intermittent devices for oil facilities. included for indexing purposes.
    oil_perc_DF['OtherEquip'] = 1 - oil_perc_DF[['Compressor-Recip', 'Compressor-Screw', 'PneuLevelControl', 'PneuPositioner',
                                                 'PneuPressureControl', 'PneuTransducer', 'PneuPump',
                                                 'ProdTank']].sum(axis=1)

    # test1 = combined_gas_EF['TotalEFs'] - combined_gas_EF['Reciprocating Compressor']  - combined_gas_EF['Screw Compressor'] - \
    #         combined_gas_EF['Level Controller'] - combined_gas_EF['Positioner'] - combined_gas_EF['Pressure Controller'] - \
    #         combined_gas_EF['Transducer'] - combined_gas_EF['Intermittent'] - gas_perc_DF['Pneucombined_gas_EF['Pump']- combined_gas_EF['Glycol Dehydrator'] - combined_gas_EF['Production Tank (fixed roof -Light/Medium Oil)']

    return gas_perc_DF, oil_perc_DF

def PercentageDistributions(gas_facility_EF, oil_facility_EF, oilandgas_pneumatics_EF, facility_data_by_subtype, GlycolDehydrator_AB_2022, GasPlants_AB_2022,CH4_density_STP, PG_equip_EF_summed):
    #centrifugal, reciprocal, glycol dehydrator, pneumatics, tanks, remaining EFs
    #Determine fraction of EF's from each source for all but gas multiwell batteries
    #Gas facilities: 351 SINGLE WELL, 361 GAS MULTIWELL GROUP, 362 GAS MULTIWELL EFFLUENT MEASUREMENT,
    #   363 GAS MULTIWELL PRORATION SE ALBERTA, 364 GAS MULTIWELL PRORATION OUTSIDE SE ALBERTA
    gas_facilities = ['351','361', '362', '363', '364']
    oil_facilities = ['311', '321', '322']

    #Calculate gas multiwell GD count per site
    GasMultiWell_GD_EquipCount = GlycolDehydrator_AB_2022-GasPlants_AB_2022 #number of GDs distributed across mutliwell gas batteries
    GasMultiWell_GD_FacilityCount = facility_data_by_subtype[facility_data_by_subtype['ReportingFacilitySubType'] == 361].count().iloc[1] #number of all facility subtypes
    Average_GD_EquipmentCount = GasMultiWell_GD_EquipCount/GasMultiWell_GD_FacilityCount
    GD_component_EF = PG_equip_EF_summed.loc['Dehydrator - Glycol']
    GD_Facility_EF = GD_component_EF * Average_GD_EquipmentCount/ CH4_density_STP #kgTHC/hr/source * m3/kg CH4

    #Combine all emission factors: Equipment EFs, Pneumatics EFs, GD EF's
    combined_gas_EF = gas_facility_EF.join(oilandgas_pneumatics_EF)
    combined_gas_EF['Glycol Dehydrator'] = 0
    #Set Gas Mutliwell GD to GD_Facility_EF
    combined_gas_EF.at[361, 'Glycol Dehydrator'] = GD_Facility_EF
    combined_gas_EF['TotalEFs'] = combined_gas_EF.sum(axis=1)

    combined_oil_EF = oil_facility_EF.join(oilandgas_pneumatics_EF)
    combined_oil_EF['TotalEFs'] = combined_oil_EF.sum(axis=1)

    gas_perc_DF, oil_perc_DF = new_DF_percentages_calc_UDF(combined_gas_EF, combined_oil_EF)

    return gas_perc_DF, oil_perc_DF

def equipment_methane_calculation_UDF(facility_data_by_subtype, gas_perc_DF, oil_perc_DF):
    gas_facility_subtypes = [351, 361, 362, 363, 364]
    oil_facility_subtypes = [311, 321, 322]
    facility_data_by_subtype_temp = pd.DataFrame()

    for gas_facilities in gas_facility_subtypes:
        facility_data_by_subtype_filtered = facility_data_by_subtype[facility_data_by_subtype['ReportingFacilitySubType'] == gas_facilities]
        facility_data_by_subtype_filtered['Vent_ReciCompressor'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities,'Compressor-Recip']
        facility_data_by_subtype_filtered['Vent_ScrewCompressor'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities,'Compressor-Screw']
        facility_data_by_subtype_filtered['PneuLevelControl'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities,'PneuLevelControl']
        facility_data_by_subtype_filtered['PneuPositioner'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities, 'PneuPositioner']
        facility_data_by_subtype_filtered['PneuPressureControl'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities, 'PneuPressureControl']
        facility_data_by_subtype_filtered['PneuTransducer'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities, 'PneuTransducer']
        facility_data_by_subtype_filtered['PneuIntermittent'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities,'PneuIntermittent']
        facility_data_by_subtype_filtered['PneuPump'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities, 'PneuPump']
        facility_data_by_subtype_filtered['GlycolDehy'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities, 'GlycolDehy']
        facility_data_by_subtype_filtered['ProdTank'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities, 'ProdTank']
        facility_data_by_subtype_filtered['OtherEquip'] = facility_data_by_subtype_filtered['ventvol'] * gas_perc_DF.at[gas_facilities, 'OtherEquip']
        facility_data_by_subtype_temp = pd.concat([facility_data_by_subtype_temp,facility_data_by_subtype_filtered])

    for oil_facilities in oil_facility_subtypes:
        facility_data_by_subtype_filtered = facility_data_by_subtype[facility_data_by_subtype['ReportingFacilitySubType'] == oil_facilities]
        facility_data_by_subtype_filtered['Vent_ReciCompressor'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities,'Compressor-Recip']
        facility_data_by_subtype_filtered['Vent_ScrewCompressor'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities,'Compressor-Screw']
        facility_data_by_subtype_filtered['PneuLevelControl'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities,'PneuLevelControl']
        facility_data_by_subtype_filtered['PneuPositioner'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities, 'PneuPositioner']
        facility_data_by_subtype_filtered['PneuPressureControl'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities, 'PneuPressureControl']
        facility_data_by_subtype_filtered['PneuTransducer'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities, 'PneuTransducer']
        facility_data_by_subtype_filtered['PneuIntermittent'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities,'PneuIntermittent']
        facility_data_by_subtype_filtered['PneuPump'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities, 'PneuPump']
        facility_data_by_subtype_filtered['GlycolDehy'] = 0
        facility_data_by_subtype_filtered['ProdTank'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities, 'ProdTank']
        facility_data_by_subtype_filtered['OtherEquip'] = facility_data_by_subtype_filtered['ventvol'] * oil_perc_DF.at[oil_facilities, 'OtherEquip']
        facility_data_by_subtype_temp = pd.concat([facility_data_by_subtype_temp, facility_data_by_subtype_filtered])

    return facility_data_by_subtype_temp

if __name__ == '__main__':
    # ----------INPUT PARAMETERS-----------
    GasMoleDensity = 23.644  # m3/kmol
    CH4_MW = 16.04  # kg/kmol
    CH4_density_STP = CH4_MW / GasMoleDensity  # kg/m3 methane
    GlycolDehydrator_AB_2022 = 1300
    GasPlants_AB_2022 = 500

    facility_subtype_data_path = "../2022v10_oilgasfacilityvol.csv"
    facility_data_by_subtype = pd.read_csv(facility_subtype_data_path)

    # Equipment, GD, and Pneumatics Emission Factors
    gas_facility_EF, oil_facility_EF, GD_AB_2022, PG_equip_EF_summed = facility_equipment_EF(GlycolDehydrator_AB_2022)

    # Unit conversion to m3/hr per source EFs
    gas_facility_EF_m3hr = gas_facility_EF / CH4_density_STP  # kgTHC/hr/source * m3/kg CH4
    oil_facility_EF_m3hr = oil_facility_EF / CH4_density_STP  # kgTHC/hr/source * m3/kg CH4
    GD_AB_2022_m3hr = GD_AB_2022 / CH4_density_STP  # kgTHC/hr/source * m3/kg CH4
    oilandgas_pneumatics_EF_m3hr = facility_pneumatics_EF()  # m3/hr/source

    gas_perc_DF, oil_perc_DF = PercentageDistributions(gas_facility_EF_m3hr, oil_facility_EF_m3hr, oilandgas_pneumatics_EF_m3hr,
                            facility_data_by_subtype, GlycolDehydrator_AB_2022, GasPlants_AB_2022, CH4_density_STP, PG_equip_EF_summed)