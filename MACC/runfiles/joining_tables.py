import pandas as pd

def joinpipelinedata():
    shapefilewell_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\ST37_SH_GCS_NAD83.csv"
    datafile_well_df = pd.read_csv(shapefilewell_path)

    neartable_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\ST37_NearTable_TableToExcel.csv"
    datafile_neartable_df = pd.read_csv(neartable_path)

    abdata_path = r"C:\Users\jyuan\OneDrive - University of Calgary\PTAC\Well Infrastructure-AB.csv"
    abdata_df = pd.read_csv(abdata_path)

    well_pipeline_neartable_df = datafile_well_df.set_index('FID').join(datafile_neartable_df.set_index('IN_FID'))

    well_pipeline_neartable_df.reset_index()
    ab_well_pipeline_neartable_df = well_pipeline_neartable_df.set_index('SurfLoc').join(abdata_df.set_index('Surface DLS'))

    print(ab_well_pipeline_neartable_df)

if __name__ == '__main__':



    joinpipelinedata()

