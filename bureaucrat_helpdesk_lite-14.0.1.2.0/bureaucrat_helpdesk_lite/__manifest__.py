{
    'name': "Bureaucrat Helpdesk Lite",

    'summary': """
        Help desk
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '14.0.1.2.0',
    'category': 'Helpdesk',

    # any module necessary for this one to work correctly
    'depends': [
        'generic_request',
        'crnd_service_desk',
        'crnd_wsd',
    ],

    # always loaded
    'data': [
    ],
    'images': ['static/description/banner.gif'],
    'demo': [],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',

    'price': 0.0,
    'currency': 'EUR',
    "live_test_url": "https://yodoo.systems/saas/"
                     "template/helpdesk-lite-demo-data-69",
}
