# coding=utf-8
import boto3
import Utilities.fileutils as fileutils
import logging

L = logging.getLogger()


def upload_reports(base_path_object):

    reports_root = base_path_object.get_reports_output_path()
    build_folder_root = base_path_object.get_build_folder_path()
    credentials = base_path_object.settings.get_upload_credential_dict()

    upload_object = S3Upload(credentials)
    upload_object.upload_folder(reports_root.as_posix(), reports_root.as_posix())
    upload_object.upload_folder(build_folder_root.as_posix(), build_folder_root.as_posix())


class S3Upload:

    def __init__(self, credentials):

        AWS_ACCESS_KEY_ID = credentials["access"]
        AWS_SECRET_ACCESS_KEY = credentials["secret"]

        self.BUCKET_NAME = credentials["bucket"]

        self.s3 = boto3.client(
            's3',
            # Hard coded strings as credentials, not recommended.
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    def upload_file(self, file_path, uploaded_path):

        try:
            # self.s3.upload_file(file_path, self.BUCKET_NAME, uploaded_path)

            # Default mime type
            content_type = 'application/octet-stream'

            if file_path.endswith(".html"):
                content_type = 'text/html'
            elif file_path.endswith(".css") or file_path.endswith(".less"):
                content_type = 'text/css'
            elif file_path.endswith(".jpg"):
                content_type = 'image/jpeg'
            elif file_path.endswith(".png"):
                content_type = 'image/png'
            elif file_path.endswith(".js") or file_path.endswith(".json"):
                content_type = 'text/javascript'

            self.s3.upload_file(file_path, self.BUCKET_NAME, uploaded_path, ExtraArgs={'ContentType': content_type,

                                                                                      'ACL': 'public-read'})
            L.info("Uploading: %s as %s", file_path, content_type)

        except:
            L.warning("Unable to upload")

    def upload_folder(self, path, root_path):
        files = fileutils.get_all_file_paths_from_directory(path)

        for each_file_to_upload in files:
            split_name = each_file_to_upload.split(root_path)[1]
            for_web = split_name.replace("\\", "/")

            # Removing the first slash
            if for_web.startswith("/"):
                for_web = for_web[1:]

            self.upload_file(each_file_to_upload, for_web)
