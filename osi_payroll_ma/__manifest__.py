# -*- coding: utf-8 -*-
{
    'name': "osi Payroll Ma",
    'summary': """""",
    'description': """
    """,
    'author': "Osisoftware",
    'website': "https://www.osisoftware.net",
    'category': 'Payroll',
    'version': '0.1',
    'depends': ['base','hr_payroll_community','l10n_maroc'],
    'data': [
        'security/ir.model.access.csv',
        'views/payroll_rubriques.xml',
        'views/payroll_rubrique_submission.xml',
        'views/payroll_cotisation.xml',
        'views/payroll_cotisation_type.xml',
    ],
}
