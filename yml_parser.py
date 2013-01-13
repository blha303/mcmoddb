import os
import yaml
import moddb_config
import sys

def LoadYMLFile(dbfile):
	# Only use for raw operations. This shouldn't be used outside of yml_parser.py
	if not os.path.exists(dbfile):
		open(dbfile, 'w').close()
	open_file = open(dbfile, 'r')
	output = yaml.safe_load(open_file.read())
	return output

def ListMods(dbfile):
	open_file = open(dbfile)
	output = yaml.safe_load(open_file.read())
	for name, info in output['mods'].iteritems():
		print name + ": " + info['name'] + " version " + str(info['ver'])
	#return '\n'.join(output['mods']).join(output['mods']['name'])

def ListModsNoInfo(dbfile):
	input = LoadYMLFile(dbfile)
	modlist = ''
	for name, info in input['mods'].iteritems():
		modlist += name + " " + str(info['ver'])
	return modlist
	
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
	try:
		return input['mods'][str(mod)]['type']
	except KeyError:
		return "error"

def GetModFile(dbfile, mod):
	input = LoadYMLFile(dbfile)
	try:
		if input['mods'][str(mod)]['type'] == "http":
			return input['mods'][str(mod)]['outfile']
	except KeyError:
		return "error"

def GetModVersion(dbfile, mod):
	input = LoadYMLFile(dbfile)
	try:
		return input['mods'][str(mod)]['ver']
	except KeyError:
		return "error"
	
def OutputInstalled(dbfile, mod, version, populate=False):
	input = LoadYMLFile(dbfile)
	try:
		if input == None and populate == True:
			print "Installed Database is empty. Populating."
			OutputDict = {'mods': {'mcmoddb': {'installed': 'y', 'version': 1.2}}}
			yaml.dump(OutputDict, open(dbfile, 'w'), default_flow_style=False)
			print "Populated installed database."
		elif populate == False:
			OutputDict = {'installed': 'y', 'version': version}
			input['mods'][mod] = OutputDict
			yaml.dump(input, open(dbfile, 'w'), default_flow_style=False)
	except:
		print "Caught error:", sys.exc_info()[0]
		raise
			
def IsModInstalled(dbfile, mod, version):
	input = LoadYMLFile(dbfile)
	try:
		if input['mods'][mod]['version'] == version and input['mods'][mod]['installed'] == 'y':
			return True
		elif input['mods'][mod]['version'] != version and input['mods'][mod]['installed'] == 'y':
			return False
		elif input['mods'][mod]['installed'] == 'n':
			return False
		elif version == "error":
			return False
	except KeyError:
		return False

def PopulateInstalledDB(installed_db, dbfile):
	installed = LoadYMLFile(installed_db)
	input = LoadYMLFile(dbfile)
	for name, value in input['mods'].iteritems():
		try:
			discard_value = installed[name]
		except KeyError:
			OutputDict = {'installed': 'n', 'version': value['ver']}
			installed['mods'][name] = OutputDict
	yaml.dump(installed, open(installed_db, 'w'), default_flow_style=False)
				
			
