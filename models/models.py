# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class  Presupuesto(models.Model):
    _name = 'presupuesto'
    _inherit = ['image.mixin', 'mail.activity.mixin', 'mail.thread']
    @api.depends('detalles_ids')
    def compute_total(self):
        for record in self:
            subtotal = 0
            for linea in self.detalles_ids:
                subtotal += linea.importe
            record.base = subtotal
            record.impuestos = subtotal * 0.16
            record.total = record.base + record.impuestos


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
    categoria_director_id = fields.Many2one(comodel_name="res.partner.category", string="Categoria Director",
                                            #segunda version
                                            default=lambda self: self.env.ref('peliculas.category_director'))
                                            #Primera version
                                            #default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')]))
    state = fields.Selection(selection=[('borrador', 'Borrador'),
                                        ('aprobado', 'Aprobado'),
                                        ('cancelado', 'Cancelado')],
                             default="borrador", string="Estados", copy=False)
    fhc_aprobado = fields.Datetime(string="Fecha de Aprobacion", copy=False)
    num_presupuesto = fields.Char(string="Numero de presupuesto", copy=False)
    actor_ids = fields.Many2many(comodel_name="res.partner", string="Actores")
    categoria_actor_id = fields.Many2one(comodel_name="res.partner.category", string="Categoria actores",
                                            default=lambda self: self.env.ref('peliculas.category_actor'))
    opinion = fields.Html(string="Opinion")
    detalles_ids = fields.One2many(comodel_name="presupuesto.detalle", inverse_name="presupuesto_id")
    campos_ocultos = fields.Boolean(string="Campos ocultos")
    currency_id = fields.Many2one(comodel_name="res.currency", string="moneda",
                                  default=lambda self: self.env.company.currency_id.id)
    terminos = fields.Text(string="Terminos")
    base = fields.Monetary(string="Total sin impuestos", compute="compute_total")
    impuestos = fields.Monetary(string="Impuestos", compute="compute_total")
    total = fields.Monetary(string="Total", compute="compute_total")





    def aprobar_presupuesto(self):
        self.state = 'aprobado'
        self.fhc_aprobado = fields.Datetime.now()


    def cancelar_presupuesto(self):
        self.state = 'cancelado'

    ##sobreescribir la funcion unlink para que odoo siga funcionando bien se agrega super
    def unlink(self):
        logger.info("******************************FUNCION UNLINK*************************")
        for record in self:
            if record.state == "cancelado":
                super(Presupuesto, record).unlink()
            else:
                raise UserError("no se puede borrar el registro por que no se encuentra en el estado cancelado")

    ##funcion create necesita un decorador
    @api.model
    def create(self, variables):
        logger.info("*** variables{0}".format(variables))
        secuencia = self.env['ir.sequence']
        correlativo = secuencia.next_by_code('secuencia.presupuesto.peliculas')
        variables['num_presupuesto'] = correlativo
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

class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"

    presupuesto_id = fields.Many2one(comodel_name="presupuesto", string="Presupuesto")

    name = fields.Many2one(comodel_name='recurso.cinematografico', string="Recurso")
    description = fields.Char(string="Descripcion", related="name.descripcion")
    contacto_id = fields.Many2one(comodel_name='res.partner', string="Contacto", related="name.contacto_id")
    imagen = fields.Binary(string="Imagen", related="name.imagen")
    cantidad = fields.Float(string="Cantidad", default=1.0, digits=(16, 4))
    precio = fields.Float(string="Precio", digits="Product Price")
    importe = fields.Monetary(string="Importe")

    currency_id = fields.Many2one(related="presupuesto_id.currency_id", string="Moneda")

    @api.onchange('name')
    def onchangue_name(self):
        if self.name:
            self.precio = self.name.precio

    @api.onchange('cantidad', 'precio')
    def onchangue_importe(self):
        self.importe = self.cantidad * self.precio

