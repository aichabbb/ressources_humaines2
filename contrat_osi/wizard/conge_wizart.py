from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging


_logger = logging.getLogger(__name__)

class conge(models.TransientModel):
    _name = 'conge'


    conge = fields.Many2one('hr.leave')



    def ajouter(self):
        type = self.env['hr.resignation.type'].search([('name', '=', 'Licenciement')]).id
        type_licenciement = self.env['type.licenciement'].search([('name', '=', 'Abondant de poste')]).id

        contract = self.env['hr.resignation'].create({
            'employee_id': self.conge.employee_id.id,
            'reason': 'test',
            'type_depart':type,
            'type_licenciement': type_licenciement,

        })
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.resignation",
            "views": [[False, "form"]],
            "res_id": contract.id,
        }