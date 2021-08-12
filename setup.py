from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='maid_manga_id',
    version='1.1',
    description='Maid Manga Indonesia wrapper using Python BeautifulSoup.',
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
    keywords='manga maid_manga maid_manga_id manga_id MaidMangaID',
    license='MIT',
    packages=find_packages(exclude=['old_version', 'downloads']),
    install_requires=[
        'requests',
        'bs4',
        'lxml',
        'img2pdf',
        'humanfriendly',
        'motor',
        'python-dateutil'
    ],
    include_package_data=True,
    zip_safe=False
)