t = Transaction(doc, 'Find and color rated walls.')

t.Start()

#fsCollector = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_DetailComponents).ToElements()

#for elem in fsCollector:
#	if elem.Family.FamilyPlacementType == FamilyPlacementType.CurveBasedDetail:
#		print elem.Id
#		symbol = elem
#		break

line = Line.CreateBound(XYZ(0,0,0),XYZ(30,0,0))

doc.Create.NewFamilyInstance.Overloads.Functions[9](line, doc.GetElement(ElementId(1452296)), doc.ActiveView)

t.Commit()