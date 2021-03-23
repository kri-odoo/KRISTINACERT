{
    'name': "Generic Request",

    'summary': """
        Incident management and helpdesk system - logging, recording,
        tracking, addressing, handling and archiving
        issues that occur in daily routine.
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'category': 'Generic Request',
    'version': '14.0.1.99.0',
    'external_dependencies': {
        'python': [
            'html2text',
        ],
        'bin': [
            'lessc',
        ],
    },

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
        'generic_mixin',
        'generic_tag',
        # 'crnd_web_diagram_plus',
        'crnd_web_list_popover_widget',
        'crnd_web_tree_colored_field',
        'base_setup',
    ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/request_sequence.xml',
        'data/mail_subtype.xml',
        'data/request_stage_type.xml',
        'data/request_event_type.xml',
        'data/ir_cron.xml',
        'data/generic_tag_model.xml',
        'data/generic_tag_category.xml',
        'data/generic_tag.xml',
        'data/request_timesheet_activity.xml',
        'data/request_channel.xml',

        'views/templates.xml',
        'views/request_views.xml',
        'views/res_config_settings_view.xml',
        'views/request_category_view.xml',
        'views/request_type_view.xml',
        'views/request_kind.xml',
        'views/request_stage_route_view.xml',
        'views/request_stage_view.xml',
        'views/request_stage_type_view.xml',
        'views/request_request_view.xml',
        'views/request_channel_view.xml',
        'views/res_partner_view.xml',
        'views/res_users.xml',
        'views/mail_templates.xml',
        'views/request_event.xml',
        'views/request_event_category.xml',
        'views/request_event_type.xml',
        'views/request_creation_template.xml',
        'views/generic_tag_menu.xml',
        'views/request_timesheet_activity.xml',
        'views/request_timesheet_line.xml',
        'wizard/request_wizard_close_views.xml',
        'wizard/request_wizard_assign.xml',
        'wizard/request_wizard_stop_work.xml',

        'templates/templates.xml',

        'reports/request_timesheet_report.xml',
        'reports/request_graph_reports.xml',
    ],

    'demo': [
        'demo/request_demo_users.xml',
        'demo/request_category_demo.xml',
        'demo/request_kind.xml',
        'demo/request_type_simple.xml',
        'demo/request_type_seq.xml',
        'demo/request_type_access.xml',
        'demo/request_type_non_ascii.xml',
        'demo/request_type_with_complex_priority.xml',
        'demo/request_mail_activity.xml',
        'demo/request_creation_template.xml',
        'demo/demo_request_timesheet_activity.xml',
    ],

    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
