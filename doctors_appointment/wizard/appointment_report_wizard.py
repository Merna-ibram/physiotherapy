from odoo import models, fields, api
from datetime import datetime, time

class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'Doctor Daily Appointment Report Wizard'

    doctors_id = fields.Many2one('hr.employee', string="الدكتور", required=True)
    date = fields.Date(string="تاريخ", required=True)

    def action_generate_report(self):
        appointments = self.env['doctor.appointment'].search([
            ('doctors_id', '=', self.doctors_id.id),
            ('appointment_date', '>=', datetime.combine(self.date, time.min)),
            ('appointment_date', '<=', datetime.combine(self.date, time.max)),
            ('is_reserved', '=', True),
        ])

        return self.env.ref('doctors_appointment.report_doctor_daily_appointments').report_action(self, data={
            'appointments': appointments.ids,
            'doctor_name': self.doctors_id.name,
            'selected_date': self.date.strftime('%Y-%m-%d'),
        })


