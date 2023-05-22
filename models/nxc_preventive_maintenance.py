from odoo import api, fields, models

class NxcPreventiveMaintenance(models.Model):
    _inherit = ''

    #Design Checklist Items
    design_attrs = {
      'readonly': [
        ('design_complete', '=', True)
      ]
    }
    design_item_1 = fields.Boolean(string="", **design_attrs)

    @api.onchange
    def _compute_engineering_checklist_status(self):