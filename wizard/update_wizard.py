from odoo import fields, models, api


class Update_wizard(models.TransientModel):
    _name = 'update.wizard'

    name = fields.Char(string="Nueva Descripción")

    def update_vista_general(self):
        presupuesto_ojb = self.env['presupuesto']
        #presupuesto_id = presupuesto_ojb.search([('id', '=', self._context['active_id'])])
        presupuesto_id = presupuesto_ojb.browse(self._context['active_id'])
        presupuesto_id.vista_general = self.name
