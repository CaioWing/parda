"""
Parda: A versatile Python module for loading, processing, 
and managing complex datasets with nested structures, 
supporting on-the-fly transformations and concurrent data handling. 

"""

__version__ = '0.1.0'
__author__ = 'Caio Wingeter <castilhocaio1164@gmail.com>'
__all__ = ['DatasetLoader']


from .parser import (
    DatasetLoader
)