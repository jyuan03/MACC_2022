import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from MACC.runfiles.EquipmentEmissionFactor import (facility_equipment_EF, facility_pneumatics_EF)
from MACC.runfiles.EF_PercentageDistributions import (PercentageDistributions, equipment_methane_calculation_UDF)
from MACC.runfiles.AER_Petrinex_ActivityDataSorting import facility_data_processing_2022
from MACC.runfiles.technologies import (site_technologies, equip_technologies, costcomparisons, abatementcomparisions)

#----------INPUT PARAMETERS-----------
GasMoleDensity = 23.644 #m3/kmol
CH4_MW = 16.04 #kg/kmol
CH4_density_STP = CH4_MW/GasMoleDensity #kg/m3 methane
GlycolDehydrator_AB_2022 = 1300
GasPlants_AB_2022 = 500
CH4GWPconstants = 28  # co2e/ch4
gasprice = 3.55 * 39  # $CAD/GJ * GJ/e3MJ * 39e3MJ/e3m3 = $CAD/e3m3
discountrate = 0.1
ch4density = 687 #kg/e3m3


#--------EQUIPMENT VENT DISTRIBUTION PER FACILITY SUBTYPE-----------
#Equipment, GD, and Pneumatics Emission Factors
gas_facility_EF, oil_facility_EF, GD_AB_2022, PG_equip_EF_summed = facility_equipment_EF(GlycolDehydrator_AB_2022)

#Unit conversion to m3/hr per source EFs
gas_facility_EF_m3hr = gas_facility_EF / CH4_density_STP #kgTHC/hr/source * m3/kg CH4
oil_facility_EF_m3hr = oil_facility_EF / CH4_density_STP #kgTHC/hr/source * m3/kg CH4
GD_AB_2022_m3hr = GD_AB_2022 / CH4_density_STP #kgTHC/hr/source * m3/kg CH4
oilandgas_pneumatics_EF_m3hr = facility_pneumatics_EF() #m3/hr

#Facility 2022 data import and sorting from Petrinex
facility_data_by_subtype = facility_data_processing_2022()

#Determining percentage distributions of the emission sources by emission factor
gas_perc_DF, oil_perc_DF = PercentageDistributions(gas_facility_EF_m3hr, oil_facility_EF_m3hr, oilandgas_pneumatics_EF_m3hr,
                            facility_data_by_subtype, GlycolDehydrator_AB_2022, GasPlants_AB_2022, CH4_density_STP, PG_equip_EF_summed)

#Calculate the equipment contribution of each facility type
facility_data_by_subtype = equipment_methane_calculation_UDF(facility_data_by_subtype, gas_perc_DF, oil_perc_DF)
facility_data_by_subtype.to_csv('./2022v10_oilgasfacilityvol.csv')

#Calculate technology costs and applicability
facility_data_by_subtype = site_technologies(facility_data_by_subtype, CH4GWPconstants, gasprice, discountrate, CH4_density_STP)
facility_data_by_subtype.to_csv('./temp_facility_data.csv')

facility_data_by_subtype = equip_technologies(facility_data_by_subtype, CH4GWPconstants, gasprice, discountrate, CH4_density_STP)

costcomparisons_casestudycosts=costcomparisons(facility_data_by_subtype, CH4GWPconstants, ch4density)
abatementcomparisions_casestudycosts=abatementcomparisions(costcomparisons_casestudycosts, CH4GWPconstants, ch4density)
abatementcomparisions_casestudycosts.to_csv(
        './temp_facilityandecon_data.csv')

print(facility_data_by_subtype)