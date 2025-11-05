import pandas as pd
import numpy as np

def getData(month):

    try:
        facilityfile_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\AER\Vol_2022-0" +  str(month) + "-AB.csv"
        datafile_facility_df = pd.read_csv(facilityfile_path)
    except:
        facilityfile_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\AER\Vol_2022-" + str(month) + "-AB.csv"
        datafile_facility_df = pd.read_csv(facilityfile_path)

    gasprod_only_datafile_df = datafile_facility_df[datafile_facility_df['ProductID'] == 'GAS']
    oilprod_only_datafile_df = datafile_facility_df[datafile_facility_df['ProductID'] == 'OIL']

    sortedgasprod_DataFile_df = gasprod_only_datafile_df.fillna(0).groupby(['ActivityID', 'ReportingFacilityID'], as_index=False, sort=False).sum()
    sortedgasprod_DataFile_df = sortedgasprod_DataFile_df.reset_index()
    sortedoilprod_DataFile_df = oilprod_only_datafile_df.fillna(0).groupby(['ActivityID', 'ReportingFacilityID'], as_index=False, sort=False).sum()
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

def facility_subtype_runs(month):
    sortedgasprod_DataFile_df, sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df, datafile_facility_df = getData(month)
    gasprod_report_volumes, oilprod_report_volumes = flatten_well_activity(sortedgasprod_DataFile_df,sortedoilprod_DataFile_df, gasprod_only_datafile_df, oilprod_only_datafile_df)
    og_reporting_volumes_df = gasprod_report_volumes.join(oilprod_report_volumes, lsuffix='_gas', rsuffix='_oil')

    fac_subtype_df = facility_subtype_sort(datafile_facility_df)
    facility_subtype_reporting_volumes_df = og_reporting_volumes_df.join(fac_subtype_df)
    facility_subtype_reporting_volumes_df = facility_subtype_reporting_volumes_df.fillna(0)
    facility_subtype_reporting_volumes_df = facility_subtype_reporting_volumes_df.sort_values(by='ReportingFacilitySubType', ascending=True)

    facility_subtype_reporting_volumes_df['Month of Production'] = month
    return facility_subtype_reporting_volumes_df

def oilemissionscalc(facility_subtype_reporting_volumes_df):

    oilemissionsfile_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\oilfacilityemissions.csv"
    oil_facility_df = pd.read_csv(oilemissionsfile_path)
    oil_facility_df = oil_facility_df.set_index('ReportingFacilityID')

    data_holding_df = pd.DataFrame()

    for facility in [311]:
        temp_facility_vol_df = facility_subtype_reporting_volumes_df[facility_subtype_reporting_volumes_df['ReportingFacilitySubType'] == facility]
        tankemissionspercentage = oil_facility_df.loc[facility, '%oftankemissions']
        temp_facility_vol_df['Vent from Tanks'] = temp_facility_vol_df.VENT_gas * tankemissionspercentage
        temp_facility_vol_df = temp_facility_vol_df.reset_index()
        data_holding_df = pd.concat([data_holding_df, temp_facility_vol_df])

        print(data_holding_df)

    return data_holding_df

def gasemissionscalc(data_holding_df, facility_subtype_reporting_volumes_df):

    gasemissionsfile_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\gasfacilityemissions.csv"
    gas_facility_df = pd.read_csv(gasemissionsfile_path)
    gas_facility_df = gas_facility_df.set_index('ReportingFacilityID')

    for facility in [361, 362, 363, 364]:
        temp_facility_vol_df = facility_subtype_reporting_volumes_df[facility_subtype_reporting_volumes_df['ReportingFacilitySubType'] == facility]
        tankemissionspercentage = gas_facility_df.loc[facility, '%oftankemissions']
        temp_facility_vol_df['Vent from Tanks'] = temp_facility_vol_df.VENT_gas * tankemissionspercentage
        temp_facility_vol_df = temp_facility_vol_df.reset_index()
        data_holding_df = pd.concat([data_holding_df, temp_facility_vol_df])

        print(data_holding_df)

    return data_holding_df

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


if __name__ == '__main__':
    annual2022_df = pd.DataFrame()
    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        facility_subtype_reporting_volumes_df = facility_subtype_runs(month)
        oilfacilityreportingvol_df = oilemissionscalc(facility_subtype_reporting_volumes_df)
        oilgasfacilityreportingvol_df = gasemissionscalc(oilfacilityreportingvol_df, facility_subtype_reporting_volumes_df)
        annual2022_df = pd.concat([annual2022_df, oilgasfacilityreportingvol_df])

    annual2022_df = annual2022_df.rename(columns={"index": "ReportingFacilityID"})
    averaged_reported_facility_vol_df = annual2022_df.groupby(['ReportingFacilityID'], as_index=False, sort=False).mean()

    vf_oilgasfacilityvol_df = fugitiveemissionsfill(averaged_reported_facility_vol_df)
    facility_infra_vf_oilgasfacilityvol_df = checkflareandtiein(vf_oilgasfacilityvol_df)

    facility_infra_vf_oilgasfacilityvol_df.to_csv('2022_oilgasfacilityvol.csv')



