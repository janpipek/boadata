from boadata.gui.qt.selectable_item_list_view import SelectableItemListView
from boadata.core.data_types import SelectableItemList
from PyQt4 import QtGui

import unittest
import _core


class TestSelectableItemListViewTest(unittest.TestCase):
    def test_create_from_empty_list(self):
        item_list = SelectableItemList()
        view = SelectableItemListView(item_list)
        self.assertEqual(item_list, view.item_list)

    def test_create_from_wrong_objects(self):
        item_list = []
        self.assertRaises(BaseException, SelectableItemListView, item_list)

        item_list = {}
        self.assertRaises(BaseException, SelectableItemListView, item_list)

    def test_correct_item_creation_in_init(self):
        item_list = SelectableItemList()
        item_list["aaa"] = "bbb"

        view = SelectableItemListView(item_list)
        assert "aaa" in view.items
        assert isinstance(view.items["aaa"], QtGui.QStandardItem)
