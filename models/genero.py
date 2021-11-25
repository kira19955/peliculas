from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'genero'
    _description = 'modelo de los tipos de genero qye hay en el cine'

    name = fields.Char()
