from setuptools import setup, find_packages

setup(
    name='sure_retry',
    version='0.1.0',
    description='A Python library providing retry decorators.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Christian Jaimes Acevedo',
    url='https://github.com/ChristianJaimes/sure_retry', 
    license='MIT',
    packages=find_packages(),  
    classifiers=[
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
    install_requires=[],  
    tests_require=['pytest'],  
    setup_requires=['pytest-runner'],  
)
