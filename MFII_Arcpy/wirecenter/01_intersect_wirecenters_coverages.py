import os
from arcpy import Exists as arcpyExist
from MFII_tools.Master.MFII_Arcpy import geotools, get_path, path_links

wirecenterIntersect = geotools.Tools()

wirecenterIntersect.outputPathFolder = path_links.basepath
wirecenterIntersect.outputName = "_01_intersect_subsidy_with_Grid"
wirecenterIntersect.create_gdb()

wirecenterIntersect.outputGDB = os.path.join(wirecenterIntersect.outputPathFolder, wirecenterIntersect.outputName + ".gdb")
wirecenterSplitPath = get_path.pathFinder()
LTE5Coverages_path = get_path.pathFinder()
states = wirecenterSplitPath.make_fips_list()


for fips in states:
    state_name = wirecenterSplitPath.query_state_name_by_fips(table_path=path_links.Fips_table_path, fips=fips)
    LTE5Coverages_path.env_0 = path_links.LTE5_gdb_path
    LTE5Coverages = LTE5Coverages_path.get_file_path_with_wildcard_from_gdb("*_"+fips+"_*")
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



droprows = get_path.pathFinder()
droprows.env_0 = os.path.join(wirecenterIntersect.outputGDB)






















