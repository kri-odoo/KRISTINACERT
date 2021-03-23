from odoo import models, fields, api


class RequestWizardStopWork(models.TransientModel):
    _name = 'request.wizard.stop.work'
    _description = 'Request Wizard: Stop Work'

    timesheet_line_id = fields.Many2one(
        'request.timesheet.line', required=True)
    date_start = fields.Datetime(
        related='timesheet_line_id.date_start', readonly=True)
    request_id = fields.Many2one(
        'request.request', related='timesheet_line_id.request_id',
        readonly=True)
    request_type_id = fields.Many2one(
        'request.type', related='timesheet_line_id.request_id.type_id',
        readonly=True, string="Request Type")
    request_text_sample = fields.Text(
        related='timesheet_line_id.request_id.request_text_sample',
        readonly=True)
    activity_id = fields.Many2one(
        'request.timesheet.activity', required=True, ondelete='cascade')
    amount = fields.Float(required=True)
    description = fields.Text()

    @api.model
    def default_get(self, fields_list):
        res = super(RequestWizardStopWork, self).default_get(fields_list)

        if res.get('timesheet_line_id') and 'amount' in fields_list:
            line = self.env['request.timesheet.line'].browse(
                res['timesheet_line_id'])
            start = fields.Datetime.from_string(line.date_start)
            end = fields.Datetime.from_string(fields.Datetime.now())
            amount_seconds = (end - start).total_seconds()

            if amount_seconds <= 60:
                # Ensure minimal amount is 1 minute
                amount_seconds = 61

            res.update({
                'amount': amount_seconds / 3600,
            })

        return res

    def _prepare_timesheet_line_data(self):
        return {
            'amount': self.amount,
            'activity_id': self.activity_id.id,
            'description': self.description,
        }

    def do_stop_work(self):
        self.ensure_one()

        self.timesheet_line_id.write(
            self._prepare_timesheet_line_data()
        )
        self.request_id.trigger_event('timetracking-stop-work', {
            'timesheet_line_id': self.timesheet_line_id.id,
        })

        if self.env.context.get('request_timesheet_start_request_id'):
            self.env['request.request'].browse(
                self.env.context.get('request_timesheet_start_request_id')
            ).action_start_work()
