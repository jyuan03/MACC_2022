import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from MACC.runfiles.clearstone_data import (facility_to_equip, facility_to_pneumatics)

def multipleregression(facilities_dataset):
    # IndependentVariables: Gas prod, oil prod, age, facility type,

    # #analysis pre-checks
    # print(facilities_dataset.head())
    # print(facilities_dataset.shape)
    # print(facilities_dataset.isna().sum())
    # print(facilities_dataset.duplicated().any())

    # #check for outliers in independant variables
    # fig, axs = plt.subplots(3, figsize=(5, 5))
    # plt1 = sns.boxplot(facilities_dataset['TV'], ax=axs[0], orient="h")
    # plt2 = sns.boxplot(facilities_dataset['Newspaper'], ax=axs[1], orient="h")
    # plt3 = sns.boxplot(facilities_dataset['Radio'], ax=axs[2], orient="h")
    # plt.tight_layout()
    # plt.show()
    #
    # sns.distplot(facilities_dataset['Sales']);

    # sns.pairplot(facilities_dataset, x_vars=['PROD_gas', 'PROD_oil', 'Age'], y_vars='FUGITIVE (e3m3)', height=4, aspect=1, kind='scatter')
    # plt.show()
    #
    # sns.heatmap(facilities_dataset.corr(), annot=True)
    # plt.show()

    # Setting the value for X and Y
    x = facilities_dataset[['PROD_gas', 'PROD_oil', 'Age']]
    y = facilities_dataset['FUGITIVE (e3m3)']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=100)
    mlr = LinearRegression()
    mlr.fit(x_train, y_train)
    # Printing the model coefficients
    print("Intercept: ", mlr.intercept_)
    print(list(zip(x, mlr.coef_)))

    intercept = mlr.intercept_
    coefficient = list(zip(x, mlr.coef_))

    # Predicting the Test and Train set result
    y_pred_mlr = mlr.predict(x_test)
    x_pred_mlr = mlr.predict(x_train)
    print("Prediction for test set: {}".format(y_pred_mlr))
    # Actual value and the predicted value
    mlr_diff = pd.DataFrame({'Actual value': y_test, 'Predicted value': y_pred_mlr})
    # print the R-squared value for the model
    print('R squared value of the model: {:.2f}'.format(mlr.score(x, y) * 100))

    difference = y_test - y_pred_mlr
    rvalue = mlr.score(x, y) * 100

    # 0 means the model is perfect. Therefore the value should be as close to 0 as possible
    meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
    meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
    rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))

    print('Mean Absolute Error:', meanAbErr)
    print('Mean Square Error:', meanSqErr)
    print('Root Mean Square Error:', rootMeanSqErr)

    mean_abs_err = meanAbErr
    mean_sq_err = meanSqErr
    rootmean_err = rootMeanSqErr

    return intercept, coefficient, difference, rvalue, mean_abs_err, mean_sq_err, rootmean_err

if __name__ == '__main__':
    # data_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\advertising.csv"
    # data_df = pd.read_csv(data_path)
    data_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\2022v10_oilgasfacilityvol.csv"
    data_df = pd.read_csv(data_path)

    #equipment counts
    fac_to_equip_df = facility_to_equip()
    fac_to_equip_df['sum_equip'] = fac_to_equip_df.sum(axis=1)
    fac_to_pneuNG_df, fac_to_pneuIA_df = facility_to_pneumatics()
    fac_to_pneuNG_df['sum_NGpneu'] = fac_to_pneuNG_df.sum(axis=1)

    # data_df = data_df[data_df['ReportingFacilitySubType']==351] #only single well oil batteries
    data_df = data_df[data_df['Area'] == 'AB']
    data_df = data_df.dropna(subset=['FUGITIVE (m3)'])
    data_df['Age'] = 2022 - pd.to_numeric(data_df['Year Well Spudded'])
    data_df['Age'] = data_df['Age'].fillna(data_df['Age'].mean(axis=0))
    subsetdata_df = data_df[['PROD_gas', 'PROD_oil', 'Age', 'FUGITIVE (m3)', 'FLARE_gas', 'ventvol', 'DISP_gas', 'Latitude', 'Longitude', 'ReportingFacilitySubType']]
    subsetdata_df = subsetdata_df.apply(pd.to_numeric)
    subsetdata_df['FUGITIVE (e3m3/m)'] = subsetdata_df['FUGITIVE (m3)']/1000/12
    subsetdata_df = subsetdata_df.set_index('ReportingFacilitySubType').join(fac_to_equip_df)
    subsetdata_df = subsetdata_df.join(fac_to_pneuNG_df)
    # subsetdata_df = subsetdata_df.reset_index(names=['ReportingFacilitySubType'])

    # subsetdata_df['AGE*PROD_gas'] = subsetdata_df['Age']* subsetdata_df['PROD_gas']
    # subsetdata_df['AGE*PROD_oil'] = subsetdata_df['Age']* subsetdata_df['PROD_oil']
    # subsetdata_df['AGE*FLARE_gas'] = subsetdata_df['Age']* subsetdata_df['FLARE_gas']
    # subsetdata_df['AGE*ventvol'] = subsetdata_df['Age']* subsetdata_df['ventvol']
    # subsetdata_df['AGE^2'] = subsetdata_df['Age']**2
    # subsetdata_df['PROD_gas^2'] = subsetdata_df['PROD_gas'] ** 2
    # subsetdata_df['PROD_oil^2'] = subsetdata_df['PROD_oil'] ** 2

    subsetdata_df.to_csv(r'C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Equipment Inventory\regressionmodellingdataset.csv')

    intercept, coefficient, difference, rvalue, mean_abs_err, mean_sq_err, rootmean_err = multipleregression(subsetdata_df)