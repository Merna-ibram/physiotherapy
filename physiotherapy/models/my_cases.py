from odoo import models, fields, api
from odoo.osv import expression

class MyCases(models.Model):
    _name = 'my.cases'
    _description = 'My Medical Cases'

    patient_id = fields.Many2one('res.partner', string='Patient')
    doctor = fields.Many2one('hr.employee', string='الاخصائي')

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id and self.patient_id.doctor:
            self.doctor = self.patient_id.doctor

    def write(self, vals):
        for rec in self:
            # لو الدكتور هيتغيّر
            if 'doctor' in vals and vals['doctor'] != rec.doctor.id:
                # ننسخ البيانات الحالية
                new_vals = rec.copy_data()[0]
                # نحدّث الدكتور الجديد
                new_vals['doctor'] = vals['doctor']
                # نعمل سجل جديد
                self.env['my.cases'].create(new_vals)
                # منرجعش نعدّل السجل الحالي
                return True
        # لو مفيش تغيير في الدكتور، نكمل الكتابة العادية
        return super(MyCases, self).write(vals)
