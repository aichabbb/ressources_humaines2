from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError

class type(models.Model):
    _name = 'type'

    name = fields.Char(
        string='Name',
        required=False)
    contrat_type_type = fields.Many2one('hr.contract.type')

#
# #
# # class preavis(models.Model):
# #     _name = 'preavis'
# #
# #     name = fields.Char(
# #         string='Name',
# #         required=False)
# #     contrat_type_pr = fields.Many2one('hr.contract.type')
#
#
#
# class raisonde(models.Model):
#     _name = 'raison'
#
#     name = fields.Char(
#         string='Name',
#         required=False)
#     contrat_type_raison = fields.Many2one('hr.contract.type')
#
#     # @api.model_create_multi
#     # def create(self, vals_list):
#     #     self.contrat_type = self.env['hr.contract.type'].search([('manufacture_pull_id', '=', False)])
#     #
#     #     res = super(raisonde, self).create(vals_list)
#     #     self.clear_caches()
#     #     return res
#
#
#
# class priode(models.Model):
#     _name = 'priode'
#
#
#     name = fields.Char(
#         string='Name',
#         required=False)
#     contrat_type_priod = fields.Many2one(comodel_name='hr.contract.type',
#         string='Période de préavis',
#         required=False)


class type_categorie(models.Model):
    _inherit = 'hr.contract.type'
    type = fields.One2many(
        'type','contrat_type_type',
        string='type',
        )
    # période = fields.One2many(
    #     'priode','contrat_type_priod',
    #     string='Raison',
    #     )
    #
    # raison = fields.One2many(
    #     'raison','contrat_type_raison',
    #     string='Raison',
    #     )


    # preavis = fields.One2many(
    #     'priode','contrat_type_priod',
    #     string='preavis',
    #     )
    # test = fields.Char(string="ttttttt")
    #
    # date_debut = fields.Date(string="date debut")
    # priode_contra  = fields.Integer(
    #     string='Priode de contrat ',
    #     required=False)



    # periode = fields.Selection(
    #     string='Type',
    #     selection=[('partiel', 'partiel'),
    #                ('plein', 'plein'), ],
    #     required=False, )







        
    



