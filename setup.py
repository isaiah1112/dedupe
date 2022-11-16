# coding=utf-8
"""Setup file for dedupe utility"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='dedupe',
    version='1.0.0',
    author='Jesse Almanrode',
    author_email='jesse@almanrode.com',
    description='Utility for comparing files based on MD5 or SHA1 hashes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['dedupe'],
    python_requires='>=3.7',
    install_requires=['click>=8.1.2',
                   ],
    entry_points={
        'console_scripts': [
            'dedupe = dedupe:cli',
        ]
    },
    platforms=['Linux', 'Darwin'],
    classifiers=[
     'Programming Language :: Python',
     'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
     'Development Status :: 5 - Production/Stable',
     'Programming Language :: Python',
     'Programming Language :: Python :: 3.7',
     'Programming Language :: Python :: 3.8',
     'Programming Language :: Python :: 3.9',
     'Programming Language :: Python :: 3.10',
     'Programming Language :: Python :: 3.11',
    ],
    )
