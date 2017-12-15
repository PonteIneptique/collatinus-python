from setuptools import setup, find_packages

version = "0.1.3"

setup(
    name='pycollatinus',
    version=version,
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/ponteineptique/collatinus-python',
    license='GNU GPL v2',
    author='Thibault Clerice, Yves Ouvrard, Philippe Verkerk',
    author_email='leponteineptique@gmail.com',
    description='Collatinus Port for Python',
    test_suite="tests",
    install_requires=[
        "unidecode==0.4.21"
    ],
    test_requires=[
        "coverage==4.4.1"
    ],
    include_package_data=True,
    zip_safe=False
)
