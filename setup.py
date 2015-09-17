import oh_my_generator

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

def cat_readme():
	with open('README.md') as f:
		return f.read()

setup(
	name='oh-my-generator',
	version=oh_my_generator.__version__,
	description=oh_my_generator.__doc__.strip(),
	long_description=cat_readme(),
	url='https://github.com/Julow/oh-my-generator',
	author=oh_my_generator.__author__,
	packages=['oh_my_generator'],
	entry_points={'console_scripts': ['omg = oh_my_generator.__main__:main']},
	keywords=['omg', 'oh-my-generator', 'generator'],
)
