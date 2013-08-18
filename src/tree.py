import logging

instruments = [0, 14, 18, 26, 32, 40, 48, 56, 66, 78, 88, 97]

class Tree:

	def __init__(self):
		self.root = None
	def add(self, packageNames):

		if self.root is None:
			self.root = TreeNode(packageNames[0], 0)

		parent = self.root
		for name in packageNames[1:]:
			if not parent.hasChild(name):
				parent.addChild(name)
			parent = parent.getChild(name)

	def __getLargestDepth(self, node):
		
		largestDepth = 0;
		for child in node.children.values():
			childDepth = self.__getLargestDepth(child)

			if childDepth > largestDepth:
				largestDepth = childDepth

		return largestDepth + 1

	def getLargestDepth(self):
		node = self.root

		if self.root is None:
			return 0

		return self.__getLargestDepth(self.root)

	def getInstrumentAtDepth(self, packageNames, depth):
		if self.root is None:
			return 0

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
	def addChild(self, value):
		instrumentNumber = len(self.children)
		instrument = 0
		if instrumentNumber > len(instruments):
			logging.warning("Not enough instruments available for unique package.")
		else:
			instrument = instruments[instrumentNumber]
		self.children[value] = TreeNode(value, instrument)
	def getChild(self, key):
		return self.children[key]

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)

	tree = Tree()
	tree.add(['com','package', 'test', 'structure'])
	tree.add(['com','package', 'util', 'security'])

	print "Tree state:"
	tree.printState()
	print "Instrument: " + str(tree.getInstrumentAtDepth(['com','package', 'util'], 2))

	print "Largest depth: " + str(tree.getLargestDepth())