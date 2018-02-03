# -*- coding: utf-8 -*-
# Copyright 2018 Humanytek
# - Ruben Bravo <rubenred18@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Invoice - Ecommerce',
    'version': '9.0.0.1.0',
    'category': 'Sales',
    'author': 'Humanytek',
    'website': "http://www.humanytek.com",
    'license': 'AGPL-3',
    'depends': [
        'website_sale_delivery',
        #'sale_order_autodetect_delivery_method',
        #'website_crm'
    ],
    'data': [
        'views/template.xml',
    ],
    'installable': True,
    'auto_install': False
}
