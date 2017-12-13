import os

from MFII_tools.MFII_Arcpy import geotools, get_path, path_links

# 1------import_wirecenters to gdb

import_wirecenters = geotools.Tools()

import_wirecenters.inputPath = path_links.basepath
import_wirecenters.outputName = "Wirecenter_vintages"
import_wirecenters.outputPathFolder = path_links.basepath
import_wirecenters.create_gdb()

# 2---import shapefile to gdb
import_wirecenters.outputGDB = os.path.join(path_links.basepath, import_wirecenters.outputName + ".gdb")
import_wirecenters.import_shapefiles_to_gdb("*")

# 3---merge output

import_wirecenters.inputGDB = os.path.join(path_links.basepath, import_wirecenters.outputName + ".gdb")

import_wirecenters.merge_feature_class("_merged_wirecenters")

# 3---join subsidy table with merged_wirecenters

right_table = path_links.subsidy_table_path
left_table_object = get_path.pathFinder(env_0=os.path.join(path_links.basepath, import_wirecenters.outputName + ".gdb"))
left_table_path = left_table_object.get_file_path_with_wildcard_from_gdb("_merged_wirecenters")

import_wirecenters.outputName = "Wirecenter_working"
import_wirecenters.create_gdb()

import_wirecenters.addJoin_and_copy_feature(left_table_path[0], right_table, create_id_field=1, joinField= "id", outpath= os.path.join(
    path_links.basepath, import_wirecenters.outputName + ".gdb", "_merged_wirecenters_pviot"),
                                            joinType="KEEP_COMMON")

