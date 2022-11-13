from elastic_tables.model import Table, Row, Block, Line, Cell


class TableGenerator:
    separator = "\t"

    def __init__(self):
        pass

    def table_from_block(self, block: Block) -> Table:
        return Table.from_block(block, self.separator)
