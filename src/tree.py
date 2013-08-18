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

	def __getDepth(self, node):
		
		largestDepth = 0;
		for child in node.children.values():
			childDepth = self.__getDepth(child)

			if childDepth > largestDepth:
				largestDepth = childDepth

		return largestDepth + 1

	def getDepth(self):
		node = self.root

		if self.root is None:
			return 0

		return self.__getDepth(self.root)

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
		instrument = len(self.children)
		if instrument > len(instruments):
			logging.warning("Not enough instruments available for unique package.")
			instrument = 0
		self.children[value] = TreeNode(value, instrument)
	def getChild(self, key):
		return self.children[key]

if __name__ == '__main__':
	tree = Tree()
	tree.add(['com','package', 'test', 'structure'])
	tree.add(['com','package', 'util', 'security'])
	tree.printState()

	print tree.getDepth()