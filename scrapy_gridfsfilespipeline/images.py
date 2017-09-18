from scrapy.pipelines.images import ImagesPipeline

from .files import GridFSFilesPipeline


class GridFSImagesPipeline(ImagesPipeline, GridFSFilesPipeline):
    """
    An extension of ImagesPipeline that store files in MongoDB GridFS.
    Is using a guid to check if the file exists in GridFS and MongoDB ObjectId to reference the file with item.
    ImagesPipeline was using a single variable 'path' for reference and identification.
    guid is used in MongoGridFSFilesPipeline because the pipeline needs a unique identifier generated based on file URL.
    MongoGridFSFilesPipeline is using ObjectId to reference the file because it's the primary key.
    """
