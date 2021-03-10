from odoo import fields
from .common import (
    RequestCase,
    freeze_time
)


class TestWizardLogTime(RequestCase):

    @classmethod
    def setUpClass(cls):
        super(TestWizardLogTime, cls).setUpClass()
        cls.request_type = cls.env.ref(
            'generic_request.request_type_simple')
        cls.activity_id_1 = cls.env.ref(
            'generic_request.request_timesheet_activity_coding')
        cls.activity_id_2 = cls.env.ref(
            'generic_request.request_timesheet_activity_analysis')
        cls.user = cls.env.ref('generic_request.user_demo_request')

    def test_log_time_start_stop(self):
        Timesheet = self.env['request.timesheet.line']

        with freeze_time("2020-01-14 03:00:00"):
            request = self.env['request.request'].create({
                'type_id': self.request_type.id,
                'request_text': 'test request',
            })

            self.assertEqual(len(request.timesheet_line_ids), 0)
            self.assertEqual(request.timesheet_start_status, 'not-started')
            self.assertFalse(Timesheet._find_running_lines())

            request.action_start_work()
            self.assertEqual(request.timesheet_start_status, 'started')
            self.assertEqual(len(request.timesheet_line_ids), 1)
            self.assertEqual(
                request.request_event_ids.sorted()[0].event_code,
                'timetracking-start-work')
            self.assertEqual(
                request.request_event_ids.sorted()[0].timesheet_line_id,
                request.timesheet_line_ids)

            running = Timesheet._find_running_lines()
            self.assertEqual(running.request_id, request)
            self.assertEqual(
                running.date_start,
                fields.Datetime.from_string("2020-01-14 03:00:00"))
            self.assertEqual(
                running.date_end,
                False)
            self.assertEqual(running.amount, 0.0)

        with freeze_time("2020-01-14 05:00:00"):
            action = request.action_stop_work()
            wizard = self.env[action['res_model']].with_context(
                action['context']
            ).create({
                'activity_id': self.activity_id_2.id,
            })
            self.assertEqual(wizard.amount, 2.0)
            wizard.do_stop_work()

            self.assertEqual(len(request.timesheet_line_ids), 1)
            self.assertEqual(request.timesheet_line_ids.amount, 2)
            self.assertEqual(
                request.timesheet_line_ids.date_start,
                fields.Datetime.from_string("2020-01-14 03:00:00"))
            self.assertEqual(
                request.timesheet_line_ids.date_end,
                fields.Datetime.from_string("2020-01-14 05:00:00"))
            self.assertEqual(
                request.request_event_ids.sorted()[0].event_code,
                'timetracking-stop-work')
            self.assertEqual(
                request.request_event_ids.sorted()[0].timesheet_line_id,
                request.timesheet_line_ids)

    def test_log_time_start_stop_running(self):
        # Start work on request when another request is already running
        Timesheet = self.env['request.timesheet.line']
        request = self.env['request.request'].create({
            'type_id': self.request_type.id,
            'request_text': 'test request',
        })

        self.assertEqual(len(request.timesheet_line_ids), 0)
        self.assertEqual(request.timesheet_start_status, 'not-started')
        self.assertFalse(Timesheet._find_running_lines())

        with freeze_time("2020-01-14 03:00:00"):
            action = request.action_start_work()
            self.assertFalse(action)
            self.assertEqual(request.timesheet_start_status, 'started')
            self.assertEqual(len(request.timesheet_line_ids), 1)

            running = Timesheet._find_running_lines()
            self.assertEqual(running.request_id, request)
            self.assertEqual(
                running.date_start,
                fields.Datetime.from_string("2020-01-14 03:00:00"))
            self.assertEqual(
                running.date_end,
                False)
            self.assertEqual(running.amount, 0.0)

        with freeze_time("2020-01-14 05:00:00"):
            request2 = self.env['request.request'].create({
                'type_id': self.request_type.id,
                'request_text': 'test request',
            })

            self.assertEqual(len(request2.timesheet_line_ids), 0)
            self.assertEqual(request2.timesheet_start_status, 'not-started')
            self.assertTrue(Timesheet._find_running_lines())
            self.assertEqual(running.request_id, request)

            action = request2.action_start_work()
            self.assertEqual(action['res_model'], 'request.wizard.stop.work')
            wizard = self.env[action['res_model']].with_context(
                action['context']
            ).create({
                'activity_id': self.activity_id_2.id,
            })
            self.assertEqual(wizard.amount, 2.0)
            self.assertEqual(wizard.request_id, request)
            wizard.do_stop_work()

            # Ensure that work stopped on previous request
            self.assertEqual(len(request.timesheet_line_ids), 1)
            self.assertEqual(request.timesheet_line_ids.amount, 2)
            self.assertEqual(
                request.timesheet_line_ids.date_start,
                fields.Datetime.from_string("2020-01-14 03:00:00"))
            self.assertEqual(
                request.timesheet_line_ids.date_end,
                fields.Datetime.from_string("2020-01-14 05:00:00"))

            # Ensure that new request have a running timesheet line
            self.assertEqual(request2.timesheet_start_status, 'started')
            self.assertEqual(len(request2.timesheet_line_ids), 1)

            running = Timesheet._find_running_lines()
            self.assertEqual(running.request_id, request2)
            self.assertEqual(
                running.date_start,
                fields.Datetime.from_string("2020-01-14 05:00:00"))
            self.assertEqual(
                running.date_end,
                False)
            self.assertEqual(running.amount, 0.0)
