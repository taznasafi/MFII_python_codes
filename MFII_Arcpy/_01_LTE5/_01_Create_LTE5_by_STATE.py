from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os



#import_state boundary to gdb
state = geotools.Tools()
state.outputPathFolder = path_links.outputbasepath
state.inputPath = path_links.raw_state_boundary_path
state.outputGDBName = path_links._01_gdb_name
state.outputGDB = os.path.join(state.outputPathFolder, state.outputGDBName +".gdb")
state.create_gdb()
state.importShapefilesToGDB()



#import LTE 5
LTE5Import = geotools.Tools()
LTE5Import.outputPathFolder = path_links.outputbasepath
LTE5Import.outputGDBName = path_links._02_gdb_name
LTE5Import.outputGDB = os.path.join(LTE5Import.outputPathFolder, LTE5Import.outputGDBName +".gdb")
LTE5Import.create_gdb()
LTE5Import.inputGDB = path_links.Coverage_path_gdb
LTE5Import.importLTE5Coverages("*_83_*", LTE5Import.outputGDB)
LTE5Import.deleteEmptyfeaturesFiles(LTE5Import.outputGDB,"gdb")

#clip LTE 5 by states
clipLTE = geotools.Tools()
clipLTE.outputPathFolder = path_links.outputbasepath
clipLTE.outputGDBName = path_links._03_gdb_name
clipLTE.outputGDB = os.path.join(clipLTE.outputPathFolder, clipLTE.outputGDBName+".gdb")
clipLTE.create_gdb()
clipfeature = os.path.join(path_links.outputbasepath,path_links._01_gdb_name+".gdb")
infeature = path_links.LTE5_coverage
clipLTE.clipshapefiles(clipfeature,infeature, "gdb")
clipLTE.deleteEmptyfeaturesFiles(clipLTE.outputGDB,"gdb")

#ADD PID AND STATE FIPS
pid = geotools.Tools()
pid.inputGDB = clipLTE.outputGDB
pid.attach_pid_StateFips_toCoverages()

#Dissolve by pid and state
dissovle = geotools.Tools()
dissovle.inputGDB = path_links.LTE5_merged_gdb_path
dissovle.outputPathFolder = path_links.outputbasepath
dissovle.outputGDBName = path_links._04_gdb_name
dissovle.create_gdb()
dissovle.outputGDB = os.path.join(dissovle.outputPathFolder, dissovle.outputGDBName+".gdb")
dissovle.dissolveCoverages()


#split LTE 5 by State and PID
split_LTE5 = geotools.Tools()
split_LTE5.outputPathFolder = path_links.outputbasepath
split_LTE5.outputGDBName = path_links._05_gdb_name
split_LTE5.create_gdb()
split_LTE5.inputGDB = path_links.LTE5_diss_gdb_path
split_LTE5.outputGDB = os.path.join(split_LTE5.outputPathFolder, split_LTE5.outputGDBName+".gdb")
split_LTE5.splitCoverages(split_fields=['STATE_FIPS', "PID"])





# create number of LTE 5 providers per state


LTE5table = geotools.Tools()
LTE5table.inputGDB = path_links.LTE5_diss_gdb_path

LTE5table.create_number_LTE5_perState_table()




