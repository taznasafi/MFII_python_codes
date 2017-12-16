import os

#basepath
outputbasepath = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages"

subsidy_table_path =r"E:\MFII_Dec2016\CSV Files\New_csv\CSV_TABLES.gdb\cetc_subsidy_pid_pivot"

raw_state_boundary_path =r"D:\Census_Data\tl_2010_state10_wgs84"
state_boundary_gdb = os.path.join(outputbasepath,"state_boundary_2010_wgs84.gdb")
Coverage_path = r"D:\Coverage_data\F-477\2016Dec\GDB\F477_bd_projected.gdb"
LTE5_coverage = os.path.join(outputbasepath, "LTE5_Coverages.gdb")


#state Fips csv
Fips_table_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\state FiPS.txt"

# Number of LTE 5 providers per state
LTE5_table_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\LTE5_number_of_providers_per_state.csv"

dba_provider_dec2016_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\wtb_dba_provider_dec2016.csv"

LTE5_gdb_path = os.path.join(outputbasepath,LTE5_coverage)

wireCenter_fc_path = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\Wirecenter_working.gdb\_merged_wirecenters_pviot"

