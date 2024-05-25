from setuptools import setup, find_packages

setup(
    name='BgsContentPlatformApi',
    version='1.0.0',
    packages=find_packages(),
    package_data={},
    install_requires=[
        'Flask==3.0.3',
        'Flask_Cors==4.0.1',
        'pymongo[srv]==3.12.0',
        'waitress==3.0.0',
        'python-dotenv==1.0.1',
        'pydantic==1.10.15',
        'fastapi==0.111.0',
        'flask_jwt_extended==4.6.0'
    ],
)