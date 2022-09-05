from setuptools import setup, find_namespace_packages

setup(
    name='clean-folder',
    version='1',
    description='first package',
    url='https://github.com/Gorobchuk',
    author='Anna Gorobchuk',
    author_email='a40290@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['sort=clean_folder.clean:sort']}
)