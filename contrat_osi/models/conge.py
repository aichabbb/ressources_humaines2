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
                raise ValidationError(_('vous pouvez choisir durée inférieure ou egale de  %s   .', qty_produced))

            # for move in self:
            #     move.quantity_done = sum(move.mapped('move_line_ids.qty_done'))




