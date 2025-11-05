import pandas as pd
import numpy as np
import math

def Flarecount(row, FlaremaxFR):
    if row['ventvol'] > FlaremaxFR:
        equipmentcount = row['ventvol'] / FlaremaxFR
        return equipmentcount
    else:
        return 1

def Flarecountrounded(row):
    if row['FlareCount'] > 1:
        roundedcount = math.ceil(row['FlareCount'])
        return roundedcount
    else:
        return 1

def casinggasmaxFR(row, casingtieinMaxFR):
    if row['ventvol'] > casingtieinMaxFR:
        return 'No'
    else:
        return 'Yes'

def vapcombcount(row, vapcombMaxFR):
    if row['ventvol'] > vapcombMaxFR:
        equipmentcount = row['ventvol'] / vapcombMaxFR
        return equipmentcount
    else:
        return 1

def vapcombcountrounded(row):
    if row['VapCombCount'] > 1:
        roundedcount = math.ceil(row['VapCombCount'])
        return roundedcount
    else:
        return 1

def gasbladdercount(row):
    if row['Gasbladdercount'] > 1:
        roundedcount = math.ceil(row['Gasbladdercount'])
        return roundedcount
    else:
        return 1

def truckscount(row, pertruckmax):
    truckcountperday = row['ventvol'] / pertruckmax
    return truckcountperday

def monthlytrucks(row):
    monthlycount = row['numberoftrucksperday'] * 30.437
    roundedcount = math.ceil(monthlycount)
    return roundedcount

def yearlytrucks(row):
    yearlycount = row['numberoftrucksperday'] * 30.437 * 12
    roundedcount = math.ceil(yearlycount)
    return roundedcount

def equip_feasibilityandcount(facility_econ_data_df, techdetails_df):
    VRUminFR = techdetails_df.at['VRU_25', 'MinFR']
    FlareminFR = techdetails_df.at['Flare', 'MinFR']
    CasingFlareminFR = techdetails_df.at['Casing_flare_low', 'MinFR']
    facility_econ_data_df['VRU_feasible min?'] = facility_econ_data_df['ventvol'] > VRUminFR
    facility_econ_data_df['Flare_feasible min?'] = facility_econ_data_df['ventvol'] > FlareminFR
    facility_econ_data_df['CasingFlare_feasible min?'] = facility_econ_data_df['ventvol'] > CasingFlareminFR

    FlaremaxFR = techdetails_df.at['Flare', 'MaxFR']
    facility_econ_data_df['FlareCount'] = facility_econ_data_df['ventvol'] / FlaremaxFR
    facility_econ_data_df['FlareCountRounded'] = facility_econ_data_df.apply(Flarecountrounded, axis=1)

    casingtieinMaxFRhigh = techdetails_df.at['Casing_tiein_high', 'MaxFR']
    facility_econ_data_df['CasingGasTieIn high feasible max?'] = facility_econ_data_df['ventvol'] < casingtieinMaxFRhigh

    casingtieinMaxFRlow = techdetails_df.at['Casing_tiein_low', 'MaxFR']
    facility_econ_data_df['CasingGasTieIn low feasible max?'] = facility_econ_data_df['ventvol'] < casingtieinMaxFRlow

    vapcombMaxFR = techdetails_df.at['Vapourcombuster_high', 'MaxFR']
    facility_econ_data_df['VapCombCount'] = facility_econ_data_df['ventvol'] / vapcombMaxFR
    facility_econ_data_df['VapCombRounded'] = facility_econ_data_df.apply(vapcombcountrounded, axis=1)

    gasbladdermax = techdetails_df.at['Gasbladder', 'MaxFR']
    facility_econ_data_df['Gasbladdercount'] = facility_econ_data_df['ventvol'] / gasbladdermax
    facility_econ_data_df['Gasbladdercountrounded'] = facility_econ_data_df.apply(gasbladdercount, axis=1)

    truckvolmaxpertruck = techdetails_df.at['Gasstorage_low_pertruck', 'MaxFR']
    facility_econ_data_df['numberoftrucksperday'] = facility_econ_data_df['ventvol']/truckvolmaxpertruck
    facility_econ_data_df['numberoftruckspermonth_rounded'] = facility_econ_data_df.apply(monthlytrucks, axis=1)
    facility_econ_data_df['numberoftrucksperyear_rounded'] = facility_econ_data_df.apply(yearlytrucks, axis=1)

    return facility_econ_data_df

def transducersizingcheck_udf(row):
    if (row['ReportingFacilitySubType'] == '311') or (row['ReportingFacilitySubType'] == '351'):
        return 'sm'
    else:
        return 'lg'
#
# def IA1_maxFR_Lower_udf(row, IA1_maxFR_Lower):
#     check = row['allpneuvents'] < IA1_maxFR_Lower
#     return check
#
def allpneuvent_udf(row):
    try:
        allpneumatictypes= ['PneuLevelControl', 'PneuPositioner', 'PneuTransducer', 'PneuPump', 'PneuIntermittent']
        allpneuvents = row[allpneumatictypes].sum()
        return allpneuvents
    except:
        allpneumatictypes= ['PneuLevelControl', 'PneuPositioner', 'PneuTransducer', 'PneuPump']
        allpneuvents = row[allpneumatictypes].sum()
        return allpneuvents
#
# def IA1_maxFR_Lower_udf(row,IA1_lower):
#     if row['allpneuvents'] < IA1_lower:
#         return True
#     else:
#         return False
#
# def IA1_maxFR_Upper_udf(row,IA1_upper):
#     if row['allpneuvents'] < IA1_upper:
#         return True
#     else:
#         return False
#
# def IA2_maxFR_Upper_udf(row,IA2_upper):
#     if row['allpneuvents'] < IA2_upper:
#         return True
#     else:
#         return False



def auxequip_feasibilityandcount(facilitydata_df, techdetails_df):
    #instrument air requirements
    IA1_maxFR_Upper = techdetails_df.at[('AllPneu_Air1','Upper')][ 'Max (e3m3/d)'] #e3m3/d
    IA2_maxFR_Upper = techdetails_df.at[('AllPneu_Air2','Upper')][ 'Max (e3m3/d)'] #e3m3/d
    IA1_maxFR_Lower = techdetails_df.at[('AllPneu_Air1','Lower')][ 'Max (e3m3/d)'] #e3m3/d

    #calculate pneumatics sum
    facilitydata_df['allpneuvents'] = facilitydata_df.apply(allpneuvent_udf, axis=1)

    facilitydata_df['IA1_lower_feasible max?'] = facilitydata_df['allpneuvents'].lt(IA1_maxFR_Lower[0])
    facilitydata_df['IA1_upper_feasible max?'] = facilitydata_df['allpneuvents'].lt(IA1_maxFR_Upper[0])
    facilitydata_df['IA2_upper_feasible max?'] = facilitydata_df['allpneuvents'].lt(IA2_maxFR_Upper[0])

    #transducer sizing
    facilitydata_df['transducer sizing'] = facilitydata_df.apply(transducersizingcheck_udf, axis=1)

    return facilitydata_df