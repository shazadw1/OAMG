# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api, _
import odoo
import os
import shutil

import csv
from io import StringIO
import base64
import pandas as pd
import io
import openpyxl
import json


class dev_model(models.Model):
    _name = 'dev.model'

    name = fields.Char('Model Name', required="1")
    menu_name = fields.Char('Menu Name', required="1")
    field_ids = fields.One2many('dev.field', 'model_id', string="Fields")
    rec_name_id = fields.Many2one('dev.field', string="Rec Name")
    order_id = fields.Many2one('dev.field', string="Order")
    is_desc = fields.Boolean('Descending Order')
    description = fields.Char('Description')

    @api.model
    def create(self, vals):
        new_id = super(dev_model, self).create(vals)
        if new_id.name:
            name = str.replace(new_id.name, ' ', '.')
            new_id.name = name.lower()
        return new_id

    def write(self, vals):
        if vals.get('name'):
            name = str.replace(vals.get('name'), ' ', '.')
            vals['name'] = name.lower()
        res = super(dev_model, self).write(vals)
        return res

    def create_form_view(self):
        vals = "\t<!-- " + self.name + " Form View -->\n"
        vals += "\t<record id='devintellecs_view_" + str.replace(self.name, '.', '_') + "_form' model='ir.ui.view'>\n"

        vals += "\t\t<field name='name'>devintellecs.view." + self.name + ".form</field>\n"
        vals += "\t\t<field name='model'>" + self.name + "</field>\n"
        vals += "\t\t<field name='priority'>16</field>\n"
        vals += "\t\t<field name='arch' type='xml'>\n"
        vals += "\t\t\t<form string='" + self.menu_name + "'>\n"
        vals += "\t\t\t\t<sheet>\n"
        vals += "\t\t\t\t\t<group>\n"
        for field in self.field_ids:
            vals += "\t\t\t\t\t\t<field name='" + field.name + "'/>\n"
        vals += "\t\t\t\t\t</group>\n"
        vals += "\t\t\t\t</sheet>\n"
        vals += "\t\t\t</form>\n"
        vals += "\t\t</field>\n"
        vals += "\t</record>\n"
        return vals

    def create_tree_view(self):
        vals = "\t<!-- " + self.name + " Tree View -->\n"
        vals += "\t<record id='devintellecs_view_" + str.replace(self.name, '.', '_') + "_tree' model='ir.ui.view'>\n"

        vals += "\t\t<field name='name'>devintellecs.view." + self.name + ".tree</field>\n"
        vals += "\t\t<field name='model'>" + self.name + "</field>\n"
        vals += "\t\t<field name='priority'>16</field>\n"
        vals += "\t\t<field name='arch' type='xml'>\n"
        vals += "\t\t\t<tree string='" + self.menu_name + "'>\n"
        for field in self.field_ids:
            if field.is_view_tree:
                vals += "\t\t\t\t<field name='" + field.name + "'/>\n"
        vals += "\t\t\t</tree>\n"
        vals += "\t\t</field>\n"
        vals += "\t</record>\n"
        return vals

    def create_action_view(self, m_name):
        vals = "\t<!-- " + self.name + " Action -->\n"
        vals += "\t<record id='devintellecs_action_" + str.replace(self.name, '.',
                                                                   '_') + "' model='ir.actions.act_window'>\n"
        vals += "\t\t<field name='name'>" + self.name + "</field>\n"
        vals += "\t\t<field name='type'>ir.actions.act_window</field>\n"
        vals += "\t\t<field name='res_model'>" + self.name + "</field>\n"
        #        vals+="\t\t<field name='view_type'>form</field>\n"
        vals += "\t\t<field name='view_mode'>tree,form</field>\n"
        vals += "\t</record>\n"
        vals += "\n\t<!-- " + self.name + " Menu -->\n"
        vals += '''\t<menuitem name="''' + self.menu_name + '''" id="menu_''' + str.replace(self.name, '.',
                                                                                            '_') + '''" parent="sub_''' + m_name + '''_menu" action="devintellecs_action_''' + str.replace(
            self.name, '.', '_') + '''"/>\n\n'''

        return vals


class dev_field(models.Model):
    _name = 'dev.field'
    _rec_name = 'f_string'
    _order = 'name'

    name = fields.Char('Field Name', required="1")
    f_string = fields.Char('Field String', required="1")
    field_type = fields.Selection([
        ('Char', 'Char'),
        ('Text', 'Text'),
        ('Float', 'Float'),
        ('Integer', 'Integer'),
        ('Date', 'Date'),
        ('Boolean', 'Boolean'),
        ('Binary', 'Binary'),
        ('Many2one', 'Many2one'),
        ('Many2many', 'Many2many'),
    ], required="1", default="Char")
    is_required = fields.Boolean('Required')
    is_copy = fields.Boolean('Copy')
    is_readonly = fields.Boolean('Readonly')
    is_index = fields.Boolean('Index')
    default_val = fields.Char('Default')
    help_val = fields.Char('Help')

    model_id = fields.Many2one('dev.model', string="Model")
    related_model = fields.Many2one('ir.model', string="Related Model")
    is_view_tree = fields.Boolean('Show in Tree')

    @api.model
    def create(self, vals):
        new_id = super(dev_field, self).create(vals)
        if new_id.name:
            name = str.replace(new_id.name, ' ', '_')
            new_id.name = name.lower()
        return new_id

    def write(self, vals):
        if vals.get('name'):
            name = str.replace(vals.get('name'), ' ', '_')
            vals['name'] = name.lower()
        res = super(dev_field, self).write(vals)
        return res

    def get_field_val(self):
        vals = ''
        vals = "\n\t" + self.name + " = fields." + self.field_type + "("

        if self.field_type in ('Many2one', 'Many2many'):
            vals = vals + "'" + self.related_model.model + "', "

        vals = vals + "string='" + self.f_string + "'"

        if self.is_required:
            vals = vals + ", required=1"
        if self.is_copy:
            vals = vals + ", copy=" + str(self.is_copy)

        if self.is_readonly:
            vals = vals + ", readonly=" + str(self.is_readonly)

        if self.is_index:
            vals = vals + ", index=" + str(self.is_index)

        if self.default_val and self.field_type in ('Char', 'Float', 'Integer', 'Text', 'Boolean'):
            if self.field_type in ('Float', 'Integer', 'Boolean'):
                vals = vals + ", default=" + str(self.default_val)
            if self.field_type in ('Char', 'Text'):
                # vals = vals +", default='"+str(self.default_val)+"'"
                vals = vals + ", default='" + str(self.default_val) + "'"

        if self.help_val:
            vals = vals + ", help='" + str(self.help_val) + "'"

        vals = vals + ")"
        return vals


class dev_class(models.Model):
    _name = 'dev.class'

    csv_file = fields.Binary(string='CSV File', onchange='import_xlsx')

    @api.model
    def import_xlsx(self, file_content):
        decoded_data = base64.b64decode(file_content)

        # Read the Excel file into a pandas DataFrame
        all_sheets = pd.read_excel(io.BytesIO(decoded_data), sheet_name=None)

        # Filter out sheets with names containing "lookup"
        filtered_sheets = {sheet_name: sheet_data for sheet_name, sheet_data in all_sheets.items() if
                           'lookup' not in sheet_name.lower()}

        model_ids_to_add = []

        # Process the filtered sheets as needed
        for sheet_name, sheet_data in filtered_sheets.items():

            is_model_column_found = False
            is_field_column_found = False

            new_model = None

            # Iterate over each row in the DataFrame
            for index in range(len(sheet_data)):
                row = sheet_data.iloc[index]

                first_column_value = str(row.iloc[0])

                # Check if the value is not empty
                if pd.notna(first_column_value) and not first_column_value.lower() == "nan":
                    if first_column_value.lower() == "model name":
                        is_model_column_found = True
                        is_field_column_found = False
                        continue

                    if first_column_value.lower() == "field name":
                        is_model_column_found = False
                        is_field_column_found = True
                        continue

                    if is_model_column_found:
                        model_name = first_column_value
                        model_rec_name = False
                        model_description = str(row.iloc[2])
                        model_order = False
                        model_menu_name = str(row.iloc[4])

                        new_model = self.env['dev.model'].create({
                            "name": model_name,
                            "description": model_description,
                            "menu_name": model_menu_name
                        })

                        model_ids_to_add.append(new_model.id)

                        self.env.cr.commit()

                        print(f"Model Name: {model_name}")
                        print(f"Model Description: {model_description}")
                        print(f"Model Order: {model_order}")
                        print(f"Model Menu Name: {model_menu_name}")


                    elif is_field_column_found:
                        field_name = first_column_value
                        field_string = str(row.iloc[1])
                        field_show_in_tree = True if str(row.iloc[2]).lower() == "yes" else False
                        field_type = str(row.iloc[3])
                        field_required = True if str(row.iloc[4]).lower() == "yes" else False
                        field_copy = True if str(row.iloc[6]).lower() == "yes" else False
                        field_index = True if str(row.iloc[7]).lower() == "yes" else False
                        field_default = str(row.iloc[8])
                        field_help = str(row.iloc[9])

                        field_readonly = True if str(row.iloc[5]).lower() == "yes" else False

                        related_model_name = str(row.iloc[10])

                        field_related_model_id = self.env['ir.model'].search([('model', '=', related_model_name)],
                                                                             limit=1)


                        new_field = self.env['dev.field'].create({
                            "name": field_name,
                            "f_string": field_string,
                            "field_type": field_type,
                            "is_view_tree": field_show_in_tree,
                            "is_required": field_required,
                            "is_copy": field_copy,
                            "is_index": field_index,
                            "default_val": field_default,
                            "help_val": field_help,
                            "is_readonly" : field_readonly,
                            "related_model": field_related_model_id.id,
                            "model_id" : new_model.id
                        })

                        self.env.cr.commit()

                        if new_model:
                            new_model.write({'field_ids': [(4, new_field.id)]})

                        self.env.cr.commit()

            for record in self:
                record.write({
                    'model_ids': [(6, 0, model_ids_to_add)]
                })

    @api.model
    def import_file(self, file_content):
        # Decode the file content and convert to string
        decoded_content = base64.b64decode(file_content).decode('utf-8')

        # Create a CSV reader
        csv_reader = csv.reader(StringIO(decoded_content))

        new_model = None
        is_model = None
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Process or print the data as needed
            columns = row[0].split(';')
            if (columns[0] == "model"):
                print("Creating Model")
                model_name = columns[1]
                # new_model = self.env['dev.model'].create({
                # "name": model_name,
                # "menu_name": "Menu Root"
                # })
            elif (columns[0] == "field"):
                print("Creating Field")
                # field_name = columns[1]
                # field_type = columns[2]
                # new_field = self.env['dev.field'].create({
                # "name": field_name,
                # "f_string": field_name,
                # "field_type" : field_type,
                # "model_id" : new_model.id
                # })
                # if new_model:
                # new_model.write({'field_ids': [(4, new_field.id)]})

            self.env.cr.commit()

    @api.onchange('csv_file')
    def on_file_change(self):
        if self.csv_file:
            # Call the import_file method with the file content
            # self.import_file(self.csv_file)
            self.import_xlsx(self.csv_file)

    json = fields.Char(store=True)

    name = fields.Char('Module Name', required="1")
    model_ids = fields.Many2many('dev.model', string='Models')
    new_module = fields.Binary('Module', readonly="1")
    nm_name = fields.Char('Zip File Name')

    o_name = fields.Char('Name', required="1")
    o_category_id = fields.Many2one('ir.module.category', string='Category', required="1")
    o_summary = fields.Char('Summary', reqquired="1")
    o_desc = fields.Text('Description', required="1")
    o_auther = fields.Char('Author')
    o_website = fields.Char('Website')
    depends = fields.Many2many('ir.module.module', string='Depends', required="1")
    version = fields.Float('Version', default=1.0)
    installable = fields.Boolean('Installable', default=True)
    application = fields.Boolean('Application', default=True)
    auto_install = fields.Boolean('Auto Install')
    o_sequence = fields.Integer('Sequence', default=80)
    o_data = fields.Char('Data')

    top_menu_name = fields.Char('Top Menu', required="1")
    sub_menu_name = fields.Char('Sub Menu', required="1")

    readme = fields.Text('Readme')
    contributors = fields.Text('Contributors')

    @api.model
    def create(self, vals):
        new_id = super(dev_class, self).create(vals)
        if new_id.name:
            name = str.replace(new_id.name, ' ', '_')
            new_id.name = name.lower()
        return new_id

    def write(self, vals):
        if vals.get('name'):
            name = str.replace(vals.get('name'), ' ', '_')
            vals['name'] = name.lower()
        res = super(dev_class, self).write(vals)
        return res

    def get_certificate(self):
        return '''# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################'''

    def get_file_name(self, name):
        name = name.split('.')
        f_name = ''
        for n in name:
            if f_name:
                f_name = f_name + '_' + n
            else:
                f_name = n
        return f_name

    def get_field_vals(self, model):
        vals = '\n'
        for field in model.field_ids:
            val = field.get_field_val()
            vals += val
        return vals

    def create_other_file(self, m_path):
        if self.readme:
            file_name = m_path + '/README.txt'
            i_f = open(file_name, 'w')
            i_f.write('\n' + self.readme + '\n')
            i_f.close()
        if self.contributors:
            file_name = m_path + '/Contributors.txt'
            f = open(file_name, 'w')
            f.write('\n' + self.contributors + '\n')
            f.close()

    def create_openerp_file(self, m_path, sec_path):
        file_name = m_path + '/__init__.py'
        i_f = open(file_name, 'w')
        i_f.write(self.get_certificate())

        i_f.write('\nfrom . import models\n\n')
        i_f.write('\n\n# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:')

        file_name = m_path + '/__manifest__.py'
        f = open(file_name, 'w')
        f.write(self.get_certificate())

        file_name = sec_path + '/ir.model.access.csv'
        csv_f = open(file_name, 'w')
        csv_f.write('id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n')
        if self.model_ids:
            for model_line in self.model_ids:
                model_o_name = model_line.name
                model_r_name = model_o_name.replace(".", "_")
                data = 'access_' + str(model_r_name) + ',' + str(model_o_name) + ',' + 'model_' + str(
                    model_r_name) + ',,1,1,1,1' + '\n'
                csv_f.write(data)
        #

        d_name = ''
        for dep in self.depends:
            if d_name:
                d_name = d_name + ",'" + dep.name + "'"
            else:
                d_name = "'" + dep.name + "'"

        f.write('\n{')
        o_name = self.o_name or ''
        if not self.o_summary:
            self.o_summary = ''
        if not self.o_auther:
            self.o_auther = ''
        if not self.o_website:
            self.o_website = ''
        val = "\n\t'name':'" + self.o_name + "',"
        val += "\n\t'category':'" + self.o_category_id.name + "', "
        val += "\n\t'summary':'" + self.o_summary + "', "
        val += "\n\t'description':'''" + self.o_desc + "''', "

        val += "\n\t'author':'" + self.o_auther + "', "
        val += "\n\t'website':'" + self.o_website + "', "
        val += "\n\t'version':'" + str(self.version) + "', "

        val += "\n\t'depends':[" + d_name + "],"
        val += "\n\t'sequence':" + str(self.o_sequence) + ", "

        val += "\n\t'data':" + self.o_data + ","

        val += "\n\t'installable':" + str(self.installable) + ", "
        val += "\n\t'application':" + str(self.application) + ", "
        val += "\n\t'auto_install':" + str(self.auto_install) + ", "
        f.write(val)

        f.write('\n}')
        f.write('\n\n# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:')

    def create_menu_file(self, v_path):
        file_name = v_path + '/menu_file.xml'
        f = open(file_name, 'w')
        f.write('''<?xml version="1.0"?>\n''')
        f.write('''<odoo>\n''')
        val = '''\t<menuitem name="''' + self.top_menu_name + '''" id="top_''' + self.name + '''_menu"/>\n'''
        val += '''\t<menuitem name="''' + self.sub_menu_name + '''" id="sub_''' + self.name + '''_menu" parent="top_''' + self.name + '''_menu"/>\n'''
        f.write(val)
        f.write("\n")
        f.write('''</odoo>''')

    def generate_module(self):
        file_path = odoo.modules.get_module_resource('OAMG-main')
        parent_folder = os.path.dirname(file_path)
        # file_path =parent_folder
        c_file_path = file_path
        file_path = os.path.join(file_path, self.name)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        m_path = file_path
        os.mkdir(file_path)

        file_path = file_path + '/' + 'models'
        os.mkdir(file_path)
        i_file_name = file_path + '/' + '__init__.py'
        i_f = open(i_file_name, 'w')
        i_f.write(self.get_certificate())

        for m in self.model_ids:
            f_name = self.get_file_name(m.name)
            file_name = file_path + '/' + f_name + '.py'
            f = open(file_name, 'w')
            i_f.write("\nfrom . import " + f_name)
            f.write(self.get_certificate())

            f.write("\nfrom odoo import models, fields, api, _")
            f.write('''\n\nclass ''' + f_name + '''(models.Model):''')
            f.write("\n\t_name = '" + m.name + "'")
            if m.rec_name_id:
                f.write("\n\t_rec_name = '" + m.rec_name_id.name + "'")

            if m.order_id:
                if m.is_desc:
                    f.write("\n\t_order = '" + m.order_id.name + " desc'")
                else:
                    f.write("\n\t_order = '" + m.order_id.name + "'")

            if m.description:
                f.write("\n\t_description = '" + m.description + "'")

            field_val = self.get_field_vals(m)
            f.write(field_val)
            f.write('\n\n\n\n# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:')
            f.close()
        i_f.write('\n\n\n\n# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:')
        i_f.close()
        v_path = m_path + '/views'
        sec_path = m_path + '/security'
        os.mkdir(v_path)
        os.mkdir(sec_path)
        lst = []
        lst.append('security/ir.model.access.csv')
        lst.append('views/menu_file.xml'),
        for m in self.model_ids:
            form = m.create_form_view()
            tree = m.create_tree_view()
            action = m.create_action_view(self.name)
            f_name = str.replace(m.name, '.', '_')
            v_file_name = f_name + "_views.xml"
            f_name = v_path + '/' + v_file_name
            lst.append('views/' + str(v_file_name))
            f = open(f_name, 'w')
            f.write('''<?xml version="1.0"?>\n''')
            f.write('''<odoo>\n''')
            f.write(form)
            f.write("\n\n")
            f.write(tree)
            f.write("\n\n")
            f.write(action)
            f.write("\n\n")
            f.write('''</odoo>''')
            f.close()
        self.o_data = str(lst)
        p = m_path + '/views'
        menu = self.create_menu_file(v_path)
        opener_file = self.create_openerp_file(m_path, sec_path)
        oth_file = self.create_other_file(m_path)

        shutil.copytree(c_file_path + '/static', m_path + '/static', False, None)

        return True

        m_zip = shutil.make_archive(m_path, 'zip', m_path)
        import base64
        with open(m_zip, "rb") as f:
            bytes = f.read()
            self.new_module = base64.b64encode(bytes)
            self.nm_name = self.name + '.zip'
        shutil.rmtree(m_path)
        os.remove(m_zip)

        return True

    def view_erd(self):

        # Update json field with data from model_ids
        json_data = []
        for model in self.model_ids:
            model_data = {
                'name': model.name,
                'menu_name': model.menu_name,
                'description': model.description,
                'fields': [],
            }
            for field in model.field_ids:
                field_data = {
                    'name': field.name,
                    'f_string': field.f_string,
                    'field_type': field.field_type,
                    'is_required': field.is_required,
                    'is_copy': field.is_copy,
                    'is_readonly': field.is_readonly,
                    'is_index': field.is_index,
                    'default_val': field.default_val,
                    'help_val': field.help_val,
                    'is_view_tree': field.is_view_tree,
                    'related_model' : field.related_model.name
                    # Add other field data as needed
                }
                model_data['fields'].append(field_data)
            json_data.append(model_data)

        # Update the json field with the serialized data
        for record in self:
            record.json = json.dumps(json_data)

        self.env.cr.commit()


        action = {
            'name': 'Dev Class Form',
            'view_mode': 'form',
            'view_id': self.env.ref('OAMG-main.view_dev_class_wizard').id,
            'view_type': 'form',
            'res_model': 'dev.class',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'current',
        }
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
