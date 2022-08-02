from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
class employee(models.Model):
    _inherit = 'hr.employee'

    année_ancienneté = fields.Integer(string="année ancienneté")
    année_globale = fields.Integer(string="globale ancienneté")
    ancienneté_négociée = fields.Integer(string="ancienneté négociée")


    def anne_aanciennete(self):
        today = fields.Date.today()


        for cant in self:
            if cant.first_contract_date:

                d2= cant.first_contract_date
                self.année_ancienneté = today.year - d2.year
                cant.année_globale = cant.année_ancienneté + cant.ancienneté_négociée
            if self.birthday:
                date = today - self.birthday

                if date >= 63  :
                    raise ValidationError(_('fin de priode de travaille de employee  .'))
