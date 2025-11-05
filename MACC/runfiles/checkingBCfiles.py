"C:\Users\jyuan\anaconda3\envs\Equipment Inventory\python.exe" "C:\Program Files\JetBrains\PyCharm Community Edition 2022.1.3\plugins\python-ce\helpers\pydev\pydevconsole.py" --mode=client --port=50817
import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['C:\\Users\\jyuan\\OneDrive - University of Calgary\\PTAC\\Equipment Inventory', 'C:/Users/jyuan/OneDrive - University of Calgary/PTAC/Equipment Inventory'])
PyDev console: starting.
Python 3.10.9 | packaged by conda-forge | (main, Jan 11 2023, 15:15:40) [MSC v.1916 64 bit (AMD64)] on win32
import pandas as pd
BC_pipedistance_link_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Shapefiles\BC_pipeline_near.csv"
BC_pipedistance_link_df = pd.read_csv(BC_pipedistance_link_path)
BC_welldata_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\MACC\GeoSCOUT\BC_welldata_AccessedMay2023.csv"
BC_welldata_df = pd.read_csv(BC_welldata_path, encoding='cp1252')
<input>:2: DtypeWarning: Columns (0,1,132,133,134,135,136,188,189,190,191,192,205,318,319,320) have mixed types. Specify dtype option on import or set low_memory=False.
print(BC_welldata_df['Well Name'].head())
0    TOURMALINE HZ SUNDOWN C-C051-H/093-P-10
1    TOURMALINE HZ SUNDOWN C-B051-H/093-P-10
2                  CANLIN STONE 15-31-076-25
3             OVV HZ SWAN LAKE C01-15-077-14
4             OVV HZ SWAN LAKE C01-15-077-14
Name: Well Name, dtype: object
def removedspaces(BC_pipedistance_link_df, BC_facilitytype_2021_df):
    BC_pipedistance_link_df['WellName_nospace'] = BC_pipedistance_link_df['WELL_NAME'].str.replace(r'[^0-9a-zA-Z]+', '', regex=True)
    BC_facilitytype_2021_df['WellName_nospace'] = BC_facilitytype_2021_df['Well Name'].str.replace(r'[^0-9a-zA-Z]+', '', regex=True)
    return BC_pipedistance_link_df, BC_facilitytype_2021_df
BC_pipedistance_link_df, BC_welldata_df = removedspaces(BC_pipedistance_link_df, BC_welldata_df)
joinedtest = BC_welldata_df.set_index('WellName_nospace').join(BC_pipedistance_link_df.set_index('WellName_nospace'), how='left')
BC_facility_link_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\BC\BC_facility_linkage.csv"
BC_facility_link_df = pd.read_csv(BC_facility_link_path)
joinedtest = joinedtest.reset_index(names='WellName_nospace')
joinedtest = joinedtest.set_index('Lic/WA/WID/Permit #').join(BC_facility_link_df.set_index('FROMWANUM'), how='left')
facilityfile_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\BC\Vol_2022_BC.csv"
datafile_facility_df = pd.read_csv(facilityfile_path)
<input>:2: DtypeWarning: Columns (9,21) have mixed types. Specify dtype option on import or set low_memory=False.
datafile_facility_df['FacilityName_nospace'] = BC_facilitytype_2021_df['Facility Name'].str.replace(r'[^0-9a-zA-Z]+', '', regex=True)
Traceback (most recent call last):
  File "C:\Users\jyuan\anaconda3\envs\Equipment Inventory\lib\code.py", line 90, in runcode
    exec(code, self.locals)
  File "<input>", line 1, in <module>
NameError: name 'BC_facilitytype_2021_df' is not defined
datafile_facility_df['FacilityName_nospace'] = datafile_facility_df['Facility Name'].str.replace(r'[^0-9a-zA-Z]+', '', regex=True)
joinedtest['FacilityName_nospace'] = joinedtest['FACILITYNAME'].str.replace(r'[^0-9a-zA-Z]+', '', regex=True)
joinedtest2 = joinedtest.set_index('FacilityName_nospace').join(datafile_facility_df.set_index('FacilityName_nospace'), how='right')
joinedtest2 = datafile_facility_df.set_index('FacilityName_nospace').join(joinedtest.set_index('FacilityName_nospace'), how='left')
