# -*- coding: utf-8 -*-
{
    'name' : 'Delivery date on SO lines',
    'version' : '1',
    'author': 'Humanytek',
    'description': """
        Adds delivery date on sale order lines
        delivery date = (product delay time) + 1 + (so create date)
    """,
    'category' : 'Sale',
    'depends' : ['sale'],
    'data': [
        'sale_view.xml',  
    ],
    'demo': [

    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
