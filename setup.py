from setuptools import setup

setup(
    name='scrapy-gridfsfilespipeline',
    version='1.0.dev1',
    description='Scrapy files and images pipelines to store in MongoDB GridFS',
    long_description='Scrapy files and images pipelines to store in MongoDB GridFS',
    url='https://github.com/zahariesergiu/scrapy-gridfsfilespipeline',
    author='Sergiu Zaharie',
    author_email='zahariesergiu@gmail.com',
    license='BSD',
    platforms=['Any'],
    packages=['scrapy_gridfsfilespipeline'],
    install_requires=[
            'Scrapy',
            'pymongo',
    ],
)
