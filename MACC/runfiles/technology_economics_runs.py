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

    #tie in compressor and pipeline
    facilitydata_df['Compressor_CAPEX'] = facilitydata_df.apply(compressors_CAPEX, args=(compressorintercept, compressorslope), axis=1)
    facilitydata_df['Pipeline_CAPEX'] = facilitydata_df['NEAR_DIST'] * pipelinecost
    facilitydata_df['TieIn_CAPEX'] = facilitydata_df['Compressor_CAPEX'] * facilitydata_df['Pipeline_CAPEX']
    facilitydata_df['TieIn_OPEX'] = facilitydata_df['TieIn_CAPEX'] * 0.1

    #grid connection
    gridcost_CAPEX = techdetails_df.at['Gridconnect', 'CAPEX'] + techdetails_df.at['Gridconnect', 'Installation'] * 1 #km
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

def auxequip_tech_econ_runs(facilitydata_df, techdetails_df):
    #reciprocating compressor
    Vent_ReciCompressor_CAPEX_fixed_Upper = techdetails_df.at[('Vent_ReciCompressor', 'Upper')]['CAPEX'][0] + \
                                                         techdetails_df.at[('Vent_ReciCompressor', 'Upper')]['Installation'][0]
    facilitydata_df['Vent_ReciCompressor_CAPEX_fixed_Upper'] = Vent_ReciCompressor_CAPEX_fixed_Upper

    Vent_ReciCompressor_OPEX_fixed_Upper = techdetails_df.at[('Vent_ReciCompressor', 'Upper')]['OPEX_fixed'][0]
    facilitydata_df['Vent_ReciCompressor_OPEX_fixed_Upper'] = Vent_ReciCompressor_OPEX_fixed_Upper

    Vent_ReciCompressor_CAPEX_fixed_Lower = techdetails_df.at[('Vent_ReciCompressor', 'Lower')]['CAPEX'][0] + \
                                                         techdetails_df.at[('Vent_ReciCompressor', 'Lower')]['Installation'][0]
    facilitydata_df['Vent_ReciCompressor_CAPEX_fixed_Lower'] = Vent_ReciCompressor_CAPEX_fixed_Lower

    Vent_ReciCompressor_OPEX_fixed_Lower = techdetails_df.at[('Vent_ReciCompressor', 'Lower')]['OPEX_fixed'][0]
    facilitydata_df['Vent_ReciCompressor_OPEX_fixed_Lower'] = Vent_ReciCompressor_OPEX_fixed_Lower

    facilitydata_df['Vent_ReciCompressor_CAPEX_fixed_Avg'] = (facilitydata_df['Vent_ReciCompressor_CAPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'Vent_ReciCompressor_CAPEX_fixed_Lower']) / 2

    facilitydata_df['Vent_ReciCompressor_OPEX_fixed_Avg'] = (facilitydata_df['Vent_ReciCompressor_OPEX_fixed_Upper'] + facilitydata_df['Vent_ReciCompressor_OPEX_fixed_Lower'])/2

    #centrifugal compressor
    Vent_ScrewCompressor_CAPEX_fixed_Upper = techdetails_df.at[('Vent_ScrewCompressor', 'Upper')]['CAPEX'][0] + \
                                                            techdetails_df.at[('Vent_ScrewCompressor', 'Upper')]['Installation'][0]
    facilitydata_df['Vent_ScrewCompressor_CAPEX_fixed_Upper'] = Vent_ScrewCompressor_CAPEX_fixed_Upper
    Vent_ScrewCompressor_OPEX_fixed_Upper = techdetails_df.at[('Vent_ScrewCompressor', 'Upper')]['OPEX_fixed'][0]
    facilitydata_df['Vent_ScrewCompressor_OPEX_fixed_Upper'] = Vent_ScrewCompressor_OPEX_fixed_Upper

    Vent_ScrewCompressor_CAPEX_fixed_Lower = techdetails_df.at[('Vent_ScrewCompressor', 'Lower')]['CAPEX'][0] + \
                                                            techdetails_df.at[('Vent_ScrewCompressor', 'Lower')]['Installation'][0]
    facilitydata_df['Vent_ScrewCompressor_CAPEX_fixed_Lower'] = Vent_ScrewCompressor_CAPEX_fixed_Lower

    Vent_ScrewCompressor_OPEX_fixed_Lower = techdetails_df.at[('Vent_ScrewCompressor', 'Lower')]['OPEX_fixed'][0]
    facilitydata_df['Vent_ScrewCompressor_OPEX_fixed_Lower'] = Vent_ScrewCompressor_OPEX_fixed_Lower

    facilitydata_df['Vent_ScrewCompressor_CAPEX_fixed_Avg'] = (facilitydata_df['Vent_ScrewCompressor_CAPEX_fixed_Upper'] +
                                                              facilitydata_df[
                                                                  'Vent_ScrewCompressor_CAPEX_fixed_Lower']) / 2

    facilitydata_df['Vent_ScrewCompressor_OPEX_fixed_Avg'] = (facilitydata_df['Vent_ScrewCompressor_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'Vent_ScrewCompressor_OPEX_fixed_Lower']) / 2

    # level controller
    PneuLevelControl_CAPEX_fixed_Upper = techdetails_df.at[('PneuLevelControl', 'Upper')]['CAPEX'][0] + \
                                                      techdetails_df.at[('PneuLevelControl',  'Upper')]['Installation'][0]
    facilitydata_df['PneuLevelControl_CAPEX_fixed_Upper'] = PneuLevelControl_CAPEX_fixed_Upper

    PneuLevelControl_OPEX_fixed_Upper = techdetails_df.at[('PneuLevelControl', 'Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuLevelControl_OPEX_fixed_Upper'] = PneuLevelControl_OPEX_fixed_Upper

    PneuLevelControl_CAPEX_fixed_Lower = techdetails_df.at[('PneuLevelControl', 'Lower')]['CAPEX'][0] + \
                                                      techdetails_df.at[('PneuLevelControl',  'Lower')]['Installation'][0]
    facilitydata_df['PneuLevelControl_CAPEX_fixed_Lower'] = PneuLevelControl_CAPEX_fixed_Lower

    PneuLevelControl_OPEX_fixed_Lower = techdetails_df.at[('PneuLevelControl', 'Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuLevelControl_OPEX_fixed_Lower'] = PneuLevelControl_OPEX_fixed_Lower

    facilitydata_df['PneuLevelControl_CAPEX_fixed_Avg'] = (facilitydata_df['PneuLevelControl_CAPEX_fixed_Upper']+
                                                              facilitydata_df[
                                                                  'PneuLevelControl_CAPEX_fixed_Lower']) / 2
    facilitydata_df['PneuLevelControl_OPEX_fixed_Avg'] = (facilitydata_df['PneuLevelControl_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'PneuLevelControl_OPEX_fixed_Lower']) / 2

    #chemical pump
    PneuPump_CAPEX_fixed_Upper = techdetails_df.at[('PneuPump', 'Upper')]['CAPEX'][0] + \
                                                      techdetails_df.at[('PneuPump', 'Upper')]['Installation'][0]
    facilitydata_df['PneuPump_CAPEX_fixed_Upper'] =PneuPump_CAPEX_fixed_Upper

    PneuPump_OPEX_fixed_Upper = techdetails_df.at[('PneuPump','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuPump_OPEX_fixed_Upper'] =PneuPump_OPEX_fixed_Upper

    PneuPump_CAPEX_fixed_Lower = techdetails_df.at[('PneuPump', 'Lower')]['CAPEX'][0]+ \
                                                      techdetails_df.at[('PneuPump', 'Lower')]['Installation'][0]
    facilitydata_df['PneuPump_CAPEX_fixed_Lower'] =PneuPump_CAPEX_fixed_Lower

    PneuPump_OPEX_fixed_Lower = techdetails_df.at[('PneuPump','Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuPump_OPEX_fixed_Lower'] =PneuPump_OPEX_fixed_Lower

    facilitydata_df['PneuPump_CAPEX_fixed_Avg'] = (facilitydata_df['PneuPump_CAPEX_fixed_Upper'] +
                                                              facilitydata_df[
                                                                  'PneuPump_CAPEX_fixed_Lower']) / 2
    facilitydata_df['PneuPump_OPEX_fixed_Avg'] = (facilitydata_df['PneuPump_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'PneuPump_OPEX_fixed_Lower']) / 2

    #actuator
    PneuPositioner_CAPEX_fixed_Upper = techdetails_df.at[('PneuPositioner','Upper')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('PneuPositioner','Upper')][ 'Installation'][0]
    facilitydata_df['PneuPositioner_CAPEX_fixed_Upper'] =PneuPositioner_CAPEX_fixed_Upper

    PneuPositioner_OPEX_fixed_Upper = techdetails_df.at[('PneuPositioner','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuPositioner_OPEX_fixed_Upper'] =PneuPositioner_OPEX_fixed_Upper

    PneuPositioner_CAPEX_fixed_Lower = techdetails_df.at[('PneuPositioner','Lower')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('PneuPositioner','Lower')][ 'Installation'][0]
    facilitydata_df['PneuPositioner_CAPEX_fixed_Lower'] =PneuPositioner_CAPEX_fixed_Lower

    PneuPositioner_OPEX_fixed_Lower = techdetails_df.at[('PneuPositioner','Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuPositioner_OPEX_fixed_Lower'] = PneuPositioner_OPEX_fixed_Lower

    facilitydata_df['PneuPositioner_CAPEX_fixed_Avg'] = (facilitydata_df['PneuPositioner_CAPEX_fixed_Upper'] +
                                                              facilitydata_df[
                                                                  'PneuPositioner_CAPEX_fixed_Lower']) / 2
    facilitydata_df['PneuPositioner_OPEX_fixed_Avg'] = (facilitydata_df['PneuPositioner_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'PneuPositioner_OPEX_fixed_Lower']) / 2

    #sm transducer for small facilties
    PneuTransducerSm_CAPEX_fixed_Upper = techdetails_df.at[('PneuTransducerSm','Upper')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('PneuTransducerSm','Upper')][ 'Installation'][0]
    facilitydata_df['PneuTransducerSm_CAPEX_fixed_Upper'] =PneuTransducerSm_CAPEX_fixed_Upper

    PneuTransducerSm_OPEX_fixed_Upper = techdetails_df.at[('PneuTransducerSm','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuTransducerSm_OPEX_fixed_Upper'] =PneuTransducerSm_OPEX_fixed_Upper

    PneuTransducerSm_CAPEX_fixed_Lower = techdetails_df.at[('PneuTransducerSm','Lower')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('PneuTransducerSm','Lower')][ 'Installation'][0]
    facilitydata_df['PneuTransducerSm_CAPEX_fixed_Lower'] =PneuTransducerSm_CAPEX_fixed_Lower

    PneuTransducerSm_OPEX_fixed_Lower = techdetails_df.at[('PneuTransducerSm','Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuTransducerSm_OPEX_fixed_Lower'] = PneuTransducerSm_OPEX_fixed_Lower

    facilitydata_df['PneuTransducerSm_CAPEX_fixed_Avg'] = (facilitydata_df['PneuTransducerSm_CAPEX_fixed_Upper'] +
                                                              facilitydata_df[
                                                                  'PneuTransducerSm_CAPEX_fixed_Lower']) / 2
    facilitydata_df['PneuTransducerSm_OPEX_fixed_Avg'] = (facilitydata_df['PneuTransducerSm_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'PneuTransducerSm_OPEX_fixed_Lower']) / 2
    #lg transducer for large facilties
    PneuTransducerLg_CAPEX_fixed_Upper = techdetails_df.at[('PneuTransducerLg','Upper')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('PneuTransducerLg','Upper')][ 'Installation'][0]
    facilitydata_df['PneuTransducerLg_CAPEX_fixed_Upper'] = PneuTransducerLg_CAPEX_fixed_Upper

    PneuTransducerLg_OPEX_fixed_Upper = techdetails_df.at[('PneuTransducerLg','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuTransducerLg_OPEX_fixed_Upper'] = PneuTransducerLg_OPEX_fixed_Upper

    PneuTransducerLg_CAPEX_fixed_Lower = techdetails_df.at[('PneuTransducerLg','Lower')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('PneuTransducerLg','Lower')][ 'Installation'][0]
    facilitydata_df['PneuTransducerLg_CAPEX_fixed_Lower'] = PneuTransducerLg_CAPEX_fixed_Lower

    PneuTransducerLg_OPEX_fixed_Lower = techdetails_df.at[('PneuTransducerLg','Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['PneuTransducerLg_OPEX_fixed_Lower'] = PneuTransducerLg_OPEX_fixed_Lower


    facilitydata_df['PneuTransducerLg_CAPEX_fixed_Avg'] = (facilitydata_df['PneuTransducerLg_CAPEX_fixed_Upper'] +
                                                              facilitydata_df[
                                                                  'PneuTransducerLg_CAPEX_fixed_Lower']) / 2
    facilitydata_df['PneuTransducerLg_OPEX_fixed_Avg'] = (facilitydata_df['PneuTransducerLg_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'PneuTransducerLg_OPEX_fixed_Lower']) / 2

    #glycol flare
    GlycolDehy_Flare_CAPEX_fixed_Upper = techdetails_df.at[('GlycolDehy_Flare','Upper')][ 'CAPEX'][0]+ \
                                                      techdetails_df.at[('GlycolDehy_Flare','Upper')][ 'Installation'][0]
    facilitydata_df['GlycolDehy_Flare_CAPEX_fixed_Upper'] = GlycolDehy_Flare_CAPEX_fixed_Upper

    GlycolDehy_Flare_OPEX_fixed_Upper = techdetails_df.at[('GlycolDehy_Flare','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['GlycolDehy_Flare_OPEX_fixed_Upper'] = GlycolDehy_Flare_OPEX_fixed_Upper

    GlycolDehy_Flare_CAPEX_fixed_Lower = techdetails_df.at[('GlycolDehy_Flare','Lower')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('GlycolDehy_Flare','Lower')][ 'Installation'][0]
    facilitydata_df['GlycolDehy_Flare_CAPEX_fixed_Lower'] = GlycolDehy_Flare_CAPEX_fixed_Lower

    GlycolDehy_Flare_OPEX_fixed_Lower = techdetails_df.at[('GlycolDehy_Flare','Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['GlycolDehy_Flare_OPEX_fixed_Lower'] = GlycolDehy_Flare_OPEX_fixed_Lower

    facilitydata_df['GlycolDehy_Flare_CAPEX_fixed_Avg'] = (facilitydata_df['GlycolDehy_Flare_CAPEX_fixed_Upper'] +
                                                              facilitydata_df[
                                                                  'GlycolDehy_Flare_CAPEX_fixed_Lower']) / 2
    facilitydata_df['GlycolDehy_Flare_OPEX_fixed_Avg'] = (facilitydata_df['GlycolDehy_Flare_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'GlycolDehy_Flare_OPEX_fixed_Lower']) / 2

    #glycol vent capture
    GlycolDehy_Vent_CAPEX_fixed_Upper = techdetails_df.at[('GlycolDehy_Vent','Upper')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('GlycolDehy_Vent','Upper')][ 'Installation'][0]
    facilitydata_df['GlycolDehy_Vent_CAPEX_fixed_Upper'] = GlycolDehy_Vent_CAPEX_fixed_Upper

    GlycolDehy_Vent_OPEX_fixed_Upper = techdetails_df.at[('GlycolDehy_Vent','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['GlycolDehy_Vent_OPEX_fixed_Upper'] = GlycolDehy_Vent_OPEX_fixed_Upper

    GlycolDehy_Vent_CAPEX_fixed_Lower = techdetails_df.at[('GlycolDehy_Vent','Lower')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('GlycolDehy_Vent','Lower')][ 'Installation'][0]
    facilitydata_df['GlycolDehy_Vent_CAPEX_fixed_Lower'] = GlycolDehy_Vent_CAPEX_fixed_Lower

    GlycolDehy_Vent_OPEX_fixed_Lower = techdetails_df.at[('GlycolDehy_Vent','Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['GlycolDehy_Vent_OPEX_fixed_Lower'] = GlycolDehy_Vent_OPEX_fixed_Lower

    facilitydata_df['GlycolDehy_Vent_CAPEX_fixed_Avg'] = (facilitydata_df['GlycolDehy_Vent_CAPEX_fixed_Upper'] +
                                                              facilitydata_df[
                                                                  'GlycolDehy_Vent_CAPEX_fixed_Lower']) / 2
    facilitydata_df['GlycolDehy_Vent_OPEX_fixed_Avg'] = (facilitydata_df['GlycolDehy_Vent_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'GlycolDehy_Vent_OPEX_fixed_Lower']) / 2

    #all pneumatics electric
    AllPneu_Elec_CAPEX_fixed_Upper = techdetails_df.at[('AllPneu_Elec','Upper')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('AllPneu_Elec','Upper')][ 'Installation'][0]
    facilitydata_df['AllPneu_Elec_CAPEX_fixed_Upper'] = AllPneu_Elec_CAPEX_fixed_Upper

    AllPneu_Elec_OPEX_fixed_Upper = techdetails_df.at[('AllPneu_Elec','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['AllPneu_Elec_OPEX_fixed_Upper'] = AllPneu_Elec_OPEX_fixed_Upper
    AllPneu_Elec_CAPEX_fixed_Lower = techdetails_df.at[('AllPneu_Elec','Lower')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('AllPneu_Elec','Lower')][ 'Installation'][0]
    facilitydata_df['AllPneu_Elec_CAPEX_fixed_Lower'] = AllPneu_Elec_CAPEX_fixed_Lower

    AllPneu_Elec_OPEX_fixed_Lower = techdetails_df.at[('AllPneu_Elec','Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['AllPneu_Elec_OPEX_fixed_Lower'] = AllPneu_Elec_OPEX_fixed_Lower


    facilitydata_df['AllPneu_Elec_CAPEX_fixed_Avg'] = (facilitydata_df['AllPneu_Elec_CAPEX_fixed_Upper'] +
                                                              facilitydata_df[
                                                                  'AllPneu_Elec_CAPEX_fixed_Lower']) / 2
    facilitydata_df['AllPneu_Elec_OPEX_fixed_Avg'] = (facilitydata_df['AllPneu_Elec_OPEX_fixed_Upper'] +
                                                             facilitydata_df[
                                                                 'AllPneu_Elec_OPEX_fixed_Lower']) / 2

    #all pneumatics IA, selected based on size of vent demand not based on average
    AllPneu_Air1_CAPEX_fixed_Upper = techdetails_df.at[('AllPneu_Air1','Upper')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('AllPneu_Air1','Upper')][ 'Installation'][0]
    facilitydata_df['AllPneu_Air1_CAPEX_fixed_Upper'] = AllPneu_Air1_CAPEX_fixed_Upper

    AllPneu_Air1_OPEX_fixed_Upper = techdetails_df.at[('AllPneu_Air1','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['AllPneu_Air1_OPEX_fixed_Upper'] = AllPneu_Air1_OPEX_fixed_Upper

    AllPneu_Air1_CAPEX_fixed_Lower = techdetails_df.at[('AllPneu_Air1','Lower')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('AllPneu_Air1','Lower')][ 'Installation'][0]
    facilitydata_df['AllPneu_Air1_CAPEX_fixed_Lower'] = AllPneu_Air1_CAPEX_fixed_Lower

    AllPneu_Air1_OPEX_fixed_Lower = techdetails_df.at[('AllPneu_Air1','Lower')][ 'OPEX_fixed'][0]
    facilitydata_df['AllPneu_Air1_OPEX_fixed_Lower'] = AllPneu_Air1_OPEX_fixed_Lower

    AllPneu_Air2_CAPEX_fixed_Upper = techdetails_df.at[('AllPneu_Air2','Upper')][ 'CAPEX'][0] + \
                                                      techdetails_df.at[('AllPneu_Air2','Upper')][ 'Installation'][0]
    facilitydata_df['AllPneu_Air2_CAPEX_fixed_Upper'] = AllPneu_Air2_CAPEX_fixed_Upper

    AllPneu_Air2_OPEX_fixed_Upper = techdetails_df.at[('AllPneu_Air2','Upper')][ 'OPEX_fixed'][0]
    facilitydata_df['AllPneu_Air2_OPEX_fixed_Upper'] = AllPneu_Air2_OPEX_fixed_Upper

    return facilitydata_df
    #
    # facilitydata_df['AllPneu_Air1_CAPEX_fixed_Avg'] = (facilitydata_df['AllPneu_Air1_CAPEX_fixed_Upper'] +
    #                                                           facilitydata_df[
    #                                                               'AllPneu_Air1_CAPEX_fixed_Lower']) / 2
    # facilitydata_df['AllPneu_Air1_OPEX_fixed_Avg'] = (facilitydata_df['AllPneu_Air1_OPEX_fixed_Upper'] +
    #                                                          facilitydata_df[
    #                                                              'AllPneu_Air1_OPEX_fixed_Lower']) / 2
    #
    #
    # facilitydata_df['AllPneu_Air2_CAPEX_fixed_Avg'] = (facilitydata_df['AllPneu_Air2_CAPEX_fixed_Upper'] +
    #                                                           facilitydata_df[
    #                                                               'AllPneu_Air2_CAPEX_fixed_Lower']) / 2
    # facilitydata_df['AllPneu_Air2_OPEX_fixed_Avg'] = (facilitydata_df['AllPneu_Air2_OPEX_fixed_Upper'] +
    #                                                          facilitydata_df[
    #                                                              'AllPneu_Air2_OPEX_fixed_Lower']) / 2




