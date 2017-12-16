
from MFII_tools.Master.MFII_Arcpy import path_links, get_path, geotools
import os





#import_state boundary to gdb
state = geotools.Tools()
state.outputPathFolder = path_links.outputbasepath
state.inputPath = path_links.raw_state_boundary_path
state.outputGDBName = "state_boundary_2010_wgs84"
state.outputGDB = os.path.join(state.outputPathFolder, state.outputGDBName +".gdb")
state.create_gdb()
state.importShapefilesToGDB()


