from datetime import timedelta

from odoo import models, fields, api, _


class RequestTimesheetLine(models.Model):
    _name = 'request.timesheet.line'
    _description = 'Request Timesheet Line'
    _order = 'date DESC, date_start DESC'

    request_id = fields.Many2one(
        'request.request', index=True, required=True,
        ondelete='cascade', readonly=True)
    date = fields.Date(index=True, default=fields.Date.today, required=True)
    date_start = fields.Datetime(index=True)
    date_end = fields.Datetime(
        readonly=True, store=True,
        compute='_compute_date_end')
    user_id = fields.Many2one(
        'res.users', required=True, index=True,
        default=lambda self: self.env.user, ondelete='restrict')
    activity_id = fields.Many2one(
        'request.timesheet.activity', required=False,
        index=True, ondelete='restrict')
    request_type_id = fields.Many2one(
        related='request_id.type_id', store=True, readonly=True)
    amount = fields.Float(required=False, string='Time spent')
    description = fields.Text()

    @api.depends('date_start', 'amount')
    def _compute_date_end(self):
        for record in self:
            if record.date_start and record.amount:
                record.date_end = fields.Datetime.to_string(
                    fields.Datetime.from_string(record.date_start) +
                    timedelta(hours=record.amount))
            else:
                record.date_end = False

    def name_get(self):
        res = []
        for record in self:
            if not record.amount and not record.activity_id:
                name = _("%s [Running]") % record.request_id.display_name
            else:
                name = "%s [%s] (%.2f hours)" % (
                    record.request_id.display_name,
                    record.activity_id.display_name,
                    record.amount or 0.0,
                )
            res += [(record.id, name)]
        return res

    @api.model
    def _get_running_lines_domain(self):
        return [
            ('user_id', '=', self.env.user.id),
            ('date_start', '!=', False),
            ('amount', '=', False),
        ]

    @api.model
    def _find_running_lines(self):
        return self.search(self._get_running_lines_domain())

    def action_edit_wizard(self):
        self.ensure_one()
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_request_wizard_add_timesheet_line',
            context={
                'default_request_id': self.request_id.id,
                'default_activity_id': self.activity_id.id,
                'default_amount': self.amount,
                'default_description': self.description,
                'default_edit_line_id': self.id})
