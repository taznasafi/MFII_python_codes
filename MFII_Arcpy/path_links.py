import os
########################
# _01_LTE
########################
# xxxxxxxxxxxxxxxxxxxxxxxxx 01 create LTE xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# import state boundary to gdb
_01_gdb_name = "state_boundary_2010_wgs84"
raw_state_boundary_path =r"D:\Census_Data\tl_2010_state10_wgs84"

# import LTE 5
_02_gdb_name = "LTE5_Coverages"

# clip LTE 5 by state
_03_gdb_name = "Clip_by_State"

# Dissolve by pid and state
_04_gdb_name = "LTE_Diss_by_pid_state"

# Split LTE 5 by State and PID
_05_gdb_name = "split_LTE5_coverages"

# xxxxxxxxxxxxxxxxxxxxxxxxx 02 create LTE xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

_06_gdb_name = "merged_LTE5"

_07_gdb_name = "LTE_Diss_by_pid_state"




#basepath
outputbasepath = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages"

subsidy_table_path =r"E:\MFII_Dec2016\CSV Files\New_csv\CSV_TABLES.gdb\cetc_subsidy_pid_pivot"



#state boundary  gdb path
state_boundary_gdb = os.path.join(outputbasepath,_01_gdb_name)

#raw Coverages form 477 bgdby
Coverage_path_gdb = r"D:\Coverage_data\F-477\2016Dec\GDB\F477_bd_projected.gdb"

# state_grid
raw_state_grid = r"E:\state_boundary_jon"


#state Fips csv
Fips_table_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\state FiPS.txt"

# Number of LTE 5 providers per state
LTE5_table_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\LTE5_number_of_providers_per_state.csv"

dba_provider_dec2016_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\wtb_dba_provider_dec2016.csv"


#wirecenter
wireCenter_fc_path = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\Wirecenter_working.gdb\_merged_wirecenters_pviot"

#wire center splits
wirecenter_splits_gdb_path = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\_03_split_subsidized_coverage.gdb"

# MF II Blocks subsidy
mfIIblocks_split_gdb_path = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\_split_MFII_subsidy_by_state_pid.gdb"


#filer_pid_maping
filer_pid_mapping_table_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\filer_pid_map-f477_dec2016_07aug2017_inventory-final.csv"

#MFII table
MFII_table =r"E:\MFII_Dec2016\CSV Files\New_csv\CSV_TABLES.gdb\mf1_subsidy_pid_block_release_candidate_sep2017"

#blocks shapefile
blocks_shapefile_path = r'D:\Census_Data\tl_2010_tabblock10_wgs84'

#blocks gdb
blocks_gdb_path = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\mfII_Blocks_2010_wgs.gdb"

# water blocks gdb
water_blocks_gdb = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\water_area_blocks_Grid.gdb"


#lete 5 clip
LTE5_coverage = os.path.join(outputbasepath, _03_gdb_name)
lte5clip_gdp_path = os.path.join(outputbasepath,"Clip_by_State.gdb" )

#lte 5 merged

LTE5_merged_gdb_path = os.path.join(outputbasepath, "_merged_LTE5.gdb")

LTE5_diss_gdb_path = os.path.join(outputbasepath, "LTE_Diss_by_pid_state.gdb")

# LTE 5 Split

LTE5Split_gdb_path = os.path.join(outputbasepath, "_04_split_LTE5_coverages.gdb")


# LTE 5 Coverages

LTE5_coverage_minus_subsidy = os.path.join(outputbasepath, "_coverage_minus_subsidy_mfi.gdb")



# Ineligible area
ineligible_coverages_gdb_path = os.path.join(outputbasepath, "_intersect_ineligible_coverages.gdb")

# Ineligible area minus diminimus

ineligible_coverages_minus_diminimus_gdb_path = os.path.join(outputbasepath, "_provider_coverages_minus_diminimus.gdb")