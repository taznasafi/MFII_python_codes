from .MFII_Arcpy import path_links, get_path, geotools
import os

print("erase wirecenters from LTE5Coverage")

erasewirecenters = geotools.Tools()

erasewirecenters.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
erasewirecenters.outputGDBName = path_links.coverage_minus_subsidy_gdb_name
erasewirecenters.create_gdb()
erasewirecenters.outputGDB = os.path.join(erasewirecenters.outputPathFolder, erasewirecenters.outputGDBName+".gdb")
erasewirecenters.erase_wireCenter_subsidy(lte5_table_folder_path=r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files",wirecenterEnv=os.path.join(r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files", path_links.wirecenter_splits_gdb_name+".gdb"),
                                          LTE5CoverageEnv=os.path.join(r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files", path_links._06_gdb_name+ ".gdb"))


print("erase MFI Coverages")

MFi = geotools.Tools()
MFi.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
MFi.outputGDBName =path_links.mfi_blocks_erased_gdb_name
MFi.create_gdb()
MFi.inputGDB =erasewirecenters.outputGDB
MFi.outputGDB = os.path.join(MFi.outputPathFolder, MFi.outputGDBName+".gdb")
MFi.erase_MFI_Blocks(lte_tableList_folder=r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files")
