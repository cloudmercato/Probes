"""Utility for collect monitoring data"""
VERSION = (0, 1, 0)
__version__ = '.'.join([str(v) for v in VERSION])
__author__ = 'Anthony Monthe'
__email__ = 'anthony@cloud-mercato.com'
__url__ = 'https://github.com/cloudmercato/probes'
__license__ = 'MIT'

from .manager import ProbeManager
