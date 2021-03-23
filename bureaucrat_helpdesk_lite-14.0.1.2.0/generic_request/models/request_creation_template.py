from odoo import models, fields


class RequestCreationTemplate(models.Model):
    _name = 'request.creation.template'
    _description = 'Request creation template'
    _order = 'name'

    name = fields.Char(required=True)
    request_category_id = fields.Many2one('request.category')
    request_type_id = fields.Many2one('request.type', required=True)
    request_text = fields.Html()
    active = fields.Boolean(default=True, index=True)

    request_tag_ids = fields.Many2many(
        'generic.tag', string='Request Tags',
        domain=[('model_id.model', '=', 'request.request')],
        help="Assign tags to requests created from this mail source")

    def _prepare_request_data(self):
        """
        :return: dictionary with default request values
        from creation template
        """
        return {
            'category_id': self.request_category_id.id,
            'type_id': self.request_type_id.id,
            'request_text': self.request_text,
            'tag_ids': [(4, t.id) for t in self.request_tag_ids],
        }

    def prepare_request_data(self, values=None):
        """
        :param values: request values dictionary
        :return: dictionary for creation request with default
        values from creation template
        """
        data = self._prepare_request_data()
        if values:
            data.update(values)
        return data

    def do_create_request(self, values):
        data = self.prepare_request_data(values)
        request = self.env['request.request'].create(data)
        return request
