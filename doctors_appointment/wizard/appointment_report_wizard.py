from odoo import models, fields
from datetime import datetime, time
import base64

class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'Doctor Daily Appointment Report Wizard'

    doctors_id = fields.Many2one('hr.employee', string="الدكتور", required=True)
    date = fields.Date(string="تاريخ", required=True)
    make_report = fields.Binary(string="تقرير PDF", readonly=True)
    report_name = fields.Char(string="اسم الملف")

    def action_generate_report(self):
        # Get appointments
        appointments = self.env['doctor.appointment'].search([
            ('doctors_id', '=', self.doctors_id.id),
            ('appointment_date', '>=', datetime.combine(self.date, time.min)),
            ('appointment_date', '<=', datetime.combine(self.date, time.max)),
            ('is_reserved', '=', True),
        ])

        # Prepare data dictionary
        data = {
            'doctor_name': self.doctors_id.name,
            'selected_date': self.date.strftime('%Y-%m-%d'),
            'appointments': appointments,
        }

        # METHOD 1: Using report action (Recommended)
        try:
            report_action = self.env.ref('doctors_appointment.report_doctor_daily_appointments_action')
            pdf_content, _ = report_action._render_qweb_pdf(self.ids, data={'data': data})
        except:
            # METHOD 2: Direct template rendering (Alternative)
            report_template = 'doctors_appointment.report_doctor_daily_appointments_template'
            pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
                report_template,
                res_ids=self.ids,
                data={'data': data}
            )

        # Encode and save PDF
        self.make_report = base64.b64encode(pdf_content)
        self.report_name = f"تقرير-{self.doctors_id.name}-{self.date}.pdf"

        # Return download action
        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content?model=appointment.report.wizard&id={self.id}&field=make_report&filename_field=report_name&download=true",
            'target': 'new',
        }