# -*- coding: utf-8 -*-
# from odoo import http


# class Peliculas(http.Controller):
#     @http.route('/peliculas/peliculas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/peliculas/peliculas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('peliculas.listing', {
#             'root': '/peliculas/peliculas',
#             'objects': http.request.env['peliculas.peliculas'].search([]),
#         })

#     @http.route('/peliculas/peliculas/objects/<model("peliculas.peliculas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('peliculas.object', {
#             'object': obj
#         })
