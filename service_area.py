# Name: MakeServiceAreaLayer_Workflow.py
# Description: Generate 1-,2-,3- minute service area around fire stations and
#              save the results to a layer file on disk. The service area
#              polygons can be used to visualize the areas that do not have
#              adequate coverage from the fire stations
# Requirements: Network Analyst Extension

#Import system modules
import arcpy
from arcpy import env

try:
    #Check out the Network Analyst extension license
    arcpy.CheckOutExtension("Network")

    #Set environment settings
    env.workspace = "E:/Teaching/GEOG_3540/GEOG_3540_S20/Assignments/Assignment3/data"
    env.overwriteOutput = True

    #Set local variables
    inNetworkDataset = "E:/Teaching/GEOG_3540/GEOG_3540_S20/Assignments/Assignment3/data/network_data/roads_ND.nd"
    outNALayerName = "SchoolAccessibility"
    impedanceAttribute = "length"
    inFacilities = "E:/Teaching/GEOG_3540/GEOG_3540_S20/Assignments/Assignment3/data/schools.shp"
    outLayerFile = "E:/Teaching/GEOG_3540/GEOG_3540_S20/Assignments/Assignment3/data/" + "/" + outNALayerName + ".lyr"

    #Create a new service area layer. We wish to generate the service area
    #polygons as rings, so that we can easily visualize the coverage for any
    #given location. We also want overlapping polygons as we can determine the
    #number of fire stations that cover a given location. We use hierarchy to
    #speed up the time taken to create the polygons. We will specify these
    #options while creating the new service area layer.
    outNALayer = arcpy.na.MakeServiceAreaLayer(inNetworkDataset, outNALayerName,
                                  impedanceAttribute, "TRAVEL_FROM", "500 1000 1500 2000 2500 3000",
                                  "DETAILED_POLYS", "MERGE", "RINGS",
                                  hierarchy = "USE_HIERARCHY")

    #Get the layer object from the result object. The service layer can now be
    #referenced using the layer object.
    outNALayer = outNALayer.getOutput(0)

    #Get the names of all the sublayers within the service area layer.
    subLayerNames = arcpy.na.GetNAClassNames(outNALayer)
    #Stores the layer names that we will use later
    facilitiesLayerName = subLayerNames["Facilities"]

    #Load the schools as facilities using default field mappings and
    #default search tolerance
    arcpy.na.AddLocations(outNALayer, facilitiesLayerName, inFacilities, "", "")

    #Solve the service area layer
    arcpy.na.Solve(outNALayer)

    #Save the solved service area layer as a layer file on disk with relative
    #paths
    arcpy.management.SaveToLayerFile(outNALayer,outLayerFile,"RELATIVE")


    outShapeFile = "E:/Teaching/GEOG_3540/GEOG_3540_S20/Assignments/Assignment3/data/" + "/" + outNALayerName + ".shp"
    arcpy.CopyFeatures_management(outShapeFile, outNALayer)

    print "Script completed successfully"

except Exception as e:
    # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    print "An error occured on line %i" % tb.tb_lineno
    print str(e)
