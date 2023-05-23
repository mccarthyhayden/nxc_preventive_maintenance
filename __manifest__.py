{
    'name': 'NXC Preventive Maintenance Addon',
    'version': '15.0',
    'category': 'maintenance',
    'summary': 'Adds preventive maintenance and cleaning checklists with activities in their own model.',
    'description': 'This custom module was developed for Next Chapter Manufacturing to create cleaing and maintenance checklists at regular intervals.',
    'author': 'Hayden McCarthy',
    'website': 'https://www.nxcmfg.com',
    'data': [
        'views/view_nxc_cleaning_monthly_form.xml',
        'views/view_nxc_cleaning_weekly_form.xml',
        'views/view_nxc_pm_weekly_form.xml',
        'models/nxc_preventive_maintenance_config.py',
        'views/view_nxc_preventive_maintenance_config.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

