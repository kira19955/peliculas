from odoo import fields, models, api


class Recursocinematografico(models.Model):
    _name = 'recurso.cinematografico'

    name = fields.Char(string="Recursos")
    descripcion = fields.Char(string="Descripcion")
    precio = fields.Float(string="Precio")
    contacto_id = fields.Many2one(comodel_name="res.partner",
                                  domain="[('is_company','=',False)]")
    imagen = fields.Binary(string="Imagen")

