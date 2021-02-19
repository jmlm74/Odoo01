from odoo import fields, models, api, _
from odoo.addons.web.controllers.main import env
from odoo.exceptions import ValidationError


class Material(models.Model):
    _name = 'hp.material'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # for the chatter
    _description = 'materials to be managed'
    _rec_name = 'mat_designation'

    @api.model
    def _default_mat_material(self):
        res = self.env['hp.material'].search([('mat_manager', '=', self.mat_manager.id)])

    name = fields.Char()
    active = fields.Boolean("Active", default=True)

    mat_seq = fields.Char(string='Material ID',
                          required=True,
                          copy=False,
                          readonly=True,
                          index=True,
                          default=lambda self: _('New'))
    mat_designation = fields.Char(string='Designation', required=True, size=30, tracking=True)
    mat_serial = fields.Char(string='Serial', size=30, tracking=True)
    mat_type = fields.Char(string='Type', size=30, tracking=True)
    mat_model = fields.Char(string='Model', size=30, tracking=True)
    mat_enable = fields.Boolean(string="Enable", default=True)
    mat_manager = fields.Many2one('res.partner', index=True, required=True, tracking=True)
    mat_material = fields.Many2one('hp.material',
                                   default=lambda self: self.env['hp.material'].
                                   search([('mat_manager', '=', self.mat_manager.id)]),
                                   tracking=True)

    @api.constrains('mat_designation', 'mat_manager')
    def check_unique(self):
        """
            Check unicity of tuple (material-manager)
            Raise error if duplicate
        """
        if not self.mat_manager.parent_id.id:
            company = self.mat_manager.name
        else:
            company = self.mat_manager.parent_id.name
        existing_records = self.env['hp.material'].search([('mat_designation', 'ilike', self.mat_designation),
                                                           ('mat_manager', 'ilike', company)])
        if len(existing_records) > 1:
            error_msg = f"Erreur : {self.mat_designation} - {company} existe déjà !"
            raise ValidationError(_(error_msg))

    @api.model
    def create(self, vals):
        if vals.get('mat_seq', _('New')) == _('New'):
            vals['mat_seq'] = self.env['ir.sequence'].next_by_code('hp.material.sequence') or _('New')
        result = super(Material, self).create(vals)
        return result

    @api.onchange('mat_manager')
    def onchange_method(self):
        res = {}
        res['domain'] = {'mat_material': [('mat_manager', '=', self.mat_manager.id)]}
        return res

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '[%s] - %s' % (rec.mat_seq, rec.mat_designation[:15])))
        return res