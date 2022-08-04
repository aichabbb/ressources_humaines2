# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
import time
import datetime


# Classe : Paie
class HrPayrollMa(models.Model):
    _name = "hr.payroll_ma"
    _description = 'Saisie des bulletins'
    _order = "number"

    @api.model
    def _get_journal(self):
        journal_id = self.env['account.journal'].search(['|', ('code', '=', 'Paie'), ('name', '=', 'Paie')])
        return journal_id and journal_id.id or False

    name = fields.Char(string='Description', required=True)
    number = fields.Char(string=u'Code', readonly=True)
    date_start = fields.Date(string=u'Date début')
    date_end = fields.Date(string=u'Date fin')
    date_salary = fields.Date(string='Date', states={'open': [('readonly', True)], 'close': [('readonly', True)]})
    company_id = fields.Many2one('res.company', string=u'Société', default=lambda self: self.env.user.company_id,
                                 copy=False)
    period_id = fields.Many2one('date.range', string=u'Période', domain=[('type_id.fiscal_period', '=', True)],
                                required=True, states={'draft': [('readonly', False)]})
    bulletin_line_ids = fields.One2many('hr.payroll.ma.bulletin', 'id_payroll_ma',
                                        string='Bulletins', states={'draft': [('readonly', False)]})
    move_id = fields.Many2one('account.move', string=u'Pièce comptable',
                              readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal', default=_get_journal,
                                 required=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(selection=(
        ('draft', 'Brouillon'),
        ('confirmed', u'Confirmé'),
        ('paid', u'Payé'),
        ('cancelled', u'Annulé')
    ), string='Statut', readonly=True, default='draft')
    total_net = fields.Float(string='Total net', compute='get_total_net', digits=(16, 2))

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('hr.payroll_ma')
        result = super(HrPayrollMa, self).create(vals)
        return result

    #@api.one
    @api.constrains('period_id')
    def _check_unicity_periode(self):
        payroll_ids = self.env['hr.payroll_ma'].search([('period_id', '=', self.period_id.id)])
        if len(payroll_ids) > 1:
            raise ValidationError(u'On ne peut pas avoir deux paies pour la même période !')

    #@api.multi
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(u"Suppression impossible")
            rec.bulletin_line_ids.unlink()
            payroll_id = super(HrPayrollMa, self).unlink()
            return payroll_id

    #@api.multi
    def get_total_net(self):
        for rec in self:
            net = sum(line.salaire_net_a_payer for line in rec.bulletin_line_ids)
            rec.total_net = net

    @api.onchange('company_id', 'period_id')
    def onchange_period_id(self):
        if self.company_id and self.period_id:
            self.name = 'Paie ' + self.company_id.name + u' de la période ' + self.period_id.name
            self.date_start = self.period_id.date_start
            self.date_end = self.period_id.date_end

    #@api.multi
    def draft_cb(self):
        for rec in self:
            if rec.move_id:
                raise ValidationError(u"Veuillez d'abord supprimer les écritures comptables associés")
            rec.state = 'draft'

    #@api.multi
    def confirm_cb(self):
        for rec in self:
            rec.action_move_create()
            rec.state = 'confirmed'
            for bulletin in rec.bulletin_line_ids:
                bulletin.name = self.env['ir.sequence'].next_by_code('hr.payroll.ma.bulletin')


    def cancel_cb(self):
        for rec in self:
            rec.state = 'cancelled'

    def get_employees(self):
        self.ensure_one()
        employees = self.env['hr.employee'].search([('active', '=', True),
                                                     ('date', '<=', self.date_end),
                                                    ('company_id', '=', self.company_id.id),


                                                    ])
        return employees

    def get_employee_contract(self, employee):
        self.ensure_one()
        contract = self.env['hr.contract'].search([('employee_id', '=', employee.id),
                                                   ('state', 'in', ('draft', 'open')),
                                                   ('actif', '=', True),
                                                   '|', ('date_end', '=', False), ('date_end', '>=', self.date_salary)],
                                                  order='date_start desc', limit=1)
        return contract

    def get_employees_leaves(self, employee):
        self.ensure_one()
        date_start = datetime.datetime.combine(self.date_start, datetime.datetime.min.time())
        date_end = datetime.datetime.combine(self.date_end, datetime.datetime.max.time())
        absences = '''  select sum(number_of_days) 
                                        from    hr_leave h
                                        left join hr_leave_type s on (h.holiday_status_id=s.id)
                                        where date_from >= '%s' and date_to <= '%s'
                                        and employee_id = %s
                                        and state = 'validate'
                                        and s.unpaid=True''' % (date_start,
                                                                date_end, employee.id)
        self.env.cr.execute(absences)
        res = self.env.cr.fetchone()
        if res[0] is None:
            days = 0
        else:
            days = res[0] * (-1)
        return days

    def prepare_payroll_line_values(self, employee, contract, days):
        self.ensure_one()
        return {
            'employee_id': employee.id,
            'employee_contract_id': contract.id,
            'working_days': contract.working_days_per_month + days,
            'normal_hours': contract.monthly_hour_number,
            'hour_base': contract.hour_salary,
            'salaire_base': contract.wage,
            'salary_type': contract.salary_type,
            'id_payroll_ma': self.id,
            'period_id': self.period_id.id,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'date_salary': self.date_salary
        }

   # @api.multi
    def generate_employees(self):
        for rec in self:
            employees = self.get_employees()
            if 1:
                sql = '''
                DELETE from hr_payroll_ma_bulletin where id_payroll_ma = %s
                    '''
                self.env.cr.execute(sql, (rec.id,))
            for employee in employees:
                contract = rec.get_employee_contract(employee)
                days = rec.get_employees_leaves(employee)
                if 1:
                    line = rec.prepare_payroll_line_values(employee, contract, days)
                    self.env['hr.payroll.ma.bulletin'].create(line)
        return True

    #@api.multi
    def compute_all_lines(self):
        for rec in self:
            for bulletin in rec.bulletin_line_ids:
                bulletin.compute_all_lines()
        return True

    def get_parametres(self):
        self.ensure_one()
        params = self.env['hr.payroll_ma.parametres']
        dictionnaire = params.search([('company_id', '=', self.company_id.id)])
        return dictionnaire

    # Generation des écriture comptable
    #@api.multi
    def action_move_create(self):
        for rec in self:
            dictionnaire = rec.get_parametres()
            date = rec.date_salary or fields.Date.context_today(self)
            journal = rec.journal_id
            move_lines = []
            bulletins = self.env['hr.payroll.ma.bulletin'].search([('id_payroll_ma', '=', rec.id)])
            salaire_brut_debit = salaire_brut_credit = 0.0
            # Cotisations
            operateur = 'in'
            ids = tuple(bulletins.ids)
            if len(bulletins) == 1:
                operateur = '='
                ids = bulletins.id
            sql = """SELECT l.name as name ,
                            sum(subtotal_employee) as subtotal_employee,
                            sum(subtotal_employer) as subtotal_employer,
                            l.credit_account_id,
                            l.debit_account_id,
                            l.cotisation_id,
                            l.type
                            FROM    hr_payroll_ma_bulletin_line l
                            where   l.type in ('cotisation','ir') and id_bulletin %s %s
                            group by l.name, l.credit_account_id, l.debit_account_id, l.cotisation_id, l.type
                  """ % (operateur, ids)
            self.env.cr.execute(sql)
            data = self.env.cr.dictfetchall()
            for line in data:
                if line['type'] == 'cotisation':
                    cotisation_id = self.env['hr.payroll_ma.cotisation'].browse(line['cotisation_id'])
                    credit_account_id = cotisation_id.credit_account_id.id
                    debit_account_id = cotisation_id.debit_account_id.id
                else:
                    credit_account_id = line['credit_account_id']
                    debit_account_id = line['debit_account_id']

                if line['subtotal_employee']:
                    move_line_credit = {
                        'account_id': credit_account_id,
                        'journal_id': journal.id,
                        'date': date,
                        'name': (line['name'] or '\\') + ' Salarial',
                        'credit': line['subtotal_employee'],
                        'debit': 0,
                    }
                    move_lines.append((0, 0, move_line_credit))
                    salaire_brut_credit += line['subtotal_employee']

                if line['subtotal_employer']:
                    move_line_debit = {
                        'account_id': debit_account_id,
                        'journal_id': journal.id,
                        'date': date,
                        'name': (line['name'] or '\\') + ' Patronal',
                        'debit': line['subtotal_employer'],
                        'credit': 0,
                    }
                    move_line_credit = {
                        'account_id': credit_account_id,
                        'journal_id': journal.id,
                        'date': date,
                        'name': (line['name'] or '\\') + ' Patronal',
                        'debit': 0,
                        'credit': line['subtotal_employer'],
                    }
                    move_lines.append((0, 0, move_line_debit))
                    move_lines.append((0, 0, move_line_credit))

            # Rubriques
            sql = """
                    SELECT  l.name as name, 
                            sum(subtotal_employee) as subtotal_employee,
                            sum(subtotal_employer) as subtotal_employer,
                            l.credit_account_id,
                            l.debit_account_id
                    FROM    hr_payroll_ma_bulletin_line l
                    where   l.type = 'majoration' and id_bulletin %s %s
                            and l.credit_account_id is not null 
                            and l.debit_account_id is not null
                    group by l.name, l.credit_account_id, l.debit_account_id
                    """ % (operateur, ids)
            self.env.cr.execute(sql)
            data_rub = self.env.cr.dictfetchall()
            for line in data_rub:
                move_line_debit_rubrique = {
                    'account_id': line['debit_account_id'],
                    # 'analytic_account_id': dictionnaire['analytic_account_id'][0],
                    'journal_id': journal.id,
                    'date': date,
                    'name': line['name'] or '\\',
                    'debit': line['subtotal_employee'],
                    'credit': 0,
                }
                move_lines.append((0, 0, move_line_debit_rubrique))
                salaire_brut_debit += line['subtotal_employee']

            # Rubriques deduction
            sql = """
                SELECT  l.name as name,
                sum(subtotal_employee) as subtotal_employee,
                sum(subtotal_employer) as subtotal_employer,
                l.credit_account_id,
                l.debit_account_id
                FROM hr_payroll_ma_bulletin_line l
                where l.type = 'retenu' and id_bulletin %s %s
                and l.credit_account_id is not null
                and l.debit_account_id is not null
                group by l.name, l.credit_account_id, l.debit_account_id
                """ % (operateur, ids)

            self.env.cr.execute(sql)
            data_rub = self.env.cr.dictfetchall()
            for line in data_rub:
                move_line_credit_rubrique = {
                    'account_id': line['credit_account_id'],
                    # 'analytic_account_id': dictionnaire['analytic_account_id'][0],
                    'journal_id': journal.id,
                    'date': date,
                    'name': line['name'] or '\\',
                    'debit': 0,
                    'credit': line['subtotal_employee'],
                }
                move_lines.append((0, 0, move_line_credit_rubrique))
                salaire_brut_credit += line['subtotal_employee']
            # salaire_net_a_payer, arrondi
            sql = '''
                    SELECT  sum(salaire_brute) as salaire_brute,
                            sum(salaire_net_a_payer) as salaire_net_a_payer,
                            sum(arrondi) as arrondi,
                            sum(deduction) as deduction
                    FROM    hr_payroll_ma_bulletin b
                            LEFT JOIN hr_payroll_ma pm ON pm.id=b.id_payroll_ma
                    where   b.id_payroll_ma = %s
                    ''' % (rec.id,)
            self.env.cr.execute(sql)
            data = self.env.cr.dictfetchall()
            data = data[0]
            move_line_arrondi = {
                'account_id': dictionnaire.salary_debit_account_id.id,
                # 'analytic_account_id': dictionnaire['analytic_account_id'][0],
                'journal_id': journal.id,
                'date': date,
                'name': 'Arrondi',
                'debit': data['arrondi'],
                'credit': 0,
            }

            move_line_credit = {
                'account_id': dictionnaire.salary_credit_account_id.id,
                'journal_id': journal.id,
                'date': date,
                'name': 'Salaire net a payer',
                'credit': data['salaire_net_a_payer'],
                'debit': 0,
            }
            salaire_brut_debit += data['arrondi']
            salaire_brut_credit += data['salaire_net_a_payer']
            move_lines.append((0, 0, move_line_arrondi))
            move_lines.append((0, 0, move_line_credit))

            # Salaire brute
            salaire_brut = salaire_brut_credit - salaire_brut_debit
            move_line_debit_brute = {
                'account_id': dictionnaire.salary_debit_account_id.id,
                # 'analytic_account_id': dictionnaire['analytic_account_id'][0],
                'journal_id': journal.id,
                'date': date,
                'name': 'Salaire brute',
                'debit': salaire_brut,
                'credit': 0,
            }
            move_lines.append((0, 0, move_line_debit_brute))

            move = {
                'ref': rec.number,
                'journal_id': journal.id,
                'date': date,
                'state': 'draft',
                'name': rec.name or '\\',
                'line_ids': move_lines}
            move_id = self.env['account.move'].create(move)
            rec.move_id = move_id
            return True


# Classe : Bulletin de paie
class hrPayrollMaBulletin(models.Model):
    _name = "hr.payroll.ma.bulletin"
    _description = 'bulletin'
    _order = "name, employee_id"

   # @api.one
    @api.constrains('period_id', 'employee_id')
    def _check_unicity_bulletin(self):
        payroll_bulletin_ids = self.env["hr.payroll.ma.bulletin"].search([('period_id', '=', self.period_id.id),
                                                                          ('employee_id', '=', self.employee_id.id)])
        if len(payroll_bulletin_ids) > 1:
            raise ValidationError(
                u'On ne peut pas avoir deux bulletin de paies pour la même période du même employé %s %s !' % (
                self.employee_id.name, self.employee_id.prenom))

    #@api.multi
    @api.depends('salaire_net_a_payer')
    def _get_amount_text(self):
        for rec in self:
            rec.salaire_net_a_payer_text = self.env.user.company_id.currency_id.amount_to_text(
                rec.salaire_net_a_payer).upper()

    name = fields.Char(string=u'Code', readonly=True)
    date_start = fields.Date(string=u'Date début', related='id_payroll_ma.date_start', store=True)
    date_end = fields.Date(string='Date fin', related='id_payroll_ma.date_end', store=True)
    date_salary = fields.Date(string='Date salaire', related='id_payroll_ma.date_salary', store=True)
    employee_id = fields.Many2one('hr.employee', string=u'Employé', required=True)
    period_id = fields.Many2one('date.range', related='id_payroll_ma.period_id', string=u'Période', store=True)
    salary_line_ids = fields.One2many('hr.payroll_ma.bulletin.line', 'id_bulletin', string='Lignes de salaire',
                                      readonly=True)
    employee_contract_id = fields.Many2one('hr.contract', string=u'Contrat de travail', required=True)
    id_payroll_ma = fields.Many2one('hr.payroll_ma', string=u'Réf Paie', ondelete='cascade')
    salaire_base = fields.Float(string='Salaire de base')
    salary_type = fields.Selection([('h', 'Horaire'),
                                    ('j', 'Journalier'),
                                    ('m', 'Mensuel')], required=True, default='m')
    taux_journalier = fields.Float(string='Taux journalier')
    normal_hours = fields.Float(string=u'Heures travaillées durant le mois')
    hour_base = fields.Float(string=u'Salaire horaire')
    comment = fields.Text(string=u'Informations complémentaires')
    salaire = fields.Float(string='Salaire de Base', readonly=True, digits=(16, 2))
    salaire_brute = fields.Float(string='Salaire brut', readonly=True, digits=(16, 2))
    salaire_brute_imposable = fields.Float(string='Salaire brut imposable', readonly=True, digits=(16, 2))
    salaire_net = fields.Float(string=u'Salaire Net', readonly=True, digits=(16, 2))
    salaire_net_a_payer = fields.Float(string=u'Salaire Net à payer', readonly=True, digits=(16, 2),
                                       help=u"Le salaire net moins les prêts ou avances")
    salaire_net_a_payer_text = fields.Char(compute='_get_amount_text', string='Salaire net à payer en lettres',
                                           store=True)
    salaire_net_imposable = fields.Float(string=u'Salaire Net Imposable', readonly=True, digits=(16, 2))
    cotisations_employee = fields.Float(string=u'Cotisations Employé', readonly=True, digits=(16, 2))
    cotisations_employer = fields.Float(string='Cotisations Employeur', readonly=True, digits=(16, 2))
    igr = fields.Float(string=u'Impot sur le revenu', readonly=True, digits=(16, 2))
    prime = fields.Float(string='Primes', readonly=True, digits=(16, 2))
    indemnite = fields.Float(string=u'Indemnités', readonly=True, digits=(16, 2))
    avantage = fields.Float(string='Avantages', readonly=True, digits=(16, 2))
    exoneration = fields.Float(string=u'Exonérations', readonly=True, digits=(16, 2))
    deduction = fields.Float(string=u'Déductions', readonly=True, digits=(16, 2))
    working_days = fields.Float(string=u'Jours travaillés', digits=(16, 2))
    prime_anciennete = fields.Float(string=u'Prime ancienneté', digits=(16, 2))
    frais_pro = fields.Float(string='Frais professionnels', digits=(16, 2))
    personnes = fields.Integer(string='Personnes')
    absence = fields.Float(string='Absences', digits=(16, 2))
    arrondi = fields.Float(string='Arrondi', digits=(16, 2))
    logement = fields.Float(string='Logement', digits=(16, 2))
    indemnites_frais_pro = fields.Float(string=u'Indemnités versées à titre de frais professionnels', readonly=True,
                                        digits=(16, 2))

    # Ajout des champs de cumul
    cumul_work_days = fields.Float(compute='get_cumuls', string=u'Cumul des JT', digits=(16, 2))
    cumul_sbi = fields.Float(compute='get_cumuls', string='Cumul SBI', digits=(16, 2))
    cumul_base = fields.Float(compute='get_cumuls', string='Cumul base', digits=(16, 2))
    cumul_sb = fields.Float(compute='get_cumuls', string='Cumul SB', digits=(16, 2))
    cumul_sni = fields.Float(compute='get_cumuls', string='Cumul SNI', digits=(16, 2))
    cumul_igr = fields.Float(compute='get_cumuls', string='Cumul IR', digits=(16, 2))
    cumul_ee_cotis = fields.Float(compute='get_cumuls', string=u'Cotisations employé', digits=(16, 2))
    cumul_er_cotis = fields.Float(compute='get_cumuls', string='Cotisations employeur', digits=(16, 2))
    cumul_fp = fields.Float(compute='get_cumuls', string='Frais professionnels', digits=(16, 2))
    cumul_avn = fields.Float(compute='get_cumuls', string=u'Avantages en nature', digits=(16, 2))
    cumul_exo = fields.Float(compute='get_cumuls', string=u'Exonérations', digits=(16, 2))
    cumul_avantages = fields.Float(compute='get_cumuls', string='Indemnités')
    cumul_indemnites_fp = fields.Float(compute='get_cumuls', string='Cumul Indemn. frais professionnels')

    company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.user.company_id,
                                 string='Société', readonly=True, copy=False)

    #@api.multi
    def get_bulletin_anterieur(self):
        self.ensure_one()
        bulletins = self.env['hr.payroll.ma.bulletin'].search([('date_salary', '<=', self.date_salary),
                                                               ('employee_id', '=', self.employee_id.id),
                                                               ('period_id.fiscal_year_id', '=',
                                                                self.period_id.fiscal_year_id.id)])
        return bulletins

    #@api.multi
    def get_cumuls(self):
        for res in self:
            bulletin_ids = res.get_bulletin_anterieur()
            res.cumul_base = sum(bulletin.salaire_base for bulletin in bulletin_ids)
            res.cumul_work_days = sum(bulletin.working_days for bulletin in bulletin_ids)
            res.cumul_sbi = sum(bulletin.salaire_brute_imposable for bulletin in bulletin_ids)
            res.cumul_sb = sum(bulletin.salaire_brute for bulletin in bulletin_ids)
            res.cumul_sni = sum(bulletin.salaire_net_imposable for bulletin in bulletin_ids)
            res.cumul_igr = sum(bulletin.igr for bulletin in bulletin_ids)
            res.cumul_ee_cotis = sum(bulletin.cotisations_employee for bulletin in bulletin_ids)
            res.cumul_er_cotis = sum(bulletin.cotisations_employer for bulletin in bulletin_ids)
            res.cumul_fp = sum(min(bulletin.frais_pro, 2500) for bulletin in bulletin_ids)
            res.cumul_avn = sum(bulletin.avantage for bulletin in bulletin_ids)
            res.cumul_exo = sum(bulletin.exoneration for bulletin in bulletin_ids)
            res.cumul_avantages = sum(bulletin.indemnite for bulletin in bulletin_ids)
            res.cumul_indemnites_fp = sum(bulletin.indemnites_frais_pro for bulletin in bulletin_ids)

        return True

    @api.model
    def _name_get_default(self):
        return self.env['ir.sequence'].next_by_code('hr.payroll.ma.bulletin')

    @api.onchange('employee_contract_id')
    def onchange_contract_id(self):
        contract = self.employee_contract_id
        if contract:
            self.salaire_base = contract.wage
            self.salary_type = contract.salary_type
            self.hour_base = contract.hour_salary
            self.normal_hours = contract.monthly_hour_number
            self.employee_id = contract.employee_id.id

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if not self.period_id:
            raise ValidationError(u"Vous devez d'abord spécifier une période !")
        if self.period_id and self.employee_id:
            if not self.employee_id.contract_id:
                return True
            else:
                days = self.id_payroll_ma.get_employees_leaves(self.employee_id)
                self.employee_contract_id = self.employee_id.contract_id.id
                self.salaire_base = self.employee_id.contract_id.wage
                self.hour_base = self.employee_id.contract_id.hour_salary
                self.normal_hours = self.employee_id.contract_id.monthly_hour_number
                self.working_days = 26 + days
                self.period_id = self.period_id.id
                self.salary_type = self.employee_id.contract_id.salary_type

    # Fonction pour la calcul de IR
    #@api.multi
    def get_ir(self, sbi, cotisations, logement):
        for bulletin in self:
            taux = 0
            somme = 0
            salaire_net_imposable = 0
            dictionnaire = bulletin.employee_id.get_parametres()
            if not bulletin.employee_contract_id.ir:
                res = {
                    'salaire_net_imposable': salaire_net_imposable,
                    'taux': 0,
                    'ir_net': 0,
                    'credit_account_id': dictionnaire.credit_account_id.id,
                    'frais_pro': 0,
                    'personnes': 0
                }
            else:
                base = 0
                nbr_jr = 0

                conge = bulletin.salary_line_ids.filtered(lambda r: r.rubrique_id and not r.rubrique_id.type)
                # print('ggggggrrrrr', conge.mapped('name'))
                if conge:
                    montant_conge = sum(line.base for line in conge)
                    nbr_jr = int(round(montant_conge * 26 / bulletin.salaire_base))
                if bulletin.working_days:
                    base = bulletin.working_days + nbr_jr
                elif bulletin.normal_hours:
                    base = bulletin.normal_hours / 8 + nbr_jr

                # Salaire Net Imposable
                fraispro = sbi * (dictionnaire.fraispro / 100)
                plafond = (dictionnaire.plafond * base) / 26
                print('ggggg', plafond, fraispro, base)
                salaire_net_imposable = sbi - cotisations - min(fraispro, plafond)
                # logement

                salaire_logement = salaire_net_imposable * 10 / 100

                salaire_net_imposable = salaire_net_imposable - min(logement, salaire_logement)

                # IR Brut
                ir_bareme = self.env['hr.payroll_ma.ir']
                ir_bareme_list = ir_bareme.search([])
                if base != 0:
                    sni = (salaire_net_imposable * 26 / base)
                else:
                    sni = 0
                for tranche in ir_bareme_list:
                    if (sni >= tranche.debuttranche / 12) and (sni < tranche.fintranche / 12):
                        taux = tranche.taux
                        somme = tranche.somme / 12
                ir_brute = ((sni * taux / 100) - somme) * base / 26
                # IR Net
                personnes = bulletin.employee_id.chargefam
                if (ir_brute - (personnes * dictionnaire.charge)) < 0:
                    ir_net = 0
                else:
                    ir_net = ir_brute - (personnes * dictionnaire.charge)

                res = {
                    'salaire_net_imposable': salaire_net_imposable,
                    'taux': taux,
                    'ir_net': ir_net,
                    'credit_account_id': dictionnaire.credit_account_id.id,
                    'frais_pro': fraispro,
                    'personnes': personnes
                }
                print('rrrrrr', res)
        return res

    def calc_seniority(self, date_embauche, date_paie):
        date_embauche = str(date_embauche).split('-')
        date_paie = str(date_paie).split('-')
        seniority_date = datetime.date(int(date_embauche[0]), int(date_embauche[1]), int(date_embauche[2]))
        date_paie = datetime.date(int(date_paie[0]), int(date_paie[1]), int(date_paie[2]))
        years = date_paie.year - seniority_date.year
        if date_paie.month < seniority_date.month or (
                date_paie.month == seniority_date.month and date_paie.day < seniority_date.day):
            years -= 1

        objet_anciennete = self.env['hr.payroll_ma.anciennete']
        liste = objet_anciennete.search([])
        if years > 0:
            for tranche in liste:
                if (years >= tranche.debuttranche) and (years < tranche.fintranche):
                    return tranche.taux
        else:
            return 0

    #@api.multi
    def compute_all_lines(self):
        for rec in self:
            dictionnaire = rec.employee_id.get_parametres()
            bulletin = rec
            rec.period_id = bulletin.id_payroll_ma.period_id.id
            # Delete bulletin lines
            sql = ''' DELETE from hr_payroll_ma_bulletin_line where id_bulletin = %s '''
            self.env.cr.execute(sql, (bulletin.id,))

            salaire_base_worked = 0
            cotisations_employee = cotisations_employer = 0
            prime = indemnite = avantage = 0
            exoneration = 0
            deduction = 0
            absence = 0
            arrondi = 0
            logement = bulletin.employee_id.logement

            # Salaire de base
            normal_hours = bulletin.normal_hours
            if bulletin.salary_type == 'm':
                salaire_base = bulletin.salaire_base
                rate = (bulletin.working_days / 26) * 100
                working = rate / 100
            elif bulletin.salary_type == 'j':
                salaire_base = bulletin.hour_base
                working = bulletin.working_days
                rate = bulletin.working_days
            else:
                salaire_base = bulletin.hour_base
                working = normal_hours
                rate = normal_hours

            if salaire_base:
                salaire_base_line = {
                    'name': 'Salaire de base',
                    'id_bulletin': bulletin.id,
                    'type': 'base',
                    'base': round(salaire_base, 2),
                    'rate_employee': rate,
                    'subtotal_employee': round(salaire_base * working, 2),
                    'deductible': False,
                    'sequence': 1
                }
                self.env['hr.payroll_ma.bulletin.line'].create(salaire_base_line)

                salaire_base_worked += round(salaire_base * working, 2)
                absence += salaire_base - (salaire_base * (bulletin.working_days / 26))
            # Rubriques majoration
            sql = '''
                    SELECT  l.montant,l.taux,r.name,r.categorie,r.type,r.formule,r.afficher,r.sequence,r.imposable,
                            r.plafond,r.ir,r.anciennete,r.absence,r.id,r.conge,r.credit_account_id, r.debit_account_id, r.is_hourly
                    FROM    hr_payroll_ma_ligne_rubrique l
                            LEFT JOIN hr_payroll_ma_rubrique r on (l.rubrique_id=r.id)
                    WHERE
                            l.id_contract=%s
                            AND (l.permanent=True OR l.date_start <= %s and l.date_stop >= %s)
                order by r.sequence
                '''
            self.env.cr.execute(sql, (bulletin.employee_contract_id.id,
                                      bulletin.period_id.date_start, bulletin.period_id.date_start,
                                      ))
            rubriques = self.env.cr.dictfetchall()

            ir = salaire_base_worked
            anciennete = 0
            for rubrique in rubriques:
                if rubrique['categorie'] == 'majoration':
                    # actualisation montant jours chômés payés & jours congés payés
                    taux = rubrique['taux']
                    montant = rubrique['montant']

                    # Rubriques par heure: Heures sup
                    if rubrique['is_hourly']:
                        if bulletin.salary_type == 'h':
                            taux_horaire = bulletin.employee_contract_id.hour_salary
                        elif bulletin.salary_type == 'j':
                            taux_horaire = bulletin.employee_contract_id.hour_salary * (
                                        bulletin.employee_contract_id.working_days_per_month or 26) / (
                                                       bulletin.employee_contract_id.monthly_hour_number or 191)
                        else:
                            taux_horaire = bulletin.salaire_base / (
                                        bulletin.employee_contract_id.monthly_hour_number or 191)

                        # Montant=Nb heure
                        # Taux: Par exemple: Heures sup 25%:  25%--125%
                        montant = montant * taux_horaire * taux / 100

                    if rubrique['absence']:
                        taux = bulletin.working_days / 26
                        montant = rubrique['montant'] * taux
                        taux = taux * 100
                        absence += rubrique['montant'] - montant

                    # Impact sur ancientte
                    if rubrique['anciennete']:
                        anciennete += montant

                    # Impact sur IR
                    if rubrique['ir']:
                        if rubrique['plafond'] == 0:
                            ir += montant
                        else:
                            ir += min(montant, rubrique['plafond'])

                    # Impact sur les cotisations
                    if not rubrique['imposable']:
                        if rubrique['plafond'] == 0:
                            exoneration += montant
                        else:
                            exoneration += min(rubrique['plafond'], montant)
                    print('ruuuuuuuuuub', rubrique['type'], rubrique['name'])
                    # type = 'majoration'
                    if rubrique['type'] == 'prime':
                        prime += montant
                    elif rubrique['type'] == 'indemnite':
                        indemnite += montant
                    elif rubrique['type'] == 'avantage':
                        avantage += montant
                    elif not rubrique['type']:
                        salaire_base_worked += montant
                        sequence = 2
                        # type = 'base'
                    if rubrique['type'] and not rubrique['imposable']:
                        sequence = 6
                    if rubrique['type'] and rubrique['imposable']:
                        sequence = 3

                    majoration_line = {
                        'name': rubrique['name'],
                        'id_bulletin': bulletin.id,
                        'type': 'majoration',
                        # 'type': type,
                        'base': rubrique['montant'],
                        'rate_employee': taux,
                        'subtotal_employee': montant,
                        'deductible': False,
                        'afficher': rubrique['afficher'],
                        'rubrique_id': rubrique['id'],
                        'credit_account_id': rubrique['credit_account_id'] or False,
                        'debit_account_id': rubrique['debit_account_id'] or False,
                        'sequence': sequence
                    }
                    self.env['hr.payroll_ma.bulletin.line'].create(majoration_line)

            # Ancienneté
            taux_anciennete = self.calc_seniority(self.employee_id.date, self.date_end) / 100
            prime_anciennete = (salaire_base_worked + anciennete) * taux_anciennete
            if taux_anciennete:
                anciennete_line = {
                    'name': 'Prime anciennete',
                    'id_bulletin': bulletin.id,
                    'type': 'anciennete',
                    'base': (salaire_base_worked + anciennete),
                    'rate_employee': taux_anciennete,
                    'subtotal_employee': prime_anciennete,
                    'deductible': False,
                    'sequence': 4
                }
                self.env['hr.payroll_ma.bulletin.line'].create(anciennete_line)
            # Cotisations
            salaire_brute = salaire_base_worked + prime + indemnite + avantage + prime_anciennete
            salaire_brute_imposable = salaire_brute - exoneration
            cotisations = bulletin.employee_contract_id.cotisation.cotisation_ids
            if bulletin.employee_id.affilie:
                for cot in cotisations:
                    if cot.plafonee:
                        base = min(cot.plafond, salaire_brute_imposable)
                    else:
                        base = salaire_brute_imposable
                    if cot.type == 'amount':
                        rate_employee = (cot.tauxsalarial / base or 100) * 100
                        rate_employer = (cot.tauxpatronal / base or 100) * 100
                        subtotal_employee = cot.tauxsalarial
                        subtotal_employer = cot.tauxpatronal
                    else:
                        rate_employee = cot.tauxsalarial
                        rate_employer = cot.tauxpatronal
                        subtotal_employee = base * cot.tauxsalarial / 100
                        subtotal_employer = base * cot.tauxpatronal / 100
                    cotisation_line = {
                        'name': cot.name,
                        'id_bulletin': bulletin.id,
                        'type': 'cotisation',
                        'base': base,
                        'rate_employee': rate_employee,
                        'rate_employer': rate_employer,
                        'subtotal_employee': subtotal_employee,
                        'subtotal_employer': subtotal_employer,
                        'credit_account_id': cot.credit_account_id.id,
                        'debit_account_id': cot.debit_account_id.id,
                        'deductible': True,
                        'cotisation_id': cot.id,
                        'sequence': 5
                    }
                    cotisations_employee += subtotal_employee
                    cotisations_employer += subtotal_employer
                    self.env['hr.payroll_ma.bulletin.line'].create(cotisation_line)

            # Impot sur le revenu
            res = rec.get_ir(ir + prime_anciennete, cotisations_employee, logement)
            if not res['ir_net'] == 0:
                ir_line = {
                    'name': 'Impot sur le revenu',
                    'id_bulletin': bulletin.id,
                    'type': 'ir',
                    'base': res['salaire_net_imposable'],
                    'rate_employee': res['taux'],
                    'subtotal_employee': res['ir_net'],
                    'credit_account_id': res['credit_account_id'],
                    'debit_account_id': res['credit_account_id'],
                    'deductible': True,
                    'sequence': 10
                }
                self.env['hr.payroll_ma.bulletin.line'].create(ir_line)

            # Rubriques Deduction
            for rubrique in rubriques:
                if rubrique['categorie'] == 'deduction':
                    deduction += rubrique['montant']
                    deduction_line = {
                        'name': rubrique['name'],
                        'id_bulletin': bulletin.id,
                        'rubrique_id': rubrique['id'],
                        'type': 'retenu',
                        'base': rubrique['montant'],
                        'rate_employee': 100,
                        'subtotal_employee': rubrique['montant'],
                        'deductible': True,
                        'afficher': rubrique['afficher'],
                        'credit_account_id': rubrique['credit_account_id'] or False,
                        'debit_account_id': rubrique['debit_account_id'] or False,
                        'sequence': 12
                    }
                    self.env['hr.payroll_ma.bulletin.line'].create(deduction_line)

            salaire_net = salaire_brute - res['ir_net'] - cotisations_employee
            salaire_net_a_payer = salaire_net - deduction

            # Arrondi
            if dictionnaire['arrondi']:
                arrondi = 1 - (round(salaire_net_a_payer, 2) - int(salaire_net_a_payer))
                if arrondi != 1:
                    arrondi = 1 - (salaire_net_a_payer - int(salaire_net_a_payer))
                    arrondi_line = {
                        'name': 'Arrondi',
                        'id_bulletin': bulletin.id,
                        'type': 'arrondi',
                        'base': arrondi,
                        'rate_employee': 100,
                        'subtotal_employee': arrondi,
                        'deductible': True,
                        'sequence': 13
                    }
                    self.env['hr.payroll_ma.bulletin.line'].create(arrondi_line)
                    salaire_net_a_payer += arrondi
                else:
                    arrondi = 0

            rec.salaire = salaire_base
            rec.salaire_brute = salaire_brute
            rec.salaire_brute_imposable = salaire_brute_imposable
            rec.salaire_net = salaire_net
            rec.salaire_net_a_payer = salaire_net_a_payer
            rec.salaire_net_imposable = res['salaire_net_imposable']
            rec.cotisations_employee = cotisations_employee
            rec.cotisations_employer = cotisations_employer
            rec.igr = res['ir_net']
            rec.prime = prime
            rec.indemnite = indemnite
            rec.avantage = avantage
            rec.deduction = deduction
            rec.prime_anciennete = prime_anciennete
            rec.exoneration = exoneration
            rec.absence = absence
            rec.frais_pro = res['frais_pro']
            rec.personnes = res['personnes']
            rec.arrondi = arrondi
            rec.logement = bulletin.employee_id.logement


# Rubrique
class HrRubrique(models.Model):
    _name = "hr.payroll_ma.rubrique"
    _description = "rubrique"

    name = fields.Char(string='Nom', required="True")
    code = fields.Char(string='Code', required=False, readonly=False)
    categorie = fields.Selection(selection=(('majoration', 'Majoration'),
                                            ('deduction', 'Deduction')), string=u'Catégorie', default='majoration')
    sequence = fields.Integer('Sequence', help=u"Ordre d'affichage dans le bulletin de paie", default=1)
    type = fields.Selection(selection=(('prime', 'Prime'),
                                       ('indemnite', u'Indemnité'),
                                       ('avantage', 'Avantage')), string='Type', default='prime')
    plafond = fields.Float(string=u'Plafond exonéré', default=0.0)
    formule = fields.Char(string='Formule', required=False, help='''
                    Pour les rubriques de type majoration, on utilise les variables suivantes :
                    salaire_base : Salaire de base
                    hour_base : Salaire horaire
                    normal_hours : Les heures normales
                    working_days : Jours travaillés (imposable)
        ''')
    imposable = fields.Boolean(string='Imposable', default=False)
    afficher = fields.Boolean(string='Afficher', help='Afficher cette rubrique sur le bulletin de paie', default=True)
    ir = fields.Boolean(string='IR', required=False)
    anciennete = fields.Boolean(string=u'Ancienneté')
    absence = fields.Boolean(string='Absence')
    conge = fields.Boolean(string=u'Congé')
    note = fields.Text(string='Commentaire')
    credit_account_id = fields.Many2one('account.account', string=u'Compte de crédit')
    debit_account_id = fields.Many2one('account.account', string=u'Compte de débit')
    company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.user.company_id,
                                 string='Société', readonly=True, copy=False)
    is_hourly = fields.Boolean(u'Par Heure?', default=False)
    pourcentage = fields.Float(u'Pourcentage')
    heures_sup = fields.Selection((('0', '0%'), ('25', '25%'), ('50', '50%'),
                                   ('100', '100%')), string='Valeur heures sup')
    jrs_conge_paye = fields.Boolean('Jour congé payé?')
    type_traitement = fields.Selection([('standard', 'Standard'), ('heure_sup', u'Heures supplémentaires')],
                                       default='standard', string="Type de traitement")


# Classe : Ligne rubrique
class HrLigneRubrique(models.Model):
    _name = "hr.payroll_ma.ligne_rubrique"
    _description = "Ligne Rubrique"
    _order = 'date_start'

    rubrique_id = fields.Many2one('hr.payroll_ma.rubrique', string='Rubrique')
    id_contract = fields.Many2one('hr.contract', string=u'Contrat', ondelete='cascade')
    montant = fields.Float(string='Montant')
    taux = fields.Float(string='Taux')
    period_id = fields.Many2one('date.range', domain="[('type_id.fiscal_period','=',True)]", string=u'Période')
    permanent = fields.Boolean(string='Rubrique Permanente')
    date_start = fields.Date(string=u'Date début')
    date_stop = fields.Date(string='Date fin')
    note = fields.Text(string='Commentaire')

   # @api.multi
    @api.constrains('date_stop')
    def _check_date(self):
        for rec in self:
            if rec.date_start > rec.date_stop:
                raise ValidationError(u'La Date début doit être inférieur à la date de fin')
            return True

   # @api.multi
    @api.onchange('rubrique_id')
    def onchange_rubrique_id(self):
        for rec in self:
            if rec.rubrique_id:
                rec.montant = rec.rubrique_id.plafond
                if rec.rubrique_id.is_hourly and rec.rubrique_id.pourcentage:
                    rec.taux = rec.rubrique_id.pourcentage
                else:
                    rec.taux = 0

    @api.onchange('period_id')
    def onchange_period_id(self):
        self.date_start = self.period_id.date_start
        self.date_stop = self.period_id.date_end


class HrPayrollMaBulletinLine(models.Model):
    _name = "hr.payroll_ma.bulletin.line"
    _description = "Ligne de salaire"
    _order = 'sequence'

    name = fields.Char(string='Description', required=True)
    id_bulletin = fields.Many2one('hr.payroll.ma.bulletin', string='Bulletin', ondelete='cascade')
    date_salary = fields.Date(related='id_bulletin.date_salary', store=True)
    period_id = fields.Many2one('date.range', related='id_bulletin.period_id', store=True)
    employee_id = fields.Many2one('hr.employee', related="id_bulletin.employee_id", store=True, string=u'Employé')
    matricule = fields.Char(related="employee_id.matricule", store=True, string=u'Matricule')
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", store=True,
                                    string=u'Département')
    job_id = fields.Many2one('hr.job', related="employee_id.job_id", store=True, string=u'Poste')
    type = fields.Selection(selection=[('other', 'Autre'),
                                       ('retenu', 'Retenue'),
                                       ('cotisation', 'Cotisation'),
                                       ('majoration', 'Majoration'),
                                       ('ir', 'IR'),
                                       ('brute', 'Salaire brut'),
                                       ('base', 'Salaire de base'),
                                       ('anciennete', 'Ancienneté'),
                                       ('arrondi', 'Arrondi')],
                            string='Type')
    credit_account_id = fields.Many2one('account.account', string=u'Compte crédit')
    debit_account_id = fields.Many2one('account.account', string=u'Compte Débit')
    base = fields.Float(string='Base', required=True, digits=(16, 2))
    subtotal_employee = fields.Float(string=u'Montant Employé', digits=(16, 2))
    subtotal_employer = fields.Float(string='Montant Employeur', digits=(16, 2))
    rate_employee = fields.Float(string=u'Taux Employé', digits=(16, 2))
    rate_employer = fields.Float(string='Taux Employeur', digits=(16, 2))
    note = fields.Text(string='Notes')
    deductible = fields.Boolean(string=u'Déductible', default=False)
    afficher = fields.Boolean(string='Afficher', default=True)
    rubrique_id = fields.Many2one('hr.payroll_ma.rubrique', 'Rubrique')
    cotisation_id = fields.Many2one('hr.payroll_ma.cotisation', 'Cotisation')
    sequence = fields.Integer('Sequence', default=1)
    company_id = fields.Many2one('res.company', related='id_bulletin.company_id', store=True)
