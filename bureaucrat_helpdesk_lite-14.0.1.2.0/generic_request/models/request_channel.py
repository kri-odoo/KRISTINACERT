import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class RequestChannel(models.Model):
    _name = "request.channel"
    _description = "Request Channel"
    _inherit = [
        'generic.mixin.name_with_code',
        'generic.mixin.uniq_name_code',
        'generic.mixin.track.changes',
    ]
    _order = 'name, id'

    name = fields.Char(required=True, index=True)
    code = fields.Char()
    active = fields.Boolean(default=True, index=True)

    request_ids = fields.One2many(
        'request.request', 'kind_id', string='Requests')
    request_count = fields.Integer(
        compute='_compute_request_count', readonly=True)

    request_open_count = fields.Integer(
        compute="_compute_request_count", readonly=True)
    request_closed_count = fields.Integer(
        compute="_compute_request_count", readonly=True)
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

    @api.depends('request_ids')
    def _compute_request_count(self):
        RequestRequest = self.env['request.request']
        now = datetime.now()
        for record in self:
            record.request_count = len(record.request_ids)
            record.request_closed_count = RequestRequest.search_count([
                ('closed', '=', True),
                ('channel_id', '=', record.id)
            ])
            record.request_open_count = RequestRequest.search_count([
                ('closed', '=', False),
                ('channel_id', '=', record.id)
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
                ('channel_id', '=', record.id)
            ])
            record.request_open_last_24h_count = RequestRequest.search_count([
                ('date_created', '>', yesterday),
                ('closed', '=', False),
                ('channel_id', '=', record.id)
            ])
            record.request_open_week_count = RequestRequest.search_count([
                ('date_created', '>', week_ago),
                ('closed', '=', False),
                ('channel_id', '=', record.id)
            ])
            record.request_open_month_count = RequestRequest.search_count([
                ('date_created', '>', month_ago),
                ('closed', '=', False),
                ('channel_id', '=', record.id)
            ])
            # Closed requests
            record.request_closed_today_count = RequestRequest.search_count([
                ('date_closed', '>=', today_start),
                ('closed', '=', True),
                ('channel_id', '=', record.id)
            ])
            record.request_closed_last_24h_count = (
                RequestRequest.search_count([
                    ('date_closed', '>', yesterday),
                    ('closed', '=', True),
                    ('channel_id', '=', record.id)
                ]))
            record.request_closed_week_count = RequestRequest.search_count([
                ('date_closed', '>', week_ago),
                ('closed', '=', True),
                ('channel_id', '=', record.id)
            ])
            record.request_closed_month_count = RequestRequest.search_count([
                ('date_closed', '>', month_ago),
                ('closed', '=', True),
                ('channel_id', '=', record.id)
            ])
            # Deadline requests
            record.request_deadline_today_count = RequestRequest.search_count([
                ('deadline_date', '>=', today_start),
                ('closed', '=', False),
                ('channel_id', '=', record.id)
            ])
            record.request_deadline_last_24h_count = (
                RequestRequest.search_count([
                    ('deadline_date', '>', yesterday),
                    ('closed', '=', False),
                    ('channel_id', '=', record.id)
                ]))
            record.request_deadline_week_count = RequestRequest.search_count([
                ('deadline_date', '>', week_ago),
                ('closed', '=', False),
                ('channel_id', '=', record.id)
            ])
            record.request_deadline_month_count = RequestRequest.search_count([
                ('deadline_date', '>', month_ago),
                ('closed', '=', False),
                ('channel_id', '=', record.id)
            ])
            # Unassigned requests
            record.request_unassigned_count = RequestRequest.search_count([
                ('user_id', '=', False),
                ('channel_id', '=', record.id)
            ])

    def action_channel_request_open_today_count(self):
        self.ensure_one()
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('date_created', '>=', today_start),
                ('closed', '=', False),
                ('channel_id', '=', self.id)])

    def action_channel_request_open_last_24h_count(self):
        self.ensure_one()
        yesterday = datetime.now() - relativedelta(days=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('date_created', '>', yesterday),
                ('closed', '=', False),
                ('channel_id', '=', self.id)])

    def action_channel_request_open_week_count(self):
        self.ensure_one()
        week_ago = datetime.now() - relativedelta(weeks=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('date_created', '>', week_ago),
                ('closed', '=', False),
                ('channel_id', '=', self.id)])

    def action_channel_request_open_month_count(self):
        self.ensure_one()
        month_ago = datetime.now() - relativedelta(months=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('date_created', '>', month_ago),
                ('closed', '=', False),
                ('channel_id', '=', self.id)])

    def action_channel_request_closed_today_count(self):
        self.ensure_one()
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            context={'search_default_filter_closed': 1},
            domain=[
                ('date_closed', '>=', today_start),
                ('closed', '=', True),
                ('channel_id', '=', self.id)])

    def action_channel_request_closed_last_24h_count(self):
        self.ensure_one()
        yesterday = datetime.now() - relativedelta(days=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            context={'search_default_filter_closed': 1},
            domain=[
                ('date_closed', '>', yesterday),
                ('closed', '=', True),
                ('channel_id', '=', self.id)])

    def action_channel_request_closed_week_count(self):
        self.ensure_one()
        week_ago = datetime.now() - relativedelta(weeks=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            context={'search_default_filter_closed': 1},
            domain=[
                ('date_closed', '>', week_ago),
                ('closed', '=', True),
                ('channel_id', '=', self.id)])

    def action_channel_request_closed_month_count(self):
        self.ensure_one()
        month_ago = datetime.now() - relativedelta(months=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            context={'search_default_filter_closed': 1},
            domain=[
                ('date_closed', '>', month_ago),
                ('closed', '=', True),
                ('channel_id', '=', self.id)])

    def action_channel_request_deadline_today_count(self):
        self.ensure_one()
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('deadline_date', '>=', today_start),
                ('closed', '=', False),
                ('channel_id', '=', self.id)])

    def action_channel_request_deadline_last_24h_count(self):
        self.ensure_one()
        yesterday = datetime.now() - relativedelta(days=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('deadline_date', '>', yesterday),
                ('closed', '=', False),
                ('channel_id', '=', self.id)])

    def action_channel_request_deadline_week_count(self):
        self.ensure_one()
        week_ago = datetime.now() - relativedelta(weeks=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('deadline_date', '>', week_ago),
                ('closed', '=', False),
                ('channel_id', '=', self.id)])

    def action_channel_request_deadline_month_count(self):
        self.ensure_one()
        month_ago = datetime.now() - relativedelta(months=1)
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('deadline_date', '>', month_ago),
                ('closed', '=', False),
                ('channel_id', '=', self.id)])

    def action_channel_request_unassigned_count(self):
        self.ensure_one()
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'generic_request.action_stat_request_count',
            domain=[
                ('user_id', '=', False),
                ('channel_id', '=', self.id)])
