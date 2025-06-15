from odoo import models, fields, api

class MyCases(models.Model):
    _name = 'my.cases'
    _description = 'My Medical Cases'

    # name = fields.Char(string='Case Title', required=True)
    patient_id = fields.Many2one('res.partner', string='Patient')
    sales_person = fields.Many2one('res.users', string='الاخصائي', related='patient_id.sales_person',)


    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.sales_person = self.patient_id.sales_person
