from odoo import models, fields


class RequestTimesheetActivity(models.Model):
    _name = 'request.timesheet.activity'
    _description = 'Request Timesheet Activity'
    _order = 'name'
    _inherit = [
        'generic.mixin.name_with_code',
        'generic.mixin.uniq_name_code',
    ]

    name = fields.Char(translate=True, index=True, required=True)
    code = fields.Char()
    description = fields.Text(translate=True)
    active = fields.Boolean(index=True, default=True)
    color = fields.Integer()

    # Technical field to find activities allowed for this request type
    request_type_ids = fields.Many2many(
        comodel_name='request.type',
        relation='request_type__timesheet_activity__rel',
        column1='activity_id',
        column2='request_type_id')
