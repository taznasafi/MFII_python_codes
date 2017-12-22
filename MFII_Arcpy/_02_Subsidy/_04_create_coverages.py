from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os

#erase wirecenters from LTE5Coverage

erasewirecenters = geotools.Tools()

erasewirecenters.outputPathFolder = path_links.outputbasepath
erasewirecenters.outputGDBName = "_coverage_minus_subsidy"
erasewirecenters.create_gdb()
erasewirecenters.outputGDB = os.path.join(erasewirecenters.outputPathFolder, erasewirecenters.outputGDBName+".gdb")
erasewirecenters.erase_wireCenter_subsidy(path_links.wirecenter_splits_gdb_path, path_links.LTE5Split_gdb_path )


#erase MFI Coverages

MFi = geotools.Tools()
MFi.outputPathFolder = path_links.outputbasepath
MFi.outputGDBName = "_coverage_minus_subsidy_mfi"
MFi.create_gdb()
MFi.inputGDB = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\_coverage_minus_subsidy.gdb"
MFi.outputGDB = os.path.join(MFi.outputPathFolder, MFi.outputGDBName+".gdb")
MFi.erase_MFI_Blocks()
