from odoo import models, fields


class RequestWizardAssign(models.TransientModel):
    _name = 'request.wizard.assign'
    _description = 'Request Wizard: Assign'

    def _default_user_id(self):
        return self.env.user

    request_ids = fields.Many2many(
        'request.request', string='Requests', required=True)
    user_id = fields.Many2one(
        'res.users', string="User", default=_default_user_id, required=True)
    partner_id = fields.Many2one(
        'res.partner', related="user_id.partner_id",
        readonly=True, store=False)
    comment = fields.Text()

    def do_assign(self):
        for rec in self:
            rec.request_ids.ensure_can_assign()
            rec.request_ids.with_context(
                assign_comment=rec.comment).write({
                    'user_id': rec.user_id.id,
                })
            if rec.comment:
                for request in rec.request_ids:
                    request.message_post(body=rec.comment)
