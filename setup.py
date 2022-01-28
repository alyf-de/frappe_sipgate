from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sipgate/__init__.py
from sipgate import __version__ as version

setup(
	name="sipgate",
	version=version,
	description="Sync contacts from Frappe/ERPNext to Sipgate",
	author="ALYF GmbH",
	author_email="hallo@alyf.de",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
