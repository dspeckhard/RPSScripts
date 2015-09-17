

category = doc.Settings.Categories.get_Item(BuiltInCategory.OST_GenericAnnotation);
for sub in category.SubCategories.GetEnumerator():
	#print dir(sub)
	gs = sub.GetGraphicsStyle(GraphicsStyleType.Projection)
	#print dir(gs.GraphicsStyleCategory)
	print "Name:",gs.Name,":: Projection LW:",gs.GraphicsStyleCategory.GetLineWeight(GraphicsStyleType.Projection), "Cut LW:",gs.GraphicsStyleCategory.GetLineWeight(GraphicsStyleType.Cut),", Color RGB:",gs.GraphicsStyleCategory.LineColor.Red,gs.GraphicsStyleCategory.LineColor.Blue,gs.GraphicsStyleCategory.LineColor.Green, doc.ActiveView.GetCategoryOverrides(gs.Id).ProjectionLinePatternId, doc.ActiveView.GetCategoryOverrides(gs.Id).CutLinePatternId