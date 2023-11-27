# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from pkg_resources import parse_requirements

with open("requirements.txt", encoding="utf-8") as fp:
    install_requires = [str(requirement) for requirement in parse_requirements(fp)]

with open("readme.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    # 发布到pypi上面可以被搜索的项目的名称
    name="my_package",
    version="0.0.1",
    author="yan yue",
    author_email="1874524491@qq.com",
    description="python 代码底座",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License, Version 2.0",
    url="http://test.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    include_package_data=True,  # 一般不需要
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'test = test.help:main'
        ]
    }
)
