from odoo import models, fields


class GenericTagCategory(models.Model):
    _inherit = "generic.tag.category"

    # technical field to be used in tag domain on request form
    request_type_ids = fields.Many2many(
        'request.type', 'request_type_tag_category_rel',
        'category_id', 'type_id', string='Request Types', readonly=True)
