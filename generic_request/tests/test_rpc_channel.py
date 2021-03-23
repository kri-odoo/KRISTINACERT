from odoo.tests import common
from odoo.addons.generic_mixin.tests.common import TEST_URL


@common.tagged('post_install', '-at_install')
class TestRequestChannelRPC(common.HttpCase):

    def setUp(self):
        super(TestRequestChannelRPC, self).setUp()
        self.admin_uid = self.env.ref('base.user_admin').id
        self.db_name = common.get_db_name()

        self.simple_type = self.env.ref('generic_request.request_type_simple')

        self.channel_api = self.env.ref('generic_request.request_channel_api')
        self.channel_call = self.env.ref(
            'generic_request.request_channel_call')

    def test_xmlrpc_request_create(self):
        request_id = self.xmlrpc_object.execute_kw(
            self.db_name, self.admin_uid, 'admin',
            'request.request', 'create', [{
                'type_id': self.simple_type.id,
                'request_text': 'Text',
            }])

        request = self.env['request.request'].browse(request_id)
        self.assertEqual(request.channel_id, self.channel_api)

    def test_xmlrpc_request_create_specific_channel(self):
        request_id = self.xmlrpc_object.execute_kw(
            self.db_name, self.admin_uid, 'admin',
            'request.request', 'create', [{
                'type_id': self.simple_type.id,
                'request_text': 'Text',
                'channel_id': self.channel_call.id,
            }])

        request = self.env['request.request'].browse(request_id)
        self.assertEqual(request.channel_id, self.channel_call)

    def test_jsonrpc_request_create(self):
        response = self.opener.post(
            "%s/jsonrpc" % TEST_URL,
            json={
                'jsonrpc': '2.0',
                'id': None,
                'method': 'call',
                'params': {
                    'service': 'object',
                    'method': 'execute_kw',
                    'args': [
                        self.db_name,
                        self.admin_uid,
                        'admin',
                        'request.request',
                        'create',
                        [{
                            'type_id': self.simple_type.id,
                            'request_text': 'Text',
                        }]
                    ],
                }})
        request_id = response.json()['result']

        request = self.env['request.request'].browse(request_id)
        self.assertEqual(request.channel_id, self.channel_api)

    def test_jsonrpc_request_create_specific_channel(self):
        response = self.opener.post(
            "%s/jsonrpc" % TEST_URL,
            json={
                'jsonrpc': '2.0',
                'id': None,
                'method': 'call',
                'params': {
                    'service': 'object',
                    'method': 'execute_kw',
                    'args': [
                        self.db_name,
                        self.admin_uid,
                        'admin',
                        'request.request',
                        'create',
                        [{
                            'type_id': self.simple_type.id,
                            'request_text': 'Text',
                            'channel_id': self.channel_call.id,
                        }]
                    ],
                }})
        request_id = response.json()['result']

        request = self.env['request.request'].browse(request_id)
        self.assertEqual(request.channel_id, self.channel_call)
