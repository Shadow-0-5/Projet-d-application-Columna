from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("boardC", ["boardC.pyx"]),
    Extension("iaC", ["iaC.pyx", "Hungarian.cpp"], language="c++"),
]

setup(
    ext_modules = cythonize(extensions, compiler_directives={'language_level': "3"})
)