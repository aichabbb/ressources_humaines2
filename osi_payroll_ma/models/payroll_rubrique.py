# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Rubrics(models.Model):
    _name = 'ma.payroll.rubrique'
    _description = 'ma.payroll.rubrique'

    name = fields.Char(string='Nom')
    code = fields.Char(string='Code')
    sequence = fields.Integer(string='Sequence')
    category  = fields.Selection([('gain', 'Gain'),('retenue', 'Retenue')], string='Categorie', required=True, )
    is_hourly  = fields.Boolean(string='Par heure ?', default =False)
    company_id = fields.Many2one('res.company', readonly=True, string=u'Societé',
                                default=lambda self: self.env['res.company']._company_default_get('ma.payroll.rubrique'))
    # Type 
    type  = fields.Selection([('a', 'Prime'),('b', 'Indemnité'),('c', 'Avantage')],string = 'Type')
    traitement_type  = fields.Selection([('a', 'Standard'),('b', 'Heures suplémentatire')],string = 'Type de traitement')
    is_imposable  = fields.Boolean(string='Imposable ?', default =False)
    plafond = fields.Float(string='Plafond exonéré')
    # Soummis
    submission_ids = fields.Many2many('ma.payroll.rubrique.submission', string="Références",
                                       help='Soumise à',)
    credit_account_id = fields.Many2one(
        'account.account',
        string='Compte de crédit',
        )
    debit_account_id = fields.Many2one(
        'account.account',
        string='Compte de débit',
        )
    comment  = fields.Text(string='Commentaire')
    
    


class RubricsSubmission(models.Model):
    _name = 'ma.payroll.rubrique.submission'

    name = fields.Char(string='Nom')
    company_id = fields.Many2one('res.company', readonly=True, string=u'Societé',
                                default=lambda self: self.env['res.company']._company_default_get('ma.payroll.rubrique.submission'))

