from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    request_event_live_time = fields.Integer(default=90)
    request_event_live_time_uom = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')], default='days', ondelete='set default')
    request_event_auto_remove = fields.Boolean(
        string='Automatically remove events older then',
        default=True)

    request_mail_suggest_partner = fields.Boolean(
        string="Suggest request partner for mail recipients")
