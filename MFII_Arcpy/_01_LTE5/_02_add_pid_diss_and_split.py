from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os

#ADD PID AND STATE FIPS to the cliped LTE 5
pid = geotools.Tools()
pid.inputGDB = os.path.join(path_links.inputbasepath, path_links._03_gdb_name+".gdb")
pid.attach_pid_StateFips_toCoverages()


# Merge cliped LTE 5
merge = geotools.Tools()
merge.inputGDB = os.path.join(path_links.inputbasepath,path_links._03_gdb_name+".gdb")
merge.outputPathFolder = path_links.inputbasepath
merge.outputGDBName = path_links._06_gdb_name
merge.create_gdb()
merge.outputGDB = os.path.join(merge.outputPathFolder, merge.outputGDBName+".gdb")
merge.mergeCoverages()



#dissolve by pid and state

dissovle = geotools.Tools()
dissovle.inputGDB = os.path.join(path_links.inputbasepath,path_links._06_gdb_name+".gdb")
dissovle.outputPathFolder = path_links.inputbasepath
dissovle.outputGDBName = path_links._07_gdb_name
dissovle.create_gdb()
dissovle.outputGDB = os.path.join(dissovle.outputPathFolder, dissovle.outputGDBName+".gdb")
dissovle.dissolveCoverages()



#split LTE 5 by State and PID
split_LTE5 = geotools.Tools()
split_LTE5.outputPathFolder = path_links.inputbasepath
split_LTE5.outputGDBName = _08_gdb_name
split_LTE5.inputGDB = os.path.join(path_links.inputbasepath, path_links._07_gdb_name+".gdb")
split_LTE5.create_gdb()
split_LTE5.outputGDB = os.path.join(split_LTE5.outputPathFolder, split_LTE5.outputGDBName+".gdb")
split_LTE5.splitCoverages(split_fields=['STATE_FIPS', "PID"])


