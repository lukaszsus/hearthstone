import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

files = [os.path.join('simulator', f) for f in os.listdir('simulator')
             if os.path.isfile(os.path.join('./simulator/', f))]
files.extend([os.path.join('mcts', f) for f in os.listdir('mcts')
             if os.path.isfile(os.path.join('./mcts/', f))])

ext_modules = list()
for file in files:
    base = os.path.basename('/root/dir/sub/file.ext')
    file_name = os.path.splitext(base)[0]
    ext_modules.append(Extension(file_name,  [file]))

setup(
    name = 'Hearthstone',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)