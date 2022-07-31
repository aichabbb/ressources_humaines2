from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging


_logger = logging.getLogger(__name__)

class conge(models.TransientModel):
    _name = 'conge'

    def ajouter(self):
        contract = self.env['hr.contract'].create({
            'employee_id': self.cantrat.employee_id.id,
            'name': s.cantrat.name,

        })
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.contract",
            "views": [[False, "form"]],
            "res_id": contract.id,
        }