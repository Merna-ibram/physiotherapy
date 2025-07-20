from odoo import models, fields, api
from odoo.osv import expression

class MyCases(models.Model):
    _name = 'my.cases'
    _description = 'My Medical Cases'

    # name = fields.Char(string='Case Title', required=True)
    patient_id = fields.Many2one('res.partner', string='Patient')
    doctor =  fields.Many2one('hr.employee',  string='الاخصائي', related='patient_id.doctor', store=True)

    @api.model
    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        user = self.env.user

        if user.has_group('doctors_appointment.group_doctors_appointment_doctor'):
            domain = expression.AND([
                domain,
                [('doctor.user_id', '=', user.id)]
            ])

        return super(MyCases, self).search_fetch(domain, field_names, offset=offset, limit=limit, order=order)

