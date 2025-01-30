from setuptools import find_packages, setup


setup(
    name='MCQGENERATOR',
    version='0.0.1',
    author='Syed Ali Faizan',
    author_email = 'faizanzaidy78@gamil.com',
    install_requires = ["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)