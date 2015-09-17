import inspect

t = Transaction(doc, 'Create family instance.')

t.Start()

#create a filtered element collector set to Category OST_Mass and Class FamilySymbol
collector = FilteredElementCollector(doc)
collector.OfCategory(BuiltInCategory.OST_Walls)
collector.OfClass(Wall)
famtypeitr = collector.GetElementIdIterator()
famtypeitr.Reset()

#Search Family Symbols in document.
for item in famtypeitr:
	walltypeID = item
	wall = doc.GetElement(walltypeID)
	properties = dir(wall)
	for property in properties:
#		print property, ": ", getattr(wall,property)
		attribute = getattr(wall,property)
		if inspect.isbuiltin(attribute):
			print property, ": ", str(attribute)
			print inspect.getmembers(attribute)
			#print attribute.__call__(attribute)
		else:
			print property, ": ", str(attribute)
t.Commit()
