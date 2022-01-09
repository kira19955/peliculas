# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class  Presupuesto(models.Model):
    _name = 'presupuesto'
    _inherit = ['image.mixin']

    name = fields.Char(string="Pelicula")
    fch_estreno = fields.Date(string="Fecha de estreno")
    clasificacion = fields.Selection(selection=[('g', 'G'),
                                               ('pg', 'PG'),
                                               ('pg-13', 'PG-13'),
                                               ('r', 'R'),
                                               ('nc-17', 'NC-17')
                                               ], string="Clasificacion")
    des_clasificacion = fields.Char(string="Descripccion Clasificacion")
    puntuacion = fields.Integer(string="Puntuacion", related="puntuacion2")
    active = fields.Boolean(string="Activo", default=True)
    director_id = fields.Many2one(comodel_name="res.partner", string="Director")
    generos_ids = fields.Many2many(comodel_name="genero", string="Genero")
    vista_general = fields.Text(string="Descripcion")
    link_trailer = fields.Char(string="Link Trailer")
    es_libro = fields.Boolean(string="Version Libro")
    libro = fields.Binary(string="Libro")
    puntuacion2 = fields.Integer(string="Puntuacion")
    libro_file = fields.Char(string="Nombre del libro")
    categoria_director_id = fields.Many2one(comodel_name="res.partner.category", string="Categoria Director", default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')]))
    state = fields.Selection(selection=[('borrador', 'Borrador'),
                                        ('aprobado', 'Aprobado'),
                                        ('cancelado', 'Cancelado')],
                             default="borrador", string="Estados", copy=False)
    fhc_aprobado = fields.Datetime(string="Fecha de Aprobacion", copy=False)

    def aprobar_presupuesto(self):
        self.state = 'aprobado'
        self.fhc_aprobado = fields.Datetime.now()


    def cancelar_presupuesto(self):
        self.state = 'cancelado'

    ##sobreescribir la funcion unlink para que odoo siga funcionando bien se agrega super
    def unlink(self):
        logger.info("******************************FUNCION UNLINK*************************")
        if self.state == "cancelado":
            super(Presupuesto, self).unlink()
        else:
            raise UserError("no se puede borrar el registro por que no se encuentra en el estado cancelado")

    ##funcion create necesita un decorador
    @api.model
    def create(self, variables):
        logger.info("*** variables{0}".format(variables))
        return super(Presupuesto, self).create(variables)

    ##funcion write
    def write(self, variables):
        logger.info("*** variables{0}".format(variables))
        if 'clasificacion' in variables:
            raise UserError("la Clasificaion no se puede editar !!")
        return super(Presupuesto, self).write(variables)

    ##funcion copy
    def copy(self, default=None):
        default =dict(default or {})
        default['name'] = self.name + '(Copia)'
        default['puntuacion2'] = 1
        return super(Presupuesto, self).copy(default)

    @api.onchange('clasificacion')
    def _onchange_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == 'g':
                self.des_clasificacion = "Publico general"
            if self.clasificacion == 'pg':
                self.des_clasificacion = "Se Recomienda compañia de un adulto"
            if self.clasificacion == 'pg-13':
                self.des_clasificacion = "Mayores de 13"
            if self.clasificacion == 'r':
                self.des_clasificacion = "En Compañia de un adulto obligatorio"
            if self.clasificacion == 'nc-17':
                self.des_clasificacion = "Solo Adultos"
        else:
            self.des_clasificacion = False

