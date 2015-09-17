t = Transaction(doc, 'Find and color rated walls.')

t.Start()

levels = []
ratings = []
rated_walls = {}
output_text = []

#patterns = FilteredElementCollector(doc).OfClass(LinePatternElement).ToElements()
#for pattern in patterns:
#	print pattern.Id,":",pattern.Name

#create new graphic style for rated walls

subCategoryName = "BCJ Rated Walls 1Hr"
category = doc.Settings.Categories.get_Item(BuiltInCategory.OST_GenericAnnotation);
if not category.SubCategories.Contains(subCategoryName):
	output_text.append(["Setting New Graphic Style",subCategoryName])
	subCategory = doc.Settings.Categories.NewSubcategory(category,subCategoryName)
else:
	for sub in category.SubCategories:
		if sub.Name == subCategoryName:
			#print sub.Name
			subCategory = sub
subCategory.LineColor=Color(250,0,0)
subCategory.SetLineWeight(10,GraphicsStyleType.Projection)	



lvl_collector = FilteredElementCollector(doc)
lvl_collector.OfClass(Level)
lvl_itr = lvl_collector.GetElementIdIterator()
lvl_itr.Reset()

for level in lvl_itr:
	lvl = doc.GetElement(level)
	levels.append([lvl.Name,lvl.Id])

for level in levels:
	# create a filter for the Level in question
	lvl_filter = ElementLevelFilter(level[1])
	
	#create a filtered element collector set to Wall Class FamilySymbol
	collector = FilteredElementCollector(doc)
	collector.OfClass(Wall).WherePasses(lvl_filter)
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
			wallDict["Level"]=[level[0],level[1]]
 			wallDict["Wall Type"]=wall.Name
			wallDict[param.Definition.Name] = param.AsString()
			if param.AsString() not in ratings:
				ratings.append(param.AsString())
			wallDict["Start"] = wall.Location.Curve.GetEndPoint(0)
			wallDict["End"]= wall.Location.Curve.GetEndPoint(1)
			rated_walls[item.ToString()] = wallDict
			
#delete existing lines
line_col = FilteredElementCollector(doc)
line_col.OfClass(CurveElement)
for line in line_col.ToElements():
	if line.LineStyle.Name == subCategoryName:
		output_text.append(["Deleting existing Detail Line:",line.Id])
		doc.Delete(line.Id)

#draw new detail lines for rated walls
for item in rated_walls:
	output_text.append(["Adding Detail Line for Wall",item,":",rated_walls[item]['Wall Type'], rated_walls[item]['Fire Rating']])
	line = Line.CreateBound(rated_walls[item]['Start'],rated_walls[item]['End'])
	dt_line = doc.Create.NewDetailCurve(doc.ActiveView, line)
	dt_line.LineStyle = subCategory.GetGraphicsStyle(GraphicsStyleType.Projection)


#place new detail components for rated walls
for item in rated_walls:
	output_text.append(["Placing Detail Component for Wall",item,":",rated_walls[item]['Wall Type'], rated_walls[item]['Fire Rating']])
	line = Line.CreateBound(rated_walls[item]['Start'],rated_walls[item]['End'])
	dt_line = doc.Create.NewDetailCurve(doc.ActiveView, line)


#find openings in walls and check if they are rated
for item in rated_walls:
	wall = doc.GetElement(ElementId(int(item)))
	for insert in wall.FindInserts(True,False,False,False):
		opening = doc.GetElement(insert)
		print opening.LookupParameter("FIRE RATING").AsString()

t.Commit()

#output = []
#for line in output_text:
#	output.append("".join(line))

#print "".join(output)
print output_text