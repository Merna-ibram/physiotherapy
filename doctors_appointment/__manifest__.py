{
    "name": "Doctor's Appointment",
    "author": 'Shins',
    'version': '0.1',
    'license': 'LGPL-3',
    "depends": ['base','hr','stock','report_xlsx', 'physiotherapy'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'wizard/patient_wiz.xml',
        "report/patient_prescription_template.xml",
        "data/header.xml",
        "report/patient_prescription_view.xml",
        'views/menu.xml',
        'views/patients_appoi.xml',
        'views/doctor_appointment_view.xml',
    ]
}