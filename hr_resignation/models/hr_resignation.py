# -*- coding: utf-8 -*-
import datetime
from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

date_format = "%Y-%m-%d"
RESIGNATION_TYPE = [('resigned', 'Normal Resignation'),
                    ('fired', 'Fired by the company')]






class HrResignationtype(models.Model):
    _name = 'hr.resignation.type'
    _inherit = 'mail.thread'
    name = fields.Char()
    seq = fields.Char(default=lambda x: _('New'))
    Type_licenciement = fields.Many2one('type.licenciement', string="Type de licenciement")








    @api.model
    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('hr.resignation.type')
        return super(HrResignationtype, self).create(vals)


class Type_licenciement(models.Model):
    _name = 'type.licenciement'
    name = fields.Char()




class HrResignation(models.Model):
    _name = 'hr.resignation'
    _inherit = 'mail.thread'
    _rec_name = 'employee_id'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee", default=lambda self: self.env.user.employee_id.id,
                                  help='Name of the employee for whom the request is creating')
    department_id = fields.Many2one('hr.department', string="Department", related='employee_id.department_id',
                                    help='Department of the employee')
    Type_départ = fields.Many2one('hr.resignation.type', string="Type de départ",
                                     )
    type_licenciement = fields.Many2one('type.licenciement', string="Raison de licenciement ",
                                     )
    neme_licenciement = fields.Char(store=True)



    resign_confirm_date = fields.Date(string="Confirmed Date",
                                      help='Date on which the request is confirmed by the employee.',
                                      track_visibility="always")
    approved_revealing_date = fields.Date(string="Approved Last Day Of Employee",
                                          help='Date on which the request is confirmed by the manager.',
                                          track_visibility="always")
    joined_date = fields.Date(string="Join Date", store=True,
                              help='Joining date of the employee.i.e Start date of the first contract')

    expected_revealing_date = fields.Date(string="Last Day of Employee", required=True,
                                          help='Employee requested date on which he is revealing from the company.')
    reason = fields.Text(string="description", required=False, help='Specify reason for leaving the company')
    notice_period = fields.Char(string="Notice Period")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved'), ('cancel', 'Rejected')],
        string='Status', default='draft', track_visibility="always")
    resignation_type = fields.Selection(selection=RESIGNATION_TYPE, help="Select the type of resignation: normal "
                                                                         "resignation or fired by the company")
    read_only = fields.Boolean(string="check field")
    bool = fields.Boolean(string="boll", default=False)
    bool_afiche_preavie = fields.Boolean(string="afiche preavie", default=False)
    employee_contract = fields.Char(String="Contract")

    type = fields.Many2one(
        'type',
        string='type',store=True
    )
    Employee_Category = fields.Many2one('category1em', string="Employee Category",store=True
                                        )
    preavis = fields.Many2one('preavis', string="preavis",store=True
                              )







    def traitement_date_fin(self):
        contrat = self.env['hr.contract'].search([('state', '=', 'open'),('contract_type_id.name', '=', 'contrat à durée indéterminée (CDI)'),('employee_id', '=', self.employee_id.id)])

        contrat.date_end = self.expected_revealing_date
        contrat.state = 'close'


    @api.onchange('Type_départ')
    @api.depends('Type_départ')
    def _compute_Type_départ(self):
        if self.Type_départ:
            self.neme_licenciement = self.Type_départ.name





    @api.onchange('employee_id')
    @api.depends('employee_id')
    def _compute_read_only(self):
        """ Use this function to check weather the user has the permission to change the employee"""
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('hr.group_hr_user'):
            self.read_only = True
        else:
            self.read_only = False

    @api.onchange('employee_id')
    def set_join_date(self):
        # self.joined_date = self.employee_id.joining_date if self.employee_id.joining_date else ''
        self.joined_date = self.employee_id.joining_date

    # @api.depends('employee_id')
    # def compute_join_date(self):
    #     # self.joined_date = self.employee_id.joining_date if self.employee_id.joining_date else ''
    #     if employee_id.joining_date :
    #         self.joined_date = self.employee_id.joining_date
    #     else :
    #         self.joined_date = False

    @api.model
    def create(self, vals):
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.resignation') or _('New')
        res = super(HrResignation, self).create(vals)
        return res

    @api.constrains('employee_id')
    def check_employee(self):
        # Checking whether the user is creating leave request of his/her own
        for rec in self:
            if not self.env.user.has_group('hr.group_hr_user'):
                if rec.employee_id.user_id.id and rec.employee_id.user_id.id != self.env.uid:
                    raise ValidationError(_('You cannot create request for other employees'))

    @api.onchange('employee_id')
    @api.depends('employee_id')
    def check_request_existence(self):
        # Check whether any resignation request already exists
        today = fields.Date.today()
        for rec in self:
            if rec.employee_id:
                resignation_request = self.env['hr.resignation'].search([('employee_id', '=', rec.employee_id.id),
                                                                         ('state', 'in', ['confirm', 'approved'])])
                if resignation_request:
                    raise ValidationError(_('There is a resignation request in confirmed or'
                                            ' approved state for this employee'))
                if rec.employee_id:
                    no_of_contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
                    for contracts in no_of_contract:

                        if contracts.state == 'open':
                            rec.employee_contract = contracts.name
                            rec.notice_period = contracts.notice_days
                            rec.Employee_Category = contracts.Employee_Category
                            rec.type = contracts.type
                            if contracts.date_fin_priode_essai:
                                start_date = fields.Date.from_string(self.expected_revealing_date)
                                end_date = fields.Date.from_string(contracts.date_fin_priode_essai)
                                if today > end_date:
                                    rec.bool = True
                                    rec.preavis = contracts.preavis





    @api.constrains('joined_date')
    def _check_dates(self):
        # validating the entered dates
        for rec in self:
            resignation_request = self.env['hr.resignation'].search([('employee_id', '=', rec.employee_id.id),
                                                                     ('state', 'in', ['confirm', 'approved'])])
            if resignation_request:
                raise ValidationError(_('There is a resignation request in confirmed or'
                                        ' approved state for this employee'))

    def confirm_resignation(self):
        if self.joined_date:
            if self.joined_date >= self.expected_revealing_date:
                raise ValidationError(_('Last date of the Employee must be anterior to Joining date'))
            for rec in self:
                rec.state = 'confirm'
                rec.resign_confirm_date = str(datetime.now())
        else:
            raise ValidationError(_('Please set joining date for employee'))

    def cancel_resignation(self):
        for rec in self:
            rec.state = 'cancel'

    def reject_resignation(self):
        for rec in self:
            rec.state = 'cancel'

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'
            rec.employee_id.active = True
            rec.employee_id.resigned = False
            rec.employee_id.fired = False

    def approve_resignation(self):
        for rec in self:
            if rec.expected_revealing_date and rec.resign_confirm_date:
                no_of_contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
                for contracts in no_of_contract:
                    if contracts.state == 'open':
                        rec.employee_contract = contracts.name
                        rec.state = 'approved'
                        rec.approved_revealing_date = rec.resign_confirm_date + timedelta(days=contracts.notice_days)
                    else:
                        rec.approved_revealing_date = rec.expected_revealing_date
                # Changing state of the employee if resigning today
                if rec.expected_revealing_date <= fields.Date.today() and rec.employee_id.active:
                    rec.employee_id.active = False
                    # Changing fields in the employee table with respect to resignation
                    rec.employee_id.resign_date = rec.expected_revealing_date
                    if rec.resignation_type == 'resigned':
                        rec.employee_id.resigned = True
                    else:
                        rec.employee_id.fired = True
                    # Removing and deactivating user
                    if rec.employee_id.user_id:
                        rec.employee_id.user_id.active = False
                        rec.employee_id.user_id = None
                rec.traitement_date_fin()

            else:
                raise ValidationError(_('Please enter valid dates.'))

    def update_employee_status(self):
        resignation = self.env['hr.resignation'].search([('state', '=', 'approved')])
        for rec in resignation:
            if rec.expected_revealing_date <= fields.Date.today() and rec.employee_id.active:
                rec.employee_id.active = False
                # Changing fields in the employee table with respect to resignation
                rec.employee_id.resign_date = rec.expected_revealing_date
                if rec.resignation_type == 'resigned':
                    rec.employee_id.resigned = True
                else:
                    rec.employee_id.fired = True
                # Removing and deactivating user
                if rec.employee_id.user_id:
                    rec.employee_id.user_id.active = False
                    rec.employee_id.user_id = None


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    resign_date = fields.Date('Resign Date', readonly=True, help="Date of the resignation")
    resigned = fields.Boolean(string="Resigned", default=False, store=True,
                              help="If checked then employee has resigned")
    fired = fields.Boolean(string="Fired", default=False, store=True, help="If checked then employee has fired")
