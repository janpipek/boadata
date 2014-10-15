from ..core import DataNode, DataObject, DataProperties, DataTree
import sqlalchemy
import pandas as pd


class TableObject(DataObject):
    def __init__(self, node=None):
        super(TableObject, self).__init__(node=node)
        self.table_name = node.table_name
        self.engine = node.parent.engine

    def as_pandas_frame(self):
        query = "SELECT * FROM %s LIMIT 1000" % self.table_name
        return pd.read_sql_query(query, self.engine)            

    @property
    def ndim(self):
        return 2

    @property
    def title(self):
        return self.table_name


class TableNode(DataNode):
    def __init__(self, table_name, parent=None):
        super(TableNode, self).__init__(parent)
        self.table_name = table_name

    @property
    def title(self):
        return self.table_name

    def create_data_object(self):
        return TableObject(self)

    node_type = "SQL Table"


class DatabaseTree(DataTree):
    def __init__(self, constr, parent=None):
        '''
        :param constr: Connection string of the database.
        '''
        super(DatabaseTree, self).__init__(parent)
        self.constr = constr
        self.engine = sqlalchemy.create_engine(constr)

    node_type = "SQL Database"

    def load_children(self):
        with self.engine.connect() as conn:
            rows = conn.execute("SHOW TABLES").fetchall()
            for row in rows:
                name = row[0]
                child = TableNode(table_name=name)
                self.add_child(child)

    @property
    def title(self):
        return "Database"