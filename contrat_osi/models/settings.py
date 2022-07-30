
from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



class settings(models.TransientModel):
    _inherit = 'res.config.settings'

    Age_la_retraite = fields.Integer()

    délai_notification = fields.Integer(string='délai notification de Age à la retraite')
    délai_notification_essai = fields.Integer(string='délai notification de période d essaie')
    plafond_des_absence_justifie = fields.Integer(string='plafond des absence justifie')
    plafond_des_absence_non_justifie = fields.Integer(string='plafond des absence nom justifie')


    def set_values(self):
        super(settings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            "contrat_osi.Age_la_retraite", self.Age_la_retraite)
        self.env['ir.config_parameter'].sudo().set_param(
            "contrat_osi.délai_notification", self.délai_notification)
        self.env['ir.config_parameter'].sudo().set_param(
            "contrat_osi.délai_notification_essai", self.délai_notification_essai)
        self.env['ir.config_parameter'].sudo().set_param(
            "contrat_osi.plafond_des_absence_justifie", self.plafond_des_absence_justifie)
        self.env['ir.config_parameter'].sudo().set_param(
            "contrat_osi.plafond_des_absence_non_justifie", self.plafond_des_absence_non_justifie)

    @api.model
    def get_values(self):
        res = super(settings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['Age_la_retraite'] = int(get_param('contrat_osi.Age_la_retraite'))
        res['délai_notification'] = int(get_param('contrat_osi.délai_notification'))
        res['délai_notification_essai'] = int(get_param('contrat_osi.délai_notification_essai'))
        res['plafond_des_absence_justifie'] = int(get_param('contrat_osi.plafond_des_absence_justifie'))
        res['plafond_des_absence_non_justifie'] = int(get_param('contrat_osi.plafond_des_absence_non_justifie'))
        return res


    # def set_values(self):
    #     res = super(settings_test, self).set_values()
    #
    #     self.env['ir.config_parameter'].sudo().set_param(
    #         "hr_resignation.no_of_days", self.Age_la_retraite)
    #
    #     return  res
    # @api.model
    # def get_values(self):
    #     res = super(settings_test, self).get_values()
    #     test = self.env['ir.config_parameter'].sudo()
    #     Age_la_retraite = int(test.get_param('contrat_osi.Age_la_retraite'))
    #     #res['no_of_days'] = int(get_param('hr_resignation.no_of_days'))
    #     res.update(
    #         Age_la_retraite= Age_la_retraite,
    #
    #     )
    #
    #     return res

# def compute_age(self):
    #     emploiye = self.env['hr.employee'].search()
    #
    #     for rc in emploiye:
    #         if rc.age == self.Age_la_retraite:
    #             date_de_retraite = rc.birthday + relativedelta(years=rc.age)
    #             date_notification_retrite = date_de_retraite - timedelta(days=self.délai_notification)
    #             user_id = rc.create_uid.id
    #             ext = self.env.ref('contrat_osi.model_hr_employee').id
    #             self.activity_ids.create(
    #                 {'activity_type_id': 4, 'res_id': self.rc.id, 'user_id': user_id,
    #                  'res_model_id': ext,
    #                  'date_deadline': date_notification_retrite,
    #                  'note': 'le cheque valider'
    #                  })
