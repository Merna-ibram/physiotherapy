from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Registration(models.Model):
    _inherit = 'res.partner'
    _description = 'registration'

    is_patient = fields.Boolean(string="Is a Patient")
    code = fields.Char(default='new', readonly=1, string="Code")
    age = fields.Integer(required=True, string="Age")
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')], string="Gender",required=True)
    
    sales_person = fields.Many2one('res.users', string='الاخصائي')

    diagnosis = fields.Text(required=True,  string="Diagnosis")

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
    aggravated_by = fields.Text(string="Aggravated By")
    relieved_by = fields.Text(string="Relieved By")

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



    @api.constrains('age')
    def _check_age_greater_zero(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError('Please enter a valid age greater than 0')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name already exists! Please try another one.')
    ]

    @api.model
    def create(self, vals):
        res = super(Registration, self).create(vals)
        if res.code == 'new':
            sequence = self.env['ir.sequence'].next_by_code('registration_seq')
            if sequence:
                # Update the record with the generated sequence
                res.code = sequence

        return res



