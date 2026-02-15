from setuptools import setup, find_packages

setup(
    name='BookSageAI',
    version='0.2.0',
    author='Md Emon Hasan',
    author_email='iconicemon01@gmail.com',
    description='A Multi-Method Hybrid Book Recommendation System built with Streamlit, Collaborative Filtering and Content-Based Filtering.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Md-Emon-Hasan/BookSageAI',
    packages=find_packages(where='app'),
    package_dir={'': 'app'},
    include_package_data=True,
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy',
        'Requests',
        'scipy',
        'pytest',
        'flask',
        'pathlib',
        'gunicorn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
