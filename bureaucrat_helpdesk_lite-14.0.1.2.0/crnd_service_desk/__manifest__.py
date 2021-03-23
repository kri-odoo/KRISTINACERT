{
    'name': 'Service Desk',
    'category': 'Service Desk',
    'summary': """
        Process addon for the Website Service Desk application.
    """,
    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'license': 'LGPL-3',
    'version': '14.0.1.3.0',
    'depends': [
        'generic_request',
    ],
    'data': [
        'data/init_data.xml',
        'data/request_type_incident.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
