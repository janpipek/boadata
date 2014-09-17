# TODO: Rebuild into proper test
import sys
sys.path += [ "../.."]

from boadata.trees.excel import ExcelFile
ef = ExcelFile(sys.argv[1])
for ef in ef.children:
    print ef.title
    print ef.to("pandas_frame")