import os
import requests
import moddb_config 

TmpDirectoryName = "./" + moddb_config.Config['tmpdir']
ModDirectoryName = "./" + moddb_config.Config['moddir']
DBDirectoryName = "./" + moddb_config.Config['dbdir']
ServerDBLocation = moddb_config.Config['serverdb']

green = "\033[32m"
red = "\033[31m"
off = "\033[0m"

def SetupEnvironment():
	if not os.path.exists(TmpDirectoryName):
		os.makedirs(TmpDirectoryName)
	if not os.path.exists(ModDirectoryName):
		os.makedirs(ModDirectoryName)
	if not os.path.exists(DBDirectoryName):
		os.makedirs(DBDirectoryName)
	if not os.path.isfile(TmpModDBFile):
		GetModDBFile(TmpModDBFile)

def GetModDBFile(target):
	moddb_file = requests.get(ServerDBLocation)
	if moddb_file.status_code == 200:
		output = open(target, 'w')
		output.write(moddb_file.text)
		#print "Written file to disk."
	elif moddb_file.status_code == 403:
		print "Something has gone server-side. Report a bug at the McMODDB website."
		sys.exit(1)
	elif moddb_file.status_code == 404:
		print "The moddb file was not found."
		sys.exit(1)
	else:
		print "Something has gone very wrong."
		print "Status code: " + str(moddb_file.status_code)

TmpModDBFile = TmpDirectoryName + "/" + moddb_config.Config['tmpdbfile']
LocalModDBFile = DBDirectoryName + "/" + moddb_config.Config['localdbfile']
GlobalModDBFile = DBDirectoryName + "/" + moddb_config.Config['globaldbfile']
