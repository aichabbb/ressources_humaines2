from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging


_logger = logging.getLogger(__name__)

class dure(models.TransientModel):
    _name = 'dure'
    mois = fields.Integer(string='mois')
    Duree = fields.Integer(string='Duree')
    jours = fields.Integer(string='jours')
    TEST = fields.Char('ttttttttttt')
    cantrat = fields.Many2one('hr.contract')

    def ajouter(self):
        Madate = str(self.cantrat.date_start)
        Liouma = Madate.split("-")[2]
        moit_test = Madate.split("-")[1]
        num = int(moit_test)

        if num == 1 or num == 3 or num == 5 or num == 7 or num == 8 or num == 10 or num == 12:
            m = self.mois * 31
            self.Duree = m + self.jours
            dure =  360 - self.cantrat.Duree

            Madate = str(self.cantrat.date_start)
            Liouma = Madate.split("-")[2]
            moit_test = Madate.split("-")[1]
            m = self.cantrat.mois - 12
            vr =abs(m)
            v = m+1
        elif num == 2:
            m = self.mois * 29
            self.Duree = m + self.jours
            dure = 360 - self.cantrat.Duree

            Madate = str(self.cantrat.date_start)
            Liouma = Madate.split("-")[2]
            moit_test = Madate.split("-")[1]
            m = self.cantrat.mois - 12
            vr = abs(m)
            v = m + 1
        elif num == 4 or num == 6 or num == 9 or num == 11:
            m = self.mois * 30
            self.Duree = m + self.jours
            dure = 360 - self.cantrat.Duree

            Madate = str(self.cantrat.date_start)
            Liouma = Madate.split("-")[2]
            moit_test = Madate.split("-")[1]
            m = self.cantrat.mois - 12
            vr = abs(m)
            v = m + 1











        if self.Duree > abs(dure)  :
            raise ValidationError(_('vous pouvez choisir durée inférieure ou egale de  %s   .',abs(m)))
        # if self.mois == abs(m) :
        #     if self.jours != 0 or self.cantrat.jours != 0:
        #         raise ValidationError(_('ne peux pas depase cntrat un an vous pouvez choisir durée inférieure ou egale de  %s .',abs(v)))
        else:
            self.cantrat.mois = self.cantrat.mois + self.mois
            self.cantrat.jours = self.cantrat.jours + self.jours
            self.cantrat.CALCULE_duree()

