from odoo import fields, models, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection([('client', 'Client'), ('provider', 'Provider')],
                                    default='client',
                                    string='Contact type')
    enable = fields.Boolean(default=True, string='Enable')

