from odoo import models, fields, api

class MyCases(models.Model):
    _name = 'my.cases'
    _description = 'My Medical Cases'

    # name = fields.Char(string='Case Title', required=True)
    patient_id = fields.Many2one('res.partner', string='Patient')
    doctor =  fields.Many2one('hr.employee',  string='الاخصائي', related='patient_id.doctor', store=True)

