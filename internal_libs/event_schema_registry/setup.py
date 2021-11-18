import os
from setuptools import find_packages, setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='event_schema_registry',
    version='0.1.0',
    packages=find_packages(include=['event_schema_registry']),
    package_data={'event_schema_registry': package_files('event_schema_registry/schemas')},
    include_package_data=True,
    install_requires=[
        'jsonschema==4.2.1',
    ],
    description='Event schema registry for aTES',
    author='korckykrou@gmail.com',
)
