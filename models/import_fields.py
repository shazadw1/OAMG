from odoo import models, fields

class FileImportWizard(models.TransientModel):
    _name = 'dev.import.fields'
    _description = 'File Import Wizard'

    file = fields.Binary(string='File to Import', required=True)
    file_name = fields.Char(string='File Name')

    def import_file(self):
        # Implement your file import logic here
        # You can access the file content using self.file
        # Process the file content as needed
        pass
