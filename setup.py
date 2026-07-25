from setuptools import find_packages,setup 
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
  '''
  func will return the list of requirements as requirments.txt will have list of libraries
  '''

  requirements = []
  with open(file_path) as file_obj:
    requirements = file_obj.readlines()

    # when it will read  first line of requirement and thn second line it will actually read \n (used for next line) which we dont wanted so  changes \n with blank space " " ->
    

    requirements = [req.replace("\n" ," ")for req in requirements]

    # not to include '-e .' in list of requirements
    
    if HYPEN_E_DOT in requirements:
      requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
  name = 'mlproject',
  version = '0.0.1',
  author = 'Laksh',
  author_email = 'lakshsadhioura03@gmail.com',
  packages = find_packages(),
  # difficult to write 100 of pacakages names so instead created a function so it can access requirements file read packages  and install them 
  install_requires = get_requirements('requirements.txt'),







)