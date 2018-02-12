import os
from arcpy import Exists as arcpyExist
from MFII_tools.Master.MFII_Arcpy import geotools, get_path, path_links




wirecenterIntersect = geotools.Tools()
wirecenterIntersect.outputPathFolder = path_links.inputbasepath
wirecenterIntersect.outputGDBName = "_01_intersect_subsidy_with_Grid"
wirecenterIntersect.create_gdb()
wirecenterIntersect.outputGDB = os.path.join(wirecenterIntersect.outputPathFolder, wirecenterIntersect.outputGDBName + ".gdb")
wirecenterSplitPath = get_path.pathFinder()
LTE5Coverages_path = get_path.pathFinder()


states = wirecenterSplitPath.make_fips_list()


for fips in states:
    state_name = wirecenterSplitPath.query_state_name_by_fips(table_path=path_links.Fips_table_path, fips=fips)

    LTE5Coverages_path.env_0 = path_links.LTE5_diss_gdb_path+".gdb"
    LTE5Coverages = LTE5Coverages_path.get_file_path_with_wildcard_from_gdb("*_"+fips)
    print(LTE5Coverages)

    if len(LTE5Coverages) ==0:
        print("the coverage list was empty, passing this fips")
    else:
        intersectlist =[path_links.wireCenter_fc_path, LTE5Coverages[0]]
        outpath = os.path.join(wirecenterIntersect.outputGDB, "wirecenter_intersect_Coverages_"+fips)

        if arcpyExist(outpath):
            print("the file exits, skipping")
        else:
            wirecenterIntersect.intersect_files(intersectlist, outpath)




droprows_geotool = geotools.Tools()

droprows_geotool.outputPathFolder = path_links.inputbasepath
droprows_geotool.outputGDBName = "_01A_cleaned_intersect_subsidy_with_LTE5"
droprows_geotool.create_gdb()
droprows_geotool.inputGDB = wirecenterIntersect.outputGDB
droprows_geotool.outputGDB = os.path.join(droprows_geotool.outputPathFolder, droprows_geotool.outputGDBName + ".gdb")

# export clean wire centers
droprows_geotool.CopyFeatureclassToFeatureclass_with_expression()

# delete feature classes that are empty

deleteFC = geotools.Tools.deleteEmptyfeaturesFiles(droprows_geotool.outputGDB,"gdb")

# create subsidized coverages:

subCoverage = geotools.Tools()

subCoverage.inputGDB = droprows_geotool.outputGDB

subCoverage.outputGDBName = path_links.wirecenter_subsidized_gdb_name
subCoverage.outputPathFolder = path_links.inputbasepath
subCoverage.create_gdb()
subCoverage.outputGDB = os.path.join(subCoverage.outputPathFolder, subCoverage.outputGDBName+".gdb")

subCoverage.export_subsidized_Coverage()

deleteSubCoverageFC = geotools.Tools.deleteEmptyfeaturesFiles(subCoverage.outputGDB,"gdb")

# split the coverages by state and provider
splitSubsidized_Coverages = geotools.Tools()
splitSubsidized_Coverages.inputGDB = subCoverage.outputGDB
splitSubsidized_Coverages.outputPathFolder = path_links.inputbasepath
splitSubsidized_Coverages.outputGDBName = path_links.wirecenter_splits_gdb_name
splitSubsidized_Coverages.create_gdb()
splitSubsidized_Coverages.outputGDB = os.path.join(splitSubsidized_Coverages.outputPathFolder, splitSubsidized_Coverages.outputGDBName+".gdb")
splitSubsidized_Coverages.splitCoverages(split_fields=["STATE_FIPS", "pid"])














