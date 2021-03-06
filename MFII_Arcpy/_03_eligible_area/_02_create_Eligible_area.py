from MFII_Arcpy import path_links, get_path, geotools
import os

# merge the coverages

merge = geotools.Tools()
merge.outputPathFolder = path_links.inputbasepath
merge.outputGDBName = "_merged_ineligible_area"
merge.create_gdb()
merge.inputGDB = os.path.join(path_links.outputbasepath, path_links.deminimus_ineligible_area_gdb_name+".gdb")
merge.outputGDB = os.path.join(merge.outputPathFolder, merge.outputGDBName+".gdb")
merge.merge_ineligible_coverages()

# erase ineligible area from state grid

erase = geotools.Tools()
erase.outputPathFolder = path_links.inputbasepath
erase.outputGDBName = "_eligible_area"
erase.create_gdb()
erase.inputGDB = merge.outputGDB
erase.outputGDB = os.path.join(erase.outputPathFolder, erase.outputGDBName+".gdb")
erase.erase_coverages_from_state_boundary()

# erase water area from eligible area

erasewater = geotools.Tools()
erasewater.outputPathFolder = path_links.outputbasepath
erasewater.outputGDBName = "_eligible_area_minus_water_area"
erasewater.create_gdb()
erasewater.outputGDB = os.path.join(erasewater.outputPathFolder, erasewater.outputGDBName+".gdb")
erasewater.inputGDB = erase.outputGDB
erasewater.erase_water_blocks_from_eligible_area()



addfield = geotools.Tools()
addfield.inputGDB = erasewater.outputGDB
addfield.add_field_for_all_fc("ELIG_AREA","DOUBLE", field_length=None)
addfield.calculate_area_in_meters("ELIG_AREA")