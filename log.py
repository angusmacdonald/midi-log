import re



def getPackageName(line):
	ma = re.match(u'[^\[A-Z]*', line) #End on capital letter (class name) or after entire name.
    
	package = None
	
	if ma:
		package = ma.group()

		#Remove possible trailing dot.
		if package.endswith('.'):
			package = package[:-1]
    
	return package

def splitPackageNames(package):
	names = re.split('[ .]', package)

	return names

if __name__ == '__main__':

	print "Starting"
	FILE = open('testLog.txt', 'r')

	i = 0
	while i < 500000:
		line = FILE.readline()

		if line == "": # Cuts off if end of file reached
			break

		package = getPackageName(line)

		print package

		splitPackage = splitPackageNames(package)

		print splitPackage

