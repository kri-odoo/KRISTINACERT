from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    request_wsd_public_ui_visibility = fields.Selection(
        selection=[
            ('redirect', 'Redirect to login'),
            ('restrict', 'Restricted UI')
        ],
        default='redirect')
    request_limit_max_text_size = fields.Integer(default=0)
