from odoo import fields, api, models
from datetime import datetime, timedelta


class Regular(models.Model):
    _inherit = 'hr.attendance'

    regularization = fields.Boolean(string="Regularization")
    # Work entry type 
    work_entry_type_id = fields.Many2one(string='Type de Prestation', comodel_name='hr.work.entry.type')
    # overiding worked hours field
    worked_hours = fields.Float(string='Worked Hours', compute='_compute_worked_hours', store=True, readonly=False)
    check_out = fields.Datetime(string="Check Out")
    
    @api.onchange('worked_hours')
    def onchange_worked_hours_osi(self):
        for rec in self:
            if rec.check_in:
                rec.check_out = rec.check_in + timedelta(hours=rec.worked_hours)
    
