from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
class hr_leave(models.Model):
    _inherit = 'hr.leave'





    def control_de_plafonds_absence(self):
        absence_justifies = self.env.ref('contrat_osi.absence_justifies')
        config = self.env['res.config.settings'].search([])
        today = fields.Date.today()
        len_C = int(len(config) - 1)
        list = []
        for rc in config:
            list.append(rc)
            _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', list)
            if rc.Age_la_retraite:
                _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', list)

        # conf = list[len_C]
        # if self.holiday_status_id == absence_justifies:
        #     conge_justifies = self.env['hr.leave'].search([('holiday_status_id', '=', "absence justifies"),('employee_id', '=', self.employee_id.id)])
        #     conge_justifies_nom_jus = self.env['hr.leave'].search([('holiday_status_id', '=', "absence nom justifies"),('employee_id', '=', self.employee_id.id)])
        #     for cong in conge_justifies:
        #         sun = cong.number_of_days
        #         qty_produced = sum(conge_justifies.mapped('number_of_days'))
        #         qty_produced_nom_justri = sum(conge_justifies_nom_jus.mapped('number_of_days'))
        #         if qty_produced >= conf.plafond_des_absence_justifie:
        #             return {
        #                 'name': _('conge'),
        #                 'view_mode': 'form',
        #                 'res_model': 'conge',
        #                 'view_id': self.env.ref('contrat_osi.view_conge').id,
        #                 'type': 'ir.actions.act_window',
        #                 'target': 'new',
        #                 'context': {'default_conge': self.id, },
        #             }
        #         elif qty_produced_nom_justri >= conf.plafond_des_absence_non_justifie:
        #             return {
        #                 'name': _('conge'),
        #                 'view_mode': 'form',
        #                 'res_model': 'conge',
        #                 'view_id': self.env.ref('contrat_osi.view_conge').id,
        #                 'type': 'ir.actions.act_window',
        #                 'target': 'new',
        #                 'context': {'default_conge': self.id, },
        #             }
        #
        #     # for move in self:
        #     #     move.quantity_done = sum(move.mapped('move_line_ids.qty_done'))
        #
        #


