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
	'name':'Banking Test Module',
	'category':'Administration', 
	'summary':'', 
	'description':'''uguigui''', 
	'author':'', 
	'website':'', 
	'version':'1.0', 
	'depends':['base'],
	'sequence':80, 
	'data':['security/ir.model.access.csv', 'views/menu_file.xml', 'views/banking_customer_views.xml'],
	'installable':True, 
	'application':True, 
	'auto_install':False, 
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: