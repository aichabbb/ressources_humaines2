from odoo import models, fields, api, _
import xlrd

from odoo.exceptions import UserError
import base64

import tempfile
import binascii


import logging

_logger = logging.getLogger(__name__)
#



class import_test_bank(models.Model):
    _name = 'import.bank'

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
            raise UserError('No such file or directory found. \n%s.' % file)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            row_vals = sheet.row_values(row)

            self.env['res.bank'].create({
                'name': row_vals[1],
                'bic': row_vals[0],

            })

            # _logger.info("testttttttttttttttttttttttt  %s",row_vals[1])
            _logger.info("testttttttttttttttttttttttt 222 %s", row_vals[0])
