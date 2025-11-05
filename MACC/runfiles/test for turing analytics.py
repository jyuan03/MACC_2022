import pandas as pd
import numpy as np
def remove_lastzero(row):
    newstring = row['CPA Pretty Well ID'][0:20]

    return newstring


test_geoscoutdata = pd.read_csv(r'C:\Users\jyuan\OneDrive - University of Calgary\Summer Research Documents\Project Data - New\geoSCOUT_data\post 2005 well_data.csv', encoding='unicode_escape')
test_birchcliff = pd.read_csv(r'C:\Users\jyuan\OneDrive - University of Calgary\Turing Analytics\BirchCliff Wells.csv')
test_opgee = pd.read_csv(r'C:\Users\jyuan\OneDrive - University of Calgary\Turing Analytics\opgeewells.csv')

test_geoscoutdata['newname'] = test_geoscoutdata.apply(remove_lastzero, axis=1)

combined = test_geoscoutdata.set_index('newname').join(test_birchcliff.set_index('Entity Name'))
combined = combined.reset_index(names='Entity Name')
combined = combined.dropna(subset='Gas Primary Sales Facility ID')
combined = combined.set_index('CPA Well ID').join(test_opgee.set_index('opgeewell')).reset_index(names='CPA Well ID')





print('id')

test = test_geoscoutdata.iloc[:,0:3]
test = test_geoscoutdata.iloc[:,0:10]
test = test.set_index('CPA Pretty Well ID')
test = test.join(test_birchcliff.set_index('Entity Name'))
test_opgee = pd.read_csv(r'C:\Users\jyuan\OneDrive - University of Calgary\Turing Analytics\opgeewells.csv')
test = test.join(test_opgee.set_index('opgeewell'))
test_opgee = pd.read_csv(r'C:\Users\jyuan\OneDrive - University of Calgary\Turing Analytics\opgeewells.csv')
test = test.join(test_opgee.set_index('opgeewell'))
test1 = test.dropna(subset=['name', 'Gas Primary Sales Facility ID'])
test1 = test.dropna(subset=['Gas Primary Sales Facility ID'])
test1 = test.dropna(subset=['name'])
test = test.reset_index(names=['CPA Pretty Well ID'])
test2 = test_geoscoutdata['CPA Pretty Well ID'].iloc[0:20]
test2 = test_geoscoutdata['CPA Pretty Well ID'].iloc[:,0:20]