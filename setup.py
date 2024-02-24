from setuptools import setup, find_packages
import os
from pathlib import Path

location = Path(os.path.abspath(os.path.dirname(__file__)))
with open(os.path.join(location, "requirements.txt"), "r") as f:
   requirements = f.read().splitlines()

with open(location / "README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="maniple",
    version="0.0.1",
    author="PyRepair Team",
    description="A package to facilitate data-wrangling for APR tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PyRepair/maniple",
    packages=find_packages(include=["maniple*"]),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "maniple=maniple.maniple:main",
            "check_pass_k=maniple.metrics.check_pass_k:main",
        ]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",  # Updated to Apache License
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    license="Apache License 2.0",
)