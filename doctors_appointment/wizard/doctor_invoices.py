from odoo import models, fields
from datetime import datetime, time
import base64
import calendar

class AppointmentReportWizard(models.TransientModel):
    _name = 'doctor.report.wizard'

    doctors_id = fields.Many2one('res.partner', string="الدكتور", required=True)
    month = fields.Selection(
        [(str(i), calendar.month_name[i]) for i in range(1, 13)],
        string="الشهر",
        required=True
    )
    year = fields.Integer(string="السنة", required=True, default=lambda self: datetime.today().year)

    make_report = fields.Binary(string="تقرير PDF", readonly=True)
    report_name = fields.Char(string="اسم الملف")

    def action_generate_report_invoice(self):
        # تحويل الشهر والسنة إلى بداية ونهاية الشهر
        month = int(self.month)
        year = self.year
        start_date = datetime(year, month, 1)
        print('start_date',start_date)
        last_day = calendar.monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59)
        print('end_date',end_date)
        print(self.doctors_id.id)

        # البحث عن المواعيد
        appointments = self.env['account.move'].search([
            ('agents_name_invoice', '=', self.doctors_id.id),
            ('invoice_date', '>=', start_date),
            ('invoice_date', '<=', end_date),
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice')
        ])

        print('appointments0',appointments)
        agesnts=(appointments.mapped('invoice_line_ids.agents'))
        print('agesnts',agesnts)
        total_amount = sum(appointments.mapped('amount_total'))
        print('total_amount',total_amount)
        total_commission = sum(appointments.mapped('commission_total'))
        print('total_commission',total_commission)
        doctor_salary = self.doctors_id.salary
        print('doctor_salary',doctor_salary)


        # إعداد البيانات للتقرير
        data = {
            'doctor_name': self.doctors_id.name,
            'selected_month': f"{calendar.month_name[month]} {year}",
            'total_amount': total_amount,
            'total_commission': total_commission,
            'doctor_salary': doctor_salary,
            'invoices_count': len(appointments),
            'has_data': bool(appointments),
        }

        # إنشاء التقرير
        try:
            report_action = self.env.ref('doctors_appointment.report_doctor_invoices_action')
            pdf_content, _ = report_action._render_qweb_pdf(self.ids, data={'data': data})
        except:
            report_template = 'doctors_appointment.report_doctor_invoices_template'
            pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
                report_template,
                res_ids=self.ids,
                data={'data': data}
            )

        self.make_report = base64.b64encode(pdf_content)
        self.report_name = f"تقرير-{self.doctors_id.name}-{calendar.month_name[month]}-{year}.pdf"

        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content?model=doctor.report.wizard&id={self.id}&field=make_report&filename_field=report_name&download=true",
            'target': 'new',
        }
