#!python

class ModALTestVersion():
    def __init__(self):
        super().__init__()

    def get_version(self):
        import sqlalchemy
        return sqlalchemy.__version__

def main():
    import sys
    print(ModALTestVersion().get_version())
    print(f"Python installed in {sys.executable}")
    print(f"Python installed in {sys.exec_prefix}")
    print(f"Python path variables in {'; '.join(sys.path)}")

if __name__ == '__main__':
    main()