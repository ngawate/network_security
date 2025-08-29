from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    '''
    This will give list of requirements
    '''
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                #ignore -e .
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    
    return requirement_lst

setup(
    name='Network Security',
    version='0.0.1',
    author='Nikhil Gawate',
    author_email='ngawate@umich.edu',
    packages=find_packages(),
    install_requires=get_requirements()
)