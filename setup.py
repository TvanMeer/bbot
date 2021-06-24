from setuptools import find_packages, setup


setup(name='bbot',
      version='0.1',
      description='A simple framework to build binance spot trading bots.',
      classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
      ],
      url='https://github.com/TvanMeer/bbot',
      author='Thomas van Meer',
      author_email='tvanmeer123@gmail.com',
      license='MIT',
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      install_requires=[
          'python-binance',
          'typeguard',
      ],
      zip_safe=False)
