# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Odoo Module Scaffold, Module Generator',
    'version': '16.0.1.0',
    'sequence': 1,
    'category': 'Tools',
    'description':
        """
This Module add below functionality into odoo

        1.Create Custom Odoo App Easily\n
        2.User can create custom app themselves who has basic knowledge of Odoo\n
        3.Download created app as a zip file
        
        odoo module 
        create odoo module 
        create odoo apps
        odoo module without technical knowledge
        Odoo module structure 
        Odoo menu and classs
        odoo Manifest file
        Odoo scaffold
        Odoo Module Scaffold
        Odoo module scaffold
Odoo app scaffold
Module scaffold
App scaffold
Create odoo module
Odoo module
Manage odoo module
Create odoo module without technical knowledge
Manage odoo module without technical knowledge
Create many odoo module 
Create many odoo app
Create custom odoo app
Manage custom odoo app
Create custom odoo app easily
Manage custom odoo app easily 
Create custom app
Odoo create custom app
Create many models , views , fields
Create odoo models views fields 
Manage custom app
Install odoo module
Install odoo app
Module scaffold

    """,
    'summary': 'odoo app will help to generate odoo module without ant technical knowledge,Module Scaffold,Create odoo module,Manage odoo module,custom Module',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/dev_class_view.xml',
        'views/dev_model_view.xml',
        'views/dev_field_view.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':39.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
    'pre_init_hook' :'pre_init_check',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
