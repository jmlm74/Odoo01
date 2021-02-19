from odoo import fields, models, api, _


class Line(models.Model):
    _name = 'hp.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # for the chatter
    _description = 'Checklist lines'
    _rec_name = 'li_name'

    name = fields.Char()
    active = fields.Boolean("Active", default=True)

    li_seq = fields.Char(string='Line ID',
                         required=True,
                         copy=False,
                         readonly=True,
                         index=True,
                         default=lambda self: _('New'))
    li_name = fields.Char(string="Nom")
    li_type2 = fields.Selection([('question', 'Question'), ('note', 'Note'), ('cat', 'Categorie'), ('rem', 'Remarque')],
                               required=True,
                               default='Question',
                               tracking=True)
    li_description = fields.Char(string='Description',
                                 required=True,
                                 size=50,
                                 tracking=True)
    li_enable = fields.Boolean(string='Enable', default=True, tracking=True)
    li_position = fields.One2many('hp.linepos', 'linpos_line', string="Positions", tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('li_seq', _('New')) == _('New'):
            vals['li_seq'] = self.env['ir.sequence'].next_by_code('hp.line.sequence') or _('New')
            if len(vals['li_description']) > 25:
                vals['li_name'] = vals['li_description'][:25]
            else:
                vals['li_name'] = vals['li_description']
        result = super(Line, self).create(vals)
        return result

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '[%s] - %s' % (rec.li_seq, rec.li_description[:25])))
        return res

    def write(self, vals):
        print("Test write function : ", vals)
        if 'li_description' in vals:
            if len(vals['li_description']) > 25:
                vals['li_name'] = vals['li_description'][:25]
            else:
                vals['li_name'] = vals['li_description']
        res = super(Line, self).write(vals)
        return res


class LinePos(models.Model):
    _name = 'hp.linepos'
    _description = 'lines positions in checklists'

    linpos_line = fields.Many2one('hp.line', string="Line", domain="[('li_enable','=', True)]")
    linpos_pos = fields.Integer(string="Position")
    linpos_checklist = fields.Many2one('hp.checklist', string='Checklist')
    linpos_li_description = fields.Char(string="Line description", related="linpos_line.li_description")
    linpos_li_enable = fields.Boolean(string="Line enable", related="linpos_line.li_enable")
