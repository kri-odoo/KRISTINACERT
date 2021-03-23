import logging
from psycopg2 import IntegrityError

from odoo import exceptions
from odoo.tools.misc import mute_logger

from .common import RequestCase, freeze_time
from ..models.request_request import html2text

_logger = logging.getLogger(__name__)


class TestRequestBase(RequestCase):
    """Test request base
    """

    def test_090_type_counters(self):
        access_type = self.env.ref(
            'generic_request.request_type_access')
        self.assertEqual(access_type.stage_count, 4)
        self.assertEqual(access_type.route_count, 3)

    def test_100_stage_previous_stage_ids(self):
        self.assertEqual(
            self.stage_draft.previous_stage_ids,
            self.stage_rejected)
        self.assertEqual(
            self.stage_sent.previous_stage_ids,
            self.stage_draft)
        self.assertEqual(
            self.stage_confirmed.previous_stage_ids,
            self.stage_sent)
        self.assertEqual(
            self.stage_rejected.previous_stage_ids,
            self.stage_sent)

    def test_110_stage_route_display_name_noname(self):
        self.route_draft_to_sent.name = False
        self.non_ascii_route_draft_to_sent.name = False

        self.assertEqual(
            self.route_draft_to_sent.display_name,
            "Draft -> Sent")

        self.assertEqual(
            self.non_ascii_route_draft_to_sent.display_name,
            u"Чорновик -> Відправлено")

    def test_115_stage_route_display_name_name(self):
        self.assertEqual(
            self.route_draft_to_sent.display_name,
            "Draft -> Sent [Send]")

    def test_117_stage_route_display_name_name_only(self):
        self.assertEqual(
            self.route_draft_to_sent.with_context(name_only=True).display_name,
            "Send")

    def test_117_stage_route_display_name_name_only_no_name(self):
        self.route_draft_to_sent.name = False
        self.assertEqual(
            self.route_draft_to_sent.with_context(name_only=True).display_name,
            "Draft -> Sent")

    def test_120_route_ensure_route__draft_sent(self):
        Route = self.env['request.stage.route']
        route = Route.ensure_route(
            self.request_1, self.stage_sent.id)
        self.assertTrue(route)
        self.assertEqual(len(route), 1)

    def test_125_route_ensure_route__draft_confirmed(self):
        Route = self.env['request.stage.route']

        with self.assertRaises(exceptions.ValidationError):
            Route.ensure_route(self.request_1, self.stage_confirmed.id)

    def test_130_request_create_simple(self):
        Request = self.env['request.request']

        request = Request.create({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'request_text': 'Request Text',
        })

        self.assertTrue(request.name.startswith('Req-'))
        self.assertEqual(request.stage_id, self.stage_draft)

    def test_135_request_create_and_assign(self):
        Request = self.env['request.request']

        request = Request.create({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'request_text': 'Request Text',
            'user_id': self.request_manager.id,
        })

        self.assertEqual(request.user_id, self.request_manager)
        self.assertTrue(request.date_assigned)

    def test_140_request_write_stage_sent(self):
        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        self.request_1.write({'stage_id': self.stage_sent.id})

        self.assertEqual(self.request_1.stage_id, self.stage_sent)

    def test_145_request_write_stage_confirmed(self):
        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        with self.assertRaises(exceptions.ValidationError):
            self.request_1.write({'stage_id': self.stage_confirmed.id})

    def test_150_request_type_sequence(self):
        Request = self.env['request.request']

        request = Request.create({
            'type_id': self.sequence_type.id,
            'category_id': self.resource_category.id,
            'request_text': 'Request Text',
        })

        self.assertTrue(request.name.startswith('RSR-'))
        self.assertEqual(request.stage_id, self.stage_new)

    def test_155_request__type_changed(self):
        Request = self.env['request.request']

        # Create new (empty) request
        request = Request.new({})
        self.assertFalse(request.stage_id)
        self.assertFalse(request.type_id)

        # Run onchange type_id:
        request.onchange_type_id()
        self.assertFalse(request.stage_id)
        self.assertFalse(request.type_id)

        request.type_id = self.simple_type
        self.assertFalse(request.stage_id)
        self.assertEqual(request.type_id, self.simple_type)

        request.onchange_type_id()
        self.assertEqual(request.stage_id, self.stage_draft)
        self.assertEqual(request.type_id, self.simple_type)

    def test_157_request__category_changed_restricts_type(self):
        Request = self.env['request.request']

        category_tech = self.env.ref(
            'generic_request.request_category_demo_technical_configuration')
        category_resource = self.env.ref(
            'generic_request.request_category_demo_resource')

        # Create new (empty) request
        request = Request.new({})
        self.assertFalse(request.stage_id)
        self.assertFalse(request.type_id)

        request.onchange_type_id()

        res = request._onchange_category_type()
        self.assertFalse(request.stage_id)
        self.assertFalse(request.type_id)
        self.assertFalse(request.category_id)

        # Choose category Demo / Technical / Configuration
        request.category_id = category_tech
        res = request._onchange_category_type()
        self.assertTrue(request.category_id)
        self.assertEqual(
            res['domain']['type_id'],
            [('category_ids', '=', category_tech.id),
             ('start_stage_id', '!=', False)])
        self.assertIn(self.access_type, category_tech.request_type_ids)
        self.assertEqual(request.category_id, category_tech)

        # Choose request type 'Grant Access'
        request.type_id = self.access_type
        request.onchange_type_id()
        self.assertEqual(request.type_id, self.access_type)
        self.assertEqual(request.stage_id, self.access_type.start_stage_id)

        # Trigger onchange categ_type, ensure type no changed
        res = request._onchange_category_type()
        self.assertEqual(request.type_id, self.access_type)

        # Choose category Demo / Resource
        request.category_id = category_resource
        self.assertNotIn(self.access_type, category_resource.request_type_ids)

        # Trigger onchanges, ensure type set to False
        res = request._onchange_category_type()
        request.onchange_type_id()
        self.assertFalse(request.type_id)
        self.assertFalse(request.stage_id)
        self.assertEqual(request.category_id, category_resource)
        self.assertEqual(
            res['domain']['type_id'],
            [('category_ids', '=', category_resource.id),
             ('start_stage_id', '!=', False)])

        # Choose type 'Printer Request'
        request.type_id = self.sequence_type
        request.onchange_type_id()
        self.assertEqual(request.type_id, self.sequence_type)
        self.assertEqual(request.stage_id, self.sequence_type.start_stage_id)
        self.assertIn(self.sequence_type, category_resource.request_type_ids)

        # Trigger onchange categ_type, ensure type no changed
        res = request._onchange_category_type()
        self.assertEqual(request.type_id, self.sequence_type)

    def test_160_request_category_display_name(self):
        self.assertEqual(
            self.tec_configuration_category.display_name,
            u"Demo / Technical / Configuration")

    def test_170_request_type_category_change(self):
        request = self.env['request.request'].create({
            'type_id': self.simple_type.id,
            'category_id': self.resource_category.id,
            'request_text': 'test',
        })

        with self.assertRaises(exceptions.ValidationError):
            request.write({'type_id': self.sequence_type.id})

        # Change category
        request.write({'category_id': self.tec_configuration_category.id})
        last_event = request.request_event_ids.sorted()[0]
        self.assertEqual(last_event.event_code, 'category-changed')
        self.assertEqual(last_event.old_category_id, self.resource_category)
        self.assertEqual(
            last_event.new_category_id, self.tec_configuration_category)

    def test_180_request_close_via_wizard(self):
        request = self.env.ref(
            'generic_request.request_request_type_sequence_demo_1')
        request.stage_id = self.env.ref(
            'generic_request.request_stage_type_sequence_sent')

        close_stage = self.env.ref(
            'generic_request.request_stage_type_sequence_closed')
        close_route = self.env.ref(
            'generic_request.request_stage_route_type_sequence_sent_to_closed')

        request.response_text = 'test response 1'

        request_closing = self.env['request.wizard.close'].create({
            'request_id': request.id,
            'close_route_id': close_route.id,
        })
        request_closing.onchange_request_id()
        self.assertEqual(request_closing.response_text, request.response_text)
        self.assertEqual(request_closing.response_text,
                         '<p>test response 1</p>')

        request_closing.close_route_id = close_route
        request_closing.response_text = 'test response 42'
        request_closing.action_close_request()

        self.assertEqual(request.stage_id, close_stage)
        self.assertEqual(request.response_text, '<p>test response 42</p>')

    def test_request_html2text(self):
        self.assertEqual(html2text(False), "")
        self.assertEqual(html2text(None), "")
        self.assertEqual(
            html2text("<h1>Test</h1>").strip(), "# Test")

    def test_190_type_default_stages(self):
        type_default_stages = self.env['request.type'].with_context(
            create_default_stages=True).create({
                'name': "test-default-stages",
                'code': "test-default-stages",
            })
        self.assertEqual(type_default_stages.route_count, 1)
        self.assertEqual(
            type_default_stages.route_ids.stage_from_id.name, 'New')
        self.assertEqual(
            type_default_stages.route_ids.stage_to_id.name, 'Closed')

    def test_200_type_no_default_stages(self):
        type_no_default_stages = self.env['request.type'].create({
            'name': "test-no-default-stages",
            'code': "test-no-default-stages",
        })
        self.assertEqual(type_no_default_stages.route_count, 0)
        self.assertEqual(len(type_no_default_stages.stage_ids), 0)

        with self.assertRaises(exceptions.ValidationError):
            self.env['request.request'].create({
                'type_id': type_no_default_stages.id,
                'request_text': 'test',
            })

    def test_210_test_kaban_readonly_fields(self):
        res = self.env['request.request'].fields_view_get(view_type='kanban')
        self.assertTrue(res['fields']['type_id']['readonly'])
        self.assertTrue(res['fields']['stage_id']['readonly'])
        self.assertTrue(res['fields']['category_id']['readonly'])

    def test_220_delete_stage_with_routes(self):
        with self.assertRaises(exceptions.ValidationError):
            self.stage_confirmed.unlink()

    def test_230_delete_stage_without_routes(self):
        stage = self.env['request.stage'].create({
            'name': 'Test',
            'code': 'test',
            'request_type_id': self.simple_type.id,
        })
        stage.unlink()  # no errors raised

    def test_240_request_events(self):
        with freeze_time('2018-07-09'):
            request = self.env['request.request'].create({
                'type_id': self.simple_type.id,
                'request_text': 'Test',
            })
            self.assertEqual(request.request_event_count, 1)
            self.assertEqual(
                request.request_event_ids.event_type_id.code, 'created')

        with freeze_time('2018-07-25'):
            # Change request text
            request.request_text = 'Test 42'

            # Refresh cache. This is required to read request_event_ids in
            # correct order
            request.refresh()

            # Check that new event generated
            self.assertEqual(request.request_event_count, 2)
            self.assertEqual(
                request.request_event_ids[0].event_type_id.code, 'changed')
            self.assertEqual(
                request.request_event_ids[0].old_text, '<p>Test</p>')
            self.assertEqual(
                request.request_event_ids[0].new_text, '<p>Test 42</p>')

            # Test autovacuum of events (by default 90 days old)
            # No events removed, date not changed
            cron_job = self.env.ref(
                'generic_request.ir_cron_request_vacuum_events')
            cron_job.method_direct_trigger()
            self.assertEqual(request.request_event_count, 2)

        with freeze_time('2018-08-09'):
            # Test autovacuum of events (by default 90 days old)
            # No events removed, events not older that 90 days
            cron_job = self.env.ref(
                'generic_request.ir_cron_request_vacuum_events')
            cron_job.method_direct_trigger()
            self.assertEqual(request.request_event_count, 2)

        with freeze_time('2018-10-19'):
            # Test autovacuum of events (by default 90 days old)
            # One events removed, created event is older that 90 days
            cron_job = self.env.ref(
                'generic_request.ir_cron_request_vacuum_events')
            cron_job.method_direct_trigger()
            self.assertEqual(request.request_event_count, 1)
            self.assertEqual(
                request.request_event_ids.event_type_id.code, 'changed')
            self.assertEqual(
                request.request_event_ids.old_text, '<p>Test</p>')
            self.assertEqual(
                request.request_event_ids.new_text, '<p>Test 42</p>')

        request.created_by_id.company_id.request_event_auto_remove = False

        with freeze_time('2018-10-27'):
            # Test autovacuum of events (by default 90 days old)
            # All events removed, all events older that 90 days
            cron_job = self.env.ref(
                'generic_request.ir_cron_request_vacuum_events')
            cron_job.method_direct_trigger()
            self.assertEqual(request.request_event_count, 1)

        with freeze_time('2018-12-27'):
            # Test autovacuum of events (by default 90 days old)
            # All events removed, all events older that 90 days
            cron_job = self.env.ref(
                'generic_request.ir_cron_request_vacuum_events')
            cron_job.method_direct_trigger()
            self.assertEqual(request.request_event_count, 1)

        request.created_by_id.company_id.request_event_auto_remove = True

        with freeze_time('2018-12-27'):
            # Test autovacuum of events (by default 90 days old)
            # All events removed, all events older that 90 days
            cron_job = self.env.ref(
                'generic_request.ir_cron_request_vacuum_events')
            cron_job.method_direct_trigger()
            self.assertEqual(request.request_event_count, 0)

    def test_250_request_create_simple_without_channel(self):
        Request = self.env['request.request']
        channel_other = self.env.ref('generic_request.request_channel_other')

        request = Request.create({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'request_text': 'Request Text',
        })

        self.assertEqual(request.channel_id, channel_other)

    def test_260_request_create_simple_with_channel_call(self):
        Request = self.env['request.request']
        channel_call = self.env.ref('generic_request.request_channel_call')

        request = Request.create({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'request_text': 'Request Text',
            'channel_id': channel_call.id,
        })

        self.assertEqual(request.channel_id, channel_call)

    def test_request_priority_changed_event_created(self):
        request = self.env['request.request'].create({
            'type_id': self.simple_type.id,
            'request_text': 'Test priority event',
        })
        self.assertEqual(request.request_event_count, 1)
        self.assertEqual(
            request.request_event_ids.event_type_id.code, 'created')

        # change priority
        request.priority = '4'

        # ensure event priority-changed created
        self.assertEqual(request.request_event_count, 2)
        self.assertSetEqual(
            set(request.request_event_ids.mapped('event_type_id.code')),
            {'created', 'priority-changed'})

    def test_unlink_just_created(self):
        request = self.env['request.request'].with_user(
            self.request_manager
        ).create({
            'type_id': self.simple_type.id,
            'request_text': 'test',
        })
        with self.assertRaises(exceptions.AccessError):
            request.unlink()

        # Managers with group *can delete requests* are allowed to delete
        # requests
        self.request_manager.groups_id |= self.env.ref(
            'generic_request.group_request_manager_can_delete_request')
        request.unlink()

    def test_unlink_processed(self):
        request = self.env['request.request'].with_user(
            self.request_manager
        ).create({
            'type_id': self.simple_type.id,
            'request_text': 'test',
        })
        request.request_text = 'test 42'
        request.user_id = self.request_manager

        with self.assertRaises(exceptions.AccessError):
            request.unlink()

        # Managers with group *can delete requests* are allowed to delete
        # requests
        self.request_manager.groups_id |= self.env.ref(
            'generic_request.group_request_manager_can_delete_request')
        request.unlink()

    def test_request_can_change_category(self):
        self.assertEqual(self.request_1.stage_id, self.stage_draft)
        self.assertTrue(self.request_1.can_change_category)

        # move request to sent stage
        self.request_1.stage_id = self.stage_sent

        # Check that changing category not allowed
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertFalse(self.request_1.can_change_category)

    def test_request_can_change_deadline(self):
        self.assertEqual(self.request_1.stage_id, self.stage_draft)
        self.assertTrue(self.request_1.can_change_deadline)

        # move request to sent stage
        self.request_1.stage_id = self.stage_sent

        # Check that changing deadline is allowed
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertTrue(self.request_1.can_change_deadline)

        # move request to confirmed stage
        self.request_1.stage_id = self.stage_confirmed

        # Check that changing deadline not allowed
        self.assertEqual(self.request_1.stage_id, self.stage_confirmed)
        self.assertFalse(self.request_1.can_change_deadline)

    def test_request_create_new_stage(self):
        stage = self.env['request.stage'].create({
            'request_type_id': self.simple_type.id,
            'name': 'Test',
            'code': 'test',
        })
        # Ensure that new stage is last stage
        self.assertEqual(stage, self.simple_type.stage_ids.sorted()[-1])

    def test_request_create_new_stage_with_sequence(self):
        stage = self.env['request.stage'].create({
            'request_type_id': self.simple_type.id,
            'name': 'Test',
            'code': 'test',
            'sequence': 0,
        })
        # Ensure that new stage is first stage
        self.assertEqual(stage, self.simple_type.stage_ids.sorted()[0])

    def test_request_create_first_stage(self):
        rtype = self.env['request.type'].with_context(
            create_default_stages=False,
        ).create({
            'name': 'Test Request Stages',
            'code': 'rest-request-stages',
        })

        self.assertFalse(rtype.stage_ids)

        # Create new stage
        stage = self.env['request.stage'].create({
            'request_type_id': rtype.id,
            'name': 'Test',
            'code': 'Test',
        })
        self.assertEqual(stage.sequence, 5)

    def test_request_suggested_recipients(self):
        author = self.env.ref('base.res_partner_address_7')
        partner = self.env.ref('base.res_partner_4')

        request = self.env.ref(
            'generic_request.request_request_type_simple_demo_3')

        # Check that author is auto subscribed, but partner is not subscribed
        self.assertIn(author, request.message_partner_ids)
        self.assertNotIn(partner, request.message_partner_ids)

        # By default suggestion for partner disabled, thus no partner
        # have to be suggested
        result = request._message_get_suggested_recipients()[request.id]
        partner_ids = [r[0] for r in result]
        self.assertFalse(partner_ids)

        # Enable suggestion for partner
        self.env.user.company_id.request_mail_suggest_partner = True

        result = request._message_get_suggested_recipients()[request.id]
        partner_ids = [r[0] for r in result]
        self.assertEqual(len(partner_ids), 1)

        # Ensure that partner is in suggested recipients
        self.assertNotIn(author.id, partner_ids)
        self.assertIn(partner.id, partner_ids)

        request.message_subscribe(partner_ids=partner.ids)

        # Ensure that after we subscribe partner it disappears from suggested
        # list
        result = request._message_get_suggested_recipients()[request.id]
        partner_ids = [r[0] for r in result]
        self.assertFalse(partner_ids)

    def test_request_creation_template(self):
        request = self.creation_template.do_create_request({})
        self.assertEqual(
            request.category_id, self.creation_template.request_category_id)
        self.assertEqual(
            request.type_id, self.creation_template.request_type_id)
        self.assertEqual(
            request.request_text, self.creation_template.request_text)

    def test_request_kind_menuitem_toggle(self):
        self.assertFalse(self.request_kind.menuitem_toggle)
        self.assertFalse(self.request_kind.menuitem_name)
        self.assertFalse(self.request_kind.menuaction_name)

        # toggle (enable) menuitem button
        self.request_kind.menuitem_toggle = True

        self.assertTrue(self.request_kind.menuitem_id)
        self.assertTrue(self.request_kind.menuaction_id)
        self.assertEqual(
            self.request_kind.menuitem_name, self.request_kind.name
        )
        self.assertEqual(
            self.request_kind.menuaction_name, self.request_kind.name
        )

    def test_default_request_text(self):
        request = self.env['request.request'].new({
            'type_id': self.access_type.id,
            'category_id': self.tec_configuration_category.id,
            'user_id': self.request_manager.id,
        })
        self.assertFalse(request.request_text)

        request.onchange_type_id()

        self.assertEqual(request.request_text,
                         request.type_id.default_request_text)

    def test_default_response_text(self):
        request = self.request_2

        close_route = self.env.ref(
            'generic_request.request_stage_route_type_access_sent_to_rejected')
        close_stage = self.env.ref(
            'generic_request.request_stage_route_type_access_sent_to_rejected')

        request.stage_id = close_stage.id

        request_closing = self.env['request.wizard.close'].create({
            'request_id': request.id,
            'close_route_id': close_route.id,
        })
        self.assertFalse(request_closing.response_text)

        request_closing.onchange_close_route_id()

        self.assertEqual(request_closing.response_text,
                         close_route.default_response_text)

        request_closing.action_close_request()

        self.assertTrue(request.closed)

        self.assertEqual(request.response_text,
                         close_route.default_response_text)

        # toggle (disable) menuitem button
        self.request_kind.menuitem_toggle = False

        action = self.request_kind.menuaction_id

        self.assertFalse(self.request_kind.menuitem_id)
        self.assertFalse(self.request_kind.menuaction_id)

        self.assertFalse(action.exists())

    def test_complex_priority(self):
        test_request = self.env.ref(
            'generic_request.demo_request_with_complex_priority')

        # test complex priority
        self.assertEqual(test_request.priority, '2')

        # change impact and urgency
        test_request.impact = '0'
        test_request.urgency = '1'

        # test complex priority calculation
        self.assertEqual(test_request.priority, '1')

        event = self.env['request.event'].search(
            [('request_id', '=', test_request.id)])
        self.assertEqual(event[0].event_code, 'urgency-changed')
        self.assertEqual(event[1].event_code, 'priority-changed')
        self.assertEqual(event[2].event_code, 'impact-changed')
        self.assertEqual(event[3].event_code, 'priority-changed')

    def test_deadline_state_1(self):
        self.request_1.deadline_date = '2020-03-17'

        with freeze_time('2020-03-16'):
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'ok')

        with freeze_time('2020-03-17'):
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'today')

        with freeze_time('2020-03-18'):
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'overdue')

    def test_deadline_state_2(self):
        self.request_1.deadline_date = '2020-03-17'

        with freeze_time('2020-03-16'):
            self.request_1.stage_id = self.stage_sent
            self.request_1.stage_id = self.stage_confirmed
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'ok')

        with freeze_time('2020-03-18'):
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'ok')

    def test_deadline_state_3(self):
        self.request_1.deadline_date = '2020-03-17'

        with freeze_time('2020-03-17'):
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'today')

            self.request_1.stage_id = self.stage_sent
            self.request_1.stage_id = self.stage_confirmed
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'ok')

        with freeze_time('2020-03-18'):
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'ok')

    def test_deadline_state_4(self):
        self.request_1.deadline_date = '2020-03-17'

        with freeze_time('2020-03-18'):
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'overdue')

            self.request_1.stage_id = self.stage_sent
            self.request_1.stage_id = self.stage_confirmed
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'overdue')

        with freeze_time('2020-03-19'):
            self.request_1.invalidate_cache()
            self.assertEqual(self.request_1.deadline_state, 'overdue')

    @mute_logger('odoo.sql_db')
    def test_20_request_type_name_uniq(self):
        Model = self.env['request.type']

        # Test name uniq constraint
        data1 = dict(code='TEST-CODE-1', name='Test Type Name 42')
        data2 = dict(code='TEST-CODE-2', name='Test Type Name 42')

        Model.create(dict(data1))
        with self.assertRaises(IntegrityError):
            Model.create(dict(data2))

    @mute_logger('odoo.sql_db')
    def test_30_request_type_code_uniq(self):
        Model = self.env['request.type']

        # Test code uniq constraints
        data1 = dict(code='TEST-CODE-4', name='Test Type Name 44')
        data2 = dict(code='TEST-CODE-4', name='Test Type Name 45')

        Model.create(dict(data1))
        with self.assertRaises(IntegrityError):
            Model.create(dict(data2))

    @mute_logger('odoo.sql_db')
    def test_40_request_type_code_ascii(self):
        Model = self.env['request.type']

        # Test code uniq constraints
        data1 = dict(code='TEST-CODE-4', name='Test Type Name 44')
        data2 = dict(code='Тестовий-код-5', name='Test Type Name 45')

        Model.create(dict(data1))
        with self.assertRaises(IntegrityError):
            Model.create(dict(data2))
