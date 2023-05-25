from . import models
from . import views
from odoo import api, SUPERUSER_ID
from odoo.addons.base.models import ir_cron

def _setup(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.model.data'].sudo().create({
        'name': 'view_nxc_engineering_checklist_mrp_production_form',
        'module': 'nxc_preventive_maintenance',
        'res_id': env.ref('nxc_engineering_checklist.view_nxc_engineering_checklist_mrp_production_form').id,
        'model': 'ir.ui.view',
    })

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.model.data'].sudo().search([
        ('module', '=', 'nxc_engineering_checklist'),
        ('name', '=', 'view_nxc_engineering_checklist_mrp_production_form')
    ]).unlink()

def post_init_hook(cr, registry):
    _setup(cr, registry)

@cron_job(
      '0 0 1 * *',
      'Create new Monthly Cleaning record',
      number_of_calls=-1,
      priority=10,
      model='nxc_cleaning_monthly',
      type='ir.actions.server',
    )
def create_new_cleaning_monthly_record(self):
      self.env['nxc_cleaning_monthly'].create({})

@cron_job(
      '0 17 * * 5',
      'Create new Weekly Cleaning record',
      number_of_calls=-1,
      priority=10,
      model='nxc_cleaning_weekly',
      type='ir.actions.server',
    )
def create_new_cleaning_weekly_record(self):
      self.env['nxc_cleaning_weekly'].create({})

@cron_job(
      '0 17 * * 5',
      'Create new Weekly PM record',
      number_of_calls=-1,
      priority=10,
      model='nxc_pm_weekly',
      type='ir.actions.server',
    )
def create_new_pm_weekly_record(self):
      self.env['nxc_pm_weekly'].create({})