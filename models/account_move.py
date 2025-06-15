from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class AccountMove(models.Model):
    _inherit = 'account.move'

    start_date = fields.Date(string="Subscription Start Date", required=True, default=fields.Date.context_today)
    months = fields.Integer(string="Months of Subscription")
    end_date = fields.Date(string="Subscription End Date", compute="_compute_end_date", store=True)
    code = fields.Char(related='partner_id.code', readonly=1, string="Code")
    age = fields.Integer(related='partner_id.age', string="Age")
    gender = fields.Selection(related='partner_id.gender', string="Gender")
    invoice_created_months = fields.Integer(string="Created Invoices Count", default=0)

    @api.depends('start_date', 'months')
    def _compute_end_date(self):
        for record in self:
            if record.start_date and record.months:
                record.end_date = record.start_date + relativedelta(months=record.months)
            else:
                record.end_date = False

    @api.model
    def create_subscription_invoices(self):
        subscription_invoices = self.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '!=', 'cancel'),
            ('months', '>=', 0),
            ('start_date', '!=', False),
        ])

        today = date.today()

        for record in subscription_invoices:
            created = record.invoice_created_months or 0
            months_total = record.months
            current_invoice_date = record.start_date

            if created >= months_total:
                continue

            invoice_template = record

            for month_index in range(created, months_total):
                if current_invoice_date > today:
                    break

                invoice_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': record.partner_id.id,
                    'invoice_date': current_invoice_date,
                    'date': current_invoice_date,
                    'months': 1,
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
                current_invoice_date += relativedelta(months=1)
