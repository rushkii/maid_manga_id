from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='maid_manga_id',
    version='1.0',
    description='Maid Manga Indonesia API Using Python Web Scraper.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/rushkii/maid_manga_id',
    author='Kee',
    author_email='riskimuhammmad1@gmail.com',
    keywords='manga maid_manga maid_manga_id manga_id',
    license='MIT',
    packages=['maid_manga'],
    install_requires=['requests', 'bs4', 'lxml', 'urllib', 're'],
    include_package_data=True,
    zip_safe=False
)