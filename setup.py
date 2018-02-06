from setuptools import setup

try:
    with open("README") as f:
        long_description = f.read()
except:
    long_description = None
    
setup(
    name='vjson',
    version='0.1',
    description='Load json with a variable template',
    long_description=long_description,
    packages=[
        'vjson',
    ],
    install_requires=[
        # pip modules here
    ],
    # Forces the package source to be deployed instead
    # of just the egg (good if we have non-source files)
    zip_safe=False,
)