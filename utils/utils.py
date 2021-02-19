from odoo import fields, models, api
from odoo.models import TransientModel


class CleanField(TransientModel):

    """Initial Settings."""

    _name = "clean.field"

    # ToDo can be removed after field is deleted

    def init_remove_field_api7(self, cr, uid, ids=None, context=None):
        """Entry function remove Field (called with API7)."""
        return self._remove_field(cr, uid, context=context)

    @api.model
    def _remove_field(self):
        """Removes the Field from the database."""
        self.env.cr.execute("""SELECT 1 FROM ir_model_fields
        WHERE model = 'res.partner'AND name='contact_type';""")
        fields = self.env.cr.fetchall()
        if fields:
            self.env.cr.execute("""DELETE FROM ir_model_fields 
            WHERE model = 'res.partner'
            AND name=''; 
            ALTER TABLE res_partner DROP COLUMN contact_type;""")
            self.env.cr.commit()
        return True