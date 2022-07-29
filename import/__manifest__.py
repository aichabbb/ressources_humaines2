{
    'name': "import data",
    'version': '15.0.1.0.0',
    'summary': """""",
    'description': """""",
    'category': 'Generic Modules/Human Resources',
    'live_test_url': '',
    'author': 'aicha',
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['hr', 'account', 'account_accountant', 'hr_payroll_community', 'hr_attendance', 'hr_timesheet_attendance',
                'hr_recruitment', 'hr_resignation', 'event', 'hr_reward_warning','base'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/import_bank.xml',
        'wizard/pyroll.xml',
        'views/menu.xml',

    ],

    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
