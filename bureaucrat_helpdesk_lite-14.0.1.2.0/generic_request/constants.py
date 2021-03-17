from odoo import _
# TODO, do we need this constant? It seems that only 'partner_id' is mentioned
# here, but have no pre/post write handlers
TRACK_FIELD_CHANGES = set((
    'stage_id', 'user_id', 'type_id', 'category_id', 'request_text',
    'partner_id', 'category_id', 'priority', 'impact', 'urgency'))
REQUEST_TEXT_SAMPLE_MAX_LINES = 3
KANBAN_READONLY_FIELDS = set(('type_id', 'category_id', 'stage_id'))
MAIL_REQUEST_TEXT_TMPL = "<h1>%(subject)s</h1>\n<br/>\n<br/>%(body)s"

AVAILABLE_PRIORITIES = [
    ('0', _('Not set')),
    ('1', _('Very Low')),
    ('2', _('Low')),
    ('3', _('Medium')),
    ('4', _('High')),
    ('5', _('Critical'))]

AVAILABLE_IMPACTS = [
    ('0', _('Not set')),
    ('1', _('Low')),
    ('2', _('Medium')),
    ('3', _('High')),
]

AVAILABLE_URGENCIES = [
    ('0', _('Not set')),
    ('1', _('Low')),
    ('2', _('Medium')),
    ('3', _('High')),
]

# This matrix allows to compute complex priority depending
# On selected impact and urgency. Inner lists represent impacts,
# List items represent urgencies. For example: request with
# low impact(0) and high urgency(2)
# will have complex_priority PRIORITY_MAP[0][2] = 3
PRIORITY_MAP = [
    [0, 1, 2, 3],
    [1, 1, 2, 3],
    [2, 2, 3, 4],
    [3, 3, 4, 5],
]
