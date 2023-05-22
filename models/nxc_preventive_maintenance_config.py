from odoo import models, fields

class NxcPreventiveMaintenanceConfig(models.Model):
    _name = 'nxc_preventive_maintenance.config'

    responsible_user_cleaning_weekly = fields.Many2one('res.users', string='Weekly Cleaning Checklist Responsible User')
    responsible_user_cleaning_monthly = fields.Many2one('res.users', string='Monthly Cleaning Checklist Responsible User')
    responsible_user_pm_weekly = fields.Many2one('res.users', string='Weekly Preventive Maintenance Checklist Responsible User')
    
    def post_init(self):
    if self.responsible_user_weekly_cleaning:
        self.env['nxc_cleaning_weekly'].create({'responsible_user': self.responsible_user_weekly_cleaning})
    if self.responsible_user_cleaning_monthly:
        self.env['nxc_cleaning_monthly'].create({'responsible_user': self.responsible_user_cleaning_monthly})
    if self.responsible_user_pm_weekly:
        self.env['nxc_pm_weekly'].create({'responsible_user': self.responsible_user_pm_weekly})

