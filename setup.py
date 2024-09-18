from setuptools import find_packages, setup 
# find_packages finds package in your local folder and wherever it finds a 
# folder with an init along it it considers that as a package

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='arshdeep',
    author_email='deeparsh618@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages() # Automatically finds all packages in the directory that contain an __init__.py file and includes them in the distribution.
)

# No, you don't have to mention the dependencies in both install_requires and requirements.txt, but the two serve slightly different purposes, and some developers prefer to use both for flexibility.