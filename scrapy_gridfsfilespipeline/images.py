import six

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from PIL import Image

from scrapy.pipelines.images import ImagesPipeline, ImageException
from scrapy.utils.misc import md5sum

from .files import GridFSFilesPipeline


class GridFSImagesPipeline(ImagesPipeline, GridFSFilesPipeline):
    """
    An extension of ImagesPipeline that store files in MongoDB GridFS.
    Is using a guid to check if the file exists in GridFS and MongoDB ObjectId to reference the file with item.
    ImagesPipeline was using a single variable 'path' for reference and identification.
    guid is used in MongoGridFSFilesPipeline because the pipeline needs a unique identifier generated based on file URL.
    MongoGridFSFilesPipeline is using ObjectId to reference the file because it's the primary key.
    """

    @classmethod
    def from_settings(cls, settings):
        store_uri = settings['MONGO_URI']
        return cls(store_uri, settings=settings)

    def image_downloaded(self, response, request, info):
        """Override to return image_ids along with checksum"""

        # First image is the original image
        image_iter = self.get_images(response, request, info)
        image_guid, image, buf = image_iter.next()
        filename = self.filename(request)
        file_data = {'scrapy_guid': image_guid, "filename": filename}
        checksum = md5sum(buf)
        buf.seek(0)

        mongo_object_id = self.store.persist_file(buf, info, file_data=file_data,
                        meta={'width': image.size[0], 'height': image.size[1]}, headers={'Content-Type': 'image/jpeg'})

        # Next images are thumbs
        thumbs = {}
        thumbs_id_iter = six.iteritems(self.thumbs)
        for thumb_guid, thumb, thumb_buf in image_iter:
            width, height = thumb.size
            thumb_buf.seek(0)
            filename = self.filename(request)
            name, ext = filename.split('.')
            thumb_id, size = thumbs_id_iter.next()
            filename = name + '_thumb_' + thumb_id + '.' + ext
            file_data = {'scrapy_guid': thumb_guid, "filename": filename}
            thumb_mongo_object_id = self.store.persist_file(thumb_buf, info, file_data=file_data,
                        meta={'width': width, 'height': height}, headers={'Content-Type': 'image/jpeg'})
            thumbs[thumb_id] = thumb_mongo_object_id
        if thumbs:
            images_mongoobjectids = {"image": mongo_object_id}
            images_mongoobjectids.update(thumbs)
            return checksum, images_mongoobjectids
        else:
            return checksum, mongo_object_id

    def get_images(self, response, request, info):
        """Override to return thumb_guid instead of thumb_path"""

        image_guid = self.file_guid(request, response=response, info=info)
        orig_image = Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.min_width, self.min_height))

        image, buf = self.convert_image(orig_image)
        yield image_guid, image, buf

        for thumb_id, size in six.iteritems(self.thumbs):
            thumb_guid = self.file_guid(request, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_guid, thumb_image, thumb_buf
