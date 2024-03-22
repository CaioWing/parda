from setuptools import setup, find_packages

setup(
    name='parda',
    version='0.1.0',
    description='A package for parsing and loading structured datasets',
    author='Caio Wingeter de Castilho',
    author_email='castilhocaio1164@gmail.com',
    url='https://github.com/CaioWing/parda',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'Pillow',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)