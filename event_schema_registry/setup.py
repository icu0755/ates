from setuptools import setup, find_packages

setup(
    name="event_schema_registry",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "jsonschema",
    ],
)