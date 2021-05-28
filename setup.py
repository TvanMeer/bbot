from setuptools import setup

setup(name='bbot',
      version='0.1',
      description='A simple framework to build binance spot trading bots',
      classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
      ],
      url='https://github.com/TvanMeer/bbot',
      author='Thomas van Meer',
      author_email='tvanmeer123@gmail.com',
      license='MIT',
      packages=['bbot'],
      install_requires=[
          'pandas',
          'python-binance',
      ],
      zip_safe=False)
