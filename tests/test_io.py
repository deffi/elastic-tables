import sys
import unittest
import subprocess

import elastic_tables.io


class IoTest(unittest.TestCase):
    def test_stdout(self):
        output = subprocess.check_output([sys.executable, __file__], text=True)
        self.assertEqual("foob  \nf  bar\n", output)


if __name__ == '__main__':
    # unittest.main()

    import elastic_tables.io

    elastic_tables.io.install()
    print("foo\tb")
    print("f\tbar")
