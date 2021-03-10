import logging
from odoo.tests import HttpCase
from odoo.tools.misc import mute_logger
from odoo.addons.generic_mixin.tests.common import (
    TEST_URL,
    AccessRulesFixMixinMT,
)
from .common import disable_mail_auto_delete

_logger = logging.getLogger(__name__)


class TestRequestMailNotificationLinks(AccessRulesFixMixinMT, HttpCase):

    def setUp(self):
        super(TestRequestMailNotificationLinks, self).setUp()

        self.request_demo_user = self.env.ref(
            'generic_request.user_demo_request')
        self.base_url = TEST_URL
        self.user_root = self.env.ref('base.user_root')

        # Subscribe demo user to printer request
        self.env.ref(
            'generic_request.request_type_sequence'
        ).message_subscribe(self.request_demo_user.partner_id.ids)

    def flush_tracking(self):
        """ Force the creation of tracking values. """
        self.env['base'].flush()
        self.cr.precommit.run()

    @mute_logger('odoo.addons.mail.models.mail_mail',
                 'requests.packages.urllib3.connectionpool',
                 'odoo.models.unlink')
    def test_assign_employee(self):
        request = self.env['request.request'].with_context(
            mail_create_nolog=True,
            mail_notrack=True,
        ).create({
            'type_id': self.env.ref(
                'generic_request.request_type_sequence').id,
            'request_text': 'Test',
        })

        with disable_mail_auto_delete(self.env):
            request.with_context(
                mail_notrack=False,
            ).write({
                'user_id': self.request_demo_user.id,
            })

        assign_messages = self.env['mail.mail'].search([
            ('model', '=', 'request.request'),
            ('res_id', '=', request.id),
            ('body_html', 'ilike',
             '%%/mail/view/request/%s%%' % request.id),
        ])
        self.assertEqual(len(assign_messages), 1)

        self.authenticate(self.request_demo_user.login, 'demo')
        with mute_logger('odoo.addons.base.models.ir_model'):
            # Hide errors about missing menus
            res = self.url_open('/mail/view/request/%s' % request.id)
        self.assertEqual(res.status_code, 200)
        self.assertNotRegex(res.url, r'^%s/web/login.*$' % self.base_url)
        self.assertRegex(
            res.url, r'^%s/web#.*id=%s.*$' % (self.base_url, request.id))

    @mute_logger('odoo.addons.mail.models.mail_mail',
                 'requests.packages.urllib3.connectionpool',
                 'odoo.models.unlink')
    def test_change_employee(self):
        request = self.env['request.request'].with_user(
            self.request_demo_user
        ).with_context(
            mail_create_nolog=True,
            mail_notrack=True,
        ).create({
            'type_id': self.env.ref(
                'generic_request.request_type_sequence').id,
            'request_text': 'Test',
        })
        self.flush_tracking()

        request.message_subscribe(
            partner_ids=self.request_demo_user.partner_id.ids,
            subtype_ids=(
                self.env.ref('mail.mt_comment') +
                self.env.ref(
                    'generic_request.mt_request_stage_changed')
            ).ids)
        self.flush_tracking()
        with disable_mail_auto_delete(self.env):
            request.with_user(self.user_root).with_context(
                mail_notrack=False,
            ).write({
                'stage_id': self.env.ref(
                    'generic_request.'
                    'request_stage_type_sequence_sent').id,
            })
            self.flush_tracking()

        messages = self.env['mail.mail'].search([
            ('model', '=', 'request.request'),
            ('res_id', '=', request.id),
            ('body_html', 'ilike',
             '%%/mail/view/request/%s%%' % request.id),
        ])
        self.flush_tracking()  # TODO: Do we need it here?
        self.assertEqual(len(messages), 1)

        self.authenticate(self.request_demo_user.login, 'demo')
        with mute_logger('odoo.addons.base.models.ir_model'):
            # Hide errors about missing menus
            res = self.url_open('/mail/view/request/%s' % request.id)
        self.assertEqual(res.status_code, 200)
        self.assertNotRegex(res.url, r'^%s/web/login.*$' % self.base_url)
        self.assertRegex(
            res.url, r'^%s/web#.*id=%s.*$' % (self.base_url, request.id))
