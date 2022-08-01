from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta


import logging


_logger = logging.getLogger(__name__)






class transformation(models.TransientModel):
    _name = 'transformation'


    indeex = fields.Integer(string="index" )


    contrat_type = fields.Many2one('hr.contract.type', invisible="1")

    contrat_type_transformation = fields.Many2one('hr.contract.type',domain="[('index', '<', indeex)]")
    cantrat = fields.Many2one('hr.contract')




    def action_de_transformation(self):
        self.ensure_one()
        today = fields.Date.today()


        for rc in self:
            if rc.contrat_type_transformation.index == 1:
                if rc.cantrat.date_end:
                    d = rc.cantrat.date_end
                    date = d + timedelta(days=1)

                    contract = rc.env['hr.contract'].create({
                        'employee_id': rc.cantrat.employee_id.id,
                        'name': rc.cantrat.name,
                        'date_start': date,
                        'contract_type_id': rc.contrat_type_transformation.id,
                        'department_id': rc.cantrat.department_id.id,
                        'job_id': rc.cantrat.job_id.id,
                        'struct_id': rc.cantrat.struct_id.id,
                        'hr_responsible_id': rc.cantrat.hr_responsible_id.id,
                        'structure_type_id': rc.cantrat.structure_type_id.id,
                        'Employee_Category': rc.cantrat.Employee_Category.id,
                        'type': rc.cantrat.type.id,
                        #'trial_date_end': "2022-09-14",
                        'state': 'draft',
                        'wage': rc.cantrat.wage,
                    })
                    rc.cantrat.state = 'close'
                    rc.cantrat.date_end = today
                    return {
                        "type": "ir.actions.act_window",
                        "res_model": "hr.contract",
                        "views": [[False, "form"]],
                        "res_id": contract.id,
                    }

        #self.cantrat.contract_type_id = self.contrat_type_transformation.id
        #self.cantrat.state_cantrat = 'TR'






