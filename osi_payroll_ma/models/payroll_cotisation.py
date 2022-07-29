from odoo import models, fields, api


class Cotisation(models.Model):
    _name = 'ma.payroll.cotisation'
    _description = 'ma.payroll.cotisation'

    # Description
    name = fields.Char(string='Nom')
    code = fields.Char(string='Code')
    company_id = fields.Many2one('res.company', readonly=True, string=u'Societé',
                                default=lambda self: self.env['res.company']._company_default_get('ma.payroll.cotisation'))
    # Taux/Montant 
    type  = fields.Selection([('a', 'Montant'),('b', 'Taux')],string = 'Type')
    salarial_amount = fields.Float(string='Salarial')
    patronal_amount = fields.Float(string='Patronal')
    # Plafond
    is_plafond  = fields.Boolean(string='Cotisation plafonée ?', default =False)
    plafond = fields.Float(string='Plafond')
    # Comptabilité
    credit_account_id = fields.Many2one(
        'account.account',
        string='Compte de crédit',
        )
    debit_account_id = fields.Many2one(
        'account.account',
        string='Compte de débit',
        )
class CotisationType(models.Model):
    _name = 'ma.payroll.cotisation.type'
    _description = 'ma.payroll.cotisation.type'

    # Description
    name = fields.Char(string='Nom')
    company_id = fields.Many2one('res.company', readonly=True, string=u'Societé',
                                default=lambda self: self.env['res.company']._company_default_get('ma.payroll.cotisation.type'))
    