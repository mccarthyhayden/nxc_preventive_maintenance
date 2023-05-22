from . import models
from . import views
from odoo import api, SUPERUSER_ID

def _setup(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.model.data'].sudo().create({
        'name': 'view_nxc_engineering_checklist_mrp_production_form',
        'module': 'nxc_engineering_checklist',
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