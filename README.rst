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

Include the pipeline(s) in ``ITEM_PIPELINES`` dict in ``settings.py``::
    ITEM_PIPELINES = {
        'scrapy_gridfsfilespipeline.files.GridFSFilesPipeline': 1,
        'scrapy_gridfsfilespipeline.images.GridFSImagesPipeline': 2,
    }
Set the ``MONGO_URI``, i.e.::

    MONGO_URI = "mongodb://localhost:27017/dbname"

Where dbname is your mogo database name.
Done!
In case of using GridFSImagesPipeline, ``IMAGES_THUMBS`` setting is also available for generating thumbs i.e.::

    IMAGES_THUMBS = {
        'small': (50, 50),
        'big': (100, 100),
    }
Output Examples
=============

Item result using GridFSImagesPipeline::

    {
        'description': u'An open source and collaborative framework for extracting the data you need from websites.\n      ',
        'image_urls': ['https://scrapy.org/img/scrapylogo.png'],
        'images': [{'checksum': '4c2b30eb691b6fb5dcafff8ae0020a75',
                 'file_guid': '27200bf84dab638cb6b102bf709d8b17201a31d5',
                 'filename': 'scrapylogo.png',
                 'mongo_objectid': ObjectId('59c3aaf2d297fb4d98f89b46'),
                 'url': 'https://scrapy.org/img/scrapylogo.png'}]
    }
Item result using GridFSImagesPipeline with IMAGES_THUMBS set::

    {
        'description': u'An open source and collaborative framework for extracting the data you need from websites.',
        'image_urls': ['https://scrapy.org/img/scrapylogo.png'],
        'images': [{'checksum': '4c2b30eb691b6fb5dcafff8ae0020a75',
                 'file_guid': '27200bf84dab638cb6b102bf709d8b17201a31d5',
                 'filename': 'scrapylogo.png',
                 'mongo_objectid': {'big': ObjectId('59c3a869d297fb4baab48d72'),
                                    'image': ObjectId('59c3a868d297fb4baab48d6e'),
                                    'small': ObjectId('59c3a869d297fb4baab48d70')},
                 'url': 'https://scrapy.org/img/scrapylogo.png'}]
     }

MongoDB GridFS documents result::

    {
        "_id" : ObjectId("59c3a868d297fb4baab48d6e"),
        "chunkSize" : 261120,
        "filename" : "scrapylogo.png",
        "length" : 6203,
        "scrapy_guid" : "27200bf84dab638cb6b102bf709d8b17201a31d5",
        "uploadDate" : ISODate("2017-09-21T11:54:17.432Z"),
        "md5" : "4c2b30eb691b6fb5dcafff8ae0020a75"
    }
    {
        "_id" : ObjectId("59c3a869d297fb4baab48d70"),
        "chunkSize" : 261120,
        "filename" : "scrapylogo_thumb_small.png",
        "length" : 980,
        "scrapy_guid" : "27200bf84dab638cb6b102bf709d8b17201a31d5",
        "uploadDate" : ISODate("2017-09-21T11:54:17.437Z"),
        "md5" : "bfa8302353cbf9bba96b88d3bb643bb4"
    }
    {
        "_id" : ObjectId("59c3a869d297fb4baab48d72"),
        "chunkSize" : 261120,
        "filename" : "scrapylogo_thumb_big.png",
        "length" : 1706,
        "scrapy_guid" : "27200bf84dab638cb6b102bf709d8b17201a31d5",
        "uploadDate" : ISODate("2017-09-21T11:54:17.442Z"),
        "md5" : "fef2ef2fdda0d99efa8dcfe62bae224a"
    }
