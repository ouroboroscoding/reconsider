#!/usr/bin/python

# Import python core modules
import re
import sys

# Import the module
import Reconsider

# parseArgs
def parseArgs(args):
	"""Parse Arguments

	Used to parse the arguments passed to the script

	Args:
		args (list): A list of strings representing arguments to a script

	Returns:
		dict: Returns a dictionary with args as keys and the values sent with
			them or True for valueless arguments

	Raises:
		ValueError: If args is not a list or tuple
	"""

	# If args is not a list
	if not isinstance(args, (list,tuple)):
		raise ValueError('args is not a list or tuple')

	# Init the return value
	dRet	= {}

	# Go through each argument
	for s in args:

		# Check the string matches the format
		oRes	= re.match(u'^--([^=]+)(?:=(.+))?$', s)

		# If we have a match
		if oRes:

			# Store it by name and value
			mGroup2	= oRes.group(2)
			dRet[oRes.group(1)]	= (not mGroup2 and True or mGroup2)

		# Else add it to the unknowns
		else:
			try:				dRet['?'].append(s)
			except KeyError:	dRet['?'] = [s]

	# Return the dict
	return dRet

# printHelp
def printHelp(script):
	"""Print Help

	Prints out the arguments needs to run the script

	Returns:
		None
	"""

	print 'Reconsider cli script copyright 2016 OuroborosCoding'
	print ''
	print script + ' --source=localhost:28015 --destination=somedomain.com:28015'
	print script + ' --destination=somedomain.com:28015 --dbs=production,staging'
	print ''
	print 'Usage:'
	print '  --source=[string]         A RethinkDB connection string representing the'
	print '                            source host. Defaults to "localhost:28015"'
	print '  --destination=[string]    A RethinkDB connection string representing the'
	print '                            destination host. Required.'
	print '  --db                      A single DB name, or a comma separated list of'
	print '                            databases on the source which will be copied to the'
	print '                            destination. Defaults to all DBs on the source'
	print '                            host'
	print '  --verbose                 Will print out what\'s happening during the clone'
	print '  --help                    Prints this message'
	print ''
	print 'A RethinkDB connection string is defined as: host[:port[:user[:password]]]'
	print 'Valid:          localhost, localhost:28015, localhost:28015:root:asdf'
	print 'Invalid:        localhost:root, 28015, root:asdf, localhost:root:asdf'

################################################################################
# Start script

# Get args
dArgs	= parseArgs(sys.argv[1:])

# If there's absolutely no args, or help is requested
if not dArgs or 'help' in dArgs:
	printHelp(sys.argv[0])
	sys.exit(1)

# If the source is not specified, use localhost
if 'source' not in dArgs:
	dSource	= {"host":"localhost","port":28015}

# Else parse the source
else:
	lSource	= dArgs['source'].split(':')
	iSource	= len(lSource)

	# If we have 1
	if iSource == 1:	dSource	= {"host":lSource[0]}
	elif iSource == 2:	dSource	= {"host":lSource[0],"port":int(lSource[1])}
	elif iSource == 3:	dSource	= {"host":lSource[0],"port":int(lSource[1]),"user":lSource[2]}
	elif iSource == 4:	dSource	= {"host":lSource[0],"port":int(lSource[1]),"user":lSource[2],"passwd":lSource[3]}

# If the destination is not specified
if 'destination' not in dArgs:
	print 'Must specify destination to copy DBs to'
	printHelp
	sys.exit(1)

# Else parse the destination
else:
	lDest	= dArgs['destination'].split(':')
	iDest	= len(lDest)

	# If we have 1
	if iDest == 1:		dDest	= {"host":lDest[0]}
	elif iDest == 2:	dDest	= {"host":lDest[0],"port":int(lDest[1])}
	elif iDest == 3:	dDest	= {"host":lDest[0],"port":int(lDest[1]),"user":lDest[2]}
	elif iDest == 4:	dDest	= {"host":lDest[0],"port":int(lDest[1]),"user":lDest[2],"passwd":lDest[3]}

# If the DBs are specified
lDBs	= ('db' in dArgs and dArgs['db'].split(',') or None)

# Call clone
Reconsider.clone(dSource, dDest, lDBs, ('verbose' in dArgs and True or False))

