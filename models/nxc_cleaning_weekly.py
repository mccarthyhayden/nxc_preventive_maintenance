from odoo import api, fields, models

class NxcCleaningWeekly(models.Model):
    _inherit = ''
    _name = 'nxc_preventive_maintenance.nxc_cleaning_weekly'

    name = fields.Char(string='Name', required=True)
    responsible_user = fields.Many2One('res.users', string='Responsible User')
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
    weekly_cleaning_attrs = {
      'readonly': [
        ('stage_id', '=', 'done')
      ]
    }
    weekly_cleaning_item_1 = fields.Boolean(string="Wipe down machine exteriors with IPA", **weekly_cleaning_attrs)
    weekly_cleaning_item_2 = fields.Boolean(string="Empty powder spill tray(s)", **weekly_cleaning_attrs)
    weekly_cleaning_item_3 = fields.Boolean(string="Empty trash bins", **weekly_cleaning_attrs)

    weekly_cleaning_checklist_complete = fields.Boolean(string="Checklist Complete", readonly=True, default=False)

    @api.onchange
    def _compute_stage_id(self):
      #This function determines the value of the stage_id.
      #Returns 'inprogress' if the checklist is started, 'done' if the checklist is complete, 'scheduled' otherwise.
      for record in self:
        if any([
          record.weekly_cleaning_item_1,
          record.weekly_cleaning_item_2,
          record.weekly_cleaning_item_3,
        ]):
          record['stage_id'] = 'inprogress'
          if record.weekly_cleaning_checklist_complete == True:
            record['stage_id'] = 'done'
        else:
          record['stage_id'] = 'scheduled'

    @api.onchange
    def _compute_checklist_complete(self):
      #This function determines the value of the weekly_cleaning_checklist_complete.
      #Returns True if the checklist is complete, False otherwise.
      for record in self:
        if all([
          record.weekly_cleaning_item_1,
          record.weekly_cleaning_item_2,
          record.weekly_cleaning_item_3,
        ]):
          record['weekly_cleaning_checklist_complete'] = True
        else:
          record['weekly_cleaning_checklist_complete'] = False

    @on_create
    def new_activity_on_creation(self):
      """Create an Odoo activity for the record on creation."""
      activity = self.env['mail.activity'].create({
        'summary': 'Weekly Cleaning Checklist',
        'type': 'todo',
        'user_type': 'generic',
        'date_deadline': fields.Datetime.now() + relativedelta(days=7),
        'res_id': self.id,
        'res_model': self._name,
      })

    @on_write
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
      model='nxc_cleaning_weekly',
      type='ir.actions.server',
    )
    def create_new_record_every_friday(self):
      """Create a new record."""
      self.env['nxc_cleaning_weekly'].create({})

    @api.model
    def _get_sequence(self):
        return 'CLEANING/WEEKLY/%03d' % self.env['ir.sequence'].next_by_code('nxc_cleaning_weekly')

    @api.on_create
    def set_name(self):
        self.name = self._get_sequence()
