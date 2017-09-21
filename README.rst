==========================
scrapy-gridfsfilespipeline
==========================

scrapy-gridfsfilespipeline is an extension of files and images pipelines to store data in MongoDB GridFS.

Installation
============

Install scrapy-gridfsfilespipeline using ``pip``::


    $ pip install git+https://github.com/zahariesergiu/scrapy-gridfsfilespipeline

Configuration
=============


Include the pipeline(s) in ITEM_PIPELINES dict in ``settings.py``::



    ITEM_PIPELINES = {
        'scrapy_gridfsfilespipeline.files.GridFSFilesPipeline': 1,
        'scrapy_gridfsfilespipeline.images.GridFSImagesPipeline': 2,
    }

Set the MONGO_URI, i.e.::


    MONGO_URI = "mongodb://localhost:27017/dbname"

Where dbname is your mogo database name.
Done!
