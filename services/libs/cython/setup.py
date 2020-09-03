from distutils.core import setup
from Cython.Build import cythonize
 
setup(
    name="matt_test",
    ext_modules = cythonize(["services/libs/cython/get_ngrams.pyx"]),
    language_level=3
)