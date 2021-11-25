# -*- coding: utf-8 -*-

from odoo import models, fields, api

class  Presupuesto(models.Model):
    _name = 'presupuesto'

    name = fields.Char(string="Nombre")
    fch_estreno = fields.Date(string="Fecha")
    clasificacion = fields.Selection(selection=[('g', 'G'),
                                               ('pg', 'PG'),
                                               ('pg-13', 'PG-13'),
                                               ('r', 'R'),
                                               ('nc-17', 'NC-17')
                                               ], string="Clasificacion")
    puntuacion = fields.Integer(string="Puntuacion")
    active = fields.Boolean()
