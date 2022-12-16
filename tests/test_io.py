import sys
import subprocess


class TestIo:
    @staticmethod
    def do_stdout_with_install():
        import elastic_tables.io
        elastic_tables.io.install()
        print("foo\tb")
        print("f\tbar")

    def test_stdout_with_install(self):
        output = subprocess.check_output([sys.executable, __file__, "do_stdout_with_install"], text=True)
        assert output == "foob\nf  bar\n"


if __name__ == '__main__':
    getattr(TestIo, sys.argv[1])(*sys.argv[2:])
