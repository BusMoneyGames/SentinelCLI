from Utilities import BaseSentinelTest, S3

class TestUpload_reports(BaseSentinelTest.SentinelBaseTest):

    def test_upload_reports(self):
        S3.upload_reports(self.sentinel_report_project_paths)

