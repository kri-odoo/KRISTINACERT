from odoo import fields, models, api

FEATURE_MODULES = [
    'crnd_mail_chatter_send_composer',
    'crnd_mail_composer_chat_history',
    'crnd_mail_composer_template_tree',
    'crnd_wsd_broadcast',
    'crnd_wsd_legal',
    'generic_assignment_hr',
    'generic_assignment_team',
    'generic_request_assignment',
    'generic_request_action',
    'generic_request_action_assignment',
    'generic_request_action_invoice',
    'generic_request_action_priority',
    'generic_request_action_project',
    'generic_request_action_subrequest',
    'generic_request_action_survey',
    'generic_request_action_tag',
    'generic_request_calendar',
    'generic_request_crm',
    'generic_request_field',
    'generic_request_invoicing',
    'generic_request_mail',
    'generic_request_parent',
    'generic_request_related_doc',
    'generic_request_related_requests',
    'generic_request_reopen_as',
    'generic_request_route_auto',
    'generic_request_sale',
    'generic_request_service',
    'generic_request_sla',
    'generic_request_sla_log',
    'generic_request_sla_priority',
    'generic_request_sla_service',
    'generic_request_survey',
    'generic_request_web_conference',
    'generic_request_weight',
]


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Modules available
    module_generic_assignment_hr = fields.Boolean(
        string="HR Assignments")
    module_generic_assignment_team = fields.Boolean(
        string="Team Assignments")
    module_generic_request_assignment = fields.Boolean(
        string="Use Custom Assignment Policies")
    module_generic_request_action = fields.Boolean(
        string="Use Automated Actions")
    module_generic_request_action_project = fields.Boolean(
        string="Tasks")
    module_generic_request_action_subrequest = fields.Boolean(
        string="Subrequests")
    module_generic_request_sla = fields.Boolean(
        string="Use Service Level Agreements")
    module_generic_request_sla_log = fields.Boolean(
        string="Log Service Level")
    module_generic_request_field = fields.Boolean(
        string="Use Custom Fields in Requests")
    module_generic_request_parent = fields.Boolean(
        string="Use Subrequests")
    module_generic_request_related_doc = fields.Boolean(
        string="Documents Related to Requests")
    module_generic_request_related_requests = fields.Boolean(
        string="Related Requests")
    module_generic_request_reopen_as = fields.Boolean(
        string="Reopen Requests")
    module_generic_request_route_auto = fields.Boolean(
        string="Use Automatic Routes")
    module_generic_request_service = fields.Boolean(
        string="Use Services")
    module_generic_request_mail = fields.Boolean(
        string="Use Mail Sources")
    module_generic_request_survey = fields.Boolean(
        string="Surveys")
    module_generic_request_action_survey = fields.Boolean(
        string="Surveys (Action)")
    module_generic_request_action_tag = fields.Boolean(
        string="Tags")
    module_generic_request_invoicing = fields.Boolean(
        string="Invoicing")
    module_generic_request_action_invoice = fields.Boolean(
        string="Action invoice")
    module_crnd_wsd_broadcast = fields.Boolean(
        string="WSD Broadcast")
    module_crnd_wsd_legal = fields.Boolean(
        string="WSD Legal")
    module_generic_request_sla_priority = fields.Boolean(
        string="SLA Priority")
    module_generic_request_sla_service = fields.Boolean(
        string="SLA Service")
    module_generic_request_sale = fields.Boolean(
        string="Request Sale")
    module_generic_request_crm = fields.Boolean(
        string="Request CRM")
    module_generic_request_calendar = fields.Boolean(
        string="Request Calendar")
    module_generic_request_action_priority = fields.Boolean(
        string="Request Action Priority")
    module_generic_request_action_assignment = fields.Boolean(
        string="Request Action Assignment")
    module_generic_request_weight = fields.Boolean(
        string="Request Weight")
    module_crnd_mail_chatter_send_composer = fields.Boolean(
        string="Mail Chatter Send Composer")
    module_crnd_mail_composer_chat_history = fields.Boolean(
        string="Mail Composer Chat History")
    module_crnd_mail_composer_template_tree = fields.Boolean(
        string="Mail Composer Template Tree")
    module_generic_request_web_conference = fields.Boolean(
        string="Request Web Conference")

    # Modules available (helpers)
    need_install_generic_assignment_hr = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_assignment_team = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_assignment = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_project = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_subrequest = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_sla = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_sla_log = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_field = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_parent = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_related_doc = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_related_requests = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_reopen_as = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_route_auto = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_service = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_mail = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_survey = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_survey = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_tag = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_invoicing = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_invoice = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_crnd_wsd_broadcast = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_crnd_wsd_legal = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_sla_priority = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_sla_service = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_sale = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_crm = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_calendar = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_priority = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_assignment = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_weight = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_crnd_mail_chatter_send_composer = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_crnd_mail_composer_chat_history = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_crnd_mail_composer_template_tree = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_web_conference = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)

    request_event_live_time = fields.Integer(
        related='company_id.request_event_live_time', readonly=False)
    request_event_live_time_uom = fields.Selection(
        related='company_id.request_event_live_time_uom',
        readonly=False,
        help='Units of Measure', ondelete='cascade'
    )
    request_event_auto_remove = fields.Boolean(
        related='company_id.request_event_auto_remove', readonly=False)
    request_mail_suggest_partner = fields.Boolean(
        related='company_id.request_mail_suggest_partner', readonly=False)
    group_request_show_stat_on_kanban_views = fields.Boolean(
        group='base.group_user',
        implied_group='generic_request.'
                      'group_request_show_stat_on_kanban_views')

    @api.depends('company_id')
    def _compute_generic_request_modules_can_install(self):
        available_module_names = self.env['ir.module.module'].search([
            ('name', 'in', FEATURE_MODULES),
            ('state', '!=', 'uninstallable'),
        ]).mapped('name')
        for record in self:
            for module in FEATURE_MODULES:
                record['need_install_%s' % module] = (
                    module not in available_module_names
                )
