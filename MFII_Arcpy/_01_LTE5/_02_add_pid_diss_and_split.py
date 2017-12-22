from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os






#ADD PID AND STATE FIPS
pid = geotools.Tools()
pid.inputGDB = path_links.lte5clip_gdp_path
pid.attach_pid_StateFips_toCoverages()


merge = geotools.Tools()
merge.inputGDB = path_links.lte5clip_gdp_path
merge.outputPathFolder = path_links.outputbasepath
merge.outputGDBName = "_merged_LTE5"
merge.create_gdb()
merge.outputGDB = os.path.join(merge.outputPathFolder, merge.outputGDBName+".gdb")
merge.mergeCoverages()



#dissolve by pid and state

dissovle = geotools.Tools()
dissovle.inputGDB = path_links.LTE5_merged_gdb_path
dissovle.outputPathFolder = path_links.outputbasepath
dissovle.outputGDBName = "LTE_Diss_by_pid_state"
dissovle.create_gdb()
dissovle.outputGDB = os.path.join(dissovle.outputPathFolder, dissovle.outputGDBName+".gdb")
dissovle.dissolveCoverages()



#split LTE 5 by State and PID
split_LTE5 = geotools.Tools()
split_LTE5.outputPathFolder = path_links.outputbasepath
split_LTE5.outputGDBName = "_04_split_LTE5_coverages"
split_LTE5.inputGDB = path_links.LTE5_diss_gdb_path
split_LTE5.create_gdb()
split_LTE5.outputGDB = os.path.join(split_LTE5.outputPathFolder, split_LTE5.outputGDBName+".gdb")
split_LTE5.splitCoverages(split_fields=['STATE_FIPS', "PID"])

