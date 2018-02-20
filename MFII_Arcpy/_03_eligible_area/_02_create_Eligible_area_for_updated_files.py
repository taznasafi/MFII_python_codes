from MFII_Arcpy import path_links, get_path, geotools
import os

# merge the coverages

merge = geotools.Tools()
merge.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
merge.outputGDBName = "_merged_ineligible_area"
merge.create_gdb()
merge.inputGDB = os.path.join(r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files\output",
                              path_links.deminimus_ineligible_area_gdb_name+".gdb")
merge.outputGDB = os.path.join(merge.outputPathFolder, merge.outputGDBName+".gdb")
merge.merge_ineligible_coverages()

# erase ineligible area from state grid

erase = geotools.Tools()
erase.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
erase.outputGDBName = "_eligible_area"
erase.create_gdb()
erase.inputGDB = merge.outputGDB
erase.outputGDB = os.path.join(erase.outputPathFolder, erase.outputGDBName+".gdb")
erase.erase_coverages_from_state_boundary()

# erase water area from eligible area

erasewater = geotools.Tools()
erasewater.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files\output"
erasewater.outputGDBName = "_eligible_area_minus_water_area"
erasewater.create_gdb()
erasewater.outputGDB = os.path.join(erasewater.outputPathFolder, erasewater.outputGDBName+".gdb")
erasewater.inputGDB = erase.outputGDB
erasewater.erase_water_blocks_from_eligible_area()



addfield = geotools.Tools()
addfield.inputGDB = erasewater.outputGDB
addfield.add_field_for_all_fc("ELIG_AREA","DOUBLE", field_length=None)
addfield.calculate_area_in_meters("ELIG_AREA")