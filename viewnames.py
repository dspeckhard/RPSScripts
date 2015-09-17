#import libraries and reference the RevitAPI and RevitAPIUI
import clr
import math

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

#set the active Revit application and document
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

#define a transaction variable and describe the transaction
t = Transaction(doc, 'This is my new transaction')

#start a transaction in the Revit database
t.Start()

#perform some action here...

#opens a .txt file with a list of filenames

viewname_list = open('C:\Users\User1\Documents\CAD\Viewnames.txt', 'r')

#collects all drafting views in the document and puts them into a document

collector = FilteredElementCollector(doc)
collector.OfCategory(BuiltInCategory.OST_Views)
viewscollector = collector.OfClass(ViewDrafting)
views = list(viewscollector)
filelist = []

#checks to see if there are any existing views in the document, skips them if they do, cleans up and adds them to a list if they dont

for line in viewname_list:

    namestring = str(line)
    trimmed_name = namestring[:-5]
    dup_counter = 0

    for v in views:
        if trimmed_name == v.ViewName:
            dup_counter = dup_counter+1
    if dup_counter == 0:
        filelist.append(trimmed_name)

#iterates through the view names and creates new views, importing and placing the relevant .dwgs.

for name in filelist:

    newview = doc.Create.NewViewDrafting()
    newview.Scale = 10
    newview.ViewName = name

    import_settings = DWGImportOptions()
    dwg_name = ('C:\Users\User1\Documents\CAD\\' + name + '.dwg')
    doc.Import(dwg_name,import_settings,newview)

viewname_list.close

#commit the transaction to the Revit database
t.Commit()

#close the script window
__window__.Close()
