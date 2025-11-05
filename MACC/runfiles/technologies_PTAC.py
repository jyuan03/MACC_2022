import pandas as pd
import numpy as np

from MACC.runfiles.case_study_cost_calculations import casestudycostcals
from MACC.runfiles.equipment_feasibility_count import equip_feasibilityandcount
from MACC.runfiles.technology_economics_runs import tech_econ_runs

def co2efiltering(row):
    try:
        return row[row['Lowest CO2e abatement cost option']]
    except:
        return np.nan
def ch4filtering(row):
    try:
        return row[row['Lowest CH4 abatement cost option']]
    except:
        return np.nan

def lowestcosttechnologyCAPEX_udf(row):

    if row['Lowest CO2e abatement cost option'] == 'VRUFlareGrid_MACCCO2e':
        CAPEX = row['VRU_CAPEX'] + row['GridConnect_CAPEX'] + row['Flare_notcasing_CAPEX'] * row['FlareCountRounded']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'VRUFlareGen_MACCCO2e':
        CAPEX = row['VRU_CAPEX'] + row['Generator_CAPEX'] + row['Flare_notcasing_CAPEX'] * row['FlareCountRounded']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'VRUTieInGrid_MACCCO2e':
        CAPEX = row['VRU_CAPEX'] + row['GridConnect_CAPEX'] + row['TieIn_CAPEX']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'VRUTieInGen_MACCCO2e':
        CAPEX = row['VRU_CAPEX'] + row['Generator_CAPEX'] + row['TieIn_CAPEX']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'Casinggasflare_MACCCO2e':
        CAPEX = row['casinggas_flare_CAPEX'] * row['FlareCountRounded']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'Casinggastiein_MACCCO2e':
        CAPEX = row['casinggas_tiein_CAPEX']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGrid_MACCCO2e':
        CAPEX = row['VRU_CAPEX'] + row['GridConnect_CAPEX'] + row['Vapcombustor_CAPEX'] * row['VapCombRounded']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGen_MACCCO2e':
        CAPEX = row['VRU_CAPEX'] + row['Generator_CAPEX'] + row['Vapcombustor_CAPEX'] * row['VapCombRounded']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGen_MACCCO2e':
        CAPEX = row['VRU_CAPEX'] + row['Generator_CAPEX'] + row['Vapcombustor_CAPEX'] * row['VapCombRounded']
        return CAPEX
    if row['Lowest CO2e abatement cost option'] == 'Gasbladdertruck_MACCCO2e':
        CAPEX = row['VRU_CAPEX'] + row['Generator_CAPEX'] + row['Vapcombustor_CAPEX'] * row['VapCombRounded']
        return CAPEX

def volumereduction_udf(row,CH4GWPconstants,ch4density):
    if row['Lowest CO2e abatement cost option'] == 'VRUTieInGrid_MACCCO2e':
        ventrate = row['ventvol'] #e3m3/d
        ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # # e3m3/d * %reduced *gCO2e/gCh4 * kgch4/e3m3 *t/1000kg =tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 /3600 * (590/ (10**6)) #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
        netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGrid_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.95*0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                10 ** 6))  # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
        netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGen_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.95* 0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 1.15 * 24 * 0.000453592  # hp * lbCO2/hp hr *24hr/d *tonne/lb = tCO2e/d
        netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'Casinggasflare_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * 0.95 * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d = tCO2/d
        netabatement = (ventabatement - emissionsfromtech) * 365  # tCO2e/y
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'Casinggastiein_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        netabatement = (ventabatement)*365 #tCO2e/y
        return netabatement

def technologies(facilitydata_df, CH4GWPconstants, gasprice, discountrate, ch4density_kgm3):
    ch4density = ch4density_kgm3*1000 #kg/e3m3

    techdetailspath = "./technologydetails.csv"
    techdetails_df = pd.read_csv(techdetailspath)
    techdetails_df = techdetails_df.set_index('technologies')

    facility_econ_data_df = tech_econ_runs(facilitydata_df, techdetails_df)
    feasbilitycheck_facility_econ_data_df = equip_feasibilityandcount(facility_econ_data_df, techdetails_df)
    techcasestudycosts = casestudycostcals(feasbilitycheck_facility_econ_data_df, techdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density)

    co2eonlytechnologies_df = techcasestudycosts.iloc[:,90:99]
    co2eonlytechnologies_df['Lowest CO2e abatement cost option'] = co2eonlytechnologies_df.idxmin(axis="columns")
    co2eonlytechnologies_df['Lowest CO2e abatement cost value'] = co2eonlytechnologies_df.apply(co2efiltering, axis=1)
    lasttwocolumns = co2eonlytechnologies_df[['Lowest CO2e abatement cost option','Lowest CO2e abatement cost value']]
    techcasestudycosts = techcasestudycosts.join(lasttwocolumns)
    techcasestudycosts['Lowest Cost Technology CAPEX'] = techcasestudycosts.apply(lowestcosttechnologyCAPEX_udf, axis=1)

    filter_results_df = techcasestudycosts[
        ['ReportingFacilityID', 'PROD_gas', 'PROD_oil', 'VENT_gas', 'ventvol', 'Flare?', 'Tie in?', 'VRU_size', 'VRU_hp',
         'VRU_feasible min?', 'Flare_feasible min?', 'CasingFlare_feasible min?', 'CasingGasTieIn high feasible max?',
         'CasingGasTieIn low feasible max?']]
    filter_results_df = filter_results_df.join(co2eonlytechnologies_df)

    ch4eonlytechnologies_df = techcasestudycosts.iloc[:,100:108]
    ch4eonlytechnologies_df['Lowest CH4 abatement cost option'] = ch4eonlytechnologies_df.idxmin(axis="columns")
    ch4eonlytechnologies_df['Lowest CH4 abatement cost value'] = ch4eonlytechnologies_df.apply(ch4filtering, axis=1)
    lasttwocolumns = ch4eonlytechnologies_df[['Lowest CH4 abatement cost option','Lowest CH4 abatement cost value']]
    techcasestudycosts = techcasestudycosts.join(lasttwocolumns)

    filter_results_df = filter_results_df.join(ch4eonlytechnologies_df)

    filter_results_df['volumereductionstCO2e/y'] = filter_results_df.apply(volumereduction_udf, args=(CH4GWPconstants,ch4density),axis=1)
    filter_results_df = filter_results_df[filter_results_df['ventvol']>0]
    filter_results_df = filter_results_df.sort_values('Lowest CO2e abatement cost value')
    filter_results_df['range'] = pd.cut(filter_results_df['Lowest CO2e abatement cost value'],
                                        [-10, 0, 10, 20, 30, 50, 100, 200, 300, 400, 500, 1000, 9000],
                                        include_lowest=True)
    sum_cost_ranges = filter_results_df.groupby(['Lowest CO2e abatement cost option', 'range'], as_index=False).sum()
    average_cost_ranges = filter_results_df.groupby(['Lowest CO2e abatement cost option', 'range'], as_index=False).mean()

    techcasestudycosts.to_csv('econdatav3_nocarb_filtered2022_alberta_methanetechcostNPV.csv')
    filter_results_df.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v2.csv')
    sum_cost_ranges.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v2_sumrange.csv')
    average_cost_ranges.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v2_averagerange.csv')
    print(feasbilitycheck_facility_econ_data_df)


if __name__ == '__main__':
    techdetailspath = "./technologydetails.csv"
    techdetails_df = pd.read_csv(techdetailspath)
    techdetails_df = techdetails_df.set_index('technologies')

    #now using file v10 with oil and gas facilities specifically
    facilitydatapath = "./2022v10_oilgasfacilityvol.csv"
    facilitydata_df = pd.read_csv(facilitydatapath)

    CH4GWPconstants = 28 #co2e/ch4
    gasprice = 3.55 * 39 # $CAD/GJ * GJ/e3MJ * 39e3MJ/e3m3 = $CAD/e3m3
    discountrate = 0.1
    ch4density = 687 #kg/e3m3

    facility_econ_data_df = tech_econ_runs(facilitydata_df, techdetails_df)
    feasbilitycheck_facility_econ_data_df = equip_feasibilityandcount(facility_econ_data_df, techdetails_df)
    techcasestudycosts = casestudycostcals(feasbilitycheck_facility_econ_data_df, techdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density)
    # techcasestudycosts.to_csv('econdatav3_nocarb_filtered2022_alberta_methanetechcostNPV.csv')


    # techcasestudycosts['techselection'] = techcasestudycosts.apply(identifytech, axis=1)
    # techcasestudycosts['Lowest cost'] = techcasestudycosts.apply(identifytech, axis=1)
    # # techcasestudycosts.to_csv('2022_alberta_methanetechcostNPV.csv')
    # filter_results_df = techcasestudycosts[x`
    #     ['ReportingFacilityID', 'PROD_gas', 'PROD_oil', 'VENT_gas', 'ventvol', 'Flare?', 'Tie in?', 'VRU_size',
    #      'VRU_feasible min?', 'Flare_feasible min?', 'CasingFlare_feasible min?', 'CasingGasTieIn high feasible max?',
    #      'CasingGasTieIn low feasible max?', 'VRUFlareGrid_MACCCO2e', 'VRUFlareGen_MACCCO2e', 'VRUTieInGrid_MACCCO2e',
    #      'VRUTieInGen_MACCCO2e', 'VRUVapcombGrid_MACCCO2e', 'VRUVapcombGen_MACCCO2e', 'Casinggasflare_MACCCO2e',
    #      'Casinggastiein_MACCCO2e', 'Gasbladdertruck_MACCCO2e']]
    # techcasestudycosts.to_csv('2022v5_oilgasfacilityvol.csv')


    co2eonlytechnologies_df = techcasestudycosts.iloc[:,90:99]
    co2eonlytechnologies_df['Lowest CO2e abatement cost option'] = co2eonlytechnologies_df.idxmin(axis="columns")
    co2eonlytechnologies_df['Lowest CO2e abatement cost value'] = co2eonlytechnologies_df.apply(co2efiltering, axis=1)
    lasttwocolumns = co2eonlytechnologies_df[['Lowest CO2e abatement cost option','Lowest CO2e abatement cost value']]
    techcasestudycosts = techcasestudycosts.join(lasttwocolumns)
    techcasestudycosts['Lowest Cost Technology CAPEX'] = techcasestudycosts.apply(lowestcosttechnologyCAPEX_udf, axis=1)

    filter_results_df = techcasestudycosts[
        ['ReportingFacilityID', 'PROD_gas', 'PROD_oil', 'VENT_gas', 'ventvol', 'Flare?', 'Tie in?', 'VRU_size', 'VRU_hp',
         'VRU_feasible min?', 'Flare_feasible min?', 'CasingFlare_feasible min?', 'CasingGasTieIn high feasible max?',
         'CasingGasTieIn low feasible max?']]
    filter_results_df = filter_results_df.join(co2eonlytechnologies_df)

    ch4eonlytechnologies_df = techcasestudycosts.iloc[:,100:108]
    ch4eonlytechnologies_df['Lowest CH4 abatement cost option'] = ch4eonlytechnologies_df.idxmin(axis="columns")
    ch4eonlytechnologies_df['Lowest CH4 abatement cost value'] = ch4eonlytechnologies_df.apply(ch4filtering, axis=1)
    lasttwocolumns = ch4eonlytechnologies_df[['Lowest CH4 abatement cost option','Lowest CH4 abatement cost value']]
    techcasestudycosts = techcasestudycosts.join(lasttwocolumns)

    filter_results_df = filter_results_df.join(ch4eonlytechnologies_df)

    filter_results_df['volumereductionstCO2e/y'] = filter_results_df.apply(volumereduction_udf, args=(CH4GWPconstants,ch4density),axis=1)
    filter_results_df = filter_results_df[filter_results_df['ventvol']>0]
    filter_results_df = filter_results_df.sort_values('Lowest CO2e abatement cost value')
    filter_results_df['range'] = pd.cut(filter_results_df['Lowest CO2e abatement cost value'],
                                        [-10, 0, 10, 20, 30, 50, 100, 200, 300, 400, 500, 1000, 9000],
                                        include_lowest=True)
    sum_cost_ranges = filter_results_df.groupby(['Lowest CO2e abatement cost option', 'range'], as_index=False).sum()
    average_cost_ranges = filter_results_df.groupby(['Lowest CO2e abatement cost option', 'range'], as_index=False).mean()

    techcasestudycosts.to_csv('econdatav3_nocarb_filtered2022_alberta_methanetechcostNPV.csv')
    filter_results_df.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v2.csv')
    sum_cost_ranges.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v2_sumrange.csv')
    average_cost_ranges.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v2_averagerange.csv')
    print(feasbilitycheck_facility_econ_data_df)
