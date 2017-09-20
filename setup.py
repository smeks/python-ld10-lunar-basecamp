from distutils.core import setup
import py2exe,sys

sys.argv.append("py2exe")

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)

script = Target(
		version = "1.0",
		name = "Basecamp Chain Reaction",
		description = "pygame/pyopengl/pyode physics based lunar lander game",
		author = "negativegeforce",
		script = "Basecamp.py",
		icon_resources = [(1,"icon.ico")])
		
setup(
	options = {	"py2exe":	{"compressed":1,
							 "optimize": 2,
							 "ascii": 1,
							 "bundle_files": 1,
							 "excludes" : ["PyOpenGL"]}},
	zipfile = None,
	windows = [script])
