{

    'name': "Real-Estate Management",
    'version': '1.0',
    'depends': ['base'],
    'author': "umer",
    'category': 'Category',
    'description': """This is a test module of Real-Estate Management!""",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'models/users.py',
        'views/estate_kanban_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
