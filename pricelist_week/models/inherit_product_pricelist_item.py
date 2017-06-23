# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Solucións Aloxa S.L. <info@aloxa.eu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    mo = fields.Boolean('Mon', default=True)
    tu = fields.Boolean('Tue', default=True)
    we = fields.Boolean('Wed', default=True)
    th = fields.Boolean('Thu', default=True)
    fr = fields.Boolean('Fri', default=True)
    sa = fields.Boolean('Sat', default=True)
    su = fields.Boolean('Sun', default=True)
