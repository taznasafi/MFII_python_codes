from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os

#import LTE 5
LTE5Import = geotools.Tools()
LTE5Import.outputPathFolder = path_links.outputbasepath
LTE5Import.outputGDBName = "LTE5_Coverages"
LTE5Import.outputGDB = os.path.join(LTE5Import.outputPathFolder, LTE5Import.outputGDBName +".gdb")
LTE5Import.create_gdb()
LTE5Import.inputGDB = path_links.Coverage_path
LTE5Import.importLTE5Coverages("*_83_*", LTE5Import.outputGDB)
LTE5Import.deleteEmptyfeaturesFiles(LTE5Import.outputGDB,"gdb")

#clip LTE 5 by states
clipLTE = geotools.Tools()
clipLTE.outputPathFolder = path_links.outputbasepath
clipLTE.outputGDBName = "Clip_by_State"
clipLTE.outputGDB = os.path.join(clipLTE.outputPathFolder, clipLTE.outputGDBName+".gdb")
clipLTE.create_gdb()
clipfeature = path_links.state_boundary_gdb
infeature = path_links.LTE5_coverage
clipLTE.clipshapefiles(clipfeature,infeature, "gdb")
clipLTE.deleteEmptyfeaturesFiles(clipLTE.outputGDB,"gdb")










