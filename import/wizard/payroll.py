from odoo import models, fields, api, _
import xlrd

from odoo.exceptions import UserError
import base64

import tempfile
import binascii


import logging

_logger = logging.getLogger(__name__)
#


class im_salary_rule(models.Model):
    _name = 'import.salary.rule'

    file_name = fields.Binary(string="fille name")

    def import_journal_entry(self):
        try:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file_name))
            book = xlrd.open_workbook(fp.name)

            # file = base64.b64decode(self.file_name)
            # file_data = self.file.decode('base64')
            # book = xlrd.open_workbook(filename=file)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.')
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        sheet = book.sheet_by_index(0)
        for row in range(1,sheet.nrows):
            row_vals = sheet.row_values(row)
            _logger.info('ttttttttttttttttt1%s', row_vals[1])

            category = self.env['hr.salary.rule.category'].search([('name','=',row_vals[1])])
            _logger.info('ttttttttttttttttt22222222%s', category)



            name = self.env['hr.salary.rule.category'].search([('name', '=', row_vals[1])])
            for i in self.env['hr.salary.rule.category'].search([('name', '=', row_vals[1])]):
                nnnname = i.name
            for i in self.env['hr.salary.rnamesule.category'].search([('name', '=', row_vals[1])]):
                id_ = i.id
                _logger.info('_id0',id_)
            # if row_vals[2] and row_vals[4]:
            #
            #     self.env['hr.salary.rule'].create({
            #         'name': nnnname,
            #         # 'category_id': 1,
            #         'category_id': id_,
            #         'code': str(row_vals[0]),
            #         'input_ids': [(0, 0, {'code': ' ', 'name': ' ', })],
            #         'note': ' ',
            #
            #     })
            # else:
            #     self.env['hr.salary.rule'].create({
            #         'name': nnnname,
            #         # 'category_id': 1,
            #         'category_id': id_,
            #
            #         'code': str(row_vals[0]),
            #         'input_ids': [(0, 0, {'code': str(row_vals[2]), 'name': str(row_vals[2]), })],
            #         'note': row_vals[4],
            #
            #     })
            #
























      
