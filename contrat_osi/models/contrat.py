
from odoo import models, fields, api, _
from datetime import datetime as dt
import datetime
import logging
_logger = logging.getLogger(__name__)



class categorie(models.Model):
    _inherit = 'hr.contract'

    #raison = fields.Many2one('raison' ,string="raison",domain="[('contrat_type_raison', '=', contract_type_id)]")
    # preavis = fields.Many2one('preavis', string="Période de préavis", domain="[('contrat_type_preavis', '=', contract_type_id)]")
    #periode = fields.Many2one('priode' ,string="Période essai",domain="[('contrat_type_priod', '=', contract_type_id)]")
    type = fields.Many2one(
        'type',
        string='type',domain="[('contrat_type_type', '=', contract_type_id)]"
        )
    #nombre_h = fields.Float(string='Contrat à temps partiel nombre d’heure' )


    # @api.depends('date_start', 'date_end')
    # def test(self):
    #
    #
    #     init_date = dt.strptime(str(self.date_start), '%Y-%m-%d')
    #     end_date = dt.strptime(str(self.date_end), '%Y-%m-%d')
    #     nombre = str((end_date - init_date).days)
    #     # if nombre >= 31:
    #     #     self.nombre_h = str((end_date - init_date).days)
    #     # else:
    #     #     self.nombre_h = str((end_date - init_date).month)
    #
    #     # d1 = date.strptime(self.date_start, fmt)
    #     #
    #     # d2 = date.strptime(self.date_end, fmt)
    #     # renew_date = fields.Date.from_string(self.date_start)
    #     # renew_date2 = fields.Date.from_string(self.date_end)
    #     # daysDiff = str((d2 - d1).days)
    #
    #     _logger.info('Device  is now disconnected cccccccccccccccccccccccccc%s', self.nombre_h)



    # @api.onchange('date_end')
    # def compute(self):
    #     if self.contract_type_id.name == "contrat à durée déterminée (CDD)":
    #         fmt = '%Y-%m-%d'
    #         d1 = datetime.strptime(self.date_start, fmt)
    #
    #         d2 = datetime.strptime(self.date_end, fmt)
    #         renew_date = fields.Date.from_string(self.date_start)
    #         renew_date2 = fields.Date.from_string(self.date_end)
    #         daysDiff = str((d2 - d1).days)
    #
    #         _logger.info('Device  is now disconnected cccccccccccccccccccccccccc%s', daysDiff)

    # @api.depends('contract_type_id')
    # def _func_contract_type_id(self):
    #     if self.contract_type_id.name == 'contrat à durée déterminée (CDD)':
    #         self.raison = self.env['raison'].search([('contrat_type', '=', self.contract_type_id)]).id
    #












