#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="python-weixin",
      version="0.0.3",
      description="Weixin API client",
      license="BSD",
      install_requires=["simplejson","requests","six", "chardet"],
      author="Zongxiao Cheng",
      author_email="cacique1103@gmail.com",
      url="https://github.com/zongxiao/python-weixin",
      packages = find_packages(),
      keywords= "weixin wechat",
      zip_safe = True)
