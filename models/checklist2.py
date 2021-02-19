from odoo import fields, models, api, _


class CheckList2(models.Model):
    _name = 'hp.checklist2'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # for the chatter
    _description = 'Checklist2 model'
    _rec_name = 'chk2_material'

    name = fields.Char()
    active = fields.Boolean("Active", default=True)

    chk2_seq = fields.Char(string='Checklist ID',
                           required=True,
                           copy=False,
                           readonly=True,
                           index=True,
                           default=lambda self: _('New'))
    chk2_state = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1')
    chk2_rem = fields.Text(string="Remarques Globales", tracking=True)
    chk2_valid = fields.Boolean(string="Valide", default=True, tracking=True)
    chk2_sticker = fields.Char(string="N° etiquette", tracking=True, default=None)

    chk2_img1 = fields.Binary(string='Photo N°1', verify_resolution=False)
    chk2_img2 = fields.Binary(string='Photo N°2', verify_resolution=False)
    chk2_img3 = fields.Binary(string='Photo N°3', verify_resolution=False)
    chk2_img4 = fields.Binary(string='Photo N°4', verify_resolution=False)

    chk2_material = fields.Many2one('hp.material',
                                    required=True,
                                    string="Line",
                                    domain="[('mat_enable','=', True)]",
                                    tracking=True)
    chk2_mat_designation = fields.Char(string='Designation',
                                       size=30,
                                       tracking=True,
                                       related="chk2_material.mat_designation")
    chk2_mat_serial = fields.Char(string='Serial',
                                  size=30,
                                  tracking=True,
                                  related="chk2_material.mat_serial")
    chk2_mat_type = fields.Char(string='Type',
                                size=30,
                                tracking=True,
                                related="chk2_material.mat_type")
    chk2_mat_model = fields.Char(string='Model',
                                 size=30,
                                 tracking=True,
                                 related="chk2_material.mat_model")
    chk2_mat_manager = fields.Many2one(string='Manager',
                                   size=30,
                                   tracking=True,
                                   related="chk2_material.mat_manager")


    # the lines
    chk2_li1 = fields.Selection([('ok', 'OK'), ('na', 'N/A'), ('ko', 'KO'), ],
                                string='Question N°1',
                                default='na',
                                tracking=True)
    chk2_li2 = fields.Selection([('ok', 'OK'), ('na', 'N/A'), ('ko', 'KO'), ],
                                string='Question N°2',
                                default='na',
                                tracking=True)
    chk2_li3 = fields.Char(string='Question N°3', tracking=True, size=10)
    chk2_rem1 = fields.Text(string="Remarques")
    chk2_li4 = fields.Selection([('ok', 'OK'), ('na', 'N/A'), ('ko', 'KO'), ],
                                string='Question N°4',
                                default='na',
                                tracking=True)
    chk2_li5 = fields.Selection([('ok', 'OK'), ('na', 'N/A'), ('ko', 'KO'), ],
                                string='Question N°5',
                                default='na',
                                tracking=True)
    chk2_li6 = fields.Selection([('ok', 'OK'), ('na', 'N/A'), ('ko', 'KO'), ],
                                string='Question N°6',
                                default='na',
                                tracking=True)


    @api.model
    def create(self, vals):
        if vals.get('chk2_seq', _('New')) == _('New'):
            vals['chk2_seq'] = self.env['ir.sequence'].next_by_code('hp.checklist2.sequence') or _('New')
        result = super(CheckList2, self).create(vals)
        return result

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '[%s] - %s' % (rec.chk2_seq, rec.chk2_material)))
        return res

    def previous(self):
        print(self.chk2_state)
        if(self.chk2_state) == '1':
            return
        new_state = int(self.chk2_state) - 1
        self.chk2_state = str(new_state)
        print("Previous")

    def next(self):
        print(self.chk2_state)
        if (self.chk2_state) == '3':
            return
        new_state = int(self.chk2_state) + 1
        self.chk2_state = str(new_state)
        print("Next")

