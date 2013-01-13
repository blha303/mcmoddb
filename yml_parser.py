import os
import yaml
import moddb_config

def LoadYMLFile(dbfile):
	# Only use for raw operations. This shouldn't be used outside of yml_parser.py
	open_file = open(dbfile)
	output = yaml.safe_load(open_file.read())
	return output

def ListMods(dbfile):
	open_file = open(dbfile)
	output = yaml.safe_load(open_file.read())
	for name, info in output['mods'].iteritems():
		print name + ": " + info['name'] + " version " + str(info['ver'])
	#return '\n'.join(output['mods']).join(output['mods']['name'])
	
