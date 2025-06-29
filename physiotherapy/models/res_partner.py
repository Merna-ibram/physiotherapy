from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.osv import expression


class Registration(models.Model):
    _inherit = 'res.partner'
    _description = 'Registration'

    is_patient = fields.Boolean(string="Is a Patient")
    code = fields.Char(default='new', readonly=1, string="Code")
    birth_date = fields.Date(string="تاريخ الميلاد", required=True)
    age = fields.Integer(string="العمر", compute="_compute_age", store=True)
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')], string="Gender",required=True)


    nationality_id = fields.Many2one('res.country', string="الجنسية", required=True)
    state_code = fields.Char(string="كود الدولة")
    national_address = fields.Text(string= "عنوان وطني")
    identity_info = fields.Text(string="رقم الهوية", required=True)

    doctor = fields.Many2one('hr.employee', string='الاخصائي')

    sales_person = fields.Many2one('res.users', string='الاخصائي')

    diagnosis = fields.Char(string="Diagnosis", tracking=True)

    # Past History
    rta = fields.Boolean(string="RTA")
    sport_injury = fields.Boolean(string="Sport Injury")
    electrical_shock = fields.Boolean(string="Electrical Shock")
    burn = fields.Boolean(string="Burn")
    lifting_heavy_object = fields.Boolean(string="Lifting Heavy Object")
    no_history_of_trauma = fields.Boolean(string="No History of Trauma")
    duration = fields.Char(string="Duration")

    # Medical history
    htn = fields.Boolean(string="HTN")
    dm = fields.Boolean(string="D.M")
    osteoporosis = fields.Boolean(string="Osteoporosis")
    cardiac_problems = fields.Boolean(string="Cardiac Problems")
    other_medical = fields.Char(string="Other Medical")
    surgical_history = fields.Text(string="Surgical History")

    # Chief Complaint
    pain = fields.Boolean(string="Pain")
    stiffness = fields.Boolean(string="Stiffness")
    weakness = fields.Boolean(string="Weakness")
    neuro_deficit = fields.Boolean(string="Neurological Deficit")
    other_chief = fields.Text(string="Other Complaint")

    # Pain Description
    onset = fields.Char(string="Onset")
    pain_localized = fields.Boolean(string="Localized")
    pain_radiated = fields.Boolean(string="Radiated")
    pain_constant = fields.Boolean(string="Constant")
    pain_intermittent = fields.Boolean(string="Intermittent")
    aggravated_by = fields.Text(string="Aggravated By", tracking=True)
    relieved_by = fields.Text(string="Relieved By", tracking=True)

    # Patient condition on arrival
    patient_wheelchair = fields.Boolean(string="Wheelchair")
    patient_assistive = fields.Boolean(string="Walking with assistive device")
    patient_carried = fields.Boolean(string="Carried by mother")
    patient_on_bed = fields.Boolean(string="On bed")
    patient_normal = fields.Boolean(string="Walking normal")
    gait_other = fields.Char(string="Gait - Other")

    # Consciousness
    oriented = fields.Boolean(string="Oriented")
    confused = fields.Boolean(string="Confused")
    vegetated = fields.Boolean(string="Vegetated")
    conscious_other = fields.Char(string="Conscious - Other")

    # Risk of falls
    risk_time = fields.Char(string="Time (seconds)")
    risk_level = fields.Selection([
        ('no', 'No Risk'),
        ('mild', 'Mild Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk')
    ], string="Risk of Falls")

    # Session details
    session = fields.Char(string="Session")
    lazer = fields.Char(string="Lazer")
    shock_wave = fields.Char(string="Shock Wave")
    traction = fields.Char(string="Traction")

    # Symptoms
    edema = fields.Boolean(string="Edema")
    swelling = fields.Boolean(string="Swelling")
    redness = fields.Boolean(string="Redness")
    hotness = fields.Boolean(string="Hotness")
    muscle_weakness = fields.Boolean(string="Muscle Weakness")
    muscle_spasm = fields.Boolean(string="Muscle Spasm")
    muscle_atrophy = fields.Boolean(string="Muscle Atrophy")

    deformity = fields.Text(string="Deformity")

    # Examination
    neuro_exam = fields.Text(string="Neurological Examination")
    active_rom = fields.Text(string="Active Range of Motion")
    passive_rom = fields.Text(string="Passive Range of Motion")
    muscle_test = fields.Text(string="Manual Muscle Test")
    special_test = fields.Text(string="Special Test")

    @api.constrains('is_patient', 'diagnosis', 'doctor')
    def _check_required_fields_for_patient(self):
        for rec in self:
            if rec.is_patient:
                if not rec.diagnosis:
                    raise ValidationError("يجب إدخال التشخيص للمريض.")
                if not rec.doctor:
                    raise ValidationError("يجب تحديد الأخصائي للمريض.")
    # @api.constrains('age')
    # def _check_age_greater_zero(self):
    #     for rec in self:
    #         if rec.age == 0:
    #             raise ValidationError('Please enter a valid age greater than 0')

    # _sql_constraints = [
    #     ('unique_name', 'unique("name")', 'This name already exists! Please try another one.')
    # ]

    @api.onchange('nationality_id')
    def _onchange_nationality(self):
        if self.nationality_id:
            self.state_code = self.nationality_id.state_code
        else:
            self.state_code = False

    @api.onchange('state_code')
    def _onchange_state_code(self):
        if self.state_code:
            country = self.env['res.country'].search([('state_code', '=', self.state_code)], limit=1)
            self.nationality_id = country if country else False
        else:
            self.nationality_id = False

    @api.model
    def create(self, vals):
        res = super(Registration, self).create(vals)

        # Generate patient code
        if res.code == 'new':
            sequence = self.env['ir.sequence'].next_by_code('registration_seq')
            if sequence:
                res.code = sequence

        # Create my.cases record automatically
        if vals.get('is_patient'):
            self.env['my.cases'].create({
                'patient_id': res.id,
            })

        if vals.get('is_patient'):
            self.env['patient.appointment'].create({
                'patient_id': res.id,
                'doctors_id': res.doctor.id if res.doctor else False,
                'appointment_date': fields.Datetime.now(),
                'appointment_type': 'checkup',
            })

        return res

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                        (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        if self.birth_date:
            today = date.today()
            self.age = today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        else:
            self.age = 0

    # @api.multi
    # def write(self, vals):
    #     res = super(Registration, self).write(vals)
    #     if 'sales_person' in vals:
    #         for partner in self:
    #             cases = self.env['my.cases'].search([('patient_id', '=', partner.id)])
    #             cases.write({'sales_person': vals['sales_person']})
    #     return res

    # @api.constrains('is_patient', 'diagnosis')
    # def _check_diagnosis_required(self):
    #     for rec in self:
    #         if rec.is_patient and not rec.diagnosis:
    #             raise ValidationError("Diagnosis is required for patients.")
    #
#
# class CountryInherit(models.Model):
#     _inherit = 'res.country'
#
#     def name_get(self):
#         result = []
#         for record in self:
#             name = f"[{record.code}] {record.name}" if record.code else record.name
#             result.append((record.id, name))
#         return result

class CountryInherit(models.Model):
    _inherit = 'res.country'

    state_code = fields.Char(string="كود الدولة", copy=False)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} [{record.state_code}]" if record.state_code else record.name
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        # Remove 'new' default; instead, use assign_missing_state_codes to fill
        return super(CountryInherit, self).create(vals)

    @api.model
    def assign_missing_state_codes(self):
        code = 101
        countries = self.search([], order='id')
        for country in countries:
            if not country.state_code or country.state_code == 'new':
                # Skip if code already used
                while str(code) in countries.mapped('state_code'):
                    code += 1
                country.state_code = str(code)
                code += 1

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = args[:]

        if name:
            domain = ['|', ('name', operator, name), ('state_code', operator, name)] + domain
        return self.search(domain, limit=limit).name_get()
