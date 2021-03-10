import logging
import time
import hashlib
import hmac
from odoo.addons.generic_mixin.tests.common import TEST_URL
from .phantom_common import TestPhantomTour

_logger = logging.getLogger(__name__)


class TestUploadFile(TestPhantomTour):
    def setUp(self):
        super(TestUploadFile, self).setUp()
        self.user = self.env.ref('crnd_wsd.user_demo_service_desk_website')
        self.request_type = self.env.ref(
            'crnd_service_desk.request_type_incident')

    def get_csrf_token(self):
        token = self.session.sid
        max_ts = int(time.time() + 3600)
        msg = '%s%s' % (token, max_ts)
        secret = self.env['ir.config_parameter'].sudo().get_param(
            'database.secret')
        hm = hmac.new(
            secret.encode('ascii'),
            msg.encode('utf-8'),
            hashlib.sha1).hexdigest()
        csrf_token = '%so%s' % (hm, max_ts)
        return csrf_token

    def test_upload_file_existing_request(self):
        self.authenticate('demo-sd-website', 'demo-sd-website')  # nosec
        test_request = self.env['request.request'].search(
            [('created_by_id', '=', self.user.id)], limit=1)
        url = '%s/requests/request/%s' % (
            TEST_URL, str(test_request.id))
        response = self.opener.get(url)
        self.assertEqual(response.status_code, 200)

        url = "%s/crnd_wsd/file_upload" % TEST_URL

        data = {
            'csrf_token': self.get_csrf_token(),
            'request_id': test_request.id,
        }
        # test upload file
        files = {
            'upload': open('crnd_wsd/static/description/index.html', 'rb'),
        }
        response = self.opener.post(url=url, files=files, data=data)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'OK')
        self.assertEqual(response_json['success'], True)
        attachment_url_file = response_json['attachment_url']
        response_attachment = self.opener.get(
            "%s%s" % (TEST_URL, attachment_url_file))
        self.assertEqual(response_attachment.status_code, 200)
        self.assertEqual(attachment_url_file[:13], '/web/content/')

        attachments = self.env['ir.attachment'].search(
            [('res_model', '=', 'request.request'),
             ('res_id', '=', test_request.id)])
        self.assertEqual(len(attachments), 1)

        # test upload image
        data = {
            'csrf_token': self.get_csrf_token(),
            'request_id': test_request.id,
            'is_image': True,
        }
        files = {
            'upload': open('crnd_wsd/static/description/banner.gif', 'rb'),
        }
        response = self.opener.post(url=url, files=files, data=data)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'OK')
        self.assertEqual(response_json['success'], True)
        attachment_url_image = response_json['attachment_url']
        response_attachment = self.opener.get(
            "%s%s" % (TEST_URL, attachment_url_image))
        self.assertEqual(response_attachment.status_code, 200)
        self.assertEqual(attachment_url_image[:11], '/web/image/')

        attachments = self.env['ir.attachment'].search(
            [('res_model', '=', 'request.request'),
             ('res_id', '=', test_request.id)])
        self.assertEqual(len(attachments), 2)

    def test_upload_file_new_request(self):
        self.authenticate('demo-sd-website', 'demo-sd-website')  # nosec

        url = "%s/crnd_wsd/file_upload" % TEST_URL

        data = {
            'csrf_token': self.get_csrf_token(),
        }
        # test upload file
        files = {
            'upload': open('crnd_wsd/static/description/index.html', 'rb'),
        }
        response = self.opener.post(url=url, files=files, data=data)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'OK')
        self.assertEqual(response_json['success'], True)
        attachment_url_file = response_json['attachment_url']
        response_attachment = self.opener.get(
            "%s%s" % (TEST_URL, attachment_url_file))
        self.assertEqual(response_attachment.status_code, 200)
        self.assertEqual(attachment_url_file[:13], '/web/content/')

        # test upload image
        data = {
            'csrf_token': self.get_csrf_token(),
            'is_image': True,
        }
        files = {
            'upload': open('crnd_wsd/static/description/banner.gif', 'rb'),
        }
        response = self.opener.post(url=url, files=files, data=data)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'OK')
        self.assertEqual(response_json['success'], True)
        attachment_url_image = response_json['attachment_url']
        response_attachment = self.opener.get(
            "%s%s" % (TEST_URL, attachment_url_image))
        self.assertEqual(response_attachment.status_code, 200)
        self.assertEqual(attachment_url_image[:11], '/web/image/')

        url = '%s/requests/new/step/data' % TEST_URL
        data = {
            'type_id': self.request_type.id,
            'req_text': 'test request with attachment' +
                        attachment_url_image + attachment_url_file,
            'csrf_token': self.get_csrf_token(),
        }
        response = self.opener.post(url=url, data=data)
        self.assertEqual(response.status_code, 200)

        test_request = self.env['request.request'].search(
            [('request_text', 'like', 'test request with attachment')],
            limit=1)
        self.assertEqual(len(test_request), 1)

        attachments = self.env['ir.attachment'].search(
            [('res_model', '=', 'request.request'),
             ('res_id', '=', test_request.id)])
        self.assertEqual(len(attachments), 2)
