from MFII_python_codes.MFII_Arcpy import path_links, get_path, geotools
import os

print("erase wirecenters from LTE5Coverage")

erasewirecenters = geotools.Tools()

erasewirecenters.outputPathFolder = path_links.inputbasepath
erasewirecenters.outputGDBName = path_links.coverage_minus_subsidy_gdb_name
erasewirecenters.create_gdb()
erasewirecenters.outputGDB = os.path.join(erasewirecenters.outputPathFolder, erasewirecenters.outputGDBName+".gdb")
erasewirecenters.erase_wireCenter_subsidy(wirecenterEnv=os.path.join(path_links.inputbasepath, path_links.wirecenter_splits_gdb_name+".gdb"),
                                          LTE5CoverageEnv=os.path.join(path_links.inputbasepath, path_links._06_gdb_name+ ".gdb"),
                                          lte5_table_folder_path=path_links.inputbasepath)


print("erase MFI Coverages")

MFi = geotools.Tools()
MFi.outputPathFolder = path_links.inputbasepath
MFi.outputGDBName =path_links.mfi_blocks_erased_gdb_name
MFi.create_gdb()
MFi.inputGDB =erasewirecenters.outputGDB
MFi.outputGDB = os.path.join(MFi.outputPathFolder, MFi.outputGDBName+".gdb")
MFi.erase_MFI_Blocks(lte_tableList_folder=path_links.inputbasepath)
