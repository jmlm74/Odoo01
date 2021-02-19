from odoo import fields, models, api, _


class CheckList(models.Model):
    _name = 'hp.checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # for the chatter
    _description = 'Checklist model'
    _rec_name = 'chk_name'

    name = fields.Char()
    active = fields.Boolean("Active", default=True)

    chk_seq = fields.Char(string='Checklist ID',
                          required=True,
                          copy=False,
                          readonly=True,
                          index=True,
                          default=lambda self: _('New'))
    chk_name = fields.Char(string="Nom", required=True, tracking=True, size=30)
    chk_description = fields.Char(string='Description', required=True, tracking=True, size=80)
    chk_enable = fields.Boolean(string='Enable', default=True, tracking=True)
    chk_lines = fields.One2many('hp.linepos', 'linpos_checklist', string="Lignes", tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('chk_seq', _('New')) == _('New'):
            vals['chk_seq'] = self.env['ir.sequence'].next_by_code('hp.checklist.sequence') or _('New')
        result = super(CheckList, self).create(vals)
        return result

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '[%s] - %s' % (rec.chk_seq, rec.chk_name)))
        return res
