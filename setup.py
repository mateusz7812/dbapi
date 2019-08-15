from setuptools import setup

setup(
    name='lists_core',
    version='',
    packages=['Forwarders', "Guards", "Managers", "Processors", "Requests", "Responses", "Takers", "Workers"],
    py_modules=['Main.py'],
    url='https://github.com/mateusz7812/modular_server',
    include_package_data=True,
    package_dir={'': 'lists_core'},
    license='',
    author='mateusz7812',
    author_email='',
    description='', install_requires=['flask']
)
