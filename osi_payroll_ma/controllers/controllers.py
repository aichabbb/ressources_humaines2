# -*- coding: utf-8 -*-
# from odoo import http


# class OsiPayrollMa(http.Controller):
#     @http.route('/osi_payroll_ma/osi_payroll_ma', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/osi_payroll_ma/osi_payroll_ma/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('osi_payroll_ma.listing', {
#             'root': '/osi_payroll_ma/osi_payroll_ma',
#             'objects': http.request.env['osi_payroll_ma.osi_payroll_ma'].search([]),
#         })

#     @http.route('/osi_payroll_ma/osi_payroll_ma/objects/<model("osi_payroll_ma.osi_payroll_ma"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('osi_payroll_ma.object', {
#             'object': obj
#         })
