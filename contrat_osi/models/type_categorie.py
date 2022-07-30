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
class Employee_C(models.Model):
    _name = 'category1em'

    name = fields.Char(
        string='Name',
        required=False)
    contrat = fields.Many2one('hr.contract')


#
class preavis(models.Model):
    _name = 'preavis'

    name = fields.Char(
        string='Name',
        required=False)
    contrat_type_pr = fields.Many2one('hr.contract.type')
    mois_essai = fields.Integer(string='mois ')
    jours_essai = fields.Integer(string='jours ')
    Duree = fields.Integer(string='Durée ', tracking=True, compute='coputeduree', store=True)

    @api.depends('mois_essai', 'jours_essai')
    def coputeduree(self):
        for rc in self:
            m = rc.mois_essai * 30
            #
            rc.Duree = m + rc.jours_essai


class raisonde(models.Model):
    _name = 'raison'

    name = fields.Char(
        string='Name',
        required=False)
    contrat_type_raison = fields.Many2one('hr.contract.type')

    # @api.model_create_multi
    # def create(self, vals_list):
    #     self.contrat_type = self.env['hr.contract.type'].search([('manufacture_pull_id', '=', False)])
    #
    #     res = super(raisonde, self).create(vals_list)
    #     self.clear_caches()
    #     return res



class priode(models.Model):
    _name = 'priode'

    type = fields.Char(
        string='type',
        required=False)

    mois_essai = fields.Integer(string='mois ')
    jours_essai = fields.Integer(string='jours ')
    Duree = fields.Integer(string='Durée ',tracking=True,compute='coputeduree',store=True)

    @api.depends('mois_essai','jours_essai')
    def coputeduree(self):
        for rc in self:
            m = rc.mois_essai * 30
            #
            rc.Duree = m + rc.jours_essai



    name = fields.Char(
        string='Name',
        required=False)
    contrat_type_priod = fields.Many2one(comodel_name='hr.contract.type',
        string='priode',
        required=False)


class type_categorie(models.Model):
    _inherit = 'hr.contract.type'
    index = fields.Integer()
    type = fields.One2many(
        'type','contrat_type_type',
        string='type',
        )
    période = fields.One2many(
        'priode','contrat_type_priod',
        string='Raison',
        )

    raison = fields.One2many(
        'raison','contrat_type_raison',
        string='Raison',
        )


    preavis = fields.One2many(
        'preavis','contrat_type_pr',
        string='preavis',
        )
    test = fields.Char(string="ttttttt")

    date_debut = fields.Date(string="date debut")
    priode_contra  = fields.Integer(
        string='Priode de contrat ',
        required=False)



    periode = fields.Selection(
        string='Type',
        selection=[('partiel', 'partiel'),
                   ('plein', 'plein'), ],
        required=False, )







        
    



