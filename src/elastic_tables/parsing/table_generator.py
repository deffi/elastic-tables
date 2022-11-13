from elastic_tables.model import Table, Row, Block, Line, Cell


class TableGenerator:
    separator = "\t"

    def __init__(self):
        pass

    def table_from_block(self, block: Block) -> Table:
        rows = (Row.from_line(line, self.separator) for line in block.lines)
        return Table(list(rows))
