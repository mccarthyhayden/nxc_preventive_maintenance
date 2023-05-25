from odoo import api, fields, models

class NxcCleaningMonthly(models.Model):
    _name = 'nxc_preventive_maintenance.nxc_cleaning_monthly'

    name = fields.Char(string='Name', required=True)
    responsible_user = fields.Many2one('res.users', string='Responsible User')
    stage_id = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('inprogress', 'In-Progress'),
            ('done', 'Done'),
        ],
        string='Stage',
        default='scheduled',
        required=True,
    )

    #Design Checklist Items
    monthly_cleaning_attrs = {
      'readonly': [
        ('stage_id', '=', 'done')
      ]
    }
    monthly_cleaning_item_1 = fields.Boolean(string="Mop/degrease floors", **monthly_cleaning_attrs)
    monthly_cleaning_item_2 = fields.Boolean(string="Vacuum top of additive machines", **monthly_cleaning_attrs)
    monthly_cleaning_item_3 = fields.Boolean(string="Clean bathrooms", **monthly_cleaning_attrs)

    monthly_cleaning_checklist_complete = fields.Boolean(string="Checklist Complete", readonly=True, default=False)

    @api.onchange('monthly_cleaning_item_1', 'monthly_cleaning_item_2', 'monthly_cleaning_item_3', 'monthly_cleaning_checklist_complete')
    def _compute_stage_id(self):
      #This function determines the value of the stage_id.
      #Returns 'inprogress' if the checklist is started, 'done' if the checklist is complete, 'scheduled' otherwise.
      for record in self:
        if any([
          record.monthly_cleaning_item_1,
          record.monthly_cleaning_item_2,
          record.monthly_cleaning_item_3,
        ]):
          record['stage_id'] = 'inprogress'
          if record.monthly_cleaning_checklist_complete == True:
            record['stage_id'] = 'done'
        else:
          record['stage_id'] = 'scheduled'

    @api.onchange('monthly_cleaning_item_1', 'monthly_cleaning_item_2', 'monthly_cleaning_item_3')
    def _compute_checklist_complete(self):
      #This function determines the value of the monthly_cleaning_checklist_complete.
      #Returns True if the checklist is complete, False otherwise.
      for record in self:
        if all([
          record.monthly_cleaning_item_1,
          record.monthly_cleaning_item_2,
          record.monthly_cleaning_item_3,
        ]):
          record['monthly_cleaning_checklist_complete'] = True
        else:
          record['monthly_cleaning_checklist_complete'] = False

    @api.model
    def new_activity_on_creation(self):
      """Create an Odoo activity for the record on creation."""
      activity = self.env['mail.activity'].create({
        'summary': 'Monthly Cleaning Checklist',
        'type': 'todo',
        'user_type': 'generic',
        'date_deadline': fields.Datetime.now() + relativedelta(months=1),
        'res_id': self.id,
        'res_model': self._name,
      })

      return activity

    @api.depends('stage_id')
    def close_activity_on_completion(self):
      """Close the activity when the record's stage_id is set to 'done'."""
      if self.stage_id == 'done':
        activities = self.env['mail.activity'].search([
          ('res_id', '=', self.id),
          ('res_model', '=', self._name),
        ])
        for activity in activities:
          activity.action_feedback()

    @api.model
    def _get_sequence(self):
      return 'CLEANING/MONTHLY/%03d' % self.env['ir.sequence'].next_by_code('nxc_cleaning_monthly')

    @api.model
    def set_name(self):
      self.name = self._get_sequence()
