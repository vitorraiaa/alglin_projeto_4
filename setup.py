from setuptools import setup, find_packages

setup(
    name='alglin_projeto_4',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'demo = cubo.cubo:run',
        ],
    },
    author='Vitor Raia e Rafael Ken',
    description='Rotacionar um cubo em 3 dimensões',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vitorraiaa/alglin_projeto_4.git',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
