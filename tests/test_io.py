import sys
import unittest
import subprocess


class IoTest(unittest.TestCase):
    @staticmethod
    def do_stdout_with_install():
        import elastic_tables.io
        elastic_tables.io.install()
        print("foo\tb")
        print("f\tbar")

    def test_stdout_with_install(self):
        output = subprocess.check_output([sys.executable, __file__, "do_stdout_with_install"], text=True)
        self.assertEqual("foob  \nf  bar\n", output)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    else:
        getattr(IoTest, sys.argv[1])(*sys.argv[2:])
