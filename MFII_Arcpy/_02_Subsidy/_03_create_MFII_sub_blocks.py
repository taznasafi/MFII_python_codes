import os

from MFII_tools.Master.MFII_Arcpy import geotools, get_path, path_links

# 1------import_wirecenters to gdb

mfIIBlocks = geotools.Tools()

mfIIBlocks.inputPath = path_links.blocks_shapefile_path
mfIIBlocks.outputGDBName = "mfII_Blocks_2010_wgs"
mfIIBlocks.outputPathFolder = path_links.outputbasepath
mfIIBlocks.create_gdb()

# 2---import shapefile to gdb
mfIIBlocks.outputGDB = os.path.join(path_links.outputbasepath, mfIIBlocks.outputGDBName + ".gdb")
mfIIBlocks.import_shapefiles_to_gdb("*")



# --- create MFII subsidy_blocks

createMFIIBlocksbyState = geotools.Tools()
createMFIIBlocksbyState.inputGDB = mfIIBlocks.outputGDB
createMFIIBlocksbyState.outputPathFolder = path_links.outputbasepath
createMFIIBlocksbyState.outputGDBName = "MFII_blocks_by_state_with_pid"
createMFIIBlocksbyState.outputGDB = os.path.join(path_links.outputbasepath, createMFIIBlocksbyState.outputGDBName+".gdb")
createMFIIBlocksbyState.create_gdb()
createMFIIBlocksbyState.create_MFII_subsidy_blocks_by_state(path_links.MFII_table)
createMFIIBlocksbyState.deleteEmptyfeaturesFiles(createMFIIBlocksbyState.outputGDB,"gdb")

# --- split MFII subsidy blocks

# split the coverages by state and provider
splitSubsidized_Coverages = geotools.Tools()
splitSubsidized_Coverages.inputGDB = createMFIIBlocksbyState.outputGDB
splitSubsidized_Coverages.outputPathFolder = path_links.outputbasepath
splitSubsidized_Coverages.outputGDBName = "04_split_MFII_subsidy_by_state_pid"
splitSubsidized_Coverages.create_gdb()
splitSubsidized_Coverages.outputGDB = os.path.join(splitSubsidized_Coverages.outputPathFolder, splitSubsidized_Coverages.outputGDBName+".gdb")
splitSubsidized_Coverages.splitCoverages(split_fields=["STATEFP10", "provider_id"])

