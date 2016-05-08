#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="python-weixin",
      version="0.1.5",
      description="Python Weixin API client",
      license="BSD",
      install_requires=["simplejson", "requests", "six", "chardet"],
      author="Zongxiao Cheng",
      author_email="cacique1103@gmail.com",
      url="https://github.com/zongxiao/python-weixin",
      download_url="https://github.com/zongxiao/python-weixin/archive/master.zip",
      packages=find_packages(),
      keywords=["python-weixin", "weixin", "wechat", "sdk"],
      zip_safe=True)
