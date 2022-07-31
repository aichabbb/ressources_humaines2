from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
class hr_leave(models.Model):
    _inherit = 'hr.leave'





    def control_de_plafonds_absence(self):
        if self.holiday_status_id.name == "absence justifies":
            conge_justifies = self.env['hr.leave'].search([('holiday_status_id', '=', "absence justifies"),('employee_id', '=', self.employee_id.id)])
            for cong in conge_justifies:
                sun = cong.number_of_days
                qty_produced = sum(conge_justifies.mapped('number_of_days'))
                if qty_produced >= 180:
                    return {
                        'name': _('conge'),
                        'view_mode': 'form',
                        'res_model': 'conge',
                        'view_id': self.env.ref('contrat_osi.view_conge').id,
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                        'context': {'default_conge': self.id, },
                    }

            # for move in self:
            #     move.quantity_done = sum(move.mapped('move_line_ids.qty_done'))




