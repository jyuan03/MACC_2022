import pandas as pd
import numpy as np
import math

def compressorcost(row, compressorintercept, compressorslope):

    stages = np.log((row['PIPE_MAOP'] / 101.325)) / np.log(1.5)
    compressorcost = compressorintercept['Other'].values + row['VENT_gas'] * stages * compressorslope['Other'].values

    return compressorcost

def VRU_CAPEX_udf(row, VRU_25_CAP, VRU_50_CAP, VRU_100_CAP, VRU_200_CAP, VRU_500_CAP):
    #check VRU size
    if row['VRU25'] == 1:
        return VRU_25_CAP
    elif ((row['VRU50'] == 1) and (row['VRU25'] == 0)):
        return VRU_50_CAP
    elif ((row['VRU100'] == 1) and (row['VRU50'] == 0) and (row['VRU25'] == 0)):
        return VRU_100_CAP
    elif ((row['VRU200'] == 1) and (row['VRU100'] == 0) and (row['VRU50'] == 0) and (row['VRU25'] == 0)):
        return VRU_200_CAP
    else:
        return VRU_500_CAP

def VRU_OPEX_udf(row, VRU_25_OP, VRU_50_OP, VRU_100_OP, VRU_200_OP, VRU_500_OP):
    #check VRU size
    if row['VRU25'] == 1:
        return VRU_25_OP
    elif ((row['VRU50'] == 1) and (row['VRU25'] == 0)):
        return VRU_50_OP
    elif ((row['VRU100'] == 1) and (row['VRU50'] == 0) and (row['VRU25'] == 0)):
        return VRU_100_OP
    elif ((row['VRU200'] == 1) and (row['VRU100'] == 0) and (row['VRU50'] == 0) and (row['VRU25'] == 0)):
        return VRU_200_OP
    else:
        return VRU_500_OP

def VRU_size_udf(row):
    #check VRU size
    if row['VRU25'] == 1:
        return 25
    elif ((row['VRU50'] == 1) and (row['VRU25'] == 0)):
        return 50
    elif ((row['VRU100'] == 1) and (row['VRU50'] == 0) and (row['VRU25'] == 0)):
        return 100
    elif ((row['VRU200'] == 1) and (row['VRU100'] == 0) and (row['VRU50'] == 0) and (row['VRU25'] == 0)):
        return 200
    else:
        return 500


def VRU_hp_udf(row):
    #check VRU size
    if row['VRU25'] == 1:
        return 10
    elif ((row['VRU50'] == 1) and (row['VRU25'] == 0)):
        return 15
    elif ((row['VRU100'] == 1) and (row['VRU50'] == 0) and (row['VRU25'] == 0)):
        return 25
    elif ((row['VRU200'] == 1) and (row['VRU100'] == 0) and (row['VRU50'] == 0) and (row['VRU25'] == 0)):
        return 50
    else:
        return 80



def VRU_tiein_grid(techdetails_df, test_sample_df, tech_econ_df):
    techdetails_df = techdetails_df.set_index('technologies')

    #facility details
    ventvol = test_sample_df.at['VENT_gas']/30.437 #e3m3/day

    #technologydetails
    VRUdetails = techdetails_df.loc[['VRU_25', 'VRU_50', 'VRU_100', 'VRU_200', 'VRU_500']]
    compressorintercept = techdetails_df.loc[['Compressor_intercept']]
    compressorslope = techdetails_df.loc[['Compressor_slope']]
    pipelinedetails = techdetails_df.loc[['Pipeline per m']]
    gridconnectdetails = techdetails_df.loc[['Gridconnect']]

    #check VRU size
    VRUsize = ()
    count = 0
    for maxthroughputs in VRUdetails['MaxFR']:
        if ventvol < maxthroughputs:
            VRUsize = maxthroughputs
            break
        else:
            count += 1


    #compressors
    stages = np.log((test_sample_df.at['PIPE_MAOP']/101.325))/np.log(1.5)
    compressorcost = compressorintercept['Other'].values + ventvol * stages * compressorslope['Other'].values

    #pipelines
    pipelineCAPEX = pipelinedetails['CAPEX'][0] * test_sample_df.at['PIPE_MAOP']

    #Obtain tech economics
    VRUCAPEX = VRUdetails.iat[count, 0]
    VRUinstallation = VRUdetails.iat[count, 1]
    VRUOPEX = VRUdetails.iat[count, 2]
    TieInCAPEX = compressorcost[0] + pipelineCAPEX
    TieInOPEX = TieInCAPEX * 0.1
    gridCAPEX = gridconnectdetails['CAPEX'][0]
    gridinstallation = gridconnectdetails['Installation'][0]
    gridOPEX = gridconnectdetails['OPEX'][0]

    totalCAPEX = VRUCAPEX + TieInCAPEX + gridCAPEX
    totalOPEX = VRUOPEX + TieInOPEX + gridOPEX

    ReportingFacilityID = test_sample_df.at['ReportingFacilityID']
    tech_econ_df.at[ReportingFacilityID, 'VRU_tiein_grid_CAPEX'] = totalCAPEX
    tech_econ_df.at[ReportingFacilityID, 'VRU_tiein_grid_OPEX'] = totalOPEX

    return tech_econ_df

def compressors_CAPEX(row, compressorintercept, compressorslope):
    stages = np.log((row['PIPE_MAOP'] / 101.325)) / np.log(1.5)
    compressorcost = compressorintercept + row['ventvol'] * stages * compressorslope

    return compressorcost

def casinggasflare_CAPEX(row, casinggas_flare_CAPEX_low, casinggas_flare_CAPEX_high, casinggas_flare_Install_high, casinggas_flare_Install_low, lowcasinggas_flareFR):
    if row['ventvol'] > lowcasinggas_flareFR:
        combinedcapex = casinggas_flare_Install_high + casinggas_flare_CAPEX_high
        return combinedcapex
    else:
        combinedcapex = casinggas_flare_CAPEX_low + casinggas_flare_Install_low
        return combinedcapex

def casinggasflare_OPEX(row, casinggas_flare_OPEX_low, casinggas_flare_OPEX_high, lowcasinggas_flareFR):
    if row['ventvol'] > lowcasinggas_flareFR:
        return casinggas_flare_OPEX_high
    else:
        return casinggas_flare_OPEX_low

def casinggastiein_CAPEX(row, casinggas_tiein_CAPEX_low, casinggas_tiein_CAPEX_high,casinggas_tiein_Install_low, casinggas_tiein_Install_high, lowcasinggas_tieinFR):
    if row['ventvol'] > lowcasinggas_tieinFR:
        combinedcapex = casinggas_tiein_CAPEX_high + casinggas_tiein_Install_high
        return combinedcapex

    else:
        combinedcapex = casinggas_tiein_CAPEX_low + casinggas_tiein_Install_low
        return combinedcapex

def casinggastiein_OPEX(row, casinggas_tiein_OPEX_low, casinggas_tiein_OPEX_high, lowcasinggas_tieinFR):
    if row['ventvol'] > lowcasinggas_tieinFR:
        return casinggas_tiein_OPEX_high
    else:
        return casinggas_tiein_OPEX_low

def vapcombcost_udf(row, vapcomb_CAPEX_high, vapcomb_OPEX_high, vapcomb_maxFR):
    if row['ventvol'] > vapcomb_maxFR:
        return vapcomb_CAPEX_high
    else:
        return vapcomb_OPEX_high

def tech_econ_runs(facilitydata_df, techdetails_df):
    #VRU
    VRU_25_OP = techdetails_df.at['VRU_25', 'OPEX']
    VRU_50_OP = techdetails_df.at['VRU_50', 'OPEX']
    VRU_100_OP = techdetails_df.at['VRU_100', 'OPEX']
    VRU_200_OP = techdetails_df.at['VRU_200', 'OPEX']
    VRU_500_OP = techdetails_df.at['VRU_500', 'OPEX']

    VRU_25_CAP = techdetails_df.at['VRU_25', 'CAPEX']
    VRU_50_CAP = techdetails_df.at['VRU_50', 'CAPEX']
    VRU_100_CAP = techdetails_df.at['VRU_100', 'CAPEX']
    VRU_200_CAP = techdetails_df.at['VRU_200', 'CAPEX']
    VRU_500_CAP = techdetails_df.at['VRU_500', 'CAPEX']

    facilitydata_df['VRU_CAPEX'] = facilitydata_df.apply(VRU_CAPEX_udf, args=(VRU_25_CAP, VRU_50_CAP, VRU_100_CAP, VRU_200_CAP, VRU_500_CAP), axis=1)
    facilitydata_df['VRU_OPEX'] = facilitydata_df.apply(VRU_OPEX_udf, args=(VRU_25_OP, VRU_50_OP, VRU_100_OP, VRU_200_OP, VRU_500_OP), axis=1)
    facilitydata_df['VRU_size'] = facilitydata_df.apply(VRU_size_udf, axis=1)
    facilitydata_df['VRU_hp'] = facilitydata_df.apply(VRU_hp_udf, axis=1)
    #compressors and pipeline
    compressorintercept = techdetails_df.at['Compressor_intercept', 'Other']
    compressorslope = techdetails_df.at['Compressor_slope', 'Other']
    pipelinecost = techdetails_df.at['Pipeline per m', 'CAPEX']


    facilitydata_df['Compressor_CAPEX'] = facilitydata_df.apply(compressors_CAPEX, args=(compressorintercept, compressorslope), axis=1)
    facilitydata_df['Pipeline_CAPEX'] = facilitydata_df['NEAR_DIST'] * pipelinecost
    facilitydata_df['TieIn_CAPEX'] = facilitydata_df['Compressor_CAPEX'] * facilitydata_df['Pipeline_CAPEX']
    facilitydata_df['TieIn_OPEX'] = facilitydata_df['TieIn_CAPEX'] * 0.1

    #grid connection
    gridcost_CAPEX = techdetails_df.at['Gridconnect', 'CAPEX'] + techdetails_df.at['Gridconnect', 'Installation']
    gridcost_OPEX = techdetails_df.at['Gridconnect', 'OPEX']
    facilitydata_df['GridConnect_CAPEX'] = gridcost_CAPEX
    facilitydata_df['GridConnect_OPEX'] = gridcost_OPEX

    #flare
    flare_notcasing_CAPEX = techdetails_df.at['Flare', 'CAPEX']
    flare_notcasing_OPEX = techdetails_df.at['Flare', 'OPEX']
    facilitydata_df['Flare_notcasing_CAPEX'] = flare_notcasing_CAPEX
    facilitydata_df['Flare_notcasing_OPEX'] = flare_notcasing_OPEX

    #casinggas flare
    casinggas_flare_OPEX_high = techdetails_df.at['Casing_flare_high', 'OPEX']
    casinggas_flare_CAPEX_high = techdetails_df.at['Casing_flare_high', 'CAPEX']
    casinggas_flare_Install_high = techdetails_df.at['Casing_flare_high', 'Installation']
    casinggas_flare_OPEX_low = techdetails_df.at['Casing_flare_low', 'OPEX']
    casinggas_flare_CAPEX_low = techdetails_df.at['Casing_flare_low', 'CAPEX']
    casinggas_flare_Install_low = techdetails_df.at['Casing_flare_high', 'Installation']
    lowcasinggas_flareFR = techdetails_df.at['Casing_flare_low', 'MaxFR']
    facilitydata_df['casinggas_flare_CAPEX'] = facilitydata_df.apply(
        casinggasflare_CAPEX, args=(casinggas_flare_CAPEX_low, casinggas_flare_CAPEX_high, casinggas_flare_Install_high, casinggas_flare_Install_low, lowcasinggas_flareFR), axis=1)
    facilitydata_df['casinggas_flare_OPEX'] = facilitydata_df.apply(
        casinggasflare_OPEX, args=(casinggas_flare_OPEX_low, casinggas_flare_OPEX_high, lowcasinggas_flareFR), axis=1)

    #casinggas tie in
    casinggas_tiein_OPEX_high = techdetails_df.at['Casing_tiein_high', 'OPEX']
    casinggas_tiein_Install_high = techdetails_df.at['Casing_tiein_high', 'Installation']
    casinggas_tiein_CAPEX_high = techdetails_df.at['Casing_tiein_high', 'CAPEX']
    casinggas_tiein_OPEX_low = techdetails_df.at['Casing_tiein_low', 'OPEX']
    casinggas_tiein_Install_low = techdetails_df.at['Casing_tiein_low', 'Installation']
    casinggas_tiein_CAPEX_low = techdetails_df.at['Casing_tiein_low', 'CAPEX']
    lowcasinggas_tieinFR = techdetails_df.at['Casing_tiein_low', 'MaxFR']
    facilitydata_df['casinggas_tiein_CAPEX'] = facilitydata_df.apply(
        casinggastiein_CAPEX, args=(casinggas_tiein_CAPEX_low, casinggas_tiein_CAPEX_high,casinggas_tiein_Install_low, casinggas_tiein_Install_high, lowcasinggas_tieinFR), axis=1)
    facilitydata_df['casinggas_tiein_OPEX'] = facilitydata_df.apply(
        casinggastiein_OPEX, args=(casinggas_tiein_OPEX_low, casinggas_tiein_OPEX_high, lowcasinggas_tieinFR), axis=1)

    #vapourcombustor
    vapcomb_CAPEX_high = techdetails_df.at['Vapourcombuster_high', 'CAPEX']
    vapcomb_OPEX_high = techdetails_df.at['Vapourcombuster_low', 'CAPEX']
    vapcomb_maxFR = techdetails_df.at['Vapourcombuster_low', 'MaxFR']
    facilitydata_df['Vapcombustor_CAPEX'] = facilitydata_df.apply(vapcombcost_udf, args=(vapcomb_CAPEX_high, vapcomb_OPEX_high, vapcomb_maxFR), axis=1)

    #gas bladder
    gasbladder_CAPEX = techdetails_df.at['Gasbladder', 'CAPEX']
    facilitydata_df['GasBladder_CAPEX'] = gasbladder_CAPEX

    #gasstorage
    gasstorage_pertruck = techdetails_df.at['Gasstorage_low_pertruck', 'CAPEX']
    facilitydata_df['gasstorage_pertruckcost'] = gasstorage_pertruck

    #generator
    generator_CAPEX = techdetails_df.at['Generator', 'CAPEX']
    facilitydata_df['Generator_CAPEX'] = generator_CAPEX

    #electricflare
    electricflare_CAPEX = techdetails_df.at['Electricflare', 'CAPEX']
    facilitydata_df['ElectricFlareInstall'] = electricflare_CAPEX

    return facilitydata_df

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

def cashflowcalc(capex, opex, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate, salesgasincome_annual):
    costofabatement = fuelcostsfromtech #$CAD/year

    netabatement = (ventabatement - emissionsfromtech) * 365 #tCO2e/year
    carbonpricing = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # carbonpricing = [50, 65, 80, 95, 110, 125, 140, 155, 170, 170, 170, 170, 170, 170, 170] #$/tCO2e
    year0 = capex
    year1 = -salesgasincome_annual - (netabatement * carbonpricing[1]) + opex + costofabatement
    year2 = -salesgasincome_annual - (netabatement * carbonpricing[2]) + opex + costofabatement
    year3 = -salesgasincome_annual - (netabatement * carbonpricing[3]) + opex + costofabatement
    year4 = -salesgasincome_annual - (netabatement * carbonpricing[4]) + opex + costofabatement
    year5 = -salesgasincome_annual - (netabatement * carbonpricing[5]) + opex + costofabatement
    year6 = -salesgasincome_annual - (netabatement * carbonpricing[6]) + opex + costofabatement
    year7 = -salesgasincome_annual - (netabatement * carbonpricing[7]) + opex + costofabatement
    year8 = -salesgasincome_annual - (netabatement * carbonpricing[8]) + opex + costofabatement
    year9 = -salesgasincome_annual - (netabatement * carbonpricing[9]) + opex + costofabatement
    year10 = -salesgasincome_annual - (netabatement * carbonpricing[10]) + opex + costofabatement
    npv = (year0/((1+discountrate) ** 0)) + (year1/((1+discountrate) ** 1)) + (year2/((1+discountrate) ** 2)) + \
          (year3/((1+discountrate) ** 3)) + (year4/((1+discountrate) ** 4)) + (year5/((1+discountrate) ** 5)) + \
          (year6/((1+discountrate) ** 6)) + (year7/((1+discountrate) ** 7)) + (year8/((1+discountrate) ** 8)) + \
          (year9/((1+discountrate) ** 9)) + (year10/((1+discountrate) ** 10))

    return npv

def abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density):
    totalabatement = (ventabatement - emissionsfromtech) * 365  #tCO2e/y
    reductionemissionstimechange = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # %reduction?
    year0 = 0
    year1 = totalabatement * reductionemissionstimechange[1]
    year2 = totalabatement * reductionemissionstimechange[2]
    year3 = totalabatement * reductionemissionstimechange[3]
    year4 = totalabatement * reductionemissionstimechange[4]
    year5 = totalabatement * reductionemissionstimechange[5]
    year6 = totalabatement * reductionemissionstimechange[6]
    year7 = totalabatement * reductionemissionstimechange[7]
    year8 = totalabatement * reductionemissionstimechange[8]
    year9 = totalabatement * reductionemissionstimechange[9]
    year10 = totalabatement * reductionemissionstimechange[10]
    npv = (year0/((1+discountrate) ** 0)) + (year1/((1+discountrate) ** 1)) + (year2/((1+discountrate) ** 2)) + \
          (year3/((1+discountrate) ** 3)) + (year4/((1+discountrate) ** 4)) + (year5/((1+discountrate) ** 5)) + \
          (year6/((1+discountrate) ** 6)) + (year7/((1+discountrate) ** 7)) + (year8/((1+discountrate) ** 8)) + \
          (year9/((1+discountrate) ** 9)) + (year10/((1+discountrate) ** 10))

    return npv

def abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants):
    totalabatement = (ventabatement)/CH4GWPconstants * 365  #tCH4/y does not account for CO2 emissions
    reductionemissionstimechange = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # %reduction?
    year0 = 0
    year1 = totalabatement * reductionemissionstimechange[1]
    year2 = totalabatement * reductionemissionstimechange[2]
    year3 = totalabatement * reductionemissionstimechange[3]
    year4 = totalabatement * reductionemissionstimechange[4]
    year5 = totalabatement * reductionemissionstimechange[5]
    year6 = totalabatement * reductionemissionstimechange[6]
    year7 = totalabatement * reductionemissionstimechange[7]
    year8 = totalabatement * reductionemissionstimechange[8]
    year9 = totalabatement * reductionemissionstimechange[9]
    year10 = totalabatement * reductionemissionstimechange[10]
    npv = (year0/((1+discountrate) ** 0)) + (year1/((1+discountrate) ** 1)) + (year2/((1+discountrate) ** 2)) + \
          (year3/((1+discountrate) ** 3)) + (year4/((1+discountrate) ** 4)) + (year5/((1+discountrate) ** 5)) + \
          (year6/((1+discountrate) ** 6)) + (year7/((1+discountrate) ** 7)) + (year8/((1+discountrate) ** 8)) + \
          (year9/((1+discountrate) ** 9)) + (year10/((1+discountrate) ** 10))

    return npv

def griddieselemissions(vru_hp):
    emissionsrate = vru_hp * 0.012519139 #hp * tCO2/hp d = tCO2/d
    return emissionsrate


def VRUFlareGrid_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True) and (row['VRU_feasible min?'] == True):
        CAPEX = row['VRU_CAPEX'] + row['GridConnect_CAPEX'] + row['Flare_notcasing_CAPEX'] * row['FlareCountRounded']
        OPEX = row['VRU_OPEX'] + row['GridConnect_OPEX'] + row['Flare_notcasing_OPEX'] * row['FlareCountRounded']
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row['ventvol'] *percentreduction * ch4density /1000 /16.04 * 44.01  #e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d
        emissionsfromtech = emissionsfromtech + row['VRU_hp'] * 0.746 * 3600 * 2 /3600 * (590/ (10**6))  #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
        salesgasincome_annual =0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def VRUFlareGridco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol'] #e3m3/d
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] *percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d
        emissionsfromtech = emissionsfromtech + row['VRU_hp'] * 0.746 * 3600 * 2 /3600 * (590/ (10**6)) #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def VRUFlareGridch4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']  # e3m3/d
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d
        emissionsfromtech = emissionsfromtech + row['VRU_hp'] * 0.746 * 3600 * 2 /3600 * (590/ (10**6)) #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g= tCO2e/d

        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
        return npv
    else:
        npv = np.nan
        return npv


def VRUFlareGen_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True) and (row['VRU_feasible min?'] == True):
        CAPEX = row['VRU_CAPEX'] + row['Generator_CAPEX'] + row['Flare_notcasing_CAPEX'] * row['FlareCountRounded']
        OPEX = row['VRU_OPEX'] + row['Flare_notcasing_OPEX'] * row['FlareCountRounded']
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        salesgasincome_annual=0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def VRUFlareGenco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def VRUFlareGench4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
        return npv

    else:
        npv = np.nan
        return npv

def VRUTieInGrid_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Tie in?'] == False) and (row['VRU_feasible min?'] == True):

        CAPEX = row['VRU_CAPEX'] + row['GridConnect_CAPEX'] + row['TieIn_CAPEX']
        OPEX = row['VRU_OPEX'] + row['GridConnect_OPEX'] + row['TieIn_OPEX']

        ventrate = row['ventvol']
        salesgasincome_annual = ventrate * gasprice * 365  # $CAD/year
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 /3600 * (590/ (10**6)) #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                           ventrate,salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def VRUTieInGridco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Tie in?'] == False) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                    10 ** 6)) # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d

        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
        return npv

    else:
        npv = np.nan
        return npv

def VRUTieInGridch4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Tie in?'] == False) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                    10 ** 6))  # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d

        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
        return npv

    else:
        npv = np.nan
        return npv

def VRUTieInGen_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Tie in?'] == False) and (row['VRU_feasible min?'] == True):
        CAPEX = row['VRU_CAPEX'] + row['Generator_CAPEX'] + row['TieIn_CAPEX']
        OPEX = row['VRU_OPEX'] + row['TieIn_OPEX']
        ventrate = row['ventvol']
        salesgasincome_annual = ventrate * gasprice * 365  # $CAD/year
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate, salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def VRUTieInGenco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Tie in?'] == False) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def VRUTieInGench4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Tie in?'] == False) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
        return npv

    else:
        npv = np.nan
        return npv

def casinggasflare_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True):
        CAPEX = row['casinggas_flare_CAPEX'] * row['FlareCountRounded']
        OPEX = row['casinggas_flare_OPEX'] * row['FlareCountRounded']
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d *365d/y = tCO2/y
        salesgasincome_annual=0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate, salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def casinggasflareco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d *365d/y = tCO2/y

        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def casinggasflarech4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Flare_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d *365d/y = tCO2/y

        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
        return npv

    else:
        npv = np.nan
        return npv

def casinggastiein_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if row['casinggas_tiein_OPEX'] > 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn high feasible max?'] == True):
            CAPEX = row['casinggas_tiein_CAPEX'] + row['TieIn_CAPEX']
            OPEX = row['casinggas_tiein_OPEX'] +row['TieIn_OPEX']
            ventrate = row['ventvol']
            salesgasincome_annual = ventrate * gasprice * 365  # $CAD/year
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d

            npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
            return npv

        else:
            npv = np.nan
            return npv

    elif row['casinggas_tiein_OPEX'] < 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn low feasible max?'] == True):
            CAPEX = row['casinggas_tiein_CAPEX'] +row['TieIn_CAPEX']
            OPEX = row['casinggas_tiein_OPEX'] +row['TieIn_OPEX']
            ventrate = row['ventvol']
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
            salesgasincome_annual= ventrate * gasprice * 365  # $CAD/year
            npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
            return npv

        else:
            npv = np.nan
            return npv

def casinggastieinco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if row['casinggas_tiein_OPEX'] > 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn high feasible max?'] == True):
            ventrate = row['ventvol']
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d

            npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
            return npv

        else:
            npv = np.nan
            return npv

    elif row['casinggas_tiein_OPEX'] < 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn low feasible max?'] == True):
            ventrate = row['ventvol']
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d

            npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
            return npv

        else:
            npv = np.nan
            return npv

def casinggastieinch4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if row['casinggas_tiein_OPEX'] > 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn high feasible max?'] == True):
            ventrate = row['ventvol']
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d

            npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
            return npv

        else:
            npv = np.nan
            return npv

    elif row['casinggas_tiein_OPEX'] < 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn low feasible max?'] == True):
            ventrate = row['ventvol']
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d

            npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density,
                                   CH4GWPconstants)
            return npv

        else:
            npv = np.nan
            return npv


def VRUVacCombGrid_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        CAPEX = row['VRU_CAPEX'] + row['GridConnect_CAPEX'] + row['Vapcombustor_CAPEX'] * row['VapCombRounded']
        OPEX = row['VRU_OPEX'] + row['GridConnect_OPEX']
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                    10 ** 6))  # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g * 365d/y = tCO2e/y
        salesgasincome_annual=0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def VRUVacCombGridco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                    10 ** 6))  # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g * 365d/y = tCO2e/y

        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def VRUVacCombGridch4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                    10 ** 6))  # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g * 365d/y = tCO2e/y

        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density,
                               CH4GWPconstants)

        return npv
    else:
        npv = np.nan
        return npv

def VRUVacCombGen_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        CAPEX = row['VRU_CAPEX'] + row['Generator_CAPEX'] + row['Vapcombustor_CAPEX'] * row['VapCombRounded']
        OPEX = row['VRU_OPEX']
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        salesgasincome_annual=0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def VRUVacCombGenco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech,
                          discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def VRUVacCombGench4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = emissionsfromtech + griddieselemissions(row['VRU_hp'])
        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
        return npv

    else:
        npv = np.nan
        return npv

def Gasbladdertruck_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech,
                      discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Tie in?'] == False):
        CAPEX = row['GasBladder_CAPEX'] * row['Gasbladdercountrounded']
        OPEX = row['gasstorage_pertruckcost'] * row['numberoftrucksperyear_rounded']
        ventrate = row['ventvol'] #e3m3/d
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  #e3m3/d * %reduced * kg/e3m3 *t/1000kg =  tCO2e/d
        salesgasincome_annual = ventrate * gasprice * 365  # $CAD/year
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def Gasbladdertruckco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech,
                      discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Tie in?'] == False):
        ventrate = row['ventvol'] #e3m3/d
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  #e3m3/d * %reduced * kg/e3m3 *t/1000kg =  tCO2e/d

        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def Gasbladdertruckch4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech,
                      discountrate, ch4density):
    if (row['Flare?'] == False) and (row['Tie in?'] == False):
        ventrate = row['ventvol'] #e3m3/d
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  #e3m3/d * %reduced * kg/e3m3 *t/1000kg =  tCO2e/d

        npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
        return npv

    else:
        npv = np.nan
        return npv


def casestudycostcals(facilitydata_df, techdetails_df, CH4GWPconstants, gasprice, discountrate,ch4density):
    # VRU with Flare and Grid Elec.
    percentreduction = techdetails_df.at['Flare', 'MethaneReduction'] * techdetails_df.at['VRU_25', 'MethaneReduction']
    emissionsfromtech = 0 #tCO2e/day
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['VRUFlareGrid_npvCAD'] = facilitydata_df.apply(VRUFlareGrid_udf, args=(percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUFlareGrid_co2enpvCAD'] = facilitydata_df.apply(VRUFlareGridco2e_udf, args=(percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUFlareGrid_ch4npvCAD'] = facilitydata_df.apply(VRUFlareGridch4_udf, args=(percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)

    # VRU with Flare and Gen Elec.
    VRUFlareGen_udfpercentreduction = techdetails_df.at['Flare', 'MethaneReduction'] * techdetails_df.at['VRU_25', 'MethaneReduction']
    emissionsfromtech = 0  # tCO2e/day
    fuelcostsfromtech = 0  # $CAD/year
    facilitydata_df['VRUFlareGen_npvCAD'] = facilitydata_df.apply(VRUFlareGen_udf, args=(VRUFlareGen_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUFlareGen_co2enpvCAD'] = facilitydata_df.apply(VRUFlareGenco2e_udf, args=(VRUFlareGen_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUFlareGen_ch4npvCAD'] = facilitydata_df.apply(VRUFlareGench4_udf, args=(VRUFlareGen_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate,ch4density), axis=1)

    # VRU with Tie-In and Grid Elec.
    VRUTieInGrid_udfpercentreduction = techdetails_df.at['Casing_tiein_high', 'MethaneReduction'] * techdetails_df.at['VRU_25', 'MethaneReduction']
    emissionsfromtech = 0 #tCO2e/day
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['VRUTieInGrid_npvCAD'] = facilitydata_df.apply(VRUTieInGrid_udf, args=(VRUTieInGrid_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUTieInGrid_co2enpvCAD'] = facilitydata_df.apply(VRUTieInGridco2e_udf, args=(VRUTieInGrid_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUTieInGrid_ch4npvCAD'] = facilitydata_df.apply(VRUTieInGridch4_udf, args=(VRUTieInGrid_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate,ch4density), axis=1)

    # VRU with Tie-In and Gen Elec.
    VRUTieInGen_udfpercentreduction = techdetails_df.at['Casing_tiein_high', 'MethaneReduction'] * techdetails_df.at['VRU_25', 'MethaneReduction']
    emissionsfromtech = 0  # tCO2e/day
    fuelcostsfromtech = 0  # $CAD/year
    facilitydata_df['VRUTieInGen_npvCAD'] = facilitydata_df.apply(VRUTieInGen_udf, args=(VRUTieInGen_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUTieInGen_co2enpvCAD'] = facilitydata_df.apply(VRUTieInGenco2e_udf, args=(VRUTieInGen_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUTieInGen_ch4npvCAD'] = facilitydata_df.apply(VRUTieInGench4_udf, args=(VRUTieInGen_udfpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)

    # VRU with VapComb and Grid Elec.
    vruvapcombpercentreduction = techdetails_df.at['Vapourcombuster_high', 'MethaneReduction'] * techdetails_df.at['VRU_25', 'MethaneReduction']
    emissionsfromtech = 0 #tCO2e/day
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['VRUVapcombGrid_npvCAD'] = facilitydata_df.apply(VRUVacCombGrid_udf, args=(vruvapcombpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUVapcombGrid_co2enpvCAD'] = facilitydata_df.apply(VRUVacCombGridco2e_udf, args=(vruvapcombpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUVapcombGrid_ch4npvCAD'] = facilitydata_df.apply(VRUVacCombGridch4_udf, args=(vruvapcombpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)

    # VRU with VapComb and Gen Elec.
    vapcombpercentreduction = techdetails_df.at['Vapourcombuster_high', 'MethaneReduction'] * techdetails_df.at['VRU_25', 'MethaneReduction']
    emissionsfromtech = 0  # tCO2e/day
    fuelcostsfromtech = 0  # $CAD/year
    facilitydata_df['VRUVapcombGen_npvCAD'] = facilitydata_df.apply(VRUVacCombGen_udf, args=(vapcombpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUVapcombGen_co2enpvCAD'] = facilitydata_df.apply(VRUVacCombGenco2e_udf, args=(vapcombpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['VRUVapcombGen_ch4npvCAD'] = facilitydata_df.apply(VRUVacCombGench4_udf, args=(vapcombpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)


    # Casing Gas Flare
    casinggasflarepercentreduction = techdetails_df.at['Casing_flare_high', 'MethaneReduction']
    emissionsfromtech = 0 #tCO2e/day
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['Casinggasflare_npvCAD'] = facilitydata_df.apply(casinggasflare_udf, args=(casinggasflarepercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['Casinggasflare_co2enpvCAD'] = facilitydata_df.apply(casinggasflareco2e_udf, args=(casinggasflarepercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['Casinggasflare_ch4npvCAD'] = facilitydata_df.apply(casinggasflarech4_udf, args=(casinggasflarepercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)


    # Casing Gas Tie-In
    casinggastieinpercentreduction = techdetails_df.at['Casing_tiein_high', 'MethaneReduction']
    emissionsfromtech = 0 #tCO2e/day
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['Casinggastiein_npvCAD'] = facilitydata_df.apply(casinggastiein_udf, args=(casinggastieinpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['Casinggastiein_co2enpvCAD'] = facilitydata_df.apply(casinggastieinco2e_udf, args=(casinggastieinpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['Casinggastiein_ch4npvCAD'] = facilitydata_df.apply(casinggastieinch4_udf, args=(casinggastieinpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)

    # Gas Bladder with truck transport
    gasbladderpercentreduction = techdetails_df.at['Gasbladder', 'MethaneReduction']
    emissionsfromtech = 0 #tCO2e/day
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['Gasbladdertruck_npvCAD'] = facilitydata_df.apply(Gasbladdertruck_udf, args=(gasbladderpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['Gasbladdertruck_co2enpvCAD'] = facilitydata_df.apply(Gasbladdertruckco2e_udf, args=(gasbladderpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['Gasbladdertruck_ch4npvCAD'] = facilitydata_df.apply(Gasbladdertruckch4_udf, args=(gasbladderpercentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)

    facilitydata_df['VRUFlareGrid_MACCCO2e'] = facilitydata_df['VRUFlareGrid_npvCAD']/facilitydata_df['VRUFlareGrid_co2enpvCAD']
    facilitydata_df['VRUFlareGen_MACCCO2e'] = facilitydata_df['VRUFlareGen_npvCAD']/facilitydata_df['VRUFlareGen_co2enpvCAD']
    facilitydata_df['VRUTieInGrid_MACCCO2e'] = facilitydata_df['VRUTieInGrid_npvCAD']/facilitydata_df['VRUTieInGrid_co2enpvCAD']
    facilitydata_df['VRUTieInGen_MACCCO2e'] = facilitydata_df['VRUTieInGen_npvCAD']/facilitydata_df['VRUTieInGen_co2enpvCAD']
    facilitydata_df['VRUVapcombGrid_MACCCO2e'] = facilitydata_df['VRUVapcombGrid_npvCAD']/facilitydata_df['VRUVapcombGrid_co2enpvCAD']
    facilitydata_df['VRUVapcombGen_MACCCO2e'] = facilitydata_df['VRUVapcombGen_npvCAD']/facilitydata_df['VRUVapcombGen_co2enpvCAD']
    facilitydata_df['Casinggasflare_MACCCO2e'] = facilitydata_df['Casinggasflare_npvCAD']/facilitydata_df['Casinggasflare_co2enpvCAD']
    facilitydata_df['Casinggastiein_MACCCO2e'] = facilitydata_df['Casinggastiein_npvCAD']/facilitydata_df['Casinggastiein_co2enpvCAD']
    facilitydata_df['Gasbladdertruck_MACCCO2e'] = facilitydata_df['Gasbladdertruck_npvCAD']/facilitydata_df['Gasbladdertruck_co2enpvCAD']

    facilitydata_df['VRUFlareGrid_MACCCH4'] = facilitydata_df['VRUFlareGrid_npvCAD'] / facilitydata_df['VRUFlareGrid_ch4npvCAD']
    facilitydata_df['VRUFlareGen_MACCCH4'] = facilitydata_df['VRUFlareGen_npvCAD'] / facilitydata_df['VRUFlareGen_ch4npvCAD']
    facilitydata_df['VRUTieInGrid_MACCCH4'] = facilitydata_df['VRUTieInGrid_npvCAD'] / facilitydata_df['VRUTieInGrid_ch4npvCAD']
    facilitydata_df['VRUTieInGen_MACCCH4'] = facilitydata_df['VRUTieInGen_npvCAD'] / facilitydata_df['VRUTieInGen_ch4npvCAD']
    facilitydata_df['VRUVapcombGrid_MACCCH4'] = facilitydata_df['VRUVapcombGrid_npvCAD'] / facilitydata_df['VRUVapcombGrid_ch4npvCAD']
    facilitydata_df['VRUVapcombGen_MACCCH4'] = facilitydata_df['VRUVapcombGen_npvCAD'] / facilitydata_df['VRUVapcombGen_ch4npvCAD']
    facilitydata_df['Casinggasflare_MACCCH4'] = facilitydata_df['Casinggasflare_npvCAD'] / facilitydata_df['Casinggasflare_ch4npvCAD']
    facilitydata_df['Casinggastiein_MACCCH4'] = facilitydata_df['Casinggastiein_npvCAD'] / facilitydata_df['Casinggastiein_ch4npvCAD']
    facilitydata_df['Gasbladdertruck_MACCCH4'] = facilitydata_df['Gasbladdertruck_npvCAD'] / facilitydata_df['Gasbladdertruck_ch4npvCAD']

    return facilitydata_df

# def identifytech(row):
#     if row['ventvol'] != 0:
#         if (row['Flare?'] == True) and (row['Tie in?'] == True):
#             #check gas bladder costs vs vap comb
#             if (row['Gasbladdertruck_MACCCO2e'] > row['VRUVapcombGrid_MACCCO2e']) or \
#                     (row['VRUTieInGrid_MACCCO2e'] > row['VRUFlareGen_MACCCO2e']) or \
#                     (row['VRUTieInGrid_MACCCO2e'] > row['VRUFlareGen_MACCCO2e']) or \
#                     (row['VRUTieInGrid_MACCCO2e'] > row['VRUFlareGen_MACCCO2e']) or \
#                     (row['VRUTieInGrid_MACCCO2e'] > row['VRUFlareGen_MACCCO2e']) or \:
#             return 'Gas Bladder and Truck'
#         elif (row['Flare?'] == True) and (row['Tie in?'] == False):
#                 if (row['VRUTieInGrid_MACCCO2e'] > row['VRUTieInGen_MACCCO2e']) or \
#                         (row['VRUTieInGrid_MACCCO2e'] > row['VRUFlareGen_MACCCO2e']) or \
#                         (row['VRUTieInGrid_MACCCO2e'] > row['VRUFlareGen_MACCCO2e']) or \
#                         (row['VRUTieInGrid_MACCCO2e'] > row['VRUFlareGen_MACCCO2e']) or \
#                         (row['VRUTieInGrid_MACCCO2e'] > row['VRUFlareGen_MACCCO2e']) or \:
#             return 'Casing or VRU tie in'
#         elif (row['Flare?'] == False) and (row['Tie in?'] == True):
#             return 'Casing or VRU flare'
#         else:
#             return 'Casing or VRU flare or tie in'
#     else:
#         return np.nan

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

def volumereduction_udf(row,CH4GWPconstants,ch4density ):
    if row['Lowest CO2e abatement cost option'] == 'VRUTieInGrid_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.95 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 /3600 * (590/ (10**6)) #hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
        netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGrid_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                10 ** 6))  # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g = tCO2e/d
        netabatement = (ventabatement-emissionsfromtech)*365 #tCO2e/y
        return netabatement

    if row['Lowest CO2e abatement cost option'] == 'VRUVapcombGen_MACCCO2e':
        ventrate = row['ventvol']
        ventabatement = ventrate * 0.99 * CH4GWPconstants * ch4density / 1000  # tCO2e/d
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





if __name__ == '__main__':
    techdetailspath = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\technologydetails.csv"
    techdetails_df = pd.read_csv(techdetailspath)
    techdetails_df = techdetails_df.set_index('technologies')

    facilitydatapath = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\2022v4_oilgasfacilityvol.csv"
    facilitydata_df = pd.read_csv(facilitydatapath)
    ch4gascomposition = 0.84163
    facilitydata_df['ventvol'] = facilitydata_df['VENT_gas'] * ch4gascomposition/30.437 #e3m3/day

    CH4GWPconstants = 28 #co2e/ch4
    gasprice = 3.55 * 39 # $CAD/GJ * GJ/e3MJ * 39e3MJ/e3m3 = $CAD/e3m3
    discountrate = 0.1
    ch4density = 687 #kg/e3m3


    facility_econ_data_df = tech_econ_runs(facilitydata_df, techdetails_df)
    feasbilitycheck_facility_econ_data_df = equip_feasibilityandcount(facility_econ_data_df, techdetails_df)
    techcasestudycosts = casestudycostcals(feasbilitycheck_facility_econ_data_df, techdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density)
    # techcasestudycosts['techselection'] = techcasestudycosts.apply(identifytech, axis=1)
    # techcasestudycosts['Lowest cost'] = techcasestudycosts.apply(identifytech, axis=1)
    # # techcasestudycosts.to_csv('2022_alberta_methanetechcostNPV.csv')
    # filter_results_df = techcasestudycosts[
    #     ['ReportingFacilityID', 'PROD_gas', 'PROD_oil', 'VENT_gas', 'ventvol', 'Flare?', 'Tie in?', 'VRU_size',
    #      'VRU_feasible min?', 'Flare_feasible min?', 'CasingFlare_feasible min?', 'CasingGasTieIn high feasible max?',
    #      'CasingGasTieIn low feasible max?', 'VRUFlareGrid_MACCCO2e', 'VRUFlareGen_MACCCO2e', 'VRUTieInGrid_MACCCO2e',
    #      'VRUTieInGen_MACCCO2e', 'VRUVapcombGrid_MACCCO2e', 'VRUVapcombGen_MACCCO2e', 'Casinggasflare_MACCCO2e',
    #      'Casinggastiein_MACCCO2e', 'Gasbladdertruck_MACCCO2e']]


    filter_results_df = techcasestudycosts[
        ['ReportingFacilityID', 'PROD_gas', 'PROD_oil', 'VENT_gas', 'ventvol', 'Flare?', 'Tie in?', 'VRU_size', 'VRU_hp',
         'VRU_feasible min?', 'Flare_feasible min?', 'CasingFlare_feasible min?', 'CasingGasTieIn high feasible max?',
         'CasingGasTieIn low feasible max?']]
    co2eonlytechnologies_df = techcasestudycosts.iloc[:,90:99]
    co2eonlytechnologies_df['Lowest CO2e abatement cost option'] = co2eonlytechnologies_df.idxmin(axis="columns")
    co2eonlytechnologies_df['Lowest CO2e abatement cost value'] = co2eonlytechnologies_df.apply(co2efiltering, axis=1)
    filter_results_df = filter_results_df.join(co2eonlytechnologies_df)

    ch4eonlytechnologies_df = techcasestudycosts.iloc[:,100:108]
    ch4eonlytechnologies_df['Lowest CH4 abatement cost option'] = ch4eonlytechnologies_df.idxmin(axis="columns")
    ch4eonlytechnologies_df['Lowest CH4 abatement cost value'] = ch4eonlytechnologies_df.apply(ch4filtering, axis=1)
    filter_results_df = filter_results_df.join(ch4eonlytechnologies_df)

    filter_results_df['volumereductionstCO2e/y'] = filter_results_df.apply(volumereduction_udf, args=(CH4GWPconstants,ch4density),axis=1)
    filter_results_df = filter_results_df[filter_results_df['ventvol']>0]
    filter_results_df = filter_results_df.sort_values('Lowest CO2e abatement cost value')

    filter_results_df.to_csv('nocarbonpricing2022_alberta_methanetechcostNPV.csv')
    print(feasbilitycheck_facility_econ_data_df)

    VRU_25_OP = techdetails_df.at['VRU_25', 'OPEX']
    VRU_50_OP = techdetails_df.at['VRU_50', 'OPEX']
    VRU_100_OP = techdetails_df.at['VRU_100', 'OPEX']
    VRU_200_OP = techdetails_df.at['VRU_200', 'OPEX']
    VRU_500_OP = techdetails_df.at['VRU_500', 'OPEX']

    VRU_25_CAP = techdetails_df.at['VRU_25', 'CAPEX']
    VRU_50_CAP = techdetails_df.at['VRU_50', 'CAPEX']
    VRU_100_CAP = techdetails_df.at['VRU_100', 'CAPEX']
    VRU_200_CAP = techdetails_df.at['VRU_200', 'CAPEX']
    VRU_500_CAP = techdetails_df.at['VRU_500', 'CAPEX']

    facilitydata_df['VRU_CAPEX'] = facilitydata_df.apply(VRU_CAPEX_udf, args=(VRU_25_CAP, VRU_50_CAP, VRU_100_CAP, VRU_200_CAP, VRU_500_CAP), axis=1)
    facilitydata_df['VRU_OPEX'] = facilitydata_df.apply(VRU_OPEX_udf, args=(VRU_25_OP, VRU_50_OP, VRU_100_OP, VRU_200_OP, VRU_500_OP), axis=1)



    test_sample_df = facilitydata_df.iloc[1] #no flare, no tie in

    techlist = ['VRU_tiein_grid', 'VRU_tiein_gen', 'VRU_flare_grid', 'VRU_flare_gen', 'Casing_tiein', 'Casing_flare']
    tech_econ_df = pd.DataFrame(columns=techlist)
    tech_econ_df = facilitydata_df[['ReportingFacilityID', 'VENT_gas']]
    tech_econ_df = tech_econ_df.set_index('ReportingFacilityID')
    VRU_tiein_grid_tech_econ_df = VRU_tiein_grid(techdetails_df, test_sample_df, tech_econ_df)

    dataholder = VRU_tiein_grid_tech_econ_df
    print(dataholder)