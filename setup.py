#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="python-weixin",
      version="0.3.0",
      description="Python Weixin API client support wechat-app",
      license="BSD",
      install_requires=["simplejson", "requests", "six", "chardet"],
      author="gusibi",
      author_email="cacique1103@gmail.com",
      url="https://github.com/gusibi/python-weixin",
      download_url="https://github.com/gusibi/python-weixin/archive/master.zip",
      packages=find_packages(),
      keywords=["python-weixin", "weixin", "wechat", "sdk", "weapp", "wxapp"],
      zip_safe=True)
