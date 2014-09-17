# TODO: Rebuild into proper test
import sys
sys.path += [ "../.."]

from boadata.trees.file import DirectoryNode
branch = DirectoryNode(sys.argv[1])
branch.dump(subtree=True)

#for d in branch.descendants:
#    print d.full_title, d.mime_type[0]