from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class RequestCategory(models.Model):
    _name = "request.category"
    _inherit = [
        'generic.mixin.parent.names',
        'generic.mixin.name_with_code',
        'generic.mixin.track.changes',
        'mail.thread',
    ]
    _description = "Request Category"
    _order = 'sequence, name'

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'

    # Defined in generic.mixin.name_with_code
    name = fields.Char()
    code = fields.Char()

    parent_id = fields.Many2one(
        'request.category', 'Parent', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)

    active = fields.Boolean(default=True, index=True)

    description = fields.Text(translate=True)
    help_html = fields.Html(translate=True)

    # Stat
    request_ids = fields.One2many(
        'request.request', 'category_id', 'Requests', readonly=True)
    request_count = fields.Integer(
        'All Requests', compute='_compute_request_count', readonly=True)
    request_open_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Open Requests")
    request_closed_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Closed Requests")
    # Open requests
    request_open_today_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="New Requests For Today")
    request_open_last_24h_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="New Requests For Last 24 Hour")
    request_open_week_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="New Requests For Week")
    request_open_month_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="New Requests For Month")
    # Closed requests
    request_closed_today_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Closed Requests For Today")
    request_closed_last_24h_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Closed Requests For Last 24 Hour")
    request_closed_week_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Closed Requests For Week")
    request_closed_month_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Closed Requests For Month")
    # Deadline requests
    request_deadline_today_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Deadline Requests For Today")
    request_deadline_last_24h_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Deadline Requests For Last 24 Hour")
    request_deadline_week_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Deadline Requests For Week")
    request_deadline_month_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Deadline Requests For Month")
    # Unassigned requests
    request_unassigned_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Unassigned Requests")

    request_type_ids = fields.Many2many(
        'request.type',
        'request_type_category_rel', 'category_id', 'type_id',
        string="Request types")
    request_type_count = fields.Integer(
        compute='_compute_request_type_count')
    sequence = fields.Integer(index=True, default=5)
    color = fields.Integer()  # for many2many_tags widget

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (parent_id, name)',
         'Category name must be unique.'),
    ]

    @api.depends('request_ids')
    def _compute_request_count(self):
        RequestRequest = self.env['request.request']
        now = datetime.now()
        for record in self:
            record.request_count = len(record.request_ids)
            record.request_closed_count = RequestRequest.search_count([
                ('closed', '=', True),
                ('category_id', '=', record.id)
            ])
            record.request_open_count = RequestRequest.search_count([
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])

            today_start = now.replace(
                hour=0, minute=0, second=0, microsecond=0)
            yesterday = now - relativedelta(days=1)
            week_ago = now - relativedelta(weeks=1)
            month_ago = now - relativedelta(months=1)
            # Open requests
            record.request_open_today_count = RequestRequest.search_count([
                ('date_created', '>=', today_start),
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])
            record.request_open_last_24h_count = RequestRequest.search_count([
                ('date_created', '>', yesterday),
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])
            record.request_open_week_count = RequestRequest.search_count([
                ('date_created', '>', week_ago),
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])
            record.request_open_month_count = RequestRequest.search_count([
                ('date_created', '>', month_ago),
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])
            # Closed requests
            record.request_closed_today_count = RequestRequest.search_count([
                ('date_closed', '>=', today_start),
                ('closed', '=', True),
                ('category_id', '=', record.id)
            ])
            record.request_closed_last_24h_count = (
                RequestRequest.search_count([
                    ('date_closed', '>', yesterday),
                    ('closed', '=', True),
                    ('category_id', '=', record.id)
                ]))
            record.request_closed_week_count = RequestRequest.search_count([
                ('date_closed', '>', week_ago),
                ('closed', '=', True),
                ('category_id', '=', record.id)
            ])
            record.request_closed_month_count = RequestRequest.search_count([
                ('date_closed', '>', month_ago),
                ('closed', '=', True),
                ('category_id', '=', record.id)
            ])
            # Deadline requests
            record.request_deadline_today_count = RequestRequest.search_count([
                ('deadline_date', '>=', today_start),
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])
            record.request_deadline_last_24h_count = (
                RequestRequest.search_count([
                    ('deadline_date', '>', yesterday),
                    ('closed', '=', False),
                    ('category_id', '=', record.id)
                ]))
            record.request_deadline_week_count = RequestRequest.search_count([
                ('deadline_date', '>', week_ago),
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])
            record.request_deadline_month_count = RequestRequest.search_count([
                ('deadline_date', '>', month_ago),
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])
            # Unassigned requests
            record.request_unassigned_count = RequestRequest.search_count([
                ('user_id', '=', False),
                ('category_id', '=', record.id)
            ])

    @api.depends('request_type_ids')
    def _compute_request_type_count(self):
        for record in self:
            record.request_type_count = len(record.request_type_ids)

    def name_get(self):
        # This is required to avoid access rights errors when tracking values
        # in chatter. (At least in Odoo 10.0)
        return super(RequestCategory, self.sudo()).name_get()

    def action_category_request_open_today_count(self):
        self.ensure_one()
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('date_created', '>=', today_start),
                ('closed', '=', False),
                ('category_id', '=', self.id)])

    def action_category_request_open_last_24h_count(self):
        self.ensure_one()
        yesterday = datetime.now() - relativedelta(days=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('date_created', '>', yesterday),
                ('closed', '=', False),
                ('category_id', '=', self.id)])

    def action_category_request_open_week_count(self):
        self.ensure_one()
        week_ago = datetime.now() - relativedelta(weeks=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('date_created', '>', week_ago),
                ('closed', '=', False),
                ('category_id', '=', self.id)])

    def action_category_request_open_month_count(self):
        self.ensure_one()
        month_ago = datetime.now() - relativedelta(months=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('date_created', '>', month_ago),
                ('closed', '=', False),
                ('category_id', '=', self.id)])

    def action_category_request_closed_today_count(self):
        self.ensure_one()
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            context={'search_default_filter_closed': 1},
            domain=[
                ('date_closed', '>=', today_start),
                ('closed', '=', True),
                ('category_id', '=', self.id)])

    def action_category_request_closed_last_24h_count(self):
        self.ensure_one()
        yesterday = datetime.now() - relativedelta(days=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            context={'search_default_filter_closed': 1},
            domain=[
                ('date_closed', '>', yesterday),
                ('closed', '=', True),
                ('category_id', '=', self.id)])

    def action_category_request_closed_week_count(self):
        self.ensure_one()
        week_ago = datetime.now() - relativedelta(weeks=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            context={'search_default_filter_closed': 1},
            domain=[
                ('date_closed', '>', week_ago),
                ('closed', '=', True),
                ('category_id', '=', self.id)])

    def action_category_request_closed_month_count(self):
        self.ensure_one()
        month_ago = datetime.now() - relativedelta(months=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            context={'search_default_filter_closed': 1},
            domain=[
                ('date_closed', '>', month_ago),
                ('closed', '=', True),
                ('category_id', '=', self.id)])

    def action_category_request_deadline_today_count(self):
        self.ensure_one()
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('deadline_date', '>=', today_start),
                ('closed', '=', False),
                ('category_id', '=', self.id)])

    def action_category_request_deadline_last_24h_count(self):
        self.ensure_one()
        yesterday = datetime.now() - relativedelta(days=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('deadline_date', '>', yesterday),
                ('closed', '=', False),
                ('category_id', '=', self.id)])

    def action_category_request_deadline_week_count(self):
        self.ensure_one()
        week_ago = datetime.now() - relativedelta(weeks=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('deadline_date', '>', week_ago),
                ('closed', '=', False),
                ('category_id', '=', self.id)])

    def action_category_request_deadline_month_count(self):
        self.ensure_one()
        month_ago = datetime.now() - relativedelta(months=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('deadline_date', '>', month_ago),
                ('closed', '=', False),
                ('category_id', '=', self.id)])

    def action_category_request_unassigned_count(self):
        self.ensure_one()
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('user_id', '=', False),
                ('category_id', '=', self.id)],
        )
