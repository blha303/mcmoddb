import os
import requests

def SetupEnvironment():
	if not os.path.exists("./tmp"):
		os.makedirs("./tmp")
	if not os.path.exists("./mods"):
		os.makedirs("./mods")
	if not os.path.isfile("./tmp/moddb_global.yml"):
		GetModDBFile('./tmp/moddb_global.yml')

def GetModDBFile(target):
	moddb_file = requests.get("http://elemeno.dyndns.org/moddb/moddb_global.yml")
	if moddb_file.status_code == 200:
		output = open(target, 'w')
		output.write(moddb_file.text)
		print "Written file to disk."
	elif moddb_file.status_code == 403:
		print "Something has gone server-side. Report a bug at the McMODDB website."
	elif moddb_file.status_code == 404:
		print "The moddb file was not found."
	else:
		print "Something has gone very wrong."
		print "Status code: " + str(moddb_file.status_code)

def TmpModDBFileName():
	return "./tmp/moddb_global.yml"

def GlobalModDBFileName():
	return "./moddb_global.yml"

def LocalModDBFileName():
	return "./moddb_local.yml" # I should make these configurable. 

def TmpDirectoryName():
	return "./tmp"
