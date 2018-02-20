from MFII_python_codes.MFII_Arcpy import path_links, get_path, geotools
import os

#intesect_ineligible area with grid

intersect_coverages = geotools.Tools()
intersect_coverages.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
intersect_coverages.outputGDBName = path_links.intersect_inelligible_coverages_gdb_name
intersect_coverages.create_gdb()
intersect_coverages.inputGDB = os.path.join(r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files",
                                            path_links.mfi_blocks_erased_gdb_name+".gdb")
intersect_coverages.outputGDB = os.path.join(intersect_coverages.outputPathFolder,
                                             intersect_coverages.outputGDBName+".gdb")
intersect_coverages.intersect_coverages_by_stateGrid(lte_output_table_folder_path=r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files")


# dissolve the by grid

diss_coverages = geotools.Tools()
diss_coverages.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
diss_coverages.outputGDBName = path_links.diss_inelligible_by_grid_gdb_name
diss_coverages.create_gdb()
diss_coverages.inputGDB = intersect_coverages.outputGDB
diss_coverages.outputGDB = os.path.join(diss_coverages.outputPathFolder,
                                        diss_coverages.outputGDBName+".gdb")
diss_coverages.dissolve_ineligible_coverages()

# erase water area

erase_water_areas = geotools.Tools()
erase_water_areas.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files"
erase_water_areas.outputGDBName = path_links.ineligible_area_with_wateronly
erase_water_areas.create_gdb()
erase_water_areas.outputGDB = os.path.join(erase_water_areas.outputPathFolder,
                                           erase_water_areas.outputGDBName+".gdb")
erase_water_areas.inputGDB = diss_coverages.outputGDB
erase_water_areas.erase_water_blocks_from_coverage(lte_table_output_folder=r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files")


# add field

addfield = geotools.Tools()
addfield.inputGDB = erase_water_areas.outputGDB
addfield.add_field_for_all_fc("AREA","DOUBLE", field_length=None)
#

addfield.calculate_area_in_meters("AREA")


# deminimus area taken away from Coverages

deminimus = geotools.Tools()
deminimus.inputGDB = erase_water_areas.outputGDB
deminimus.outputPathFolder = r"D:\FCC_GIS_Projects\MFII\DataCollection\final_eligible_area\MFII_python_codes\Coverages\updated_files\output"
deminimus.outputGDBName = path_links.deminimus_ineligible_area_gdb_name
deminimus.create_gdb()
deminimus.outputGDB = os.path.join(deminimus.outputPathFolder, deminimus.outputGDBName+".gdb")
deminimus.drop_diminimus_area()