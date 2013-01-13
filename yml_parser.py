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
	
def GetModLink(dbfile, mod):
	open_file = open(dbfile)
	output = yaml.safe_load(open_file.read())
	try:
		if output['mods'][str(mod)]['type'] == "http":
			return "http://" + output['mods'][str(mod)]['url']
		elif output['mods'][str(mod)]['type'] == "git":
			return "git://" + output['mods'][str(mod)]['url']
		else:
			print "Error: Mod %s does not have a `type` value in the database, aborting." % mod
			return "error"
	except KeyError:
		print "Error: Mod %s does not exist, or there has been an internal error." % mod
		return "error"
	
def GetModType(dbfile, mod):
	input = LoadYMLFile(dbfile)
	return input['mods'][str(mod)]['type']

def GetModFile(dbfile, mod):
	input = LoadYMLFile(dbfile)
	if input['mods'][str(mod)]['type'] == "http":
		return input['mods'][str(mod)]['outfile']
	
