from setuptools import setup, find_packages

setup(
    name='enviratronlogger',
    version='1.0.0',
    #url='https://github.com/mypackage.git',
    author='Scott Zarecor',
    author_email='scott@zarecor.com',
    description='A module for logging plant growth chamber conditions for the Enviratron project.',
    #packages=find_packages(),
    py_modules=["enviratron_logger", "chamber"],
    entry_points={
        'console_scripts': [
            'enviratronlogger=enviratron_logger:main'
        ]
    },
    #install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1'],
    install_requires=['lxml >= 3.8.0', 'python-json-logger', 'requests', 'PyYAML'],
)