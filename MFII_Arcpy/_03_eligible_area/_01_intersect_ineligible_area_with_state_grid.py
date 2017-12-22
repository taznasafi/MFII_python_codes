from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os

#intesect_eligible area

intersect_coverages = geotools.Tools()
intersect_coverages.outputPathFolder = path_links.outputbasepath
intersect_coverages.outputGDBName = "_intersect_ineligible_coverages"
intersect_coverages.create_gdb()
intersect_coverages.inputGDB = path_links.LTE5_coverage_minus_subsidy
intersect_coverages.outputGDB = os.path.join(intersect_coverages.outputPathFolder, intersect_coverages.outputGDBName+".gdb")
intersect_coverages.intersect_coverages_by_stateGrid()


# dissolve the by grid

diss_coverages = geotools.Tools()
diss_coverages.outputPathFolder = path_links.outputbasepath
diss_coverages.outputGDBName = "_dissovled_ineligible_coverages"
diss_coverages.create_gdb()
diss_coverages.inputGDB = intersect_coverages.outputGDB
diss_coverages.outputGDB = os.path.join(diss_coverages.outputPathFolder, diss_coverages.outputGDBName)
diss_coverages.dissolve_ineligible_coverages()

# erase water area


erase_water_areas = geotools.Tools()
erase_water_areas.outputPathFolder = path_links.outputbasepath
erase_water_areas.outputGDBName = "__ineligible_area_minus_water_area"
erase_water_areas.create_gdb()
erase_water_areas.outputGDB = os.path.join(erase_water_areas.outputPathFolder, erase_water_areas.outputGDBName+".gdb")
erase_water_areas.inputGDB = diss_coverages.outputGDB
erase_water_areas.erase_water_blocks_from_coverage()