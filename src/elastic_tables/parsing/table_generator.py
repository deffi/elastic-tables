from elastic_tables.model import Table, Row, Block, Line


class TableGenerator:
    separator = "\t"

    def __init__(self):
        pass

    def _row_from_line(self, line: Line) -> Row:
        return Row(line.content.split(self.separator), line.terminator)

    def table_from_block(self, block: Block) -> Table:
        rows = (self._row_from_line(line) for line in block.lines)
        return Table(list(rows))
