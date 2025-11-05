import pandas as pd
import numpy as np
import regex as re

def getDataAB(month):

    try:
        facilityfile_path = "./data/AER/Vol_2022-0" +  str(month) + "-AB.csv"
        datafile_facility_df = pd.read_csv(facilityfile_path)
    except:
        facilityfile_path = "./data/AER/Vol_2022-" + str(month) + "-AB.csv"
        datafile_facility_df = pd.read_csv(facilityfile_path)

    gasprod_only_datafile_df = datafile_facility_df[datafile_facility_df['ProductID'] == 'GAS']
    oilprod_only_datafile_df = datafile_facility_df[datafile_facility_df['ProductID'] == 'OIL']

    sortedgasprod_DataFile_df = gasprod_only_datafile_df.fillna(0)[['ActivityID', 'ReportingFacilityID', 'Volume']].groupby(['ActivityID', 'ReportingFacilityID'], as_index=False, sort=False).sum()
    sortedgasprod_DataFile_df = sortedgasprod_DataFile_df.reset_index()
    sortedoilprod_DataFile_df = oilprod_only_datafile_df.fillna(0)[['ActivityID', 'ReportingFacilityID', 'Volume']].groupby(['ActivityID', 'ReportingFacilityID'], as_index=False, sort=False).sum()
    sortedoilprod_DataFile_df = sortedoilprod_DataFile_df.reset_index()

    gasprod_only_datafile_df = gasprod_only_datafile_df['ReportingFacilityID'].unique().tolist()
    oilprod_only_datafile_df = oilprod_only_datafile_df['ReportingFacilityID'].unique().tolist()

    return sortedgasprod_DataFile_df,sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df, datafile_facility_df

def getDataSK(month):

    try:
        facilityfile_path = "./data/SK/Vol_2022-0" +  str(month) + "-SK.csv"
        datafile_facility_df = pd.read_csv(facilityfile_path)
    except:
        facilityfile_path = "./data/SK/Vol_2022-" + str(month) + "-SK.csv"
        datafile_facility_df = pd.read_csv(facilityfile_path)

    gasprod_only_datafile_df = datafile_facility_df[datafile_facility_df['ProductID'] == 'GAS']
    gasprod_only_datafile_df['Volume'] = gasprod_only_datafile_df['Volume'].astype(dtype=float, errors='ignore')
    oilprod_only_datafile_df = datafile_facility_df[datafile_facility_df['ProductID'] == 'OIL']
    oilprod_only_datafile_df['Volume'] = oilprod_only_datafile_df['Volume'].astype(dtype=float, errors='ignore')

    sortedgasprod_DataFile_df = gasprod_only_datafile_df.fillna(0)[['ActivityID', 'ReportingFacilityID', 'Volume']].groupby(['ActivityID', 'ReportingFacilityID'], as_index=False, sort=False).sum()
    sortedgasprod_DataFile_df = sortedgasprod_DataFile_df.reset_index()
    sortedoilprod_DataFile_df = oilprod_only_datafile_df.fillna(0)[['ActivityID', 'ReportingFacilityID', 'Volume']].groupby(['ActivityID', 'ReportingFacilityID'], as_index=False, sort=False).sum()
    sortedoilprod_DataFile_df = sortedoilprod_DataFile_df.reset_index()

    gasprod_only_datafile_df = gasprod_only_datafile_df['ReportingFacilityID'].unique().tolist()
    oilprod_only_datafile_df = oilprod_only_datafile_df['ReportingFacilityID'].unique().tolist()

    return sortedgasprod_DataFile_df,sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df, datafile_facility_df

def getDataBC():
    facilityfile_path = "./data/BC/Vol_2022_BC.csv"
    datafile_facility_df = pd.read_csv(facilityfile_path)

    gasprod_only_datafile_df = datafile_facility_df[datafile_facility_df['ProductID'] == 'GAS']
    gasprod_only_datafile_df['Volume'] = gasprod_only_datafile_df['Volume'].astype(dtype=float, errors='ignore')
    oilprod_only_datafile_df = datafile_facility_df[datafile_facility_df['ProductID'] == 'OIL']
    oilprod_only_datafile_df['Volume'] = oilprod_only_datafile_df['Volume'].astype(dtype=float, errors='ignore')

    sortedgasprod_DataFile_df = gasprod_only_datafile_df.fillna(0)[['ActivityID', 'ReportingFacilityID', 'Volume']].groupby(['ActivityID', 'ReportingFacilityID'], as_index=False, sort=False).sum()
    sortedgasprod_DataFile_df = sortedgasprod_DataFile_df.reset_index()
    sortedoilprod_DataFile_df = oilprod_only_datafile_df.fillna(0)[['ActivityID', 'ReportingFacilityID', 'Volume']].groupby(['ActivityID', 'ReportingFacilityID'], as_index=False, sort=False).sum()
    sortedoilprod_DataFile_df = sortedoilprod_DataFile_df.reset_index()

    gasprod_only_datafile_df = gasprod_only_datafile_df['ReportingFacilityID'].unique().tolist()
    oilprod_only_datafile_df = oilprod_only_datafile_df['ReportingFacilityID'].unique().tolist()

    return sortedgasprod_DataFile_df,sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df, datafile_facility_df

def flatten_well_activity(sortedgasprod_DataFile_df,sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df):

    gasprod_facility_list = pd.DataFrame(index=gasprod_only_datafile_df)
    oilprod_facility_list = pd.DataFrame(index=oilprod_only_datafile_df)
    for column in ['PROD', 'FUEL', 'DISP', 'FLARE', 'VENT']:
        gasprod_facility_list = gasprod_facility_list.join(sortedgasprod_DataFile_df[sortedgasprod_DataFile_df['ActivityID'] == column].set_index('ReportingFacilityID')['Volume'])
        gasprod_facility_list = gasprod_facility_list.rename(columns={'Volume': column})
        oilprod_facility_list = oilprod_facility_list.join(sortedoilprod_DataFile_df[sortedoilprod_DataFile_df['ActivityID'] == column].set_index('ReportingFacilityID')['Volume'])
        oilprod_facility_list = oilprod_facility_list.rename(columns={'Volume': column})

    return gasprod_facility_list, oilprod_facility_list

def facility_subtype_sort(datafile_facility_df):
    datafile_facility_df = datafile_facility_df.drop_duplicates(subset=['ReportingFacilityID'])
    datafile_facility_df = datafile_facility_df.set_index('ReportingFacilityID')
    facility_subtype_only_df = datafile_facility_df['ReportingFacilitySubType']

    return facility_subtype_only_df

def facility_subtype_runs_AB(month):
    sortedgasprod_DataFile_df, sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df, datafile_facility_df = getDataAB(month)
    gasprod_report_volumes, oilprod_report_volumes = flatten_well_activity(sortedgasprod_DataFile_df,sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df)
    og_reporting_volumes_df = gasprod_report_volumes.join(oilprod_report_volumes, lsuffix='_gas', rsuffix='_oil')

    fac_subtype_df = facility_subtype_sort(datafile_facility_df)
    facility_subtype_reporting_volumes_df = og_reporting_volumes_df.join(fac_subtype_df)
    facility_subtype_reporting_volumes_df = facility_subtype_reporting_volumes_df.fillna(0)
    facility_subtype_reporting_volumes_df = facility_subtype_reporting_volumes_df.sort_values(by='ReportingFacilitySubType', ascending=True)

    facility_subtype_reporting_volumes_df['Month of Production'] = month
    return facility_subtype_reporting_volumes_df

def facility_subtype_runs_SK(month):
    sortedgasprod_DataFile_df, sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df, datafile_facility_df = getDataSK(month)
    gasprod_report_volumes, oilprod_report_volumes = flatten_well_activity(sortedgasprod_DataFile_df,sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df)
    og_reporting_volumes_df = gasprod_report_volumes.join(oilprod_report_volumes, lsuffix='_gas', rsuffix='_oil')

    fac_subtype_df = facility_subtype_sort(datafile_facility_df)
    facility_subtype_reporting_volumes_df = og_reporting_volumes_df.join(fac_subtype_df)
    facility_subtype_reporting_volumes_df = facility_subtype_reporting_volumes_df.fillna(0)
    facility_subtype_reporting_volumes_df = facility_subtype_reporting_volumes_df.sort_values(by='ReportingFacilitySubType', ascending=True)

    facility_subtype_reporting_volumes_df['Month of Production'] = month
    return facility_subtype_reporting_volumes_df

def facility_subtype_runs_BC():
    sortedgasprod_DataFile_df, sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df, datafile_facility_df = getDataBC()
    gasprod_report_volumes, oilprod_report_volumes = flatten_well_activity(sortedgasprod_DataFile_df,sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df)
    og_reporting_volumes_df = gasprod_report_volumes.join(oilprod_report_volumes, lsuffix='_gas', rsuffix='_oil')

    fac_subtype_df = facility_subtype_sort(datafile_facility_df)
    facility_subtype_reporting_volumes_df = og_reporting_volumes_df.join(fac_subtype_df)
    facility_subtype_reporting_volumes_df = facility_subtype_reporting_volumes_df.fillna(0)
    facility_subtype_reporting_volumes_df = facility_subtype_reporting_volumes_df.sort_values(by='ReportingFacilitySubType', ascending=True)

    return facility_subtype_reporting_volumes_df

def oilemissionscalc(facility_subtype_reporting_volumes_df):

    oilemissionsfile_path = "./data/oilfacilityemissions_ef.csv"
    oil_facility_df = pd.read_csv(oilemissionsfile_path)
    oil_facility_df = oil_facility_df.set_index('ReportingFacilityID')

    data_holding_df = pd.DataFrame()

    for facility in [311, 321, 322]:
        temp_facility_vol_df = facility_subtype_reporting_volumes_df[facility_subtype_reporting_volumes_df['ReportingFacilitySubType'] == facility]
        tankemissionspercentage = oil_facility_df.loc[facility, '%oftankemissions']
        temp_facility_vol_df['Vent from Tanks'] = temp_facility_vol_df.VENT_gas * tankemissionspercentage
        temp_facility_vol_df = temp_facility_vol_df.reset_index()
        data_holding_df = pd.concat([data_holding_df, temp_facility_vol_df])

        print(data_holding_df)

    return data_holding_df

def gasemissionscalc(data_holding_df, facility_subtype_reporting_volumes_df):

    gasemissionsfile_path = "./data/gasfacilityemissions_ef.csv"
    gas_facility_df = pd.read_csv(gasemissionsfile_path)
    gas_facility_df = gas_facility_df.set_index('ReportingFacilityID')

    for facility in [351, 361, 362, 363, 364]:
        temp_facility_vol_df = facility_subtype_reporting_volumes_df[facility_subtype_reporting_volumes_df['ReportingFacilitySubType'] == facility]
        tankemissionspercentage = gas_facility_df.loc[facility, '%oftankemissions']
        temp_facility_vol_df['Vent from Tanks'] = temp_facility_vol_df.VENT_gas * tankemissionspercentage
        temp_facility_vol_df = temp_facility_vol_df.reset_index()
        data_holding_df = pd.concat([data_holding_df, temp_facility_vol_df])

        print(data_holding_df)

    return data_holding_df

def gas_analysis_methane_UDF_AB(pipedist_averaged_reported_facility_vol_df):
    #----- ADD FLUID ANALYSIS DETAILS--------------------------
    fluidanalysis_path = "./data/GeoSCOUT/AB_fluidanalysis_AccessedMay2023.csv"
    fluidanalysis_df = pd.read_csv(fluidanalysis_path)

    #Convert UWI from long to short
    fluidanalysis_df = fluidanalysis_df[fluidanalysis_df['Well Identifier'].notna()]
    fluidanalysis_df['SurfLocUWI'] = fluidanalysis_df['Well Identifier'].apply(short_UWI_UDF)

    #Take subset of fluid analysis dataframe for join
    data_file_fluidanalysis_df = fluidanalysis_df[['SurfLocUWI', 'Well Identifier', 'Formation', 'Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)', 'Gross Heating Value(MJ/m3)', 'C1 Air Free']]
    data_file_fluidanalysis_df[['Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)', 'Gross Heating Value(MJ/m3)', 'C1 Air Free']] = data_file_fluidanalysis_df[['Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)', 'Gross Heating Value(MJ/m3)', 'C1 Air Free']].apply(pd.to_numeric)

    #Fill empty C1 Air Free concentration data
    data_file_fluidanalysis_df['C1 Air Free'] = data_file_fluidanalysis_df['C1 Air Free'].fillna(data_file_fluidanalysis_df['C1 Air Free'].mean(axis=0))

    #Join fluid analysis to data file and return back to main
    new_pipedist_averaged_vol = pipedist_averaged_reported_facility_vol_df.set_index('Surf. Loc.').join(data_file_fluidanalysis_df.set_index('SurfLocUWI'))

    return new_pipedist_averaged_vol

def gas_analysis_methane_UDF_SK(pipedist_averaged_reported_facility_vol_df):
    #----- ADD FLUID ANALYSIS DETAILS--------------------------
    fluidanalysis_path = "./data/GeoSCOUT/SK_fluidanalysis_AccessedMay2023.csv"
    fluidanalysis_df = pd.read_csv(fluidanalysis_path)

    #Convert UWI from long to short
    fluidanalysis_df = fluidanalysis_df[fluidanalysis_df['Well Identifier'].notna()]
    fluidanalysis_df['SurfLocUWI'] = fluidanalysis_df['Well Identifier'].apply(short_UWI_UDF)

    #Take subset of fluid analysis dataframe for join
    data_file_fluidanalysis_df = fluidanalysis_df[['SurfLocUWI', 'Well Identifier', 'Formation', 'Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)', 'Gross Heating Value(MJ/m3)', 'C1 Air Free']]

    #Fill empty C1 Air Free concentration data
    data_file_fluidanalysis_df['C1 Air Free'] = data_file_fluidanalysis_df['C1 Air Free'].fillna(data_file_fluidanalysis_df['C1 Air Free'].mean(axis=0))

    #Join fluid analysis to data file and return back to main
    new_pipedist_averaged_vol = pipedist_averaged_reported_facility_vol_df.reset_index(names=['ReportingFacilityID']).set_index('Surf. Loc.').join(data_file_fluidanalysis_df.set_index('SurfLocUWI'))

    return new_pipedist_averaged_vol


def year_UDF(row):
    dates = str(row['Date Well Spudded'])
    year = dates[0:4]
    return year

def pipedistance_AB(averaged_reported_facility_vol_df):
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.reset_index('ReportingFacilityID')

    abdata_path = "./data/Shapefiles/Well Infrastructure-AB.csv"
    abdata_df = pd.read_csv(abdata_path)

    welldata_path = "./data/GeoSCOUT/AB_welldata_AccessedMay2023.csv"
    welldata_df = pd.read_csv(welldata_path,encoding='cp1252')
    prod_type = ['Pump OIL', 'Pump GAS']
    welldata_df = welldata_df[welldata_df['Well Status Text'].isin(prod_type)]
    welldata_df = welldata_df[['CPA Well ID','Well Status Text', 'Surf. Loc.', 'Date Well Spudded']]
    welldata_df['Year Well Spudded'] = welldata_df.apply(year_UDF, axis=1)
    abdata_df = abdata_df.set_index('WellIdentifier').join(welldata_df.set_index('CPA Well ID'), how='left')
    abdata_df = abdata_df[['Well Status Text', 'Surf. Loc.', 'Date Well Spudded', 'Year Well Spudded', 'Surface DLS', 'LinkedFacilityID']]
    abdata_df = gas_analysis_methane_UDF_AB(abdata_df)

    shapefilewell_path = "./data/Shapefiles/ST37_SH_GCS_NAD83.csv"
    datafile_well_df = pd.read_csv(shapefilewell_path)

    neartable_path = "./data/Shapefiles/ngstatus_neartable_TableToExcel.csv"
    datafile_neartable_df = pd.read_csv(neartable_path)

    pipeline_path = "./data/Shapefiles/ngstatus1TableToExcel.csv"
    pipelinedata_df = pd.read_csv(pipeline_path)

    well_pipeline_neartable_df = datafile_well_df.set_index('FID').join(datafile_neartable_df.set_index('IN_FID'))
    well_pipeline_neartable_df = well_pipeline_neartable_df.reset_index(names=['FID'])

    ab_well_pipeline_neartable_df = well_pipeline_neartable_df.set_index('SurfLoc').join(abdata_df.set_index('Surface DLS'))
    ab_well_pipeline_neartable_df = ab_well_pipeline_neartable_df.reset_index(names=['SurfLoc'])

    pipelinedata_ab_well_pipeline_neartable_df = ab_well_pipeline_neartable_df.set_index('NEAR_FID').join(pipelinedata_df.set_index('OBJECTID_1'), how='left',  lsuffix='_main', rsuffix='_pipelinedata')
    pipelinedata_ab_well_pipeline_neartable_df = pipelinedata_ab_well_pipeline_neartable_df.reset_index(names=['NEAR_FID'])

    only_pipedist_facility = pipelinedata_ab_well_pipeline_neartable_df[['LinkedFacilityID', 'Latitude', 'Longitude', 'NEAR_DIST', 'PIPE_MAOP', 'SurfLoc', 'Date Well Spudded', 'Year Well Spudded', 'Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)', 'Gross Heating Value(MJ/m3)', 'C1 Air Free']]
    only_pipedist_facility[["Year Well Spudded"]] = only_pipedist_facility[["Year Well Spudded"]].apply(pd.to_numeric)
    only_pipedist_facility = only_pipedist_facility.groupby(['LinkedFacilityID', 'SurfLoc', 'Date Well Spudded']).mean()
    only_pipedist_facility = only_pipedist_facility.reset_index(names=['LinkedFacilityID', 'SurfLoc', 'Date Well Spudded'])
    only_pipedist_facility = only_pipedist_facility.set_index(['LinkedFacilityID'])

    connect_pipeline_distance_df = averaged_reported_facility_vol_df.set_index('ReportingFacilityID').join(only_pipedist_facility, how='left')

    # connect_pipeline_distance_df = averaged_reported_facility_vol_df.set_index('ReportingFacilityLocation').join(
    #     only_pipedist_facility.set_index('SurfLoc'), how='left')
    connect_pipeline_distance_df['Area'] = 'AB'
    return connect_pipeline_distance_df

def SK_BT_namechange_UDF(row):
    facilityID = str(row['ReportingFacilityID'])
    SKBTfacilityID = "SKBT" + facilityID

    return SKBTfacilityID

def pipedistance_SK(averaged_reported_facility_vol_df):
    SK_facilitytowell_path = "./data/Shapefiles/Well to Facility Link-SK.csv"
    SK_facilitytowell_df = pd.read_csv(SK_facilitytowell_path)
    SK_facilitytowell_df = SK_facilitytowell_df[['LinkedFacilityID', 'WellIdentifier']]

    vertical_well_pipeline_path = "./data/Shapefiles/vertical_well_SK_pipelines.csv"
    vertical_well_pipeline_prox_df = pd.read_csv(vertical_well_pipeline_path)
    nonvertical_well_pipeline_path = "./data/Shapefiles/nonvertical_well_SK_pipelines.csv"
    nonvertical_well_pipeline_prox = pd.read_csv(nonvertical_well_pipeline_path)
    SK_well_pipeline = pd.concat([vertical_well_pipeline_prox_df, nonvertical_well_pipeline_prox]).set_index('SURFACELANDLOCATION')
    SK_well_pipeline = SK_well_pipeline[['NEAR_DIST', 'BOTTOMHOLELANDLOCATION']]

    SK_welldata_path = "./data/GeoSCOUT/SK_welldata_AccessedMay2023.csv"
    SK_welldata_df = pd.read_csv(SK_welldata_path,encoding='cp1252')
    SK_welldata_df = SK_welldata_df[['CPA Well ID', 'Surf. Loc.', 'Area', 'Well Status Text', 'Date Well Spudded']]
    SK_welldata_df['Year Well Spudded'] = SK_welldata_df.apply(year_UDF, axis=1)

    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.join(SK_facilitytowell_df.set_index('LinkedFacilityID'),how='outer')
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.reset_index(names=['ReportingFacilityID'])

    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.set_index('WellIdentifier').join(SK_welldata_df.set_index('CPA Well ID'),how='outer')
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.reset_index(names=['CPA Well ID'])
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.set_index('Surf. Loc.').join(SK_well_pipeline,how='outer')
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.reset_index(names=['Surf. Loc.'])
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.dropna(subset=['ReportingFacilityID']).set_index('ReportingFacilityID')
    averaged_reported_facility_vol_df['NEAR_DIST'] = averaged_reported_facility_vol_df['NEAR_DIST'].fillna(averaged_reported_facility_vol_df['NEAR_DIST'].mean(axis=0))

    facilityprod = ['Act GAS Prod', 'Act OIL Prod']
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df[averaged_reported_facility_vol_df['Well Status Text'].isin(facilityprod)]

    return averaged_reported_facility_vol_df

def short_UWI_UDF(row):
    shortened_UWI = row[4:18]
    return shortened_UWI

def BC_facility_gasanalysis_pipeline(BC_facility_df):
    BC_facility_link_path = "./data/BC/BC_facility_linkage.csv"
    BC_facility_link_df = pd.read_csv(BC_facility_link_path)

    BC_pipedistance_link_path = "./data/Shapefiles/BC_pipeline_near.csv"
    BC_pipedistance_link_df = pd.read_csv(BC_pipedistance_link_path)
    BC_pipedistance_link_df = BC_pipedistance_link_df[['WELL_NAME', 'NEAR_DIST']]
    BC_pipedistance_link_df['NEAR_DIST'] = BC_pipedistance_link_df['NEAR_DIST'].apply(pd.to_numeric)

    BC_welldata_path = "./data/GeoSCOUT/BC_welldata_AccessedMay2023.csv"
    BC_welldata_df = pd.read_csv(BC_welldata_path, encoding='cp1252')
    BC_welldata_df = BC_welldata_df[['Well Name', 'CPA Well ID', 'Well Status Text', 'Surf. Loc.', 'Date Well Spudded', 'Lic/WA/WID/Permit #']]
    BC_welldata_df['Year Well Spudded'] = BC_welldata_df.apply(year_UDF, axis=1)

    BC_gasanalysis_path = "./data/GeoSCOUT/BC_fluidanalysis_AccessedMay2023.csv"
    BC_gasanalysis_df = pd.read_csv(BC_gasanalysis_path)
    BC_gasanalysis_df = BC_gasanalysis_df[
        ['Well Name', 'Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)',
         'Gross Heating Value(MJ/m3)', 'C1 Air Free']]
    BC_gasanalysis_df[
        ['Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)', 'Gross Heating Value(MJ/m3)', 'C1 Air Free']] = BC_gasanalysis_df[
        ['Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)', 'Gross Heating Value(MJ/m3)', 'C1 Air Free']].apply(
        pd.to_numeric)

    BC_pipedistance_link_df, BC_welldata_df = removedspaces(BC_pipedistance_link_df, BC_welldata_df)

    joinedtest = BC_welldata_df.set_index('WellName_nospace').join(BC_pipedistance_link_df.set_index('WellName_nospace'), how='left')
    joinedtest = joinedtest.reset_index(names='WellName_nospace')
    joinedtest = joinedtest.set_index('Lic/WA/WID/Permit #').join(BC_facility_link_df.set_index('FROMWANUM'), how='left')
    joinedtest = joinedtest.reset_index(names='WA Num')
    joinedtest = joinedtest.set_index('Well Name').join(BC_gasanalysis_df.set_index('Well Name'), how='left')
    joinedtest = joinedtest.reset_index(names='Well Name')
    joinedtest['Year Well Spudded'] = joinedtest['Year Well Spudded'].apply(pd.to_numeric)
    joinedtest = joinedtest[['FACILITYNAME','Year Well Spudded', 'C1 Air Free']].groupby(['FACILITYNAME']).mean()

    BC_facility_df = BC_facility_df.set_index('Facility Name')
    BC_facility_df = BC_facility_df.join(joinedtest, how='left')
    BC_facility_df = BC_facility_df.reset_index(names='Facility Name')

    return BC_facility_df

def removedspaces(BC_pipedistance_link_df, BC_facilitytype_2021_df):
    BC_pipedistance_link_df['WellName_nospace'] = BC_pipedistance_link_df['WELL_NAME'].str.replace(r'[^0-9a-zA-Z]+', '', regex=True)
    BC_facilitytype_2021_df['WellName_nospace'] = BC_facilitytype_2021_df['Well Name'].str.replace(r'[^0-9a-zA-Z]+', '', regex=True)

    return BC_pipedistance_link_df, BC_facilitytype_2021_df

def pipedistance_BC(BC_facilitytype_2021_df):
    BC_pipedistance_link_path = "./data/Shapefiles/BC_pipeline_near.csv"
    BC_pipedistance_link_df = pd.read_csv(BC_pipedistance_link_path)

    BC_pipedistance_link_df, BC_facilitytype_2021_df = removedspaces(BC_pipedistance_link_df, BC_facilitytype_2021_df)
    BC_pipedistance_link_df = BC_pipedistance_link_df[['NEAR_DIST', 'WELL_SURFA', 'WELL_NAME', 'WellName_nospace']]

    BC_facilitytype_2021_df = BC_facilitytype_2021_df.set_index('WellName_nospace').join(BC_pipedistance_link_df.set_index('WellName_nospace'), how='left')
    BC_facilitytype_2021_df = BC_facilitytype_2021_df.reset_index(names=['WellName_nospace'])

    BC_facilityconnectwell_df = BC_facility_df.set_index('ReportingFacilityLocation').join(BC_welldata_df.set_index('Surf. Loc.'), how='left')
    BC_facilityconnectwell_df = BC_facilityconnectwell_df.reset_index(names=['ReportingFacilityLocation'])

    return BC_facilitytype_2021_df

def gas_analysis_methane_UDF_BC(BC_facilitytype_2021_df):
    BC_gasanalysis_path = "./data/GeoSCOUT/BC_fluidanalysis_AccessedMay2023.csv"
    BC_gasanalysis_df = pd.read_csv(BC_gasanalysis_path)
    BC_gasanalysis_df = BC_gasanalysis_df[['Well Name','Well Identifier', 'Formation', 'Gauge Pressure Received(kPa)', 'Gauge Temp. Received(C)', 'Gross Heating Value(MJ/m3)', 'C1 Air Free']]
    BC_facilitytype_2021_df = BC_facilitytype_2021_df.set_index('Well Name').join(BC_gasanalysis_df.set_index('Well Name'), how='left')
    BC_facilitytype_2021_df = BC_facilitytype_2021_df.reset_index(names=['Well Name']).set_index('Surf. Loc.')

    return BC_facilitytype_2021_df

def fugitiveemissionsfill(OG_data_holding_df):
    tanks_unintended_emissions = 13.12 #Rutherford et al. Unintended vent count kgCH4/abnormal emission
    tank_unintended_activityfactor = 0.31 ##Rutherford et al. Unintended vent activity factor abnormal emission/tank

    OG_data_holding_df['Unintended Vents kgCH4/tank'] = tank_unintended_activityfactor * tanks_unintended_emissions

    methanedensity_STP = 0.7168 #kg/m3 https://www.engineeringtoolbox.com/methane-d_1420.html

    OG_data_holding_df['Unintended Vents 10^3m3 CH4/tank'] = OG_data_holding_df['Unintended Vents kgCH4/tank'] / methanedensity_STP /1000

    return OG_data_holding_df

def checkflareandtiein(OG_data_holding_df):
    OG_data_holding_df['Tie in?'] = np.where(OG_data_holding_df['DISP_gas'] != 0, True, False)
    OG_data_holding_df['Flare?'] = np.where(OG_data_holding_df['FLARE_gas'] != 0, True, False)

    return OG_data_holding_df

def defCH4_composition_UDF(row):
    facility_gascomp = row

def checkvru25(row):

    if row['ventvol'] <= 0.707925:
        return[1]
    else:
        return[0]

def checkvru50(row):

    if row['ventvol'] <= 1.41585:
        return[1]
    else:
        return[0]

def checkvru100(row):

    if row['ventvol'] <= 2.8317:
        return[1]
    else:
        return[0]

def checkvru200(row):

    if row['ventvol'] <= 5.6634:
        return [1]
    else:
        return [0]

def checkvru500(row):

    if row['ventvol'] <= 14.1585:
        return [1]
    else:
        return [0]

def CH4_composition_UDF(row):
    try:
        daily_CH4_vol = float(row['VENT_gas']) * float(row['C1 Air Free'])/30.437 #e3m3/day
    except:
        ch4gascomposition = 0.91880 #mol percent = vol percent from 2018 Alberta Upstream doc by CE
        daily_CH4_vol = float(row['VENT_gas']) * ch4gascomposition / 30.437  # e3m3/day

    return daily_CH4_vol

def fugitives_AB(AB_facilitydata):
    fugitvesAB_path = "./data/AER/OneStop_2021_AER.csv"
    fugitvesAB_df = pd.read_csv(fugitvesAB_path)
    fugitvesAB_df = fugitvesAB_df[['Reporting Facility', 'COMPRESSOR (m3)', 'PNEUMATICINSTRUMENT (m3)', 'PNEAMATICPUMP (m3)', 'FUGITIVE (m3)', 'ROUTINEVENT (m3)']]
    fugitives_data = AB_facilitydata.join(fugitvesAB_df.set_index('Reporting Facility'), how='left', rsuffix='AB')
    return fugitives_data

# Leak rate gps

def fugitives_BC(BC_facilitydata):
    fugitvesBC_path = "./data/BC/LDAR_BC_2021.csv"
    fugitvesBC_df = pd.read_csv(fugitvesBC_path)

    fugitvesBC_df = fugitvesBC_df[['Kermit FacilityID', 'Process Block', 'Process Block Other', 'Leaking Comp', 'Leaking Comp Other', 'Leaking Service', 'Repair Applied', 'Leak Rate CMH']]
    fugitvesBC_df['FUGITIVE (m3)'] = fugitvesBC_df['Leak Rate CMH']*8760 #conversion from h to annual emissions rate
    fugitvesBC_df = fugitvesBC_df.groupby('Kermit FacilityID').sum()
    fugitives_data = BC_facilitydata.set_index('ReportingFacilityID').join(fugitvesBC_df, how='left', rsuffix='BC')
    return fugitives_data

def facility_data_processing_2022():
    #Obtain an average of all AB 2022 wellsite data
    annual2022AB_df = pd.DataFrame()
    for month in [1]: #,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        facility_subtype_reporting_volumes_df_AB = facility_subtype_runs_AB(month)
        annual2022AB_df = pd.concat([annual2022AB_df, facility_subtype_reporting_volumes_df_AB])

    # annual2022_df = annual2022_df.rename(columns={"index": "ReportingFacilityID"})
    annual2022AB_df = annual2022AB_df.reset_index().rename(columns={"index": "ReportingFacilityID"})
    averaged_reported_facility_vol_df = annual2022AB_df.groupby(['ReportingFacilityID'], as_index=False, sort=False).mean()

    facilityfile_path = "./data/AER/Vol_2022-01-AB.csv"
    datafile_facility_df = pd.read_csv(facilityfile_path)
    temp_data_df = datafile_facility_df.drop_duplicates(subset=['ReportingFacilityID']).set_index('ReportingFacilityID')
    temp_data_df = temp_data_df[['ReportingFacilityName', 'ReportingFacilityLocation']]
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.set_index('ReportingFacilityID').join(temp_data_df, how='left')

    #Obtain a subset of the datafile with only the facilities listed
    facility_subtype_list = [311, 321, 322, 351, 361, 362, 363, 364]
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df[averaged_reported_facility_vol_df['ReportingFacilitySubType'].isin(facility_subtype_list)]

    #Import pipeline distance and join to main datafile
    gaspipedist_averaged_reported_ABfacility_vol_df = pipedistance_AB(averaged_reported_facility_vol_df)

    #Import fluid analysis from GeoSCOUT and join to main datafile
    # gas_analysis_methane_AB = gas_analysis_methane_UDF_AB(pipedist_averaged_reported_ABfacility_vol_df)
    gaspipedist_averaged_reported_ABfacility_vol_df['C1 Air Free'] = gaspipedist_averaged_reported_ABfacility_vol_df['C1 Air Free'].fillna(gaspipedist_averaged_reported_ABfacility_vol_df['C1 Air Free'].mean(axis=0))
    gaspipedist_averaged_reported_ABfacility_vol_df = gaspipedist_averaged_reported_ABfacility_vol_df.dropna(subset=['FLARE_gas'])
    fugitives_methane_AB = fugitives_AB(gaspipedist_averaged_reported_ABfacility_vol_df)

    # Obtain an average of all SK 2022 wellsite data
    annual2022SK_df = pd.DataFrame()
    for month in [1]: #, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        facility_subtype_reporting_volumes_df_SK = facility_subtype_runs_SK(month)
        annual2022SK_df = pd.concat([annual2022SK_df, facility_subtype_reporting_volumes_df_SK])

    # annual2022_df = annual2022_df.rename(columns={"index": "ReportingFacilityID"})
    annual2022SK_df = annual2022SK_df.reset_index().rename(columns={"index": "ReportingFacilityID"})
    averaged_reported_facility_vol_df = annual2022SK_df.groupby(['ReportingFacilityID'], as_index=False, sort=False).mean()

    facilityfile_path = "./data/SK/Vol_2022-01-SK.csv"
    datafile_facility_df = pd.read_csv(facilityfile_path)
    temp_data_df = datafile_facility_df.drop_duplicates(subset=['ReportingFacilityID']).set_index('ReportingFacilityID')
    temp_data_df = temp_data_df[['ReportingFacilityName', 'ReportingFacilityLocation']]
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df.set_index('ReportingFacilityID').join(temp_data_df, how='left')

    #Obtain a subset of the datafile with only the facilities listed
    facility_subtype_list = [311, 321, 322, 351, 361, 362, 363, 364]
    averaged_reported_facility_vol_df = averaged_reported_facility_vol_df[averaged_reported_facility_vol_df['ReportingFacilitySubType'].isin(facility_subtype_list)]

    #Import pipeline distance and join to main datafile
    pipedist_averaged_reported_SKfacility_vol_df = pipedistance_SK(averaged_reported_facility_vol_df)

    #Import fluid analysis from GeoSCOUT and join to main datafile
    gas_analysis_methane_SK = gas_analysis_methane_UDF_SK(pipedist_averaged_reported_SKfacility_vol_df)
    gas_analysis_methane_SK['C1 Air Free'] = gas_analysis_methane_SK['C1 Air Free'].fillna(gas_analysis_methane_SK['C1 Air Free'].mean(axis=0))
    gas_analysis_methane_SK = gas_analysis_methane_SK.dropna(subset=['FLARE_gas'])
    gas_analysis_methane_SK['Area'] = 'SK'
    gas_analysis_methane_SK['PIPE_MAOP'] = gaspipedist_averaged_reported_ABfacility_vol_df['PIPE_MAOP'].mean()
    gas_analysis_methane_SK = gas_analysis_methane_SK.drop_duplicates(subset=['ReportingFacilityID'])

    # # Obtain an average of all BC 2022 wellsite data
    annual2022BC_df = facility_subtype_runs_BC()
    annual2022BC_df = annual2022BC_df.reset_index().rename(columns={"index": "ReportingFacilityID"})
    annual2022BC_df = annual2022BC_df.groupby(['ReportingFacilityID'], as_index=False, sort=False).mean()
    facilityfile_path = "./data/BC/Vol_2022_BC.csv"
    datafile_facility_df = pd.read_csv(facilityfile_path)
    temp_data_df = datafile_facility_df.drop_duplicates(subset=['ReportingFacilityID'])
    temp_data_df = temp_data_df.set_index('ReportingFacilityID')
    temp_data_df = temp_data_df[['Facility Name', 'Facility Location']]
    BCaveraged_reported_facility_vol_df = annual2022BC_df.set_index('ReportingFacilityID').join(temp_data_df, how='left')

    #Obtain a subset of the datafile with only the facilities listed
    facility_subtype_list = [311, 321, 322, 351, 361, 362, 363, 364]
    BCaveraged_reported_facility_vol_df = BCaveraged_reported_facility_vol_df[BCaveraged_reported_facility_vol_df['ReportingFacilitySubType'].isin(facility_subtype_list)]

    gas_analysis_methane_BC = BC_facility_gasanalysis_pipeline(BCaveraged_reported_facility_vol_df)

    gas_analysis_methane_BC['C1 Air Free'] = gas_analysis_methane_BC['C1 Air Free'].fillna(gas_analysis_methane_BC['C1 Air Free'].mean(axis=0))
    gas_analysis_methane_BC = gas_analysis_methane_BC.dropna(subset=['FLARE_gas'])
    gas_analysis_methane_BC['Area'] = 'BC'
    gas_analysis_methane_BC = gas_analysis_methane_BC.round({'Year Well Spudded': 0})
    gas_analysis_methane_BC['PIPE_MAOP'] = gaspipedist_averaged_reported_ABfacility_vol_df['PIPE_MAOP'].mean()
    gas_analysis_methane_BC = gas_analysis_methane_BC.reset_index(names=['ReportingFacilityID'])
    gas_analysis_methane_BC = gas_analysis_methane_BC.drop_duplicates(subset=['ReportingFacilityID'])
    fugitives_methane_BC = fugitives_BC(gas_analysis_methane_BC)


    # # Obtain an average of all BC 2021 wellsite data
    # BC_facility_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\BC\Vol_2021-BC.csv"
    # BC_facility_df = pd.read_csv(BC_facility_path)
    # list2021 = [202111, 202110, 202109, 202108, 202107, 202106, 202105, 202104, 202103, 202102, 202101]
    # BC_facility2021_df = BC_facility_df[BC_facility_df['PROD_PERIOD'].isin(list2021)]
    # BC_facility2021_df = BC_facility2021_df.groupby(['FAC_ID_CODE'], as_index=False, sort=False).mean()
    # BC_facility2021_df = BC_facility2021_df.rename(columns={"PROD GAS": "PROD_gas", "FUEL GAS": "FUEL_gas", "FLARE GAS": "FLARE_gas", "VENT GAS": "VENT_gas", "TOT DELVRS GAS": "DISP_gas", "PROD OIL": "PROD_oil"})
    #
    # #Determine what kind of battery the BC facility is
    # BC_facilitytype_2021_df = BC_facility_type(BC_facility2021_df)


    #Append AB and SK data together
    AB_SK_BA_facilitydata = pd.concat([fugitives_methane_AB, gas_analysis_methane_SK, fugitives_methane_BC], sort=False)
    AB_SK_BA_facilitydata['Age'] = 2022 - pd.to_numeric(AB_SK_BA_facilitydata['Year Well Spudded'])

    #Check for facility infrastructure of flare and tie in
    facility_infra_vf_oilgasfacilityvol_df = checkflareandtiein(AB_SK_BA_facilitydata)

    # ch4gascomposition = 0.91880 #mol percent = vol percent from 2018 Alberta Upstream doc by CE
    # facility_infra_vf_oilgasfacilityvol_df['ventvol'] = facility_infra_vf_oilgasfacilityvol_df['VENT_gas'].apply(CH4_composition_UDF) * ch4gascomposition/30.437 #e3m3/day

    facility_infra_vf_oilgasfacilityvol_df['ventvol'] = facility_infra_vf_oilgasfacilityvol_df['VENT_gas'] / 30.437 #volume of gas through device e3m3/day
    facility_infra_vf_oilgasfacilityvol_df['ch4_ventvol'] = facility_infra_vf_oilgasfacilityvol_df.apply(CH4_composition_UDF, axis=1)  # volume of methane emitted e3m3/day

    facility_infra_vf_oilgasfacilityvol_df['VRU25'] = facility_infra_vf_oilgasfacilityvol_df.apply(checkvru25, axis=1)
    facility_infra_vf_oilgasfacilityvol_df['VRU50'] = facility_infra_vf_oilgasfacilityvol_df.apply(checkvru50, axis=1)
    facility_infra_vf_oilgasfacilityvol_df['VRU100'] = facility_infra_vf_oilgasfacilityvol_df.apply(checkvru100, axis=1)
    facility_infra_vf_oilgasfacilityvol_df['VRU200'] = facility_infra_vf_oilgasfacilityvol_df.apply(checkvru200,axis=1)
    facility_infra_vf_oilgasfacilityvol_df['VRU500'] = facility_infra_vf_oilgasfacilityvol_df.apply(checkvru500, axis=1)
    facility_infra_vf_oilgasfacilityvol_df= facility_infra_vf_oilgasfacilityvol_df.reset_index().rename(columns={"index": "ReportingFacilityID"})
    facility_infra_vf_oilgasfacilityvol_df.to_csv('2022v10_oilgasfacilityvol.csv')
    return facility_infra_vf_oilgasfacilityvol_df

if __name__ == '__main__':
    months = range[0,13]
    year = 2021
    facility_data_processing_2022()



    #
    # summed_reported_facility_vol_df = annual2022_df.groupby(['ReportingFacilityID'], as_index=False, sort=False).sum()
    # summed_reported_facility_vol_df.to_csv('2022_oilgasfacilityvol_sum.csv')


