from odoo import models, fields, api, _
import xlrd

from odoo.exceptions import UserError
import base64

import tempfile
import binascii


import logging

_logger = logging.getLogger(__name__)
#
# try:
#     import xlrd
#     try:
#         from xlrd import xlsx
#     except ImportError:
#         xlsx = None
# except ImportError:
#     xlrd = xlsx = None
#
# try:
#     from . import odf_ods_reader
# except ImportError:
#     odf_ods_reader = None

class hr_salary_rule(models.Model):
    _inherit = 'hr.salary.rule'


    file_name = fields.Binary(string="fille name" )
    def script(self):
        category = self.env['hr.salary.rule.category'].search([])
        categ = self.env['hr.salary.rule'].search([])
        for rec in category:
            for r in category:
              for t in categ:
              
                  if rec != t.category_id:
                      if rec.name == r.name:
                         _logger.info('ttttttttttttttttt1%s', rec.name)
                         _logger.info('ttttttttttttttttt1%s', r.name)

                         rec.sudo().unlink()


    def import_journal_entry(self):
        try:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file_name))
            book = xlrd.open_workbook(fp.name)

            #file = base64.b64decode(self.file_name)
            #file_data = self.file.decode('base64')
            #book = xlrd.open_workbook(filename=file)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' )
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            row_vals = sheet.row_values(row)
            category = self.env['hr.salary.rule.category'].search([('name', '!=', row_vals[1])])
            if category:
                
               self.env['hr.salary.rule.category'].create({
                    'name': row_vals[1],
                    'code': row_vals[0],

                })
            name = self.env['hr.salary.rule.category'].search([('name', '=', row_vals[1])])
            for i in self.env['hr.salary.rule.category'].search([('name', '=', row_vals[1])]):
                nnnname = i.name
            for i in self.env['hr.salary.rule.category'].search([('name', '=', row_vals[1])]):
                id_ = i.id
            if row_vals[2] and row_vals[4]:


                self.env['hr.salary.rule'].create({
                    'name':  nnnname,
                    #'category_id': 1,
                    'category_id':  id_,
                    'code': str(row_vals[0]),
                    'input_ids': [(0, 0, {'code': ' ' ,'name': ' ' ,})],
                    'note': ' ',

                })
            else:
                self.env['hr.salary.rule'].create({
                    'name': nnnname,
                    #'category_id': 1,
                    'category_id':  id_,

                    'code': str(row_vals[0]),
                    'input_ids': [(0, 0, {'code': str(row_vals[2]) ,'name': str(row_vals[2]) ,})],
                    'note': row_vals[4],

                })





            #_logger.info("testttttttttttttttttttttttt  %s",row_vals[1])
            _logger.info("testttttttttttttttttttttttt 222 %s",row_vals[0])




class import_bank(models.Model):
    _inherit = 'res.bank'


    file_name = fields.Binary(string="fille name" )

    def import_journal_entry(self):
        try:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file_name))
            book = xlrd.open_workbook(fp.name)

            #file = base64.b64decode(self.file_name)
            #file_data = self.file.decode('base64')
            #book = xlrd.open_workbook(filename=file)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % file)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            row_vals = sheet.row_values(row)

            self.env['res.bank'].create({
                'name': row_vals[1] ,
                'bic': row_vals[0],
            
        
            })




            #_logger.info("testttttttttttttttttttttttt  %s",row_vals[1])
            _logger.info("testttttttttttttttttttttttt 222 %s",row_vals[0])
