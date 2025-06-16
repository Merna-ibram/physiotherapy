from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class AccountMove(models.Model):
    _inherit = 'account.move'

    date = fields.Date(string="Subscription Start Date", required=True)
    months = fields.Integer(string="Months of Subscription")
    end_date = fields.Date(string="Subscription End Date", compute="_compute_end_date", store=True)
    code = fields.Char(related='partner_id.code', readonly=1, string="Code")
    age = fields.Integer(related='partner_id.age', string="Age")
    gender = fields.Selection(related='partner_id.gender', string="Gender")
    invoice_created_months = fields.Integer(string="Created Invoices Count", default=0)

    @api.depends('date', 'months')
    def _compute_end_date(self):
        for record in self:
            if record.date and record.months:
                record.end_date = record.date + relativedelta(months=record.months)
            else:
                record.end_date = False

    @api.model
    def create_subscription_invoices(self):
        subscription_invoices = self.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '!=', 'cancel'),
            ('months', '>=', 0),
            ('date', '!=', False),
        ])

        today = date.today()

        for record in subscription_invoices:
            created = record.invoice_created_months or 0
            months_total = record.months
            start_date = record.date

            if created >= months_total:
                continue

            invoice_template = record

            for month_index in range(created, months_total):
                invoice_date = start_date + relativedelta(months=month_index)
                if invoice_date > today:
                    break

                invoice_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': record.partner_id.id,
                    'invoice_date': invoice_date,
                    'date': invoice_date,
                    'invoice_line_ids': [
                        (0, 0, {
                            'name': line.name,
                            'quantity': line.quantity,
                            'price_unit': line.price_unit,
                            'product_id': line.product_id.id,
                            'account_id': line.account_id.id,
                            'tax_ids': [(6, 0, line.tax_ids.ids)],
                        }) for line in invoice_template.invoice_line_ids
                    ],
                }

                self.create(invoice_vals)
                record.invoice_created_months += 1
