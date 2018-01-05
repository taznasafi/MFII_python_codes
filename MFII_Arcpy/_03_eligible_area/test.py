from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os

'''
erase_water_areas = geotools.Tools()
erase_water_areas.outputPathFolder = path_links.outputbasepath
erase_water_areas.outputGDBName = "_ineligible_area_minus_water_area"
erase_water_areas.create_gdb()
erase_water_areas.outputGDB = os.path.join(erase_water_areas.outputPathFolder, erase_water_areas.outputGDBName+".gdb")
erase_water_areas.inputGDB = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\_dissovled_ineligible_coverages.gdb"
erase_water_areas.erase_water_blocks_from_coverage()



# add field

addfield = geotools.Tools()

addfield.inputGDB = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\water_area_blocks_Grid.gdb"
addfield.add_field_for_all_fc("WATER_AREA","DOUBLE",field_length=None)
addfield.calculate_area_in_meters("WATER_AREA")
'''

# deminimus area

deminimus = geotools.Tools()
deminimus.inputGDB = r"E:\MFII_Dec2016\GIS\Subsidy_information\WireCenter_Vintages\water_area_blocks_Grid.gdb"
deminimus.outputPathFolder = path_links.inputbasepath
deminimus.outputGDBName = "_provider_coverages_minus_diminimus"
deminimus.outputGDB = os.path.join(deminimus.outputPathFolder, deminimus.outputGDBName+".gdb")
deminimus.drop_diminimus_area()