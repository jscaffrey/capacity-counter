from setuptools import find_packages, setup

setup(
    name='capacity-counter',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
	'flask-migrate',
	'flask-sqlalchemy',
        'flask-login',
        'flask-apscheduler',
        'flask-wtf'
        ],
)
