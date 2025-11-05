import pandas as pd
import numpy as np

from MACC.runfiles.case_study_cost_calculations import (casestudycostcals, auxequip_casestudycostcals)
from MACC.runfiles.equipment_feasibility_count import (equip_feasibilityandcount, auxequip_feasibilityandcount)
from MACC.runfiles.technology_economics_runs import (tech_econ_runs, auxequip_tech_econ_runs)

def sitewideoption(row):
    try:
        return row[row['LowestSiteWide_type']]
    except:
        return np.nan

def sitewideoption_abatement(row):
    try:
        if row['HighestSiteWideabatement_volreductions_type'] == 'PneuGDvent':
            if row['GlycolDehy'] != 0:
                abatement_cost = row['pneu_components_MACCCO2e'] + row['GD_VentMACCCO2e']
            else:
                abatement_cost = row['pneu_components_MACCCO2e']
            return abatement_cost

        elif row['HighestSiteWideabatement_volreductions_type'] == 'PneuGDflare':
            if row['GlycolDehy'] != 0:
                abatement_cost = row['pneu_components_MACCCO2e'] + row['GD_FlareMACCCO2e']
            else:
                abatement_cost = row['pneu_components_MACCCO2e']
            return abatement_cost
        else:
            abatement_type_string = row['HighestSiteWideabatement_volreductions_type']
            abatement_cost_string = abatement_type_string+"_MACCCO2e"
            return row[abatement_cost_string]

    except:
        return np.nan

def co2efiltering(row):
    try:
        return row[row['Lowest CO2e abatement cost option sepvssite']]
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

# def volumereduction_udf(row,CH4GWPconstants,ch4density):
#     if row['Lowest CO2e abatement cost option'] == 'LowestSiteWideOption':
#         if row['LowestSiteWide_type'] == 'VRUTieInGrid_MACCCO2e':
#             ventrate = row['ventvol'] #e3m3/d
#             ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # # e3m3/d * %reduced *gCO2e/gCh4 * kgch4/e3m3 *t/1000kg =tCO2e/d
#             emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 /3600 * (590/ (10**6)) #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
#             netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
#             return netabatement
#
#         if row['LowestSiteWide_type'] == 'VRUVapcombGrid_MACCCO2e':
#             ventrate = row['ventvol']
#             ventabatement = ventrate * 0.95*0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#             emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
#                     10 ** 6))  # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
#             netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
#             return netabatement
#
#         if row['LowestSiteWide_type'] == 'VRUVapcombGen_MACCCO2e':
#             ventrate = row['ventvol']
#             ventabatement = ventrate * 0.95* 0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#             emissionsfromtech = row['VRU_hp'] * 1.15 * 24 * 0.000453592  # hp * lbCO2/hp hr *24hr/d *tonne/lb = tCO2e/d
#             netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
#             return netabatement
#
#         if row['LowestSiteWide_type'] == 'Casinggasflare_MACCCO2e':
#             ventrate = row['ventvol']
#             percentreduction=  0.95
#             ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#             emissionsfromtech = row[
#                                     'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d = tCO2/d
#             netabatement = (ventabatement - emissionsfromtech) * 365  # tCO2e/y
#             return netabatement
#
#         if row['LowestSiteWide_type'] == 'Casinggastiein_MACCCO2e':
#             ventrate = row['ventvol']
#             ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#             netabatement = (ventabatement)*365 #tCO2e/y
#             return netabatement
#
#     if row['Lowest CO2e abatement cost option'] == 'LowestSeparateEquipCostOption':
#         if row['LowestCostPneumatic'] == 'Elec_MACCCO2e':
#             percentreduction_pneu = 1
#             ventrate_pneu = row['allpneuvents']  # e3m3/d
#             ventabatement_pneu = ventrate_pneu * percentreduction_pneu * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#             emissionsfromtech = 0
#             netabatement_pneu = ventabatement_pneu - emissionsfromtech
#
#         elif row['LowestCostPneumatic'] == 'IA_MACCCO2e':
#             percentreduction_pneu = 1
#             ventrate_pneu = row['allpneuvents']  # e3m3/d
#             ventabatement_pneu = ventrate_pneu * percentreduction_pneu * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#             emissionsfromtech = 0
#             netabatement_pneu = ventabatement_pneu - emissionsfromtech
#
#         elif row['LowestCostPneumatic'] == 'pneu_components_MACCCO2e':
#             percentreduction_pneu = 1
#             ventrate_pneu = row[['PneuPump', 'PneuTransducer', 'PneuLevelControl', 'PneuPositioner' ]].sum()  # e3m3/d
#             ventabatement_pneu = ventrate_pneu * percentreduction_pneu * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#             emissionsfromtech = 0
#             netabatement_pneu = ventabatement_pneu - emissionsfromtech
#
#         if row['GlycolDehy'] !=0:
#             if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
#                 percentreduction = 1
#                 ventrate = row['GlycolDehy']  # e3m3/d
#                 ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#                 emissionsfromtech = ventrate * percentreduction * ch4density * 44.01 / 16.04 / 1000  # tCO2/d emissions from combustion
#                 netabatement_GD = (ventabatement-emissionsfromtech) * 365  # tCO2e/y
#
#             elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
#                 percentreduction = 1
#                 ventrate = row['GlycolDehy']  # e3m3/d
#                 ventabatement = 0
#                 emissionsfromtech = 0
#                 netabatement_GD = (ventabatement-emissionsfromtech) * 365  # tCO2e/y
#         else:
#             netabatement_GD = 0
#         if row['Vent_ReciCompressor'] != 0:
#             percentreduction_recicomp = 1
#             ventrate_recicomp = row['Vent_ReciCompressor']
#             ventabatement_recicomp = ventrate_recicomp * percentreduction_recicomp * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#         else:
#             ventabatement_recicomp = 0
#         if row['Vent_ScrewCompressor'] != 0:
#             percentreduction_screwcomp = 1
#             ventrate_screwcomp = row['Vent_ScrewCompressor']
#             ventabatement_screwcomp = ventrate_screwcomp * percentreduction_screwcomp * CH4GWPconstants * ch4density / 1000  # tCO2e/d
#         else:
#             ventabatement_screwcomp = 0
#
#         netabatement = netabatement_GD + netabatement_pneu + ventabatement_recicomp + ventabatement_screwcomp
#     else:
#         netabatement = np.nan
#
#     return netabatement

def site_technologies(facilitydata_df, CH4GWPconstants, gasprice, discountrate, ch4density_kgm3):
    ch4density = ch4density_kgm3*1000 #kg/e3m3

    techdetailspath = "./data/technologydetails.csv"
    techdetails_df = pd.read_csv(techdetailspath)
    techdetails_df = techdetails_df.set_index(['technologies'])

    facility_econ_data_df = tech_econ_runs(facilitydata_df, techdetails_df)
    feasbilitycheck_facility_econ_data_df = equip_feasibilityandcount(facility_econ_data_df, techdetails_df)
    techcasestudycosts = casestudycostcals(feasbilitycheck_facility_econ_data_df, techdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density)

    return techcasestudycosts

def volumereduction_udf(row,CH4GWPconstants,ch4density):
    if row['Lowest CO2e abatement cost option'] == 'VRUTieInGrid_MACCCO2e':
        ventrate = row['ventvol'] #e3m3/d
        ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # # e3m3/d * %reduced *gCO2e/gCh4 * kgch4/e3m3 *t/1000kg =tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 /3600 * (590/ (10**6)) #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
        netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'VRUTieInGen_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # # e3m3/d * %reduced *gCO2e/gCh4 * kgch4/e3m3 *t/1000kg =tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 1.15 * 24 * 0.000453592  # hp * lbCO2/hp hr *24hr/d *tonne/lb = tCO2e/d
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
        percentreduction=  0.95
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d = tCO2/d
        netabatement = (ventabatement - emissionsfromtech) * 365  # tCO2e/y
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'Casinggastiein_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        netabatement = (ventabatement)*365 #tCO2e/y
        return netabatement

    else:
        if row['LowestCostPneumatic'] == 'Elec_MACCCO2e':
            percentreduction_pneu = 1
            ventrate_pneu = row['allpneuvents']  # e3m3/d
            ventabatement_pneu = ventrate_pneu * percentreduction_pneu * CH4GWPconstants * ch4density / 1000  # tCO2e/d
            emissionsfromtech = 0
            netabatement_pneu = (ventabatement_pneu - emissionsfromtech)* 365

        elif row['LowestCostPneumatic'] == 'IA_MACCCO2e':
            percentreduction_pneu = 1
            ventrate_pneu = row['allpneuvents']  # e3m3/d
            ventabatement_pneu = ventrate_pneu * percentreduction_pneu * CH4GWPconstants * ch4density / 1000  # tCO2e/d
            emissionsfromtech = 0
            netabatement_pneu = (ventabatement_pneu - emissionsfromtech)* 365

        elif row['LowestCostPneumatic'] == 'pneu_components_MACCCO2e':
            percentreduction_pneu = 1
            ventrate_pneu = row[['PneuPump', 'PneuTransducer', 'PneuLevelControl', 'PneuPositioner' ]].sum()  # e3m3/d
            ventabatement_pneu = ventrate_pneu * percentreduction_pneu * CH4GWPconstants * ch4density / 1000  # tCO2e/d
            emissionsfromtech = 0
            netabatement_pneu = (ventabatement_pneu - emissionsfromtech)* 365

        if row['GlycolDehy'] !=0:
            if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
                percentreduction = 1
                ventrate = row['GlycolDehy']  # e3m3/d
                ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
                emissionsfromtech = ventrate * percentreduction * ch4density * 44.01 / 16.04 / 1000  # tCO2/d emissions from combustion
                netabatement_GD = (ventabatement-emissionsfromtech) * 365  # tCO2e/y

            elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
                percentreduction = 1
                ventrate = row['GlycolDehy']  # e3m3/d
                ventabatement = 0
                emissionsfromtech = 0
                netabatement_GD = (ventabatement-emissionsfromtech) * 365  # tCO2e/y
        else:
            netabatement_GD = 0

        if row['Vent_ReciCompressor'] != 0:
            percentreduction_recicomp = 1
            ventrate_recicomp = row['Vent_ReciCompressor']
            ventabatement_recicomp = (ventrate_recicomp * percentreduction_recicomp * CH4GWPconstants * ch4density / 1000 )* 365 # tCO2e/y
        else:
            ventabatement_recicomp = 0

        if row['Vent_ScrewCompressor'] != 0:
            percentreduction_screwcomp = 1
            ventrate_screwcomp = row['Vent_ScrewCompressor']
            ventabatement_screwcomp = (ventrate_screwcomp * percentreduction_screwcomp * CH4GWPconstants * ch4density / 1000)* 365  # tCO2e/y
        else:
            ventabatement_screwcomp = 0

        netabatement = netabatement_GD + netabatement_pneu + ventabatement_recicomp + ventabatement_screwcomp
        return netabatement

def discountedvolumereduction_udf(row,CH4GWPconstants,ch4density):
    if row['Lowest CO2e abatement cost option'] == 'VRUTieInGrid_MACCCO2e':
        netabatement = row['VRUTieInGrid_co2enpvCAD']
        return netabatement
    if row['Lowest CO2e abatement cost option'] == 'VRUTieInGen_MACCCO2e':
        netabatement = row['VRUTieInGen_co2enpvCAD']
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGrid_MACCCO2e':
        netabatement = row['VRUVapcombGrid_co2enpvCAD']
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGen_MACCCO2e':
        netabatement = row['VRUVapcombGen_co2enpvCAD']
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'Casinggasflare_MACCCO2e':
        netabatement = row['Casinggasflare_co2enpvCAD']
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'Casinggastiein_MACCCO2e':
        netabatement = row['Casinggastiein_co2enpvCAD']
        return netabatement

    else:
        if row['LowestCostPneumatic'] == 'Elec_MACCCO2e':
            netabatement_pneu = row['Elec_co2enpvCAD']

        elif row['LowestCostPneumatic'] == 'IA_MACCCO2e':
            netabatement_pneu = row['IA_co2enpvCAD']

        elif row['LowestCostPneumatic'] == 'pneu_components_MACCCO2e':
            netabatement_pneu = row[['PneuPump_co2enpvCAD', 'PneuTransducer_co2enpvCAD', 'PneuLevelControl_co2enpvCAD', 'PneuPositioner_co2enpvCAD' ]].sum()

        if row['GlycolDehy'] !=0:
            if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
                netabatement_GD = row['GDFlare_co2enpvCAD']

            elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
                netabatement_GD = row['GDVent_co2enpvCAD']
        else:
            netabatement_GD = 0

        if row['Vent_ReciCompressor'] != 0:
            ventabatement_recicomp = row['ReciComp_co2enpvCAD']
        else:
            ventabatement_recicomp = 0

        if row['Vent_ScrewCompressor'] != 0:
            ventabatement_screwcomp = row['ScrewComp_co2enpvCAD']
        else:
            ventabatement_screwcomp = 0

        netabatement = netabatement_GD + netabatement_pneu + ventabatement_recicomp + ventabatement_screwcomp
        return netabatement



def equip_technologies(facilitydata_df, CH4GWPconstants, gasprice, discountrate, ch4density_kgm3):
    ch4density = ch4density_kgm3*1000 #kg/e3m3

    techdetailspath = "./data/technologydetails_equip.csv"
    techdetails_df = pd.read_csv(techdetailspath)
    techdetails_df = techdetails_df.set_index(['technologies', 'Range'])

    facilitydata_econ_df = auxequip_tech_econ_runs(facilitydata_df, techdetails_df)
    feasbilitycheck_facility_econ_data_df = auxequip_feasibilityandcount(facilitydata_econ_df, techdetails_df)
    techcasestudycosts = auxequip_casestudycostcals(feasbilitycheck_facility_econ_data_df, techdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density)

    return techcasestudycosts

def LowestCostPneumaticOption_udf(row):
    pneumatic_technologies_df = row[['IA_MACCCO2e', 'Elec_MACCCO2e', 'pneu_components_MACCCO2e']]
    pneumatic_technologies_df = pd.to_numeric(pneumatic_technologies_df)
    pneumatic_technologies_df['LowestCostPneumaticOption'] = pneumatic_technologies_df.idxmin(axis="row")
    return row[pneumatic_technologies_df['LowestCostPneumaticOption']]

def LowestCostPneumatic_type(row):
    lowestcost = row['LowestCostPneumatic']
    if lowestcost == 'IA_MACCCO2e':
        return 'IA'
    elif lowestcost == 'Elec_MACCCO2e':
        return 'Elec'
    else:
        return 'pneu_components'

def LowestCostGD_udf(row):
    GD_technologies_df = row['GD_FlareMACCCO2e', 'GD_VentMACCCO2e']
    GD_technologies_df['LowestCostGD'] = GD_technologies_df.idxmin(axis="columns")
    return row[GD_technologies_df['LowestCostGD']]

def LowestCostGD_type(row):
    lowestcost = row['LowestCostGD']
    if lowestcost == 'GD_FlareMACCCO2e':
        return 'GD Flare'
    else:
        return 'GD Vent'

def lowest_sep_equip_option(row, pneu_tech, GD_status, GD_lowestcost, Reci_status, Screw_status):
    if GD_status != 0:
        if Reci_status != 0:
            if GD_lowestcost == 'GD_FlareMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDFlare_npvCAD', 'ReciComp_npvCAD']
                LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()

            elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDVent_npvCAD', 'ReciComp_npvCAD']
                LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
        if Screw_status != 0:
            if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDFlare_npvCAD', 'ScrewComp_npvCAD']
                LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
            elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDVent_npvCAD', 'ScrewComp_npvCAD']
                LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
        elif (Reci_status==0 and Screw_status==0):
            if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDFlare_npvCAD']
                LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
            elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDVent_npvCAD']
                LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
    else:
        if Reci_status != 0:
            case_tech_list_nvp = [pneu_tech, 'ReciComp_npvCAD']
            LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
        if Screw_status != 0:
            case_tech_list_nvp = [pneu_tech, 'ScrewComp_npvCAD']
            LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
        elif (Reci_status==0 and Screw_status==0):
            LowestSeparateEquipOption_nvp = np.nan
    return LowestSeparateEquipOption_nvp

def LowestSepEquipCost_npv(row):
    GD_status = row['GlycolDehy']
    GD_lowestcost = row['LowestCostGD']
    Reci_status = row['Vent_ReciCompressor']
    Screw_status = row['Vent_ScrewCompressor']

    if row['LowestCostPneumatic'] == 'IA_MACCCO2e':
        pneu_tech = 'IA_npvCAD'
        lowest_sep_nvp = lowest_sep_equip_option(row, pneu_tech, GD_status,GD_lowestcost, Reci_status, Screw_status)

    elif row['LowestCostPneumatic'] == 'Elec_MACCCO2e':
        pneu_tech = 'Elec_npvCAD'
        lowest_sep_nvp = lowest_sep_equip_option(row, pneu_tech, GD_status,GD_lowestcost, Reci_status, Screw_status)

    else:
        pneu_tech = 'pneu_components_npv'
        lowest_sep_nvp = lowest_sep_equip_option(row, pneu_tech, GD_status, GD_lowestcost, Reci_status, Screw_status)

    return lowest_sep_nvp
        # if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
        #     case_tech_list_nvp = ['Elec_npvCAD', 'GDFlare_npvCAD', 'ReciComp_npvCAD', 'ScrewComp_npvCAD']
        #     LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
        #     return LowestSeparateEquipOption_nvp
        #
        # elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
        #     case_tech_list_nvp = ['Elec_npvCAD', 'GDVent_npvCAD', 'ReciComp_npvCAD', 'ScrewComp_npvCAD']
        #     LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
        #     return LowestSeparateEquipOption_nvp
        #
        # if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
        #     case_tech_list_nvp = ['pneu_components_npv', 'GDFlare_npvCAD', 'ReciComp_npvCAD', 'ScrewComp_npvCAD']
        #     LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
        #     return LowestSeparateEquipOption_nvp
        #
        # elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
        #     case_tech_list_nvp = ['pneu_components_npv', 'GDVent_npvCAD', 'ReciComp_npvCAD', 'ScrewComp_npvCAD']
        #     LowestSeparateEquipOption_nvp = row[case_tech_list_nvp].sum()
        #     return LowestSeparateEquipOption_nvp

def lowest_sep_equip_option_co2enpv(row, pneu_tech, GD_status, GD_lowestcost, Reci_status, Screw_status):
    if GD_status != 0:
        if Reci_status != 0:
            if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDFlare_co2enpvCAD', 'ReciComp_co2enpvCAD']
                LowestSeparateEquipOption_co2envp = row[case_tech_list_nvp].sum()

            elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDVent_co2enpvCAD', 'ReciComp_co2enpvCAD']
                LowestSeparateEquipOption_co2envp = row[case_tech_list_nvp].sum()
        if Screw_status != 0:
            if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDFlare_co2enpvCAD', 'ScrewComp_co2enpvCAD']
                LowestSeparateEquipOption_co2envp = row[case_tech_list_nvp].sum()

            elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDVent_co2enpvCAD', 'ScrewComp_co2enpvCAD']
                LowestSeparateEquipOption_co2envp = row[case_tech_list_nvp].sum()
        elif (Reci_status==0 and Screw_status==0):
            if row['LowestCostGD'] == 'GD_FlareMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDFlare_co2enpvCAD']
                LowestSeparateEquipOption_co2envp = row[case_tech_list_nvp].sum()

            elif row['LowestCostGD'] == 'GD_VentMACCCO2e':
                case_tech_list_nvp = [pneu_tech, 'GDVent_co2enpvCAD']
                LowestSeparateEquipOption_co2envp = row[case_tech_list_nvp].sum()
    else:
        if Reci_status != 0:
            case_tech_list_nvp = [pneu_tech, 'ReciComp_co2enpvCAD']
            LowestSeparateEquipOption_co2envp = row[case_tech_list_nvp].sum()

        if Screw_status != 0:
            case_tech_list_nvp = [pneu_tech, 'ScrewComp_co2enpvCAD']
            LowestSeparateEquipOption_co2envp = row[case_tech_list_nvp].sum()
        elif (Reci_status == 0 and Screw_status == 0):
            LowestSeparateEquipOption_co2envp = np.nan

    return LowestSeparateEquipOption_co2envp

def LowestSepEquipCost_co2enpv(row):
    GD_status = row['GlycolDehy']
    GD_lowestcost = row['LowestCostGD']
    Reci_status = row['Vent_ReciCompressor']
    Screw_status = row['Vent_ScrewCompressor']

    if row['LowestCostPneumatic'] == 'IA_MACCCO2e':
        pneu_tech = 'IA_co2enpvCAD'
        LowestSepEquipCost_co2enpv = lowest_sep_equip_option_co2enpv(row, pneu_tech, GD_status,GD_lowestcost, Reci_status, Screw_status)

    elif row['LowestCostPneumatic'] == 'Elec_MACCCO2e':
        pneu_tech = 'Elec_co2enpvCAD'
        LowestSepEquipCost_co2enpv = lowest_sep_equip_option(row, pneu_tech, GD_status,GD_lowestcost, Reci_status, Screw_status)

    else:
        pneu_tech = 'pneu_components_co2enpv'
        LowestSepEquipCost_co2enpv = lowest_sep_equip_option(row, pneu_tech, GD_status, GD_lowestcost, Reci_status, Screw_status)

    return LowestSepEquipCost_co2enpv

def checking_compressor_GD_UDF(row):
    if row['LowestCostPneumatic'] == 'IA_MACCCO2e':
        pneu_tech = 'IA'
    elif row['LowestCostPneumatic'] == 'Elec_MACCCO2e':
        pneu_tech = 'Elec'
    else:
        pneu_tech = 'pneu'
    if row['GlycolDehy'] != 0:
        if row['LowestCostGD'] == 'GD_VentMACCCO2e':
            GD = 'GDVent'
        elif row['LowestCostGD'] == 'GD_FlareMACCCO2e':
            GD = 'GDFlare'
    else:
        GD = ''
    if row['Vent_ReciCompressor']!= 0:
        comp = 'Reci'
    elif row['Vent_ScrewCompressor'] != 0:
        comp = 'Screw'
    else:
        comp = ''
    lowestsepoption = pneu_tech+GD+comp
    return lowestsepoption

def separate_tech_options(row):
    if row['GlycolDehy'] !=0:
        if row['Vent_ReciCompressor']!= 0:
            sep_equip_option = row['LowestCostGD_type'] + row['LowestCostPneumatic_type'] + 'Reci_comp'
            return sep_equip_option
        elif row['Vent_ScrewCompressor']!= 0:
            sep_equip_option = row['LowestCostGD_type'] + row['LowestCostPneumatic_type'] + 'Screw_comp'
            return sep_equip_option
        else:
            sep_equip_option = row['LowestCostGD_type'] + row['LowestCostPneumatic_type']
            return sep_equip_option
    else:
        if row['Vent_ReciCompressor'] != 0:
            sep_equip_option =  row['LowestCostPneumatic_type'] + 'Reci_comp'
            return sep_equip_option
        elif row['Vent_ScrewCompressor'] != 0:
            sep_equip_option =  row['LowestCostPneumatic_type'] + 'Screw_comp'
            return sep_equip_option
        else:
            sep_equip_option = row['LowestCostPneumatic_type']
            return sep_equip_option

def sepvssite(row):
    if row['Lowest CO2e abatement cost option sepvssite']=='LowestSeparateEquipCostOption':
        return row['LowestSeparateEquipCostType']
    else:
        return row['LowestSiteWide_type']

def costcomparisons(techcasestudycosts, CH4GWPconstants,ch4density):
    #comparing site-wide costs
    site_wide_costs = techcasestudycosts.loc[:,['VRUFlareGrid_MACCCO2e', 'VRUFlareGen_MACCCO2e', 'VRUTieInGrid_MACCCO2e', 'VRUTieInGen_MACCCO2e', 'VRUVapcombGrid_MACCCO2e', 'VRUVapcombGen_MACCCO2e', 'Casinggasflare_MACCCO2e', 'Casinggastiein_MACCCO2e', 'Gasbladdertruck_MACCCO2e']]
    techcasestudycosts['LowestSiteWide_type'] = site_wide_costs.idxmin(axis=1)
    techcasestudycosts['LowestSiteWideOption'] = techcasestudycosts.apply(sitewideoption, axis=1)
    #comparing separate equipment costs
    #IA, Elec or Separate Pneu
    pneumatic_technologies_df = techcasestudycosts[['IA_MACCCO2e', 'Elec_MACCCO2e', 'pneu_components_MACCCO2e']]
    techcasestudycosts['LowestCostPneumatic'] = pneumatic_technologies_df.idxmin(axis=1)
    techcasestudycosts['LowestCostPneumatic_type'] = techcasestudycosts.apply(LowestCostPneumatic_type, axis=1)

    #GD technologies
    GD_technologies_df = techcasestudycosts[['GD_FlareMACCCO2e', 'GD_VentMACCCO2e']]
    techcasestudycosts['LowestCostGD'] = GD_technologies_df.idxmin(axis=1)
    techcasestudycosts['LowestCostGD_type'] = techcasestudycosts.apply(LowestCostGD_type, axis=1)

    #determine the lowest costs for separate equipments
    techcasestudycosts['LowestSepEquipCost_npv'] = techcasestudycosts.apply(LowestSepEquipCost_npv, axis=1)
    techcasestudycosts['LowestSepEquipCost_co2enpv'] = techcasestudycosts.apply(LowestSepEquipCost_co2enpv, axis=1)
    techcasestudycosts['LowestSeparateEquipCostType'] = techcasestudycosts.apply(checking_compressor_GD_UDF, axis=1)
    techcasestudycosts['LowestSeparateEquipCostOption'] =  techcasestudycosts['LowestSepEquipCost_npv'] /techcasestudycosts['LowestSepEquipCost_co2enpv']

#~~~~~OPTION TO PRIORITIZE SITE-WIDE OPTIONS FIRST
    # techcasestudycosts['LowestSeparateEquipCostvalue'] = techcasestudycosts['LowestSepEquipCost_npv'] / techcasestudycosts['LowestSepEquipCost_co2enpv']
    # site_wide_tech = techcasestudycosts[techcasestudycosts['LowestSiteWideOption'].notnull()]
    # site_wide_tech['Lowest CO2e abatement cost option'] = site_wide_tech['LowestSiteWide_type']
    # site_wide_tech['Lowest CO2e abatement cost value'] = site_wide_tech.apply(co2efiltering, axis=1)
    #
    # separate_tech = techcasestudycosts[techcasestudycosts['LowestSiteWideOption'].isna()]
    # separate_tech['Lowest CO2e abatement cost option'] = separate_tech.apply(separate_tech_options, axis=1)
    # separate_tech['Lowest CO2e abatement cost value'] = separate_tech['LowestSeparateEquipCostvalue']
    # co2eonlytechnologies_df = pd.concat([site_wide_tech[['Lowest CO2e abatement cost option','Lowest CO2e abatement cost value']], separate_tech[['Lowest CO2e abatement cost option','Lowest CO2e abatement cost value']]], axis=0)

#~~~~~ASSESSING ALL OPTIONS EQUALLY
    co2eonlytechnologies_df = pd.concat(
        [techcasestudycosts['LowestSeparateEquipCostOption'], techcasestudycosts['LowestSiteWideOption']], axis=1)
    co2eonlytechnologies_df['Lowest CO2e abatement cost option sepvssite'] = co2eonlytechnologies_df.idxmin(axis="columns")
    co2eonlytechnologies_df['Lowest CO2e abatement cost value'] = co2eonlytechnologies_df.apply(co2efiltering,axis=1)

    lasttwocolumns = co2eonlytechnologies_df[['Lowest CO2e abatement cost option sepvssite', 'Lowest CO2e abatement cost value']]
    techcasestudycosts = techcasestudycosts.join(lasttwocolumns)
    techcasestudycosts['Lowest CO2e abatement cost option'] = techcasestudycosts.apply(sepvssite, axis=1)
    techcasestudycosts['volumereductionstCO2e/y'] = techcasestudycosts.apply(volumereduction_udf, args=(CH4GWPconstants,ch4density),axis=1)
    techcasestudycosts['discounted_volumereductionstCO2e/y'] = techcasestudycosts.apply(discountedvolumereduction_udf, args=(CH4GWPconstants,ch4density),axis=1)
    techcasestudycosts = techcasestudycosts[techcasestudycosts['ventvol']>0]
    techcasestudycosts = techcasestudycosts[techcasestudycosts['Area']=='AB']
    techcasestudycosts = techcasestudycosts.sort_values('Lowest CO2e abatement cost value')

    techcasestudycosts['range'] = pd.cut(techcasestudycosts['Lowest CO2e abatement cost value'],
                                        [-10, 0, 10, 20, 30, 50, 100, 200, 300, 400, 500, 1000, 9000],
                                        include_lowest=True)
    techcasestudycosts = techcasestudycosts.dropna(subset='Lowest CO2e abatement cost value')
    sum_cost_ranges = techcasestudycosts[['volumereductionstCO2e/y','Lowest CO2e abatement cost option', 'range']].groupby(['Lowest CO2e abatement cost option', 'range'], as_index=False).sum()
    sum_discountedcost_ranges = techcasestudycosts[['discounted_volumereductionstCO2e/y','Lowest CO2e abatement cost option', 'range']].groupby(['Lowest CO2e abatement cost option', 'range'], as_index=False).sum()
    average_cost_ranges = techcasestudycosts[['Lowest CO2e abatement cost value','Lowest CO2e abatement cost option', 'range']].groupby(['Lowest CO2e abatement cost option', 'range'], as_index=False).mean()

    # average_cost_ranges_sitewide = average_cost_ranges_sitewide.dropna(subset=['LowestSiteWideOption'])    techcasestudycosts_sitewide_only = techcasestudycosts[techcasestudycosts['Lowest CO2e abatement cost option'] == 'LowestSiteWideOption']
    # techcasestudycosts_sitewide_only['range'] = pd.cut(techcasestudycosts_sitewide_only['Lowest CO2e abatement cost value'],
    #                                     [-10, 0, 10, 20, 30, 50, 100, 200, 300, 400, 500, 1000, 9000],
    #                                     include_lowest=True)
    # sum_cost_ranges_sitewide = techcasestudycosts_sitewide_only[['volumereductionstCO2e/y','LowestSiteWide_type', 'range']].groupby(['LowestSiteWide_type', 'range'], as_index=False).sum()
    # average_cost_ranges_sitewide = techcasestudycosts_sitewide_only[['LowestSiteWideOption','LowestSiteWide_type', 'range']].groupby(['LowestSiteWide_type', 'range'], as_index=False).mean()
    # average_cost_ranges_sitewide = average_cost_ranges_sitewide.dropna(subset=['LowestSiteWideOption'])

    # techcasestudycosts_sep_equip_only = techcasestudycosts[techcasestudycosts['Lowest CO2e abatement cost option'] == 'LowestSeparateEquipCostOption']
    # techcasestudycosts_sep_equip_only['range'] = pd.cut(techcasestudycosts_sep_equip_only['Lowest CO2e abatement cost value'],
    #                                     [-10, 0, 10, 20, 30, 50, 100, 200, 300, 400, 500, 1000, 9000],
    #                                     include_lowest=True)
    # sum_cost_ranges_sep_equip = techcasestudycosts_sep_equip_only[['volumereductionstCO2e/y','LowestCostGD_type','LowestCostPneumatic_type' , 'range']].groupby(['LowestCostGD_type','LowestCostPneumatic_type', 'range'], as_index=False).sum()
    # average_cost_ranges_sep_equip = techcasestudycosts_sep_equip_only[['LowestSeparateEquipCostOption', 'LowestCostGD_type','LowestCostPneumatic_type', 'range']].groupby(['LowestCostGD_type','LowestCostPneumatic_type', 'range'], as_index=False).mean()
    # average_cost_ranges_sep_equip = average_cost_ranges_sep_equip.dropna(subset=['LowestSeparateEquipCostOption'])


    # techcasestudycosts.to_csv('econdatav3_nocarb_filtered2022_alberta_methanetechcostNPV_v3.csv')
    # filter_results_df.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v2.csv')
    # sum_cost_ranges = pd.concat([sum_cost_ranges_sitewide,sum_cost_ranges_sep_equip])
    sum_cost_ranges = sum_cost_ranges[sum_cost_ranges['volumereductionstCO2e/y']> 0]
    sum_cost_ranges.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v6_sumrange.csv')
    sum_discountedcost_ranges.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v6_discountsumrange.csv')

    # average_cost_ranges = pd.concat([average_cost_ranges_sitewide, average_cost_ranges_sep_equip])
    average_cost_ranges = average_cost_ranges.dropna(subset=['Lowest CO2e abatement cost value'])
    average_cost_ranges.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_v6_averagerange.csv')

    return techcasestudycosts

def highest_abatement_selection_MACC(row):
    if (row['GlycolDehy'] != 0) and (row['Vent_ReciCompressor'] != 0) and (row['Vent_ScrewCompressor'] != 0):
        temp_tech_list = row.loc[['VRUFlareGrid_co2enpvCAD', 'VRUFlareGen_co2enpvCAD', 'VRUTieInGrid_co2enpvCAD',
                                      'VRUTieInGen_co2enpvCAD', 'VRUVapcombGrid_co2enpvCAD', 'VRUVapcombGen_co2enpvCAD',
                                      'Casinggasflare_co2enpvCAD', 'Casinggastiein_co2enpvCAD',
                                      'Gasbladdertruck_co2enpvCAD',
                                      'PneuGDvent_co2enpvCAD', 'PneuGDflare_co2enpvCAD', 'IAGDflare_co2enpvCAD',
                                      'IAGDvent_co2enpvCAD',
                                      'ElecGDflare_co2enpvCAD', 'ElecGDvent_co2enpvCAD']]
        highest_abatement = temp_tech_list.idxmax()
        return highest_abatement

    if (row['GlycolDehy'] != 0) or (row['Vent_ReciCompressor'] != 0) or (row['Vent_ScrewCompressor'] != 0):
        temp_tech_list = row.loc[['VRUFlareGrid_co2enpvCAD', 'VRUFlareGen_co2enpvCAD', 'VRUTieInGrid_co2enpvCAD',
                                  'VRUTieInGen_co2enpvCAD', 'VRUVapcombGrid_co2enpvCAD', 'VRUVapcombGen_co2enpvCAD',
                                  'Casinggasflare_co2enpvCAD', 'Casinggastiein_co2enpvCAD',
                                  'Gasbladdertruck_co2enpvCAD']]
        highest_abatement = temp_tech_list.idxmax()
        return highest_abatement

def volumetric_max_udf(row):
    columnname = row['HighestSiteWideabatement_volreductions_type']
    highest_volumetric_reduction = row.loc[columnname]
    return highest_volumetric_reduction

def GD_check(row):
    if row['GlycolDehy'] ==0:
        return 0
    else:
        return 1
def reci_check(row):
    if row['Vent_ReciCompressor'] == 0:
        return 0
    else:
        return 1
def screw_check(row):
    if row['Vent_ScrewCompressor'] == 0:
        return 0
    else:
        return 1


def volumereduction_abatement(techcasestudycosts, CH4GWPconstants, ch4density):
    ventrate = techcasestudycosts['ventvol']  # e3m3/d
    techselection_df = pd.DataFrame()

    VRUFlareGridventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # # e3m3/d * %reduced *gCO2e/gCh4 * kgch4/e3m3 *t/1000kg =tCO2e/d
    VRUFlareGridemissionsfromtech = techcasestudycosts['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
            10 ** 6)) + ventrate * 0.95 * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d = tCO2/d) #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
    VRUFlareGridnetabatement = (VRUFlareGridventabatement - VRUFlareGridemissionsfromtech) * 365  # tCO2e/y

    VRUFlareGenventabatement = ventrate * 0.95 * 0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    VRUFlareGenemissionsfromtech = techcasestudycosts[
                                       'VRU_hp'] * 1.15 * 24 * 0.000453592 + ventrate * 0.95 * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d = tCO2/d) # hp * lbCO2/hp hr *24hr/d *tonne/lb = tCO2e/d
    VRUFlareGennetabatement = (VRUFlareGenventabatement - VRUFlareGenemissionsfromtech) * 365  # tCO2e/y

    VRUTieInGridventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # # e3m3/d * %reduced *gCO2e/gCh4 * kgch4/e3m3 *t/1000kg =tCO2e/d
    VRUTieInGridemissionsfromtech = techcasestudycosts['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (
            590 / (10 ** 6))  # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
    VRUTieInGridnetabatement = (VRUTieInGridventabatement - VRUTieInGridemissionsfromtech) * 365  # tCO2e/y

    VRUTieInGenventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # # e3m3/d * %reduced *gCO2e/gCh4 * kgch4/e3m3 *t/1000kg =tCO2e/d
    VRUTieInGenemissionsfromtech = techcasestudycosts[
                                       'VRU_hp'] * 1.15 * 24 * 0.000453592  # hp * lbCO2/hp hr *24hr/d *tonne/lb = tCO2e/d
    VRUTieInGennetabatement = (VRUTieInGenventabatement - VRUTieInGenemissionsfromtech) * 365  # tCO2e/y

    VRUVapcombGridventabatement = ventrate * 0.95 * 0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    VRUVapcombGridemissionsfromtech = techcasestudycosts['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
            10 ** 6)) + ventrate * 0.95 * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d = tCO2/d) # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
    VRUVapcombGridnetabatement = (VRUVapcombGridventabatement - VRUVapcombGridemissionsfromtech) * 365  # tCO2e/y

    VRUVapcombGenventabatement = ventrate * 0.95 * 0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    VRUVapcombGenemissionsfromtech = techcasestudycosts[
                                         'VRU_hp'] * 1.15 * 24 * 0.000453592 + ventrate * 0.95 * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d = tCO2/d)# hp * lbCO2/hp hr *24hr/d *tonne/lb = tCO2e/d
    VRUVapcombGennetabatement = (VRUVapcombGenventabatement - VRUVapcombGenemissionsfromtech) * 365  # tCO2e/y

    Casinggasflarepercentreduction = 0.95
    Casinggasflareventabatement = ventrate * Casinggasflarepercentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    Casinggasflareemissionsfromtech = techcasestudycosts[
                                          'ventvol'] * Casinggasflarepercentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d = tCO2/d
    Casinggasflarenetabatement = (Casinggasflareventabatement - Casinggasflareemissionsfromtech) * 365  # tCO2e/y

    Casinggastieinventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    Casinggastieinnetabatement = (Casinggastieinventabatement) * 365  # tCO2e/y

    Gasbladdertruckpercentreduction = 0.95
    Gasbladdertruckventabatement = ventrate * Gasbladdertruckpercentreduction * CH4GWPconstants * ch4density / 1000  # e3m3/d * %reduced * kg/e3m3 *t/1000kg =  tCO2e/d
    Gasbladdertrucknetabatement = (Gasbladdertruckventabatement) * 365  # tCO2e/y

    percentreduction_pneu = 1
    ventrate_pneu = techcasestudycosts[
        ['PneuPump', 'PneuTransducer', 'PneuLevelControl', 'PneuPositioner']].sum(axis=1)  # e3m3/d
    ventabatement_pneu = ventrate_pneu * percentreduction_pneu * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech_pneu = 0
    netabatement_pneu = ventabatement_pneu - emissionsfromtech_pneu

    GDventabatement = 0
    GDemissionsfromtech = 0
    netabatement_GD = (GDventabatement - GDemissionsfromtech) * 365  # tCO2e/y

    GDpercentreduction = 1
    GDflarerate = techcasestudycosts['GlycolDehy']  # e3m3/d
    GDflareabatement = GDflarerate * GDpercentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    GDflareemissionsfromtech = GDflarerate * GDpercentreduction * ch4density * 44.01 / 16.04 / 1000  # tCO2/d emissions from combustion
    netabatement_GDflare = (GDflareabatement - GDflareemissionsfromtech) * 365  # tCO2e/y


    percentreduction_allpneu = 1
    ventrate_allpneu = techcasestudycosts['allpneuvents']  # e3m3/d
    ventabatement_allpneu = ventrate_allpneu * percentreduction_allpneu * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech_allpneu = 0
    netabatement_allpneu = (ventabatement_allpneu - emissionsfromtech_allpneu)*365 #tCO2e/y

    percentreduction_recicomp = 1
    ventrate_recicomp = techcasestudycosts['Vent_ReciCompressor']
    ventabatement_recicomp = (ventrate_recicomp * percentreduction_recicomp * CH4GWPconstants * ch4density / 1000)*365  # tCO2e/y

    percentreduction_screwcomp = 1
    ventrate_screwcomp = techcasestudycosts['Vent_ScrewCompressor']
    ventabatement_screwcomp = (ventrate_screwcomp * percentreduction_screwcomp * CH4GWPconstants * ch4density / 1000 )*365 # tCO2e/y

    techcasestudycosts['GD_check'] = techcasestudycosts.apply(GD_check, axis=1)
    techcasestudycosts['reci_check'] = techcasestudycosts.apply(reci_check,axis=1)
    techcasestudycosts['screw_check'] = techcasestudycosts.apply(screw_check, axis=1)

    IAGDflarenetabatement = netabatement_GDflare * techcasestudycosts['GD_check'] + netabatement_allpneu + ventabatement_recicomp * techcasestudycosts['reci_check'] + ventabatement_screwcomp *techcasestudycosts['screw_check']
    IAGDventnetabatement = netabatement_GD * techcasestudycosts['GD_check'] + netabatement_allpneu + ventabatement_recicomp * techcasestudycosts['reci_check'] + ventabatement_screwcomp *techcasestudycosts['screw_check']
    ElecGDflarenetabatement = netabatement_GDflare * techcasestudycosts['GD_check'] + netabatement_allpneu + ventabatement_recicomp * techcasestudycosts['reci_check'] + ventabatement_screwcomp *techcasestudycosts['screw_check']
    ElecGDventnetabatement = netabatement_GD * techcasestudycosts['GD_check'] + netabatement_allpneu + ventabatement_recicomp * techcasestudycosts['reci_check'] + ventabatement_screwcomp *techcasestudycosts['screw_check']
    PneuGDflarenetabatement = netabatement_GDflare * techcasestudycosts['GD_check'] + netabatement_allpneu + ventabatement_recicomp * techcasestudycosts['reci_check'] + ventabatement_screwcomp *techcasestudycosts['screw_check']
    PneuGDventnetabatement = netabatement_GD* techcasestudycosts['GD_check'] + netabatement_allpneu + ventabatement_recicomp * techcasestudycosts['reci_check'] + ventabatement_screwcomp *techcasestudycosts['screw_check']

    tech_list = (VRUFlareGridnetabatement, VRUFlareGennetabatement, VRUTieInGridnetabatement,
                 VRUTieInGennetabatement, VRUVapcombGridnetabatement, VRUVapcombGennetabatement,
                 Casinggasflarenetabatement, Casinggastieinnetabatement, Gasbladdertrucknetabatement,
                 PneuGDventnetabatement, PneuGDflarenetabatement, IAGDflarenetabatement, IAGDventnetabatement,
                 ElecGDflarenetabatement, ElecGDventnetabatement)
    tech_label = ('VRUFlareGrid', 'VRUFlareGen', 'VRUTieInGrid',
                  'VRUTieInGen', 'VRUVapcombGrid', 'VRUVapcombGen',
                  'Casinggasflare', 'Casinggastiein', 'Gasbladdertruck',
                  'PneuGDvent', 'PneuGDflare', 'IAGDflare', 'IAGDvent',
                  'ElecGDflare', 'ElecGDvent')

    techselection_df = pd.DataFrame([VRUFlareGridnetabatement, VRUFlareGennetabatement, VRUTieInGridnetabatement,
                 VRUTieInGennetabatement, VRUVapcombGridnetabatement, VRUVapcombGennetabatement,
                 Casinggasflarenetabatement, Casinggastieinnetabatement, Gasbladdertrucknetabatement,
                 PneuGDventnetabatement, PneuGDflarenetabatement, IAGDflarenetabatement, IAGDventnetabatement,
                 ElecGDflarenetabatement, ElecGDventnetabatement], index=tech_label).transpose()
    techselection_df = techselection_df.join(techcasestudycosts[['VRUFlareGrid_MACCCO2e', 'VRUFlareGen_MACCCO2e', 'VRUTieInGrid_MACCCO2e',
                  'VRUTieInGen_MACCCO2e', 'VRUVapcombGrid_MACCCO2e', 'VRUVapcombGen_MACCCO2e',
                  'Casinggasflare_MACCCO2e', 'Casinggastiein_MACCCO2e', 'Gasbladdertruck_MACCCO2e']])
    techselection_df.loc[techselection_df['VRUFlareGrid_MACCCO2e'].isna(), 'VRUFlareGrid'] = np.nan
    techselection_df.loc[techselection_df['VRUFlareGen_MACCCO2e'].isna(), 'VRUFlareGen'] = np.nan
    techselection_df.loc[techselection_df['VRUTieInGrid_MACCCO2e'].isna(), 'VRUTieInGrid'] = np.nan
    techselection_df.loc[techselection_df['VRUTieInGen_MACCCO2e'].isna(), 'VRUTieInGen'] = np.nan
    techselection_df.loc[techselection_df['VRUVapcombGrid_MACCCO2e'].isna(), 'VRUVapcombGrid'] = np.nan
    techselection_df.loc[techselection_df['VRUVapcombGen_MACCCO2e'].isna(), 'VRUVapcombGen'] = np.nan
    techselection_df.loc[techselection_df['Casinggasflare_MACCCO2e'].isna(), 'Casinggasflare'] = np.nan
    techselection_df.loc[techselection_df['Casinggastiein_MACCCO2e'].isna(), 'Casinggastiein'] = np.nan
    techselection_df.loc[techselection_df['Gasbladdertruck_MACCCO2e'].isna(), 'Gasbladdertruck'] = np.nan
    techselection_df = techselection_df.drop(columns=['VRUFlareGrid_MACCCO2e', 'VRUFlareGen_MACCCO2e', 'VRUTieInGrid_MACCCO2e',
                  'VRUTieInGen_MACCCO2e', 'VRUVapcombGrid_MACCCO2e', 'VRUVapcombGen_MACCCO2e',
                  'Casinggasflare_MACCCO2e', 'Casinggastiein_MACCCO2e', 'Gasbladdertruck_MACCCO2e'])

    techselection_df['HighestSiteWideabatement_volreductions_type'] = techselection_df.idxmax(axis='columns')
    techselection_df['HighestSiteWideabatement_volreductions'] = techselection_df.apply(volumetric_max_udf, axis=1)
    techcasestudycosts = techcasestudycosts.join(techselection_df[['HighestSiteWideabatement_volreductions_type', 'HighestSiteWideabatement_volreductions']])
    techcasestudycosts['HighestSiteWideAbatement_volreductions_MACCCO2e'] = techcasestudycosts.apply(sitewideoption_abatement, axis=1)

    return techcasestudycosts


def abatementcomparisions (techcasestudycosts, CH4GWPconstants,ch4density):
    #comparing site-wide costs
    techcasestudycosts['PneuGDvent_co2enpvCAD'] = techcasestudycosts[
        ['ReciComp_co2enpvCAD', 'ScrewComp_co2enpvCAD', 'PneuPositioner_co2enpvCAD', 'PneuLevelControl_co2enpvCAD',
         'PneuTransducer_co2enpvCAD', 'PneuPump_co2enpvCAD','GDFlare_co2enpvCAD']].sum(axis=1)
    techcasestudycosts['PneuGDflare_co2enpvCAD'] = techcasestudycosts[
        ['ReciComp_co2enpvCAD', 'ScrewComp_co2enpvCAD', 'PneuPositioner_co2enpvCAD', 'PneuLevelControl_co2enpvCAD',
         'PneuTransducer_co2enpvCAD', 'PneuPump_co2enpvCAD','GDVent_co2enpvCAD']].sum(axis=1)
    techcasestudycosts['IAGDflare_co2enpvCAD'] = techcasestudycosts[
        ['ReciComp_co2enpvCAD', 'ScrewComp_co2enpvCAD', 'IA_co2enpvCAD', 'GDFlare_co2enpvCAD']].sum(axis=1)
    techcasestudycosts['IAGDvent_co2enpvCAD'] = techcasestudycosts[
        ['ReciComp_co2enpvCAD', 'ScrewComp_co2enpvCAD', 'IA_co2enpvCAD', 'GDVent_co2enpvCAD']].sum(axis=1)
    techcasestudycosts['ElecGDflare_co2enpvCAD'] = techcasestudycosts[
        ['ReciComp_co2enpvCAD', 'ScrewComp_co2enpvCAD', 'Elec_co2enpvCAD', 'GDFlare_co2enpvCAD']].sum(axis=1)
    techcasestudycosts['ElecGDvent_co2enpvCAD'] = techcasestudycosts[
        ['ReciComp_co2enpvCAD', 'ScrewComp_co2enpvCAD','Elec_co2enpvCAD', 'GDVent_co2enpvCAD']].sum(axis=1)

    # #removing GD at zero, handle tech selection differently. Some sites do not have glycol dehy emissions assigned
    # techcasestudycosts['HighestSiteWideabatement_volreductions_type'] = techcasestudycosts.apply(highest_abatement_selection_MACC, axis=1)
    # techcasestudycosts['HighestSiteWideAbatement_volreductions_MACCCO2e'] = techcasestudycosts.apply(sitewideoption_abatement, axis=1)
    techcasestudycosts = volumereduction_abatement(techcasestudycosts,CH4GWPconstants,ch4density)

    # techcasestudycosts['highestabatement_volumereductionstCO2e/y'] = techcasestudycosts.apply(volumereduction_abatement_udf, args=(CH4GWPconstants,ch4density),axis=1)
    techcasestudycosts['abatement_range'] = pd.cut(techcasestudycosts['HighestSiteWideAbatement_volreductions_MACCCO2e'],
                                        [-10, 0, 10, 20, 30, 50, 100, 200, 300, 400, 500, 1000, 9000],
                                        include_lowest=True)

    sum_cost_ranges_abatement= techcasestudycosts[['HighestSiteWideabatement_volreductions','HighestSiteWideabatement_volreductions_type', 'abatement_range']].groupby(['HighestSiteWideabatement_volreductions_type', 'abatement_range'], as_index=False).sum()
    sum_cost_ranges_abatement = sum_cost_ranges_abatement[sum_cost_ranges_abatement['HighestSiteWideabatement_volreductions']> 0]
    average_cost_ranges_abatement = techcasestudycosts[['HighestSiteWideAbatement_volreductions_MACCCO2e','HighestSiteWideabatement_volreductions_type', 'abatement_range']].groupby(['HighestSiteWideabatement_volreductions_type', 'abatement_range'], as_index=False).mean()
    average_cost_ranges_abatement = average_cost_ranges_abatement.dropna(subset=['HighestSiteWideAbatement_volreductions_MACCCO2e'])

    techcasestudycosts.to_csv('econdatav3_nocarb_filtered2022_alberta_methanetechcostNPV_v5.csv')
    sum_cost_ranges_abatement.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_abatement_v5_sumrange.csv')
    average_cost_ranges_abatement.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV_abatement_v5_averagerange.csv')

    return techcasestudycosts


if __name__ == '__main__':
    techdetailspath = "./data/technologydetails.csv"
    techdetails_df = pd.read_csv(techdetailspath)
    techdetails_df = techdetails_df.set_index('technologies')

    #now using file v10 with oil and gas facilities specifically
    facilitydatapath = "./data/2022v10_oilgasfacilityvol.csv"
    facilitydata_df = pd.read_csv(facilitydatapath)
    facilitydata_df = facilitydata_df[facilitydata_df['ventvol'] > 0]

    #auxiliary equipment tech
    auxtechdetailspath = "./data/technologydetails_equip.csv"
    auxtechdetails_df = pd.read_csv(auxtechdetailspath)
    auxtechdetails_df = auxtechdetails_df.set_index(['technologies', 'Range'])

    CH4GWPconstants = 28 #co2e/ch4
    gasprice = 3.55 * 39 # $CAD/GJ * GJ/e3MJ * 39e3MJ/e3m3 = $CAD/e3m3
    discountrate = 0.1
    ch4density = 687 #kg/e3m3

    facility_econ_data_df = tech_econ_runs(facilitydata_df, techdetails_df)
    feasbilitycheck_facility_econ_data_df = equip_feasibilityandcount(facility_econ_data_df, techdetails_df)
    techcasestudycosts = casestudycostcals(feasbilitycheck_facility_econ_data_df, techdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density)

    facilitydata_equipecon_df = auxequip_tech_econ_runs(techcasestudycosts, auxtechdetails_df)
    feasbilitycheck_equip_econ_data_df = auxequip_feasibilityandcount(facilitydata_equipecon_df, auxtechdetails_df)
    techandauxequip_casestudycosts = auxequip_casestudycostcals(feasbilitycheck_equip_econ_data_df, auxtechdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density)
    techandauxequip_casestudycosts.to_csv(
        './temp_facilityandecon_data.csv')


    # auxtechdetailspath = r"C:/Users/jyuan/OneDrive - University of Calgary/PTAC/Equipment Inventory/temp_facilityandecon_data.csv"
    # techandauxequip_casestudycosts = pd.read_csv(auxtechdetailspath)

    techandauxequip_casestudycosts = costcomparisons(techandauxequip_casestudycosts, CH4GWPconstants, ch4density)
    techandauxequip_casestudycosts = abatementcomparisions(techandauxequip_casestudycosts, CH4GWPconstants, ch4density)
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
