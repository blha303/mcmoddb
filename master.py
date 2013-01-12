#!/usr/bin/env python2

import os
import sys
import platform
import moddb_config
import hashlib
import shutil

if platform.system() == "Linux":
	import linux_util as moddb_util
elif platform.system() == "Windows":
	import windows_util as moddb_util
elif platform.system() == "Darwin":
	print "Sorry, but Mac support does not exist currently."
	print "Feel free to submit a patch."
	sys.exit(1)
else:
	print "Sorry, but your platform isn't currently supported."
	sys.exit(1)

moddb_util.SetupEnvironment()

if moddb_config.Config['autodl'] == True:
	if not os.path.isfile(moddb_util.TmpModDBFileName()):
		print "ERROR: Automatic download of the global Mod DB failed. Change 'autodl' in moddb_config.py to False to disable this."
	else:
		if moddb_config.Config['checkdl'] == True:
			tmpfile_hash = hashlib.md5(open(moddb_util.TmpModDBFileName(), 'r').read()).hexdigest()
			localfile_hash = hashlib.md5(open(moddb_util.GlobalModDBFileName(), 'r').read()).hexdigest()
			if moddb_config.Config['showchecksum'] == True:
				print "Downloaded DB hash: " + tmpfile_hash
				print "Local DB hash: " + localfile_hash
			if tmpfile_hash != localfile_hash:
				print "Local ModDB is different than the Server DB, replacing local DB with the downloaded DB."
				print "If this is not true, the ModDB that was downloaded may be corrupt. Running this again should fix this."
				localfile = open(moddb_util.GlobalModDBFileName(), 'w')
				tmpfile = open(moddb_util.TmpModDBFileName(), 'r')
				localfile.write(tmpfile.read())
				localfile.close()
				tmpfile.close()
			else:
				print "Local ModDB is the same as the server DB."
		elif moddb_config.Config['checkdl'] == False:
			print "ModDB checking is disabled."
			print "WARNING: This will stop the mod database from being automatically updated. Your local DB will be out of date."
			print "I HIGHLY recommend you enable DB checking."
		else:
			print "Config value of checkdl is invalid."
elif moddb_config.Config['autodl'] == False:
	print "ModDB Auto-downloading is disabled."
	print "WARNING: This will stop the mod database from being automatically updated. Your local DB will be outdated."
	print "I HIGHLY reccommend you enable DB auto-downloading."


# Delete temporary files
#os.removedirs(moddb_util.TmpDirectoryName())
shutil.rmtree(moddb_util.TmpDirectoryName())
#except OSError:
#	print "Unable to remove temp directories. Remove the tmp directory yourself."

