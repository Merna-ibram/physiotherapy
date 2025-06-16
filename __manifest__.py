# -*- coding: utf-8 -*-
{
    'name': "physiotherapy",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'version': '0.1',
    'license': 'LGPL-3',
    'application': True,

    'depends': [
        'base',
        'account',
        'mail',
        'hr',
    ],

    'data': [
        # Security
        'security/ir.model.access.csv',


        # Data
        'data/sequence.xml',


        # Views
        'views/base_menu.xml',
        'views/res_partner_view.xml',
        'views/account_move_view.xml',
        'views/my_cases_views.xml',
        'views/my_cases_views.xml',
        'views/hr_employee_view.xml',

        # Wizards


        # Reports
        'reports/registration_report.xml',

    ],


}
