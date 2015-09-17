import clr

t = Transaction(doc, 'Find and color rated walls.')

t.Start()

levels = []
ratings = []
rated_walls = {}
output_text = []

#load family for line based detail components for rated walls (doesn't work)
#print doc.LoadFamily.Overloads.Functions[2].__doc__

#family = clr.Reference[Family]()

#doc_path = doc.PathName.split("\\")
#doc_path.pop()
#load_path = "\\".join(path) + "\\01 00 00 Fire Tape.rfa"
#print load_path

#status, family = doc.LoadFamily.Overloads.Functions[0](load_path)
#print status
#print family

# assign symbols from already loaded version (Ids likely not the same in new doc)
symb1hr = doc.GetElement(ElementId(3291085))
symb2hr = doc.GetElement(ElementId(3291087))

#create a filtered element collector set to Wall Class FamilySymbol
collector = FilteredElementCollector(doc,doc.ActiveView.Id)
collector.OfClass(Wall)
famtypeitr = collector.GetElementIdIterator()
famtypeitr.Reset()

#Search Family Symbols in document.
for item in famtypeitr:
	wall = doc.GetElement(item)
	#for param in wall.WallType.Parameters:
	#	print param.Id, param.Definition.ParameterType, param.Definition.BuiltInParameter,param.Definition.Name, param.AsValueString()
	type = doc.GetElement(wall.WallType.Id)
	param = type.LookupParameter("Fire Rating")
	# if the param Text exists, it's rated
	if param.AsString():
		wallDict={}
		wallDict["Wall Type"]=wall.Name
		wallDict[param.Definition.Name] = param.AsString()
		if param.AsString() not in ratings:
			ratings.append(param.AsString())
		wallDict["Start"] = wall.Location.Curve.GetEndPoint(0)
		wallDict["End"]= wall.Location.Curve.GetEndPoint(1)
		rated_walls[item.ToString()] = wallDict

#delete existing lines
#line_col = FilteredElementCollector(doc)
#line_col.OfClass(CurveElement)
#for line in line_col.ToElements():
#	if line.LineStyle.Name == subCategoryName:
#		output_text.append(["Deleting existing Detail Line:",line.Id.ToString()])
#		doc.Delete(line.Id)

#delete existing detail components that use the same name we do
lines = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()
for line in lines:
	if line.Name == "1 hour" or line.Name == "2 hour":
		#print line.Id,line.Name
		doc.Delete(line.Id)

#draw new detail lines for rated walls
#for item in rated_walls:
#	output_text.append(["Adding Detail Line for Wall",item,":",rated_walls[item]['Wall Type'].ToString(), rated_walls[item]['Fire Rating'].ToString()])
#	line = Line.CreateBound(rated_walls[item]['Start'],rated_walls[item]['End'])
#	dt_line = doc.Create.NewDetailCurve(doc.ActiveView, line)
#	dt_line.LineStyle = subCategory.GetGraphicsStyle(GraphicsStyleType.Projection)


#place new detail components for rated walls
for item in rated_walls:
	if rated_walls[item]['Fire Rating'] == "1":
		output_text.append(["Placing Detail Component for Wall",item,":",rated_walls[item]['Wall Type'], rated_walls[item]['Fire Rating']])
		line = Line.CreateBound(rated_walls[item]['Start'],rated_walls[item]['End'])
		dt_line = doc.Create.NewFamilyInstance.Overloads.Functions[9](line,symb1hr,doc.ActiveView)
	if rated_walls[item]['Fire Rating'] == "2":
		output_text.append(["Placing Detail Component for Wall",item,":",rated_walls[item]['Wall Type'], rated_walls[item]['Fire Rating']])
		line = Line.CreateBound(rated_walls[item]['Start'],rated_walls[item]['End'])
		dt_line = doc.Create.NewFamilyInstance.Overloads.Functions[9](line,symb2hr,doc.ActiveView)


#find openings in walls and check if they are rated
for item in rated_walls:
	wall = doc.GetElement(ElementId(int(item)))
	for insert in wall.FindInserts(True,False,False,False):
		opening = doc.GetElement(insert)
		if not opening.LookupParameter("FIRE RATING").AsString():
			list = ["Item:",opening.Id.ToString(),opening.Name.ToString(),"is not rated, but in rated wall with ID:",opening.Host.Id.ToString(),opening.Host.Name.ToString()]
			#doc.Selection.SetElementIds(opening.Id)
			TaskDialog.Show("Revit"," ".join(list))

t.Commit()

output = []
for line in output_text:
	output.append(" ".join(line))

#TaskDialog.Show("Revit","\n".join(output))
#print output_text
