doc_path = doc.PathName.split("\\")
doc_path.pop()
load_path = "\\".join(doc_path) + "\\01 00 00 Fire Tape.rfa"
print load_path

t = Transaction(doc, 'loadfamily')
t.Start()
try:
	import clr
	family = clr.Reference[Family]()
	# family is now an Object reference (not set to an instance of an object!)
	success = doc.LoadFamily(load_path, family)  # explicitly choose the overload
	# family is now a Revit Family object and can be used as you wish
	
	success, family = doc.LoadFamily.Overloads.Functions[0](load_path)
	
 	if success:
 		print family
	else:
		print "Success? ->",success
    	
	t.Commit()
except:
    t.Rollback()