#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name: GitHub-FirstPythonScript.py
    Aurthor: Kelechi Igwe
    Description: Sample script to extract KS rivers within 10 km buffer of Flint Hills ecoregion
    Date created: 09/11/2024
    Python Version: 3.9.16
"""

# Import arcpy module and allow overwrites
import arcpy
arcpy.env.overwriteOutput = True

# Set current workspace
arcpy.env.workspace = "C:\\Users\\kelechi\\Documents\\GitHub\\firstpythonscript-Kelechi-igwe\\GIS_projects\\ExerciseData.gdb"

# Select Flint Hills ecoregion
selectEcoregion = arcpy.management.SelectLayerByAttribute('ks_ecoregions', 'NEW_SELECTION',"US_L3NAME = 'Flint Hills' ")

# Create a 10 km buffer around selected ecoregion
createBuffer_10km = arcpy.analysis.Buffer(selectEcoregion, 'Buffer_10km', '10 Kilometers')

# Clip rivers within buffer
arcpy.analysis.Clip('ks_major_rivers', createBuffer_10km,'ks_rivers_10km')

# Add a 'Miles' field to attribute table of selected rivers
arcpy.AddField_management('ks_rivers_10km', 'riverMiles', 'FLOAT')

# Calculate values for the riverMiles field to two decimal places
arcpy.CalculateField_management("ks_rivers_10km", "riverMiles", "round((!Shape_Length! * 0.00062137), 2)", "PYTHON3")

# Create a summary table for sum of all rivers within the 10 Km buffer
arcpy.analysis.Statistics("ks_rivers_10km", "Sum_riverMiles", [["riverMiles", "SUM"]])

# Extract value from Summary table using da.Cursor method and list comprehension
sum_values = [row[0] for row in arcpy.da.SearchCursor("Sum_riverMiles", "SUM_riverMiles")]
print("The Sum of the 10 km buffer rivers in Miles is: {} Miles".format(round(sum_values[0],2)))
