import os

from MFII_tools.Master.MFII_Arcpy import geotools, get_path, path_links

print("1------import_wirecenters to gdb")

mfIIBlocks = geotools.Tools()

mfIIBlocks.inputPath = path_links.blocks_shapefile_path
mfIIBlocks.outputGDBName = "mfII_Blocks_2010_wgs"
mfIIBlocks.outputPathFolder = path_links.inputbasepath
mfIIBlocks.create_gdb()

print("2---import shapefile to gdb")
mfIIBlocks.outputGDB = os.path.join(path_links.inputbasepath, mfIIBlocks.outputGDBName + ".gdb")
mfIIBlocks.import_shapefiles_to_gdb("*")



print('--- create MFII subsidy_blocks')

createMFIIBlocksbyState = geotools.Tools()
createMFIIBlocksbyState.inputGDB = mfIIBlocks.outputGDB
createMFIIBlocksbyState.outputPathFolder = path_links.inputbasepath
createMFIIBlocksbyState.outputGDBName = path_links.mfi_subsidized_blocks_gdb_name
createMFIIBlocksbyState.outputGDB = os.path.join(path_links.inputbasepath, createMFIIBlocksbyState.outputGDBName + ".gdb")
createMFIIBlocksbyState.create_gdb()
createMFIIBlocksbyState.create_MFII_subsidy_blocks_by_state(path_links.MFII_table)
createMFIIBlocksbyState.deleteEmptyfeaturesFiles(createMFIIBlocksbyState.outputGDB,"gdb")

print('--- split MFII subsidy blocks')

# split the coverages by state and provider
splitSubsidized_Coverages = geotools.Tools()
splitSubsidized_Coverages.inputGDB = createMFIIBlocksbyState.outputGDB
splitSubsidized_Coverages.outputPathFolder = path_links.inputbasepath
splitSubsidized_Coverages.outputGDBName = path_links.mfi_subsidized_splits_gdb_name
splitSubsidized_Coverages.create_gdb()
splitSubsidized_Coverages.outputGDB = os.path.join(splitSubsidized_Coverages.outputPathFolder, splitSubsidized_Coverages.outputGDBName+".gdb")
splitSubsidized_Coverages.splitCoverages(split_fields=["STATEFP10", "provider_id"])

