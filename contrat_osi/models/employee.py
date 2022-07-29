from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
class employee(models.Model):
    _inherit = 'hr.employee'

    # année_ancienneté = fields.Integer(string="année ancienneté")
    # année_globale = fields.Integer(string="globale ancienneté")
    # année_ancienneté2 = fields.Char(string="année ancienneté")
    # ancienneté_négociée = fields.Integer(string="ancienneté négociée")
    # date_start_z = fields.Date('Start Date', required=True, default=fields.Date.today,index=True)
    #
    #
    # def anne_aanciennete(self):
    #     today = fields.Date.today()
    #
    #
    #     for cant in self:
    #         renew_date = fields.Date.from_string(cant.date_start_z)
    #         renew_date2 = fields.Date.from_string(cant.first_contract_date)
    #
    #         d = cant.date_start_z
    #         d2= cant.first_contract_date
    #         Madate_d2 = str(d2)
    #         Madate_d = str(today)
    #         date = cant.date_start_z
    #         moit_test = Madate_d2.split("-")[2]
    #         moit_test_today = Madate_d.split("-")[2]
    #         raise ValidationError(_('NE PEUX PAS DEPASSE CONTRAT CDD UN AN %s %s  .',moit_test_today,moit_test))
    #         if moit_test_today > moit_test :
    #             cant.ancienneté_négociée = cant.année_ancienneté +2
    #             cant.année_globale = cant.année_ancienneté + cant.ancienneté_négociée
    #
    #
    #         # date = str(g)
    #         # #diff = (d.date() - d2.date())
    #         # datee = date.split("days")[0]
    #         # # ittt = int(datee)
    #         # # date2 =  ittt / 360
    #         # #
    #         # cant.année_ancienneté2 = datee
    #         # if cant.année_ancienneté2 :
    #         #     cant.année_ancienneté = int(cant.année_ancienneté2) / 360
    #         #
    #         #
    #         # cant.année_globale = cant.année_ancienneté + cant.ancienneté_négociée
    #         #
    #         #
    #         # _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', datee)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

