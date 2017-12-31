from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os

# all of the end product will go in a input basefile path

#import_state boundary to gdb (1)
print("\n\n\t\t\timport_state boundary to gdb")
state = geotools.Tools()
state.outputPathFolder = path_links.inputbasepath
state.inputPath = path_links.raw_state_boundary_path
state.outputGDBName = path_links._01_gdb_name
state.outputGDB = os.path.join(state.outputPathFolder, state.outputGDBName +".gdb")
state.create_gdb()
state.importShapefilesToGDB()



#import LTE 5 (2)
print("\n\n\t\t\tImport LTE5")
LTE5Import = geotools.Tools()
LTE5Import.outputPathFolder = path_links.inputbasepath
LTE5Import.outputGDBName = path_links._02_gdb_name
LTE5Import.outputGDB = os.path.join(LTE5Import.outputPathFolder, LTE5Import.outputGDBName +".gdb")
LTE5Import.create_gdb()
LTE5Import.inputGDB = path_links.Coverage_path_gdb
LTE5Import.importLTE5Coverages("*_83_*", LTE5Import.outputGDB)
LTE5Import.deleteEmptyfeaturesFiles(LTE5Import.outputGDB,"gdb")

#clip LTE 5 by states (3)
print("\n\n\t\t\tclip LTE 5 by state")
clipLTE = geotools.Tools()
clipLTE.outputPathFolder = path_links.inputbasepath
clipLTE.outputGDBName = path_links._03_gdb_name
clipLTE.outputGDB = os.path.join(clipLTE.outputPathFolder, clipLTE.outputGDBName+".gdb")
clipLTE.create_gdb()
clipfeature = state.outputGDB
infeature = LTE5Import.outputGDB
clipLTE.clipshapefiles(clipfeature,infeature, "gdb")
clipLTE.deleteEmptyfeaturesFiles(clipLTE.outputGDB,"gdb")

#ADD PID AND STATE FIPS
print("\n\n\t\t\tADDing PID and STATE FiPS")
pid = geotools.Tools()
pid.inputGDB = clipLTE.outputGDB
pid.attach_pid_StateFips_toCoverages()

# Merge cliped LTE5 (4)
merge = geotools.Tools()
merge.inputGDB = clipLTE.outputGDB
merge.outputPathFolder = path_links.inputbasepath
merge.outputGDBName = path_links._04_gdb_name
merge.create_gdb()
merge.outputGDB = os.path.join(merge.outputPathFolder, merge.outputGDBName+".gdb")
merge.mergeCoverages()


#Dissolve by pid and state (5)
print("\n\n\t\t\tDissolving by pid and state")
dissovle = geotools.Tools()
dissovle.inputGDB = merge.outputGDB
dissovle.outputPathFolder = path_links.inputbasepath
dissovle.outputGDBName = path_links._05_gdb_name
dissovle.create_gdb()
dissovle.outputGDB = os.path.join(dissovle.outputPathFolder, dissovle.outputGDBName+".gdb")
dissovle.dissolveCoverages()


#split LTE 5 by State and PID (6)
print("\n\n\t\t\tSplit LTE 5 by State and PID")
split_LTE5 = geotools.Tools()
split_LTE5.outputPathFolder = path_links.inputbasepath
split_LTE5.outputGDBName = path_links._06_gdb_name
split_LTE5.create_gdb()
split_LTE5.inputGDB = os.path.join(path_links.inputbasepath, path_links._04_gdb_name )
split_LTE5.outputGDB = os.path.join(split_LTE5.outputPathFolder, split_LTE5.outputGDBName+".gdb")
split_LTE5.splitCoverages(split_fields=['STATE_FIPS', "PID"])





# create number of LTE 5 providers per state

print("\n\n\t\t\tCreate number of LTE5 provider by state")
LTE5table = geotools.Tools()
LTE5table.inputGDB = os.path.join(path_links.inputbasepath, path_links._04_gdb_name +".gdb")
LTE5table.create_number_LTE5_perState_table()




