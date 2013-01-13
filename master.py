#!/usr/bin/env python2

import os
import sys
import platform
import moddb_config
import hashlib
import shutil
import yml_parser
import requests

if platform.system() == "Linux":
	print "Detected OS: Linux."
	try:
		import platform_utils.linux_util as moddb_util
	except ImportError:
		print "ERROR: error ImportError caught, exiting"
		sys.exit(1)
	print moddb_util.green + "Loaded Linux util successfully." + moddb_util.off
elif platform.system() == "Windows":
	print "Detected OS: Windows"
	try:
		import platform_utils.windows_util as moddb_util
	except ImportError:
		print "ERROR: error ImportError caught, exiting"
		sys.exit(1)
	print moddb_util.green + "Loaded Windows util successfully." + moddb_util.off
elif platform.system() == "Darwin":
	print "Sorry, but Mac support does not exist currently."
	print "Feel free to submit a patch."
	sys.exit(1)
else:
	if moddb_config.Config['forced-platform'].lower() == "linux":
		print "WARNING: Forcing platform Linux."
		try:
			import platform_utils.linux_util as moddb_util	
		except ImportError:
			print "ERROR: error ImportError caught, exiting"
			sys.exit(1)
		print moddb_util.green + "Loaded Linux util successfully." + moddb_util.off
	elif moddb_config.Config['forced-platform'].lower() == "windows":
		print "WARNING: Forcing platform Windows."
		try:
			import platform_utils.windows_util as moddb_util
		except ImportError:
			print "ERROR: error ImportError caught, exiting"
		print moddb_util.green + "Loaded Windows util successfully." + moddb_util.off
	elif moddb_config.Config['forced-platform'].lower() == "":
		print "Sorry, but your platform isn't currently supported."
		print "You can force a platform to load in the config with the forced-platform value."
		sys.exit(1)
	else:
		print "ERROR: Forced platform is invalid."
		sys.exit(1)

moddb_util.SetupEnvironment()
def UpdateDB(force=False):
	if moddb_config.Config['autodl'] == True:
		if not os.path.isfile(moddb_util.TmpModDBFile):
			print moddb_util.red + "ERROR: Automatic download of the global Mod DB failed. Change 'autodl' in moddb_config.py to False to disable this." + moddb_util.off
		else:
			if not os.path.isfile(moddb_util.GlobalModDBFile):
				print moddb_util.green + "Copying downloaded DB to global DB" + moddb_util.off
				localfile = open(moddb_util.GlobalModDBFile, 'w')
				tmpfile = open(moddb_util.TmpModDBFile, 'r')
				localfile.write(tmpfile.read())
				localfile.close()
				tmpfile.close()
			elif moddb_config.Config['checkdl'] == True:
				tmpfile_hash = hashlib.md5(open(moddb_util.TmpModDBFile, 'r').read()).hexdigest()
				localfile_hash = hashlib.md5(open(moddb_util.GlobalModDBFile, 'r').read()).hexdigest()
				if moddb_config.Config['showchecksum'] == True:
					print "Downloaded DB hash: " + tmpfile_hash
					print "Local DB hash: " + localfile_hash
				if tmpfile_hash != localfile_hash:
					print moddb_util.green + "Local ModDB is different than the Server DB, replacing local DB with the downloaded DB." + moddb_util.off
					print moddb_util.red + "If this is not true, the ModDB that was downloaded may be corrupt. Running this again should fix this." + moddb_util.off
					localfile = open(moddb_util.GlobalModDBFile, 'w')
					tmpfile = open(moddb_util.TmpModDBFile, 'r')
					localfile.write(tmpfile.read())
					localfile.close()
					tmpfile.close()
				else:
					if force == True:
						print moddb_util.green + "Local ModDB is the same as the server DB. Ignoring." + moddb_util.off
					else:
						print moddb_util.green + "Local ModDB is the same as the server DB." + moddb_util.off
			elif moddb_config.Config['checkdl'] == False:
				print moddb_util.red + "ModDB checking is disabled." + moddb_util.off
				print moddb_util.red + "WARNING: This will stop the mod database from being automatically updated. Your local DB will be out of date." + moddb_util.off
				print moddb_util.red + "I HIGHLY recommend you enable DB checking." + moddb_util.off
			else:
				print "Config value of checkdl is invalid."
	elif moddb_config.Config['autodl'] == False:
		print moddb_util.red + "ModDB Auto-downloading is disabled." + moddb_util.off
		print moddb_util.red + "WARNING: This will stop the mod database from being automatically updated. Your local DB will be outdated." + moddb_util.off
		print moddb_util.red + "I HIGHLY reccommend you enable DB auto-downloading." + moddb_util.off
	if force == True:
		print moddb_util.green + "Forcing a DB update..." + moddb_util.off
		moddb_util.GetModDBFile(moddb_util.TmpModDBFile) 
		localfile = open(moddb_util.GlobalModDBFile, 'w')
		tmpfile = open(moddb_util.TmpModDBFile, 'r')
		localfile.write(tmpfile.read())
		localfile.close()
                tmpfile.close()
		print moddb_util.green + "Update complete." + moddb_util.off
UpdateDB(False)

def InstallMod(mod):
	GetLink = yml_parser.GetModLink(moddb_util.GlobalModDBFile, mod)
	if GetLink.lower() == "error":
		print "ERROR: The specified mod either does not exist, or there is a incomplete entry for it in the database."
	elif yml_parser.IsModInstalled(moddb_util.InstalledDBFile, mod, yml_parser.GetModVersion(moddb_util.GlobalModDBFile, mod)) == True:
		print "Specified mod is already installed at the latest version."
	elif yml_parser.GetModType(moddb_util.GlobalModDBFile, mod) == "http":
		mod_dl = requests.get(GetLink, stream=True)
		print "Downloading mod " + mod + " from " + GetLink
		outfile = open(moddb_util.ModDirectoryName + yml_parser.GetModFile(moddb_util.GlobalModDBFile, mod), 'w')
		if mod_dl.status_code == 200:
			outfile.write(mod_dl.raw.read())
			print "File " + yml_parser.GetModFile(moddb_util.GlobalModDBFile, mod) + " has been written to your mods folder."
			yml_parser.OutputInstalled(moddb_util.InstalledDBFile, mod, yml_parser.GetModVersion(moddb_util.GlobalModDBFile, mod))
		elif mod_dl.status_code == 403:
			print "Permission denied on opening the remote file."
		elif mod_dl.status_code == 404:
			print "File not found on remote server. Your ModDB is probably out of date."
		elif mod_dl.status_code == 500:
			print "Remote server has issues."
		else:
			print "Something went wrong. Status code is " + str(mod_dl.status_code)
	elif yml_parser.GetModType(moddb_util.GlobalModDBFile) == "git":
		print "git support WIP"

while True:
	try:
		input_cmd = raw_input("mcmoddb> ").lower().split(' ')
	except EOFError:
		print 'Quitting...'
		break
	except KeyboardInterrupt:
		print 'Quitting...'
		break
	if input_cmd[0] == "quit" or input_cmd[0] == "exit":
		break
	elif input_cmd[0] == "updatedb":
		UpdateDB(True)
	elif input_cmd[0] == "list":
		yml_parser.ListMods(moddb_util.GlobalModDBFile)
	elif input_cmd[0] == "help":
		print "Commands:"
		print "quit: quits the prompt"
		print "exit: see quit"
		print "help: displays this help"
		print "updatedb: updates the database"
		print "setupdb: Sets up your installed database."
		print "populatedb: Populates your installed database with the server database."
		print "install: Installs a mod."
	elif input_cmd[0] == "install":
		try:
			InstallMod(input_cmd[1])
		except IndexError:
			print "You must specify a mod"
	elif input_cmd[0] == "setupdb":
		yml_parser.OutputInstalled(moddb_util.InstalledDBFile, "nomod", "0.0", True)
	elif input_cmd[0] == "populatedb":
		yml_parser.PopulateInstalledDB(moddb_util.InstalledDBFile, moddb_util.GlobalModDBFile)
	else:
		print "Unknown command"
	#print input_cmd[0]


# Delete temporary files
#os.removedirs(moddb_util.TmpDirectoryName())
shutil.rmtree(moddb_util.TmpDirectoryName)
#except OSError:
#	print "Unable to remove temp directories. Remove the tmp directory yourself."

