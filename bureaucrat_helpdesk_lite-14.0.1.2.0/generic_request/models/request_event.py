import logging
import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from .request_request import (AVAILABLE_PRIORITIES,
                              AVAILABLE_IMPACTS,
                              AVAILABLE_URGENCIES)
_logger = logging.getLogger(__name__)


class RequestEvent(models.Model):
    _name = 'request.event'
    _description = 'Request Event'
    _order = 'date DESC, id DESC'
    _log_access = False

    event_type_id = fields.Many2one(
        'request.event.type', required=True, readonly=True)
    event_code = fields.Char(
        related='event_type_id.code', readonly=True)
    request_id = fields.Many2one(
        'request.request', index=True, required=True, readonly=True,
        ondelete='cascade')
    date = fields.Datetime(
        default=fields.Datetime.now, required=True, index=True, readonly=True)
    user_id = fields.Many2one('res.users', required=True, readonly=True)

    # Assign related events
    old_user_id = fields.Many2one('res.users', readonly=True)
    new_user_id = fields.Many2one('res.users', readonly=True)

    # Change request description
    old_text = fields.Html(readonly=True)
    new_text = fields.Html(readonly=True)

    # Change request deadline
    old_deadline = fields.Date()
    new_deadline = fields.Date()

    # Request stage change
    route_id = fields.Many2one('request.stage.route', readonly=True)
    old_stage_id = fields.Many2one('request.stage', readonly=True)
    new_stage_id = fields.Many2one('request.stage', readonly=True)

    # Request Category Change
    old_category_id = fields.Many2one('request.category', readonly=True)
    new_category_id = fields.Many2one('request.category', readonly=True,)

    # Priority changed
    old_priority = fields.Selection(
        selection=AVAILABLE_PRIORITIES, readonly=True)
    new_priority = fields.Selection(
        selection=AVAILABLE_PRIORITIES, readonly=True)

    old_impact = fields.Selection(
        selection=AVAILABLE_IMPACTS, readonly=True)
    new_impact = fields.Selection(
        selection=AVAILABLE_IMPACTS, readonly=True)

    old_urgency = fields.Selection(
        selection=AVAILABLE_URGENCIES, readonly=True)
    new_urgency = fields.Selection(
        selection=AVAILABLE_URGENCIES, readonly=True)

    # Kanban state changed
    old_kanban_state = fields.Selection(
        selection="_get_selection_kanban_state",
        readonly=True)
    new_kanban_state = fields.Selection(
        selection="_get_selection_kanban_state",
        readonly=True)

    # Timetracking
    timesheet_line_id = fields.Many2one(
        'request.timesheet.line', 'Timesheet line',
        readonly=True, ondelete='cascade')

    assign_comment = fields.Text()

    def _get_selection_kanban_state(self):
        return self.env['request.request']._fields['kanban_state'].selection

    def name_get(self):
        res = []
        for record in self:
            res.append((
                record.id,
                "%s [%s]" % (
                    record.request_id.name,
                    record.event_type_id.display_name)
            ))
        return res

    def get_context(self):
        """ Used in notifications and actions to be backward compatible
        """
        self.ensure_one()
        return {
            'old_user': self.old_user_id,
            'new_user': self.new_user_id,
            'old_text': self.old_text,
            'new_text': self.new_text,
            'route': self.route_id,
            'old_stage': self.old_stage_id,
            'new_stage': self.new_stage_id,
            'old_priority': self.old_priority,
            'new_priority': self.new_priority,
            'old_kanban_state': self.old_kanban_state,
            'new_kanban_state': self.new_kanban_state,
            'request_event': self,
        }

    @api.model
    def _scheduler_vacuum(self, days=False):
        """ Run vacuum for events.
            Delete all events older than <days>
        """
        if days:
            _logger.warning(
                "Passing request event's time to live in scheduler is"
                " deprecated! Please, update cron job to "
                "call '_scheduler_vacuum' without arguments")

        if self.env.user.company_id.request_event_live_time_uom == 'days':
            delta = relativedelta(
                days=+self.env.user.company_id.request_event_live_time)
        elif self.env.user.company_id.request_event_live_time_uom == 'weeks':
            delta = relativedelta(
                days=+self.env.user.company_id.request_event_live_time*7)
        elif self.env.user.company_id.request_event_live_time_uom == 'months':
            delta = relativedelta(
                months=+self.env.user.company_id.request_event_live_time)
        vacuum_date = datetime.datetime.now() - delta
        if self.env.user.company_id.request_event_auto_remove:
            self.sudo().search(
                [('date', '<', fields.Datetime.to_string(vacuum_date))],
            ).unlink()
