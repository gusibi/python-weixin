#!/usr/bin/env python
from io import open

from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(name="python-weixin",
      version="0.4.7",
      description="Python Weixin API client support wechat-app",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="BSD",
      install_requires=requirements,
      author="gusibi",
      author_email="cacique1103@gmail.com",
      url="https://github.com/gusibi/python-weixin",
      download_url="https://github.com/gusibi/python-weixin/archive/master.zip",
      packages=find_packages(),
      keywords=["python-weixin", "weixin", "wechat", "sdk", "weapp", "wxapp"],
      zip_safe=True)
