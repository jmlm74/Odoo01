# -*- coding: utf-8 -*-
# from odoo import http


# class Hp(http.Controller):
#     @http.route('/hp/hp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hp/hp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hp.listing', {
#             'root': '/hp/hp',
#             'objects': http.request.env['hp.hp'].search([]),
#         })

#     @http.route('/hp/hp/objects/<model("hp.hp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hp.object', {
#             'object': obj
#         })
