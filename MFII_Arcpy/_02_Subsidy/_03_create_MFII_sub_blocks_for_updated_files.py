import os

from MFII_python_codes.MFII_Arcpy import geotools, get_path, path_links

print("1------import block to gdb")

mfIIBlocks = geotools.Tools()

mfIIBlocks.inputPath = path_links.blocks_shapefile_path
mfIIBlocks.outputGDBName = "mfII_Blocks_2010_wgs"
mfIIBlocks.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
mfIIBlocks.create_gdb()

print("2---import shapefile to gdb")
mfIIBlocks.outputGDB = os.path.join(r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files", mfIIBlocks.outputGDBName + ".gdb")
mfIIBlocks.import_shapefiles_to_gdb("*")



print('--- create MFII subsidy_blocks')

createMFIIBlocksbyState = geotools.Tools()
createMFIIBlocksbyState.inputGDB = mfIIBlocks.outputGDB
createMFIIBlocksbyState.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
createMFIIBlocksbyState.outputGDBName = path_links.mfi_subsidized_blocks_gdb_name
createMFIIBlocksbyState.outputGDB = os.path.join(createMFIIBlocksbyState.outputPathFolder, createMFIIBlocksbyState.outputGDBName + ".gdb")
createMFIIBlocksbyState.create_gdb()
createMFIIBlocksbyState.create_MFII_subsidy_blocks_by_state(path_links.MFII_table)
createMFIIBlocksbyState.deleteEmptyfeaturesFiles(createMFIIBlocksbyState.outputGDB,"gdb")

print('--- split MFII subsidy blocks')

# split the coverages by state and provider
splitSubsidized_Coverages = geotools.Tools()
splitSubsidized_Coverages.inputGDB = createMFIIBlocksbyState.outputGDB
splitSubsidized_Coverages.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
splitSubsidized_Coverages.outputGDBName = path_links.mfi_subsidized_splits_gdb_name
splitSubsidized_Coverages.create_gdb()
splitSubsidized_Coverages.outputGDB = os.path.join(splitSubsidized_Coverages.outputPathFolder, splitSubsidized_Coverages.outputGDBName+".gdb")
splitSubsidized_Coverages.splitCoverages(split_fields=["STATEFP10", "provider_id"])

