from setuptools import setup
from setuptools import find_packages

setup(
    name='myprotein_webscraper',
    version='0.01',
    description='webscraper to obtain data on nutrition products on the MyProtein website',
    url='https://github.com/amyjanem/Data_Collection_Project',
    author='Amy Mallett'
    license='MIT'   #check what to use here
    packages=find_packages()
    install_requires=['datetime', 'json', 'os', 'requests', 'selenium', 'time', 'uuid'],
    
)


