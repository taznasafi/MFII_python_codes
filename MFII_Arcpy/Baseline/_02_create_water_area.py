from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os


#create water area from blocks
water_area = geotools.Tools()
water_area.outputPathFolder = path_links.inputbasepath
water_area.outputGDBName = "water_area_blocks"
water_area.create_gdb()
water_area.inputGDB = path_links.blocks_gdb_path
water_area.outputGDB = os.path.join(water_area.outputPathFolder, water_area.outputGDBName+".gdb")
water_area.create_water_area_blocks("ALAND10 = 0")


#dissovle water area

diss_water_area = geotools.Tools()
diss_water_area.inputGDB = water_area.outputGDB
diss_water_area.outputPathFolder = path_links.inputbasepath
diss_water_area.outputGDBName = "water_area_blocks_diss"
diss_water_area.create_gdb()
diss_water_area.outputGDB = os.path.join(diss_water_area.outputPathFolder,diss_water_area.outputGDBName+".gdb")
diss_water_area.dissolveWaterArea()

#Intersect_water_area_with_grid

intersect = geotools.Tools()
intersect.inputGDB = diss_water_area.outputGDB
intersect.outputPathFolder = path_links.inputbasepath
intersect.outputGDBName = "water_area_blocks_Grid"
intersect.create_gdb()
intersect.outputGDB = os.path.join(intersect.outputPathFolder, intersect.outputGDBName+".gdb")
intersect.intersect_water_by_stateGrid()



# add field

addfield = geotools.Tools()

addfield.inputGDB = intersect.outputGDB
addfield.add_field_for_all_fc("WATER_AREA","DOUBLE",field_length=None)
addfield.calculate_area_in_meters("WATER_AREA")
