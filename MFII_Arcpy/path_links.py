import os
########################
# _01_LTE              #
########################
# xxxxxxxxxxxxxxxxxxxxxxxxx 01 create LTE by state.py xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# import state boundary to gdb
_01_gdb_name = "state_boundary_2010_wgs84"


# import LTE 5
_02_gdb_name = "LTE5_Coverages"

# clip LTE 5 by state
_03_gdb_name = "Clip_by_State"

# merage by state
_04_gdb_name = "merged_LTE5"

# Dissolve by pid and state
_05_gdb_name = "LTE_Diss_by_pid_state"

# Split LTE 5 by State and PID
_06_gdb_name = "split_LTE5_coverages"

# xxxxxxxxxxxxxxxxxxxxxxx input file paths xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#basepath for output
wirecenter_vintages_path = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages"

#basepath for input
inputbasepath =r"D:\FCC_GIS_Projects\MFII\June2017_Eligible_area\input"

#basepath for output
outputbasepath = r"D:\FCC_GIS_Projects\MFII\June2017_Eligible_area\output"

# raw state boundary shapefiles
raw_state_boundary_path =r"D:\Census_Data\tl_2010_state10_wgs84"

#state boundary  gdb path
state_boundary_gdb = os.path.join(inputbasepath,_01_gdb_name+".gdb")

# wirecenter subsidy table already pivoted
subsidy_table_path =r"E:\MFII_Dec2016\CSV Files\New_csv\CSV_TABLES.gdb\cetc_subsidy_pid_pivot"

#raw Coverages form 477 gdb
Coverage_path_gdb = r"D:\Coverage_data\F-477\2017June\f477_geom_bd_orig.gdb"


# state_grid
raw_state_grid = r"E:\state_boundary_jon"


#state Fips csv
Fips_table_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\state FiPS.txt"

# Number of LTE 5 providers per state
LTE5_table_path = "LTE5_number_of_providers_per_state.csv"

dba_provider_dec2016_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\wtb_dba_provider_dec2016.csv"

########################
#     Subsidy          #
########################

########################################### wirecenters ##########################################

# import wire center 1

wirecenter_vintages_name = "Wirecenter_vintages"

#wirecenter
wireCenter_fc_path = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\Wirecenter_working.gdb\_merged_wirecenters_pviot"

#wirecenter subsidzed coverage
wirecenter_subsidized_gdb_name = "_02_subsidized_coverage"

#wire center splits
wirecenter_splits_gdb_name = "_03_split_subsidized_coverage"

#coverage_minus_wirecenter_subsidy

coverage_minus_subsidy_gdb_name = "_coverage_minus_subsidy"

mfi_subsidized_blocks_gdb_name = "MFII_blocks_by_state_with_pid"

# erase mF i blocks
mfi_blocks_erased_gdb_name = "_coverage_minus_subsidy_mfi"

#mfi blocks that are subsidized splits
mfi_subsidized_splits_gdb_name = "04_split_MFI_subsidy_by_state_pid"

LTE5_diss_gdb_path = os.path.join(inputbasepath, "LTE_Diss_by_pid_state")

diced_lte5 = os.path.join(inputbasepath, "_diced_LTE5_Coverages")


########################
#    Eligible Area     #
########################


# intersect the ineligible area
intersect_inelligible_coverages_gdb_name = "_intersect_ineligible_coverages"

# dissolve ineligible area by grid
diss_inelligible_by_grid_gdb_name = "_dissovled_ineligible_coverages"

# Ineligible area with water only
ineligible_area_with_wateronly = "_ineligible_area_minus_water_area"

# erase water area from Eligible area
erase_water_from_ineligible_area_gdb_name = "_ineligible_area_minus_water_area"


#deminimus ineligible area
deminimus_ineligible_area_gdb_name = "_provider_coverages_minus_diminimus"


#filer_pid_maping
#filer_pid_mapping_table_path = r"E:\MFII_Dec2016\MFII_python_codes\CSVs\filer_pid_map-f477_dec2016_07aug2017_inventory-final.csv"
filer_pid_mapping_table_path = r"D:\FCC_GIS_Projects\MFII\June2017_Eligible_area\csv\providers_featureclass-f477_jun2017.csv"

#MFII table
MFII_table =r"E:\MFII_Dec2016\CSV Files\New_csv\CSV_TABLES.gdb\mf1_subsidy_pid_block_release_candidate_sep2017"

#blocks shapefile
blocks_shapefile_path = r'D:\Census_Data\tl_2010_tabblock10_wgs84'

#blocks gdb
blocks_gdb_path = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\mfII_Blocks_2010_wgs.gdb"

# water blocks gdb
water_blocks_gdb = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\water_area_blocks_Grid.gdb"


#lete 5 clip
LTE5_coverage = os.path.join(inputbasepath, _03_gdb_name+".gdb")
lte5clip_gdp_path = os.path.join(inputbasepath, "Clip_by_State.gdb")

