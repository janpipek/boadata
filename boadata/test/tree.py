# TODO: Rebuild into proper test
import sys
sys.path += [ "../.."]

from boadata.trees.file import DirectoryNode
branch = DirectoryNode(sys.argv[1])
branch.dump()