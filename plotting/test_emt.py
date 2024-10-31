from utils import Config

path = ('setup.ini')

c = Config()
c.setup(path)
print(c.multifile)