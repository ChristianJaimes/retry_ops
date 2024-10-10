from setuptools import setup, find_packages

setup(
    name='retry_ops',
    version='0.2.0',
    description='A Python library providing retry decorators.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Christian Jaimes Acevedo',
    url='https://github.com/ChristianJaimes/retry_ops', 
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
