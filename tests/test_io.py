import sys
import unittest
import subprocess

import elastic_tabs.io


class MyTestCase(unittest.TestCase):
    def test_stdout(self):
        output = subprocess.check_output([sys.executable, __file__], text=True)
        self.assertEqual("foob  \nf  bar\n", output)


if __name__ == '__main__':
    # unittest.main()

    import elastic_tabs.io

    elastic_tabs.io.install()
    print("foo\tb")
    print("f\tbar")
