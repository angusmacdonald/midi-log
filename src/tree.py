import logging
import re


class PackageTree:
	'''	A tree of package names, where each package name also has a MIDI instrument number attached. 
		The instrument number is unique amongst packages sharing the same parent package.

		It is intended that for a given package you can use getInstrumentAtDepth() to get the instrument 
		to be used for that package and all sub-packages. I.E. If you have a common package structure where
		everything begins with 'org.company.product', then the instruments will be selected from the instruments
		in the sub-packages of this (at depth 4).
	'''

	def __init__(self, instruments = [0, 14, 18, 26, 32, 40, 48, 56, 66, 78, 88, 97]):
		self.root = None
		self.instruments = instruments
		self.customInstrument = dict()
	def add(self, packageName):
		'''	Add a FQ package to the tree. This will be parsed into individual package names in the tree.

			packageName: e.g. 'com.company.product.other'
		'''
		packageNamesArray = splitPackageNames(packageName)
		if self.root is None:
			self.root = TreeNode(packageNamesArray[0], 0)

		parent = self.root
		for name in packageNamesArray[1:]:
			if not parent.hasChild(name):
				parent.addChild(name, self.instruments)
			parent = parent.getChild(name)

	def __getLargestDepth(self, node):
		largestDepth = 0;
		for child in node.children.values():
			childDepth = self.__getLargestDepth(child)

			if childDepth > largestDepth:
				largestDepth = childDepth

		return largestDepth + 1

	def getLargestDepth(self):
		''' Get the depth of this tree. '''
		node = self.root

		if self.root is None:
			return 0

		return self.__getLargestDepth(self.root)

	def getInstrumentAtDepth(self, package, depth):
		''' Get the instrument to be used for the given FQ package name, by selecting the instrument at the
			given depth in this package name.

			depth: If the depth is greater than this package name, use the instrument at the deepest traversed node.
		'''
		
		customInstrument = self.getCustomInstrument(package)

		if customInstrument is not None:
			return customInstrument

		if self.root is None:
			return 0

		packageNames = splitPackageNames(package)

		instrument = 0
		currentDepth = 0

		parent = self.root
		for name in packageNames[1:]:
			logging.debug("Iteration at '{0}', depth {1}".format(name, currentDepth))
			
			if not parent.hasChild(name):
				logging.debug("No child with name {0}".format(name))
				return parent.instrument

			instrument = parent.instrument

			logging.debug("Name [{0}], Depth [{1}], Instrument [{2}]".format(name, currentDepth, instrument))
			
			parent = parent.getChild(name)
			currentDepth += 1

			if depth == currentDepth:
				logging.debug("Reached depth at {0}, instrument is {1}".format(parent.data, parent.instrument))
				return parent.instrument
			

		return instrument

	def __getWithDepth(self, node, depth):
		spacing = ""
		for x in range (0, depth):
			spacing = spacing + " "
		return spacing + node.data + " (i:" + str(node.instrument) + ")"

	def setCustomInstrument(self, package, instrument):
		''' Override any instrument specified in the tree with this custom instrument.
			Has to be an exact match on a specific package.
		'''
		self.customInstrument[package] = instrument
	def getCustomInstrument(self, package):
		''' Gets the instrument to be used by this package. Will be none if no instrument was specified through
			setCustomInstrument().
		'''
		if package in self.customInstrument:
			return self.customInstrument[package]
		else :
			return None

	def __print(self,node, depth):
		if node is not None:
			print self.__getWithDepth(node, depth)
		for child in node.children.values():
			self.__print(child, depth+1)
	def printState(self):
		self.__print(self.root, 0)

class TreeNode:
	def __init__(self, value, instrument):
		self.data = value
		self.children = dict()
		self.instrument = instrument
	def hasChild(self, key):
		return key in self.children
	def addChild(self, value, instruments):
		instrumentNumber = len(self.children)
		instrument = 0
		if instrumentNumber > len(instruments):
			logging.warning("Not enough instruments available for unique package.")
		else:
			instrument = instruments[instrumentNumber]
		self.children[value] = TreeNode(value, instrument)
	def getChild(self, key):
		return self.children[key]

def splitPackageNames(package):
	names = re.split('[ .]', package)
	return names
def getDepth(package):
	return len(splitPackageNames(package))


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)

	tree = PackageTree()
	tree.add('com.package.test.structure')
	tree.add('com.package.util.security')

	print "Tree state:"
	tree.printState()
	print "Instrument: " + str(tree.getInstrumentAtDepth('com.package.util', 2))

	print "Largest depth: " + str(tree.getLargestDepth())