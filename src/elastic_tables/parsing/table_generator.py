from elastic_tables.model import Table, Row, Block, Line, Cell


class TableGenerator:
    separator = "\t"

    def __init__(self):
        pass

    def _row_from_line(self, line: Line) -> Row:
        # TODO defer to Row.from_line?
        cells = [Cell(text) for text in line.content.split(self.separator)]
        return Row(cells, line.terminator)

    def table_from_block(self, block: Block) -> Table:
        rows = (self._row_from_line(line) for line in block.lines)
        return Table(list(rows))
