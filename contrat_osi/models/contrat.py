from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
# class employee(models.Model):
#     _inherit = 'hr.employee'
#
#     année_ancienneté = fields.Integer(string="année ancienneté")
#     année_globale = fields.Integer(string="globale ancienneté")
#     année_ancienneté2 = fields.Char(string="année ancienneté")
#     ancienneté_négociée = fields.Integer(string="ancienneté négociée")
#     date_start_z = fields.Date('Start Date', required=True, default=fields.Date.today,index=True)
#
#
#     def anne_aanciennete(self):
#         today = fields.Date.today()
#
#
#         for cant in self:
#             renew_date = fields.Date.from_string(cant.date_start_z)
#             renew_date2 = fields.Date.from_string(cant.first_contract_date)
#
#             d = cant.date_start_z
#             d2= cant.first_contract_date
#             g = renew_date - today
#
#             date = str(g)
#             #diff = (d.date() - d2.date())
#             datee = date.split("days")[0]
#             # ittt = int(datee)
#             # date2 =  ittt / 360
#             #
#             cant.année_ancienneté2 = datee
#             if cant.année_ancienneté2 :
#                 cant.année_ancienneté = int(cant.année_ancienneté2) / 360
#
#
#             cant.année_globale = cant.année_ancienneté + cant.ancienneté_négociée
#
#
#             _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', datee)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# class settings(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     Age_la_retraite = fields.Integer()
#
#     délai_notification = fields.Integer(string='délai notification de Age à la retraite')
#     délai_notification_essai = fields.Integer(string='délai notification de période d essaie')
#
#
#     def set_values(self):
#         super(settings, self).set_values()
#         self.env['ir.config_parameter'].sudo().set_param(
#             "contrat_osi.Age_la_retraite", self.Age_la_retraite)
#         self.env['ir.config_parameter'].sudo().set_param(
#             "contrat_osi.délai_notification", self.délai_notification)
#         self.env['ir.config_parameter'].sudo().set_param(
#             "contrat_osi.délai_notification_essai", self.délai_notification_essai)
#
#
#     @api.model
#     def get_values(self):
#         res = super(settings, self).get_values()
#         get_param = self.env['ir.config_parameter'].sudo().get_param
#         res['Age_la_retraite'] = int(get_param('contrat_osi.Age_la_retraite'))
#         res['délai_notification'] = int(get_param('contrat_osi.délai_notification'))
#         res['délai_notification_essai'] = int(get_param('contrat_osi.délai_notification_essai'))
#         return res
#
#
#     # def set_values(self):
#     #     res = super(settings_test, self).set_values()
#     #
#     #     self.env['ir.config_parameter'].sudo().set_param(
#     #         "hr_resignation.no_of_days", self.Age_la_retraite)
#     #
#     #     return  res
#     # @api.model
#     # def get_values(self):
#     #     res = super(settings_test, self).get_values()
#     #     test = self.env['ir.config_parameter'].sudo()
#     #     Age_la_retraite = int(test.get_param('contrat_osi.Age_la_retraite'))
#     #     #res['no_of_days'] = int(get_param('hr_resignation.no_of_days'))
#     #     res.update(
#     #         Age_la_retraite= Age_la_retraite,
#     #
#     #     )
#     #
#     #     return res
#
# # def compute_age(self):
#     #     emploiye = self.env['hr.employee'].search()
#     #
#     #     for rc in emploiye:
#     #         if rc.age == self.Age_la_retraite:
#     #             date_de_retraite = rc.birthday + relativedelta(years=rc.age)
#     #             date_notification_retrite = date_de_retraite - timedelta(days=self.délai_notification)
#     #             user_id = rc.create_uid.id
#     #             ext = self.env.ref('contrat_osi.model_hr_employee').id
#     #             self.activity_ids.create(
#     #                 {'activity_type_id': 4, 'res_id': self.rc.id, 'user_id': user_id,
#     #                  'res_model_id': ext,
#     #                  'date_deadline': date_notification_retrite,
#     #                  'note': 'le cheque valider'
#     #                  })


class categorie2(models.Model):
    _inherit = 'hr.contract'
    bool_test = fields.Boolean('bool_test', default=True)

    # def priode_esai(self):
    #     self.write({'state_cantrat': 'RN'
    #                 })
    #     self.write({'bool_test': False
    #                 })
    #     if self.bool_période2 == True:
    #
    #         if self.contract_type_id.name == "contrat à durée indéterminée (CDI)":
    #             if self.duree_essai > self.période.Duree:
    #                 self.bool_test = False
    #                 self.write({'state_cantrat': 'RN'
    #                             })
    #                 self.write({'bool_test': False
    #                             })
                    #raise ValidationError(_('ne peux pas dépasse priode essai  initiale.'))
    #
    @api.onchange('duree_essai')
    @api.depends('duree_essai')
    #fonction pour test duree_essai suprieure aduree sur le loi

    def function_duree_essai(self):

        for r in self:
            if r.contract_type_id.name == "contrat à durée déterminée (CDD)" :
                if self.duree_essai > 32:
                    raise ValidationError(_('ne peux pas depasse un mois de priode essai '))


            if r.contract_type_id.name == "contrat à durée indéterminée (CDI)" and r.bool_période2 == True:
                r.int_r = r.période.Duree
                if r.duree_essai >  r.période.Duree:
                    self.bool_test = False
                    raise ValidationError(_('ne peux pas dépasse priode essai  initiale.'))

                    self.write({'bool_test': False
                                })
                    r.bool_test = False
            # if r.contract_type_id.name == "contrat à durée indéterminée (CDI)" and r.bool_période2 == False:
            #     r.int_r = r.période.Duree*2
            #     if r.duree_essai > r.int_r:
            #         self.bool_test = False
            #         raise ValidationError(_('ne peux pas dépasse priode essai  initiale.'))
            #
            #         self.write({'bool_test': False
            #                     })
            #         r.bool_test = False

    @api.onchange('duree_preavie')
    @api.depends('duree_preavie')
    def function_duree_preavis(self):
        # fonction pour test preavis_essai suprieure aduree sur le loi

        for r in self:
            if r.contract_type_id.name == "contrat à durée indéterminée (CDI)" and r.bool_période2 == True:
                r.int_r = r.période.Duree
                if r.duree_preavie > r.preavis.Duree:
                    self.bool_test = False
                    raise ValidationError(_('ne peux pas dépasse priode essai  initiale.'))

                    self.write({'bool_test': False
                                })
                    r.bool_test = False

            # if r.contract_type_id.name == "contrat à durée indéterminée (CDI)" and r.bool_période2 == False:
            #     r.int_r = r.période.Duree * 2
            #     if r.duree_preavie > r.int_r:
            #         self.bool_test = False
            #         raise ValidationError(_('ne peux pas dépasse priode essai  initiale.'))
            #
            #         self.write({'bool_test': False
            #                     })
            #         r.bool_test = False

    #
    # def write(self, vals_list):
    #     res = super(categorie2, self).write(vals_list)
    #     for rec in res:
    #
    #         rec.tttttttttttttttt()
    #
    #
    #         #     for rc in self:
    #
    #
    #
    #         return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(categorie2, self).create(vals_list)

        for rec in res:
            rec.int_r = rec.période.Duree


            rec.CALCULE_duree()
            rec.période_essai()



            #     for rc in self:

            if rec.bool_période2 == True:


                if rec.contract_type_id.name == "contrat à durée indéterminée (CDI)":
                    if rec.duree_essai > rec.période.Duree:
                        raise ValidationError(_('ne peux pas dépasse priode essai  initiale.'))
                        rec.int_r = rec.duree_essai
                        rec.bool_test = False
                    if rec.duree_preavie > rec.preavis.Duree:
                        raise ValidationError(_('ne peux pas dépasse priode essai  initiale.'))
                        rec.int_r = rec.duree_essai
                        rec.bool_test = False

            #         # if rec.Employee_Category.name == 'employés':
                    #
                    #
                    #     if rec.mois_essai > rec.période.mois_essai :
                    #         raise ValidationError(_('NE PEUX PAS DEPASSE CONTRAT CDD UN AN .'))
                    #
                    # if rec.Employee_Category.name == 'cadres et assimilés':
                    #
                    #     if rec.mois_essai > rec.période.mois_essai:
                    #         raise ValidationError(_('NE PEUX PAS DEPASSE CONTRAT CDD UN AN .'))
                    #
                    # if rec.Employee_Category.name == 'ouvriers':
                    #
                    #     if rec.mois_essai > rec.période.mois_essai:
                    #         raise ValidationError(_('NE PEUX PAS DEPASSE CONTRAT CDD UN AN .'))

            if not rec.rounouv:

                # vals.get('probability', 0) >= 100
                if rec.Duree >= 361:
                    raise ValidationError(_('ne peux pas cree un cantrat cdd pour une durée plus un an.'))
            return rec




class categorie(models.Model):
    _inherit = 'hr.contract'
    Employee_Category = fields.Many2one('category1em', string="Employee Category",
                             tracking=True)

    raison = fields.Many2one('raison', string="raison", domain="[('contrat_type_raison', '=', contract_type_id)]",tracking=True)
    preavis = fields.Many2one('preavis', string="preavis",
                              domain="[('contrat_type_pr', '=', contract_type_id)]")
    période = fields.Many2one('priode', string="Période essai",
                              domain="[('contrat_type_priod', '=', contract_type_id)]" , store=True,tracking=True)
    Renouvellement_période_essai = fields.Char(string="Renouvellement de la période essai ",tracking=True)
    bool_période = fields.Boolean('ttttt', default=False, store=True)
    bool_période2 = fields.Boolean('testttttt', default=False, store=True)

    type = fields.Many2one(
        'type',
        string='type', domain="[('contrat_type_type', '=', contract_type_id)]",tracking=True
    )
    date_start = fields.Date('Start Date', required=True, default=fields.Date.today, tracking=True,
        help="Start date of the contract.", index=True)
    date_end = fields.Date('End Date', tracking=True,
        help="End date of the contract (if it's a fixed-term contract).")
    date_validation = fields.Date('date validation',compute='invisibility',store=True)
    contract_type_id = fields.Many2one('hr.contract.type', "Contract Type",tracking=True)


    nombre_h = fields.Char(string='Contrat à temps partiel nombre d’heure',tracking=True)
    Duree = fields.Integer(string='Durée ',tracking=True,compute='coputeduree',store=True)
    duree_essai = fields.Integer(string='duree_essai ',tracking=True,compute='coputeduree_essai',store=True)
    duree_preavie = fields.Integer(string='duree_essai ',tracking=True,compute='coputeduree_preavie',store=True)
    int_r = fields.Integer( store=True)
    date_fin_priode_essai = fields.Date(string='date de fin de période essai ',store=True,tracking=True)
    mois = fields.Integer(string='mois ',tracking=True,store=True)
    jours = fields.Integer(string='jours ',tracking=True,store=True)
    mois_essai = fields.Integer(string='mois ' ,tracking=True,store=True)
    jours_essai = fields.Integer(string='jours ', tracking=True,store=True)
    mois_preavie = fields.Integer(string='mois ', tracking=True, store=True)
    jours_preavie  = fields.Integer(string='jours ', tracking=True, store=True)

    duree_type = fields.Selection([('A', "jours"), ('B', "mois"), ('C', "annes")], default='A',tracking=True)
    invisibi = fields.Selection([('AA', "A"), ('BB', "B"), ('CB', "C")], default='AA',compute='invisibility',store=True)
    state_cantrat = fields.Selection([('CR', "create"), ('MD', "modification"), ('TR', "transformation"), ('RN', "renouvellement")], default='CR',tracking=True)
    rounouv = fields.Boolean('ttttt', default=False,store=True)
    bool_type = fields.Boolean('Active', default=True,compute='type_fanction',store=True)
    transformation = fields.Boolean('Active', default=True)
    test_write = fields.Boolean('write', default=True,store=True)
    date_tesssst = fields.Datetime()
    contract_type_id = fields.Many2one('hr.contract.type', "Contract Type", tracking=True)
    périodicité  = fields.Selection([('hebdomadaire', "hebdomadaire"),('heure', "horaire"), ('journalier', "journalier"), ('quinzaine', "quinzaine"), ('mensuelle', "mensuelle")],tracking=True)




    def compute_priode_essai(self):
        emploiye = self.env['hr.employee'].search([])
        config = self.env['res.config.settings'].search([])
        today = fields.Date.today()
        len_C =int(len(config)-1)
        list = []

        for rc in config:
            list.append(rc)
            if rc.délai_notification:
                _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', list)


        #conf = list[len_C]


        #_logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', conf.Age_la_retraite)
        for rc in emploiye:

            if 1:

                date_de_retraite = self.employee_id.birthday + relativedelta(years=int(rc.age))
                #date_notification_PRIODE = self.date_fin_priode_essai - timedelta(days=conf.délai_notification)
                if 1:
                    user_id = self.employee_id.create_uid.id
                    ext = self.env.ref('hr.model_hr_employee').id
                    self.activity_ids.create(
                        {'activity_type_id': 4, 'res_id': self.employee_id.id, 'user_id': user_id,
                         'res_model_id': ext,
                         'date_deadline': self.date_fin_priode_essai,
                         'note': 'le cheque valider'
                         })

                    # exp_date = fields.Date.from_string(i.expiry_date) - timedelta(days=i.before_days)
                    # if date_now == exp_date or date_now == i.expiry_date:  # on Expire date and few days(As it set) before expire date
                    #     print('mail send started before few')
                    # mail_content = "  Hello  " + i.employee_ref.name + ",<br>Your Document " + i.name + \
                    #                " is going to expire on " + str(i.expiry_date) + \
                    #                ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('délai notification de prioe essai') ,
                        'author_id': self.env.user.partner_id.id,
                        'body_html': 'mail_content',
                        'email_to': self.hr_responsible_id.id,
                    }
                    self.env['mail.mail'].create(main_content).send()








    def compute_age(self):
        emploiye = self.env['hr.employee'].search([])
        config = self.env['res.config.settings'].search([])
        today = fields.Date.today()
        len_C =int(len(config)-1)
        list = []

        for rc in config:
            list.append(rc)
            if rc.Age_la_retraite:
                _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', list)


        conf = list[len_C]


        _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', conf.Age_la_retraite)
        for rc in emploiye:

            if int(rc.age)  == conf.Age_la_retraite:

                date_de_retraite = self.employee_id.birthday + relativedelta(years=int(rc.age))
                date_notification_retrite = date_de_retraite - timedelta(days=conf.délai_notification)
                if date_notification_retrite == today:
                    user_id = self.employee_id.create_uid.id
                    ext = self.env.ref('hr.model_hr_employee').id
                    self.activity_ids.create(
                        {'activity_type_id': 4, 'res_id': self.employee_id.id, 'user_id': user_id,
                         'res_model_id': ext,
                         'date_deadline': date_de_retraite,
                         'note': 'le cheque valider'
                         })

                    # exp_date = fields.Date.from_string(i.expiry_date) - timedelta(days=i.before_days)
                    # if date_now == exp_date or date_now == i.expiry_date:  # on Expire date and few days(As it set) before expire date
                    #     print('mail send started before few')
                    # mail_content = "  Hello  " + i.employee_ref.name + ",<br>Your Document " + i.name + \
                    #                " is going to expire on " + str(i.expiry_date) + \
                    #                ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('délai notification de Age à la retraite') ,
                        'author_id': self.env.user.partner_id.id,
                        'body_html': 'mail_content',
                        'email_to': self.hr_responsible_id.id,
                    }
                    self.env['mail.mail'].create(main_content).send()

        #
        # for v in list:
        #     _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', v[5])
        #

            #
            #
            #
            # if rc.age  == config.Age_la_retraite:
            #     date_de_retraite = self.employee_id.birthday + relativedelta(years=5)
            #     date_notification_retrite = date_de_retraite - timedelta(days=6)
            #     user_id = self.employee_id.create_uid.id
            #     ext = self.env.ref('hr.model_hr_employee').id
            #     self.activity_ids.create(
            #         {'activity_type_id': 4, 'res_id': self.employee_id.id, 'user_id': user_id,
            #          'res_model_id': ext,
            #          'date_deadline': date_de_retraite,
            #          'note': 'le cheque valider'
            #          })

        # for rc in emploiye:
        #     for v in config:
        #         if rc.age == v.Age_la_retraite:
        #


    #
    # def statecantrat(self):
    #     self.bool_type = False



    def write(self, vals_list):

        if 'contract_type_id' in vals_list and self.transformation == True:
            raise ValidationError(_('ne peux pas modifier .'))
        if 'date_start' in vals_list and self.transformation == True:
            raise ValidationError(_('ne peux pas modifier .'))
        if 'raison' in vals_list and self.transformation == True:
            raise ValidationError(_('ne peux pas modifier .'))
        if self.bool_test == False:
            raise ValidationError(_('ne peux pas modifier .'))

        for rc in self:
            if rc.test_write == False:
                raise ValidationError(_('ne peux pas modifier  priode essai  initiale.'))

            if rc.transformation == True and rc.rounouv == False:
                vals_list['state_cantrat'] = 'MD'

            #
            #     if 'contract_type_id' in vals_list and  rc.contract_type_id.name == "contrat à durée indéterminée (CDI)":
            #        if  'duree_essai' in vals_list and  rc.bool_test == True:
            #            raise ValidationError(_('ne peux pas dépasse priode essai  initiale.'))

        res = super(categorie, self).write(vals_list)

        return res










    @api.model_create_multi
    def create(self, vals_list):

        for rec in vals_list:






            contrat_cdd = self.env['hr.contract.type'].search(
                [('name', '=', 'contrat à durée déterminée (CDD)')]).id
            cantr = self.env['hr.contract'].search(
                [('employee_id', '=', rec.get('employee_id')), ('contract_type_id', '=', contrat_cdd)])
            _logger.info('Device  is now disconnected zzzzzzzzzzzzzzzzzzzz%s', cantr)
            for rc in cantr:
                if rec.get('raison') != False:


                    _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', rec.get('raison'))
                    if rec.get('raison') == rc.raison.id:
                        raise ValidationError(_('change raison.'))



            contrat_cdi = self.env['hr.contract.type'].search(
                [('name', '=', 'contrat à durée indéterminée (CDI)')]).id
            _logger.info('Device  is now disconnected zzzzzzzzzzzzzzzzzzzz%s',contrat_cdi)

            TEST = self.env['hr.contract'].search(
                [('state', '=', 'open'), ('employee_id', '=', rec.get('employee_id'))])
            if TEST:
                raise ValidationError(_('You cannot create CANTRAT.'))
        res = super(categorie, self).create(vals_list)
        self.CALCULE_duree()
        self.période_essai()



        return res





    @api.onchange('Duree')

    @api.depends('Duree')
    def cdd(self):
        if self.contract_type_id.name == "contrat à durée déterminée (CDD)":


            if self.Duree > 180 or self.Duree == 180:
                self.mois_essai = 1
                self.jours_essai = 0
                if self.duree_essai > 32:
                    raise ValidationError(_('ne peux pas depasse un mois de priode essai '))


            elif self.Duree < 180:
                duree = self.Duree / 7
                _logger.info('Device  is now disconnected UUUUUUUUUUUUUUUUUUUUUUUUUUUU%s', duree)
                Madate = str(duree)
                Liouma = Madate.split(".")[0]
                str2 = Madate.split(".")[1]
                self.jours_essai = int(Liouma)
                if self.jours_essai > 14 :
                    self.jours_essai = 14
            if self.Duree > 363:
                raise ValidationError(_('ne peux pas depasse un mois de priode essai '))






    @api.onchange('Employee_Category')

    @api.depends('Employee_Category')
    def tttt(self):
        CDI = self.env.ref('contrat_osi.hr_ctr_type_cdi')
        record1 = self.env.ref('contrat_osi.record1')
        record2 = self.env.ref('contrat_osi.record2')
        record3 = self.env.ref('contrat_osi.record3')

        if self.contract_type_id == CDI:

            if self.Employee_Category == record1:

                self.période =  self.env['priode'].search(
                    [('name', '=', '1,5 mois')])

                self.mois_essai = self.période.mois_essai
                self.jours_essai = self.période.jours_essai
                self.int_r = self.période.Duree
                if self.employee_id.année_globale <= 1:
                    self.preavis =  self.env['preavis'].search(
                        [('name', '=', '8 jours')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                if self.employee_id.année_globale >= 1 and self.employee_id.année_globale <= 5:
                    self.preavis = self.env['preavis'].search(
                        [('name', '=', '1 mois')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                if self.employee_id.année_globale >= 5:
                    self.preavis = self.env['preavis'].search(
                        [('name', '=', '2 mois')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                # if self.Duree> 12:
                #     raise ValidationError(_('NE PEUX PAS DEPASSE CONTRAT CDD UN AN .'))


            if self.Employee_Category == record2:

                self.période = self.env['priode'].search(
                    [('name', '=', '3 mois')])

                self.mois_essai = self.période.mois_essai
                self.jours_essai = self.période.jours_essai
                self.int_r = self.période.Duree

                if self.employee_id.année_globale < 1:
                    self.preavis = self.env['preavis'].search(
                        [('name', '=', '1 mois')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                if self.employee_id.année_globale > 1 and self.employee_id.année_globale < 5:
                    self.preavis = self.env['preavis'].search(
                        [('name', '=', '2 mois')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                if self.employee_id.année_globale > 5:
                    self.preavis = self.env['preavis'].search(
                        [('name', '=', '3 mois')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                #
            if self.Employee_Category == record3:

                self.période = self.env['priode'].search(
                    [('name', '=', '15 jours')])

                self.mois_essai = self.période.mois_essai
                self.jours_essai = self.période.jours_essai
                self.int_r = self.période.Duree

                #VAR = max(self.employee_id.année_ancienneté, self.employee_id.ancienneté_négociée)
                if self.employee_id.année_globale < 1:
                    self.preavis = self.env['preavis'].search(
                        [('name', '=', '8 jours')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                if self.employee_id.année_globale > 1 and self.employee_id.année_globale < 5:
                    self.preavis = self.env['preavis'].search(
                        [('name', '=', '1 mois')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                if self.employee_id.année_globale > 5:
                    self.preavis = self.env['preavis'].search(
                        [('name', '=', '2 mois')])

                    self.mois_preavie = self.preavis.mois_essai
                    self.jours_preavie = self.preavis.jours_essai
                #
            #self.période_essai()
            #self.date_fin_priode_essai = self.date_start + timedelta(days=self.duree_essai)

    @api.depends('jours_essai')
    @api.onchange('mois_essai')
    @api.depends('mois_essai')
    @api.onchange('jours_essai')
    def coputeduree_essai(self):
        for rc in self:
            # m = rc.mois_essai * 30
            # #
            # rc.duree_essai = m + rc.jours_essai
            Madate = str(self.date_start)
            Liouma = Madate.split("-")[2]
            moit_test = Madate.split("-")[1]
            num = int(moit_test)

            if num == 1 or num == 3 or num == 5 or num == 7 or num == 8 or num == 10 or num == 12:
                m = rc.mois_essai * 31
                #
                rc.duree_essai = m + rc.jours_essai
            elif num == 2:
                m = rc.mois_essai * 29
                #
                rc.duree_essai = m + rc.jours_essai
            elif num == 4 or num == 6 or num == 9 or num == 11:
                m = rc.mois_essai * 30
                #
                rc.duree_essai = m + rc.jours_essai


    @api.depends('mois_preavie')
    @api.depends('jours_preavie')
    @api.onchange('mois_preavie')
    @api.onchange('jours_preavie')
    def coputeduree_preavie(self):
        for rc in self:
            Madate = str(self.date_start)
            Liouma = Madate.split("-")[2]
            moit_test = Madate.split("-")[1]
            num = int(moit_test)

            if num == 1 or num == 3 or num == 5 or num ==7 or num == 8 or num == 10 or num ==12:
                m = rc.mois_preavie * 31
                #
                rc.duree_preavie = m + rc.jours_preavie
            elif  num == 2:
                m = rc.mois_preavie * 29
                #
                rc.duree_preavie = m + rc.jours_preavie
            elif num == 4 or num ==  6 or num == 9 or num == 11 :
                m = rc.mois_preavie * 30
                #
                rc.duree_preavie = m + rc.jours_preavie

    @api.depends('mois')
    @api.onchange('mois')
    @api.depends('jours')
    @api.onchange('jours')
    def coputeduree(self):
        for rc in self:
            # m = rc.mois * 31
            # #
            # rc.Duree = m + rc.jours
            Madate = str(self.date_start)
            Liouma = Madate.split("-")[2]
            moit_test = Madate.split("-")[1]
            num = int(moit_test)
            if  num == 7 :
                _logger.info('Device  is now disconnected kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk%s', moit_test)
                m = rc.mois * 31
                #
                rc.Duree = m + rc.jours
            elif num == 2:
                m = rc.mois * 29
                #
                rc.Duree = m + rc.jours
            elif num == 4 or num == 6 or num == 9 or num == 11:
                m = rc.mois * 30
                #
                rc.Duree = m + rc.jours
            rc.CALCULE_duree()
            rc.CALCULE_duree()



    def CALCULE_duree(self):

        if self.contract_type_id.name == "contrat à durée déterminée (CDD)":
            m = self.mois * 30
            #
            self.Duree  = m + self.jours
            if self.jours:


                self.date_end = self.date_start + timedelta(days=self.jours) - timedelta(days=1)
            if self.mois:
                self.date_end = self.date_start + relativedelta(months=self.mois) - timedelta(days=1)

                # if self.Duree> 12:
                #     raise ValidationError(_('NE PEUX PAS DEPASSE CONTRAT CDD UN AN .'))

            if self.mois and self.jours:

                self.date_end = self.date_start + relativedelta(months=self.mois) + timedelta(days=self.jours) - timedelta(days=1)


                # if self.Duree> 1:
                #     raise ValidationError(_('NE PEUX PAS DEPASSE CONTRAT CDD UN AN .'))

            self.teeeest()
            self.période_essai()

    def période_essai(self):
        if self.duree_essai:


          self.date_fin_priode_essai = self.date_start + timedelta(days=self.duree_essai)

    def FUNCRenouvellement_période_essai(self):
        var = self.duree_essai
        self.bool_période2 = False
        if self.date_fin_priode_essai  and self.bool_période2 == False:


            self.jours_essai = self.jours_essai *2
            self.mois_essai = self.mois_essai *2
            rounev = self.duree_essai *2
            self.date_fin_priode_essai = self.date_start + timedelta(days=rounev)



            self.bool_période = True


    def button_transformation(self):
        self.transformation = False
        self.write({'state_cantrat': 'TR'
                    })
        self.cloturer_contrat()

        return {
            'name': _('transformation'),
            'view_mode': 'form',
            'res_model': 'transformation',
            'view_id': self.env.ref('contrat_osi.view_wizard').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_contrat_type': self.contract_type_id.id,'default_cantrat':self.id,'default_indeex':self.contract_type_id.index},
        }




    def button_renouvellement(self):
        for rc in self:
             rc.rounouv = True
        self.write({'rounouv': True
                    })

        self.write({'state_cantrat': 'RN'
                    })

        if self.contract_type_id.name == "contrat à durée déterminée (CDD)":

            Madate = str(self.date_start)
            Liouma = Madate.split("-")[2]

            if self.mois > 6  :

                return {
                    'name': _('dure'),
                    'view_mode': 'form',
                    'res_model': 'dure',
                    'view_id': self.env.ref('contrat_osi.view_duree').id,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_cantrat': self.id},
                }
            elif self.Duree > 180:
                return {
                    'name': _('dure'),
                    'view_mode': 'form',
                    'res_model': 'dure',
                    'view_id': self.env.ref('contrat_osi.view_duree').id,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_cantrat': self.id},
                }

            elif self.jours != 0 and self.mois == 6 :
                return {
                    'name': _('dure'),
                    'view_mode': 'form',
                    'res_model': 'dure',
                    'view_id': self.env.ref('contrat_osi.view_duree').id,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_cantrat': self.id},
                }

            elif self.mois <= 6 or self.Duree <= 180:
                # if self.jours > int(Liouma):
                #     raise ValidationError(_('vous pouvez choisir jours inférieure ou egale de  %s   .', Liouma))

                self.mois = self.mois * 2
                if self.jours:
                   self.jours = self.jours * 2
                self.CALCULE_duree()



            if self.mois >12 :
                raise ValidationError(_('ne peux pas renouvelé un cantrat cdd pour une durée max  un an '))









    @api.depends('contract_type_id')
    def invisibility(self):
        if self.contract_type_id.name == "contrat à durée déterminée (CDD)":
            self.invisibi ='AA'
        elif self.contract_type_id.name == "contrat à durée indéterminée (CDI)":
            self.invisibi = 'BB'


    @api.depends('type')
    def type_fanction(self):
        if self.type.name =='Temps partiel':
            self.bool_type = False


    def teeeest(self):
        if self.date_end:
            self.date_validation = self.date_end - timedelta(days=10)

    def valider(self):
        today = date.today()
        _logger.info('Device  is now disconnected zzzzzzzzzzzzzzzzzzzz%s', today)
        if self.create_uid.id:
            user_id = self.create_uid.id
            ext = self.env.ref('contrat_osi.model_hr_contract').id
            self.activity_ids.create(
                {'activity_type_id': 4, 'res_id': self.id, 'user_id': user_id,
                 'res_model_id': ext,
                 'date_deadline': self.date_end,
                 'note': 'le cheque valider'
                 })
