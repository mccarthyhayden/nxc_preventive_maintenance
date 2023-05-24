from odoo import api, fields, models

class NxcPmWeekly(models.Model):
    _inherit = ''
    _name = 'nxc_preventive_maintenance.nxc_pm_weekly'

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
    weekly_pm_attrs = {
      'readonly': [
        ('stage_id', '=', 'done')
      ]
    }
    weekly_pm_item_1 = fields.Boolean(string="Top off laser chillers (Distilled Water)", **weekly_pm_attrs)
    weekly_pm_item_2 = fields.Boolean(string="Vacuum & empty waste canister", **weekly_pm_attrs)
    weekly_pm_item_3 = fields.Boolean(string="Inspect mesh screen for damage", **weekly_pm_attrs)
    weekly_pm_item_4 = fields.Boolean(string="Brush material and empty bin", **weekly_pm_attrs)
    weekly_pm_item_5 = fields.Boolean(string="Top off main EDM reservoir (Filtered Water)", **weekly_pm_attrs)
    weekly_pm_item_6 = fields.Boolean(string="Top off EDM chiller (Tap Water)", **weekly_pm_attrs)
    weekly_pm_item_7 = fields.Boolean(string="Top off reservoir to fill line", **weekly_pm_attrs)
    weekly_pm_item_8 = fields.Boolean(string="Evaluate capacity & empty waste as needed", **weekly_pm_attrs)
    weekly_pm_item_9 = fields.Boolean(string="Drain, clean, and refill ultrasonic cleaner", **weekly_pm_attrs)

    weekly_pm_checklist_complete = fields.Boolean(string="Checklist Complete", readonly=True, default=False)

    @api.onchange('weekly_pm_item_1', 'weekly_pm_item_2', 'weekly_pm_item_3', 'weekly_pm_item_4', 'weekly_pm_item_5', 'weekly_pm_item_6', 'weekly_pm_item_7', 'weekly_pm_item_8', 'weekly_pm_item_9', 'weekly_pm_checklist_complete')
    def _compute_stage_id(self):
      #This function determines the value of the stage_id.
      #Returns 'inprogress' if the checklist is started, 'done' if the checklist is complete, 'scheduled' otherwise.
      for record in self:
        if any([
          record.weekly_pm_item_1,
          record.weekly_pm_item_2,
          record.weekly_pm_item_3,
          record.weekly_pm_item_4,
          record.weekly_pm_item_5,
          record.weekly_pm_item_6,
          record.weekly_pm_item_7,
          record.weekly_pm_item_8,
          record.weekly_pm_item_9,
        ]):
          record['stage_id'] = 'inprogress'
          if record.weekly_pm_checklist_complete == True:
            record['stage_id'] = 'done'
        else:
          record['stage_id'] = 'scheduled'

    @api.onchange('weekly_pm_item_1', 'weekly_pm_item_2', 'weekly_pm_item_3', 'weekly_pm_item_4', 'weekly_pm_item_5', 'weekly_pm_item_6', 'weekly_pm_item_7', 'weekly_pm_item_8', 'weekly_pm_item_9')
    def _compute_checklist_complete(self):
      #This function determines the value of the weekly_pm_checklist_complete.
      #Returns True if the checklist is complete, False otherwise.
      for record in self:
        if all([
          record.weekly_pm_item_1,
          record.weekly_pm_item_2,
          record.weekly_pm_item_3,
          record.weekly_pm_item_4,
          record.weekly_pm_item_5,
          record.weekly_pm_item_6,
          record.weekly_pm_item_7,
          record.weekly_pm_item_8,
          record.weekly_pm_item_9,
        ]):
          record['weekly_pm_checklist_complete'] = True
        else:
          record['weekly_pm_checklist_complete'] = False

    @api.model
    def new_activity_on_creation(self):
      """Create an Odoo activity for the record on creation."""
      activity = self.env['mail.activity'].create({
        'summary': 'Weekly Preventive Maintenance Checklist',
        'type': 'todo',
        'user_type': 'generic',
        'date_deadline': fields.Datetime.now() + relativedelta(days=7),
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

    @cron_job(
      '0 17 * * 5',
      'Create a new record.',
      number_of_calls=-1,
      priority=10,
      model='nxc_pm_weekly',
      type='ir.actions.server',
    )
    def create_new_record_every_friday(self):
      """Create a new record."""
      self.env['nxc_pm_weekly'].create({})

    @api.model
    def _get_sequence(self):
      return 'PM/WEEKLY/%03d' % self.env['ir.sequence'].next_by_code('nxc_pm_weekly')

    @api.model
    def set_name(self):
      self.name = self._get_sequence()