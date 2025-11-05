import pandas as pd
import numpy as np
import math

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
        # fuelcostsfromtech = row['VRU_hp'] * 24 * 365 * 0.746 * 0.13
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
        # fuelcostsfromtech = row['VRU_hp'] * 24 * 365 * 0.746 * 0.13
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
        emissionsfromtech =  griddieselemissions(row['VRU_hp'])
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate, salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def VRUTieInGenco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Tie in?'] == False) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech =  griddieselemissions(row['VRU_hp'])
        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def VRUTieInGench4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['Tie in?'] == False) and (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech =  griddieselemissions(row['VRU_hp'])
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
            CAPEX = row['casinggas_tiein_CAPEX']
            OPEX = row['casinggas_tiein_OPEX']
            ventrate = row['ventvol']
            salesgasincome_annual = ventrate * gasprice * 365  # $CAD/year
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
            emissionsfromtech = 0
            npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
            return npv

        else:
            npv = np.nan
            return npv

    elif row['casinggas_tiein_OPEX'] < 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn low feasible max?'] == True):
            CAPEX = row['casinggas_tiein_CAPEX']
            OPEX = row['casinggas_tiein_OPEX']
            ventrate = row['ventvol']
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
            salesgasincome_annual= ventrate * gasprice * 365  # $CAD/year
            emissionsfromtech = 0
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
            emissionsfromtech = 0

            npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
            return npv

        else:
            npv = np.nan
            return npv

    elif row['casinggas_tiein_OPEX'] < 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn low feasible max?'] == True):
            ventrate = row['ventvol']
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
            emissionsfromtech = 0

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
            emissionsfromtech = 0

            npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
            return npv

        else:
            npv = np.nan
            return npv

    elif row['casinggas_tiein_OPEX'] < 6300:
        if (row['Tie in?'] == False) and (row['CasingGasTieIn low feasible max?'] == True):
            ventrate = row['ventvol']
            ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
            emissionsfromtech = 0

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
        emissionsfromtech = row[
                                'ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  +row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                    10 ** 6))
        # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d *365d/y = tCO2/y
        # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g * 365d/y = tCO2e/y
        salesgasincome_annual=0
        # fuelcostsfromtech = row['VRU_hp'] * 24 * 365 * 0.746 * 0.13
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate, ventrate,salesgasincome_annual)
        return npv

    else:
        npv = np.nan
        return npv

def VRUVacCombGridco2e_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row['ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  +row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                    10 ** 6))
        # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d *365d/y = tCO2/y
        # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g * 365d/y = tCO2e/y
        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def VRUVacCombGridch4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = row['ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  +row['VRU_hp'] * 0.746 * 3600 * 2 / 3600 * (590 / (
                    10 ** 6))
        # e3m3/d * kg/e3m3 * t/1000kg * tmol/tCH4 * tCO2/tmol = tCO2/d *365d/y = tCO2/y
        # hp * 0.746kW/hp * 3600s/h *24h/d * 1kWh/3600kJ *590gCO2e/kwh * t/10^6g * 365d/y = tCO2e/y
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
        emissionsfromtech = row['ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  + griddieselemissions(row['VRU_hp'])
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
        emissionsfromtech = row['ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  + griddieselemissions(row['VRU_hp'])
        npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
        return npv

    else:
        npv = np.nan
        return npv

def VRUVacCombGench4_udf(row, percentreduction, emissionsfromtech, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if (row['VRU_feasible min?'] == True):
        ventrate = row['ventvol']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = row['ventvol'] * percentreduction * ch4density / 1000 / 16.04 * 44.01  + griddieselemissions(row['VRU_hp'])
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
    emissionsfromtech = 0 #CO2e/day
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

def ReciComp_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    CAPEX = row['Vent_ReciCompressor_CAPEX_fixed_Avg']
    OPEX = row['Vent_ReciCompressor_OPEX_fixed_Avg']
    ventrate = row['Vent_ReciCompressor']
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
    emissionsfromtech = 0
    salesgasincome_annual = 0
    npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                       ventrate, salesgasincome_annual)
    return npv

def ReciCompco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['Vent_ReciCompressor']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def ReciCompch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['Vent_ReciCompressor']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def ScrewComp_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    CAPEX = row['Vent_ScrewCompressor_CAPEX_fixed_Avg']
    OPEX = row['Vent_ScrewCompressor_OPEX_fixed_Avg']
    ventrate = row['Vent_ScrewCompressor']
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
    emissionsfromtech = 0
    salesgasincome_annual = 0
    npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                       ventrate, salesgasincome_annual)
    return npv

def ScrewCompco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['Vent_ScrewCompressor']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def ScrewCompch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['Vent_ScrewCompressor']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def PneuPositioner_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    CAPEX = row['PneuPositioner_CAPEX_fixed_Avg']
    OPEX = row['PneuPositioner_OPEX_fixed_Avg']
    ventrate = row['PneuPositioner']
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
    emissionsfromtech = 0
    salesgasincome_annual = 0
    npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                       ventrate, salesgasincome_annual)
    return npv

def PneuPositionerco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['PneuPositioner']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def PneuPositionerch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['PneuPositioner']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def PneuLevelControl_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    CAPEX = row['PneuLevelControl_CAPEX_fixed_Avg']
    OPEX = row['PneuLevelControl_OPEX_fixed_Avg']
    ventrate = row['PneuLevelControl']
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
    emissionsfromtech = 0
    salesgasincome_annual = 0
    npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                       ventrate, salesgasincome_annual)
    return npv

def PneuLevelControlco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['PneuLevelControl']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def PneuLevelControlch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['PneuLevelControl']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def PneuTransducer_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if row['transducer sizing'] == 'sm':
        CAPEX = row['PneuTransducerSm_CAPEX_fixed_Avg']
        OPEX = row['PneuTransducerSm_OPEX_fixed_Avg']
        ventrate = row['PneuTransducer']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = 0
        salesgasincome_annual = 0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                           ventrate, salesgasincome_annual)
        return npv

    else:
        CAPEX = row['PneuTransducerLg_CAPEX_fixed_Avg']
        OPEX = row['PneuTransducerLg_OPEX_fixed_Avg']
        ventrate = row['PneuTransducer']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = 0
        salesgasincome_annual = 0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                           ventrate, salesgasincome_annual)
        return npv

def PneuTransducerco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['PneuTransducer']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def PneuTransducerch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['PneuTransducer']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def PneuPump_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    CAPEX = row['PneuPump_CAPEX_fixed_Avg']
    OPEX = row['PneuPump_OPEX_fixed_Avg']
    ventrate = row['PneuPump']
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
    emissionsfromtech = 0
    salesgasincome_annual = 0
    npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                       ventrate, salesgasincome_annual)
    return npv

def PneuPumpco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['PneuPump']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def PneuPumpch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['PneuPump']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def IA_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    if row['IA1_lower_feasible max?'] is True:
        CAPEX = row['AllPneu_Air1_CAPEX_fixed_Lower']
        OPEX = row['AllPneu_Air1_CAPEX_fixed_Lower']
        ventrate = row['allpneuvents']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = 0
        salesgasincome_annual = 0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                           ventrate, salesgasincome_annual)
        return npv
    elif row['IA1_upper_feasible max?'] is True:
        CAPEX = row['AllPneu_Air1_CAPEX_fixed_Upper']
        OPEX = row['AllPneu_Air1_CAPEX_fixed_Upper']
        ventrate = row['allpneuvents']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
        emissionsfromtech = 0
        salesgasincome_annual = 0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                           ventrate, salesgasincome_annual)
        return npv

    else:
        CAPEX = row['AllPneu_Air2_CAPEX_fixed_Upper']
        OPEX = row['AllPneu_Air2_CAPEX_fixed_Upper']
        ventrate = row['allpneuvents']
        ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
        emissionsfromtech = 0
        salesgasincome_annual = 0
        npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                           ventrate, salesgasincome_annual)
        return npv

def IAco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['allpneuvents']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def IAch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['allpneuvents']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def Elec_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    CAPEX = row['AllPneu_Elec_CAPEX_fixed_Avg']
    OPEX = row['AllPneu_Elec_OPEX_fixed_Avg']
    ventrate = row['allpneuvents']
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
    emissionsfromtech = 0
    salesgasincome_annual = 0
    npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                       ventrate, salesgasincome_annual)
    return npv

def Elecco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['allpneuvents']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def Elecch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['allpneuvents']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def GDFlare_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    CAPEX = row['GlycolDehy_Flare_CAPEX_fixed_Avg']
    OPEX = row['GlycolDehy_Flare_OPEX_fixed_Avg']
    ventrate = row['GlycolDehy']
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
    emissionsfromtech = 0
    salesgasincome_annual = 0
    npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                       ventrate, salesgasincome_annual)
    return npv

def GDVent_udf(row, percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density):
    CAPEX = row['GlycolDehy_Vent_CAPEX_fixed_Avg']
    OPEX = row['GlycolDehy_Vent_CAPEX_fixed_Avg']
    ventrate = row['GlycolDehy']
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density/1000 #tCO2e/d
    emissionsfromtech = 0
    salesgasincome_annual = 0
    npv = cashflowcalc(CAPEX, OPEX, ventabatement, emissionsfromtech, gasprice, fuelcostsfromtech, discountrate,
                       ventrate, salesgasincome_annual)
    return npv

def GDFlareco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['GlycolDehy']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = ventrate * percentreduction * ch4density * 44.01 / 16.04 / 1000  # tCO2/d emissions from combustion

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def GDFlarech4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['GlycolDehy']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = ventrate * percentreduction * ch4density * 44.01 / 16.04 / 1000  # tCO2/d emissions from combustion

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def GDco2e_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['GlycolDehy']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcco2e(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density)
    return npv

def GDch4_udf(row, percentreduction, CH4GWPconstants, discountrate, ch4density):
    ventrate = row['GlycolDehy']  # e3m3/d
    ventabatement = ventrate * percentreduction * CH4GWPconstants * ch4density / 1000  # tCO2e/d
    emissionsfromtech = 0

    npv = abatementcalcch4(ventabatement, emissionsfromtech, discountrate, ventrate, ch4density, CH4GWPconstants)
    return npv

def auxequip_casestudycostcals(facilitydata_df, techdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density):
    #compressors
    # ReciprocatingComp
    # ventreductionrate_m3perhr_upper = techdetails_df.at[[('Vent_ReciCompressor', 'Upper')]['GHG_Reduction_high']]
    # ventreductionrate_m3perhr_lower = techdetails_df.at[[('Vent_ReciCompressor', 'Upper')]['GHG_Reduction_low']]

    percentreduction = techdetails_df.at[('Vent_ReciCompressor', 'Upper')]['GHG_Reduction_high'][0]
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['ReciComp_npvCAD'] = facilitydata_df.apply(ReciComp_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['ReciComp_co2enpvCAD'] = facilitydata_df.apply(ReciCompco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['ReciComp_ch4npvCAD'] = facilitydata_df.apply(ReciCompch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    # ScrewComp
    percentreduction = techdetails_df.at[('Vent_ScrewCompressor', 'Upper')]['GHG_Reduction_high'][0]
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['ScrewComp_npvCAD'] = facilitydata_df.apply(ScrewComp_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['ScrewComp_co2enpvCAD'] = facilitydata_df.apply(ScrewCompco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['ScrewComp_ch4npvCAD'] = facilitydata_df.apply(ScrewCompch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    #all pneumatics vs elec or IA
    #PneuPositioner
    percentreduction = techdetails_df.at[('PneuPositioner', 'Upper')]['GHG_Reduction_high'][0]
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['PneuPositioner_npvCAD'] = facilitydata_df.apply(PneuPositioner_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['PneuPositioner_co2enpvCAD'] = facilitydata_df.apply(PneuPositionerco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['PneuPositioner_ch4npvCAD'] = facilitydata_df.apply(PneuPositionerch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    #PneuLevelControl
    percentreduction = techdetails_df.at[('PneuLevelControl', 'Upper')]['GHG_Reduction_high'][0]
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['PneuLevelControl_npvCAD'] = facilitydata_df.apply(PneuLevelControl_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['PneuLevelControl_co2enpvCAD'] = facilitydata_df.apply(PneuLevelControlco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['PneuLevelControl_ch4npvCAD'] = facilitydata_df.apply(PneuLevelControlch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    #PneuTransducer (check facility size)
    percentreduction = techdetails_df.at[('PneuTransducerSm', 'Upper')]['GHG_Reduction_high'][0]#percent reductions the same regardless of size
    fuelcostsfromtech = 0 #$CAD/year
    facilitydata_df['PneuTransducer_npvCAD'] = facilitydata_df.apply(PneuTransducer_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['PneuTransducer_co2enpvCAD'] = facilitydata_df.apply(PneuTransducerco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['PneuTransducer_ch4npvCAD'] = facilitydata_df.apply(PneuTransducerch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    #PneuPump
    percentreduction = techdetails_df.at[('PneuPump', 'Upper')]['GHG_Reduction_high'][0]
    fuelcostsfromtech = 0  # $CAD/year
    facilitydata_df['PneuPump_npvCAD'] = facilitydata_df.apply(PneuPump_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['PneuPump_co2enpvCAD'] = facilitydata_df.apply(PneuPumpco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['PneuPump_ch4npvCAD'] = facilitydata_df.apply(PneuPumpch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    #IA
    percentreduction = techdetails_df.at[('AllPneu_Air1', 'Upper')]['GHG_Reduction_high'][0]# percent reductions the same regardless of version of IA
    fuelcostsfromtech = 0  # $CAD/year
    facilitydata_df['IA_npvCAD'] = facilitydata_df.apply(IA_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['IA_co2enpvCAD'] = facilitydata_df.apply(IAco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['IA_ch4npvCAD'] = facilitydata_df.apply(IAch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    #Electric
    percentreduction = techdetails_df.at[('AllPneu_Elec', 'Upper')]['GHG_Reduction_high'][0]# percent reductions the same regardless of version of IA
    fuelcostsfromtech = 0  # $CAD/year
    facilitydata_df['Elec_npvCAD'] = facilitydata_df.apply(Elec_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['Elec_co2enpvCAD'] = facilitydata_df.apply(Elecco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['Elec_ch4npvCAD'] = facilitydata_df.apply(Elecch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    #glycol dehydrators
    #gd flares
    #gd flares
    percentreduction = techdetails_df.at[('GlycolDehy_Flare', 'Upper')]['GHG_Reduction_high'][0]# percent reductions the same regardless of version of IA
    fuelcostsfromtech = 0  # $CAD/year
    facilitydata_df['GDFlare_npvCAD'] = facilitydata_df.apply(GDFlare_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['GDFlare_co2enpvCAD'] = facilitydata_df.apply(GDFlareco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['GDFlare_ch4npvCAD'] = facilitydata_df.apply(GDFlarech4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)


    #gd vent capture
    percentreduction = techdetails_df.at[('GlycolDehy_Vent', 'Upper')]['GHG_Reduction_high'][0]# percent reductions the same regardless of version of IA
    fuelcostsfromtech = 0  # $CAD/year
    facilitydata_df['GDVent_npvCAD'] = facilitydata_df.apply(GDVent_udf, args=(percentreduction, CH4GWPconstants, gasprice, fuelcostsfromtech, discountrate, ch4density), axis=1)
    facilitydata_df['GDVent_co2enpvCAD'] = facilitydata_df.apply(GDco2e_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)
    facilitydata_df['GDVent_ch4npvCAD'] = facilitydata_df.apply(GDch4_udf, args=(percentreduction, CH4GWPconstants, discountrate, ch4density), axis=1)

    #IA vs. Elec vs. Separate Pneu Components
    facilitydata_df['IA_MACCCO2e'] = facilitydata_df['IA_npvCAD'] / facilitydata_df['IA_co2enpvCAD']
    facilitydata_df['Elec_MACCCO2e'] = facilitydata_df['Elec_npvCAD'] / facilitydata_df['Elec_co2enpvCAD']
    pneumaticslist_npv = ['PneuPump_npvCAD', 'PneuTransducer_npvCAD', 'PneuLevelControl_npvCAD', 'PneuPositioner_npvCAD']
    pneumaticslist_npvco2 = ['PneuPump_co2enpvCAD', 'PneuTransducer_co2enpvCAD', 'PneuLevelControl_co2enpvCAD', 'PneuPositioner_co2enpvCAD']
    facilitydata_df['pneu_components_npv'] = facilitydata_df[pneumaticslist_npv].sum(axis=1)
    facilitydata_df['pneu_components_co2enpv'] = facilitydata_df[pneumaticslist_npvco2].sum(axis=1)
    facilitydata_df['pneu_components_MACCCO2e'] = facilitydata_df['pneu_components_npv'] / facilitydata_df['pneu_components_co2enpv']

    #GD Flare vs. GD Vent Capture
    facilitydata_df['GD_FlareMACCCO2e'] = facilitydata_df['GDFlare_npvCAD']/ facilitydata_df['GDFlare_co2enpvCAD']
    facilitydata_df['GD_VentMACCCO2e'] = facilitydata_df['GDVent_npvCAD'] / facilitydata_df['GDVent_co2enpvCAD']

    #compressors
    facilitydata_df['ReciCompMACCCO2e'] = facilitydata_df['ReciComp_npvCAD'] / facilitydata_df['ReciComp_co2enpvCAD']
    facilitydata_df['ScrewCompMACCCO2e'] = facilitydata_df['ScrewComp_npvCAD'] / facilitydata_df['ScrewComp_co2enpvCAD']

    return facilitydata_df

if __name__ == '__main__':
    from technology_economics_runs import (tech_econ_runs, auxequip_tech_econ_runs)

    # ----------INPUT PARAMETERS-----------
    GasMoleDensity = 23.644  # m3/kmol
    CH4_MW = 16.04  # kg/kmol
    CH4_density_STP = CH4_MW / GasMoleDensity  # kg/m3 methane
    ch4density = CH4_density_STP*1000 #kg/e3m3 methane
    GlycolDehydrator_AB_2022 = 1300
    GasPlants_AB_2022 = 500
    CH4GWPconstants = 28  # co2e/ch4
    gasprice = 3.55 * 39  # $CAD/GJ * GJ/e3MJ * 39e3MJ/e3m3 = $CAD/e3m3
    discountrate = 0.1

    facility_subtype_data_path = "../../temp_facility_data.csv"
    facilitydata_df = pd.read_csv(facility_subtype_data_path)

    techdetailspath = "./technologydetails_equip.csv"
    techdetails_df = pd.read_csv(techdetailspath)
    techdetails_df = techdetails_df.set_index(['technologies', 'Range'])

    facilitydata_econ_df = auxequip_tech_econ_runs(facilitydata_df, techdetails_df)

    test = auxequip_casestudycostcals(facilitydata_econ_df, techdetails_df, CH4GWPconstants, gasprice, discountrate, ch4density)