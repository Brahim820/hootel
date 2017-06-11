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
from openerp import http
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)


class website_wubook(http.Controller):
    @http.route(['/wubook/push/reservations'], type='http', cors="*",
                auth="public", methods=['POST'], website=True, csrf=False)
    def wubook_push_reservations(self, **kwargs):
        rcode = kwargs['rcode']
        lcode = kwargs['lcode']

        _logger.info("WUBOOK PUSH RESERVATIONS")
        _logger.info(kwargs)

        # WuBook Check
        if rcode == '2000' and lcode == '1000':
            return request.make_response('200 OK', [('Content-Type', 'text/plain')])

        # TODO: SECURITY CHECK HERE... LCODE DEFINED?

        # Create Reservation
        request.env['wubook'].sudo().fetch_booking(lcode, rcode)

        return request.make_response('200 OK', [('Content-Type', 'text/plain')])

    @http.route(['/wubook/push/rooms'], type='http', cors="*",
                auth="public", methods=['POST'], website=True, csrf=False)
    def wubook_push_rooms(self, **kwargs):
        _logger.info("WUBOOK PUSH ROOMS")
        _logger.info(kwargs)

        # {'dfrom': u'22/06/2017', 'dto': u'24/06/2017', 'lcode': u'NUM'}
        # More Info: http://tdocs.wubook.net/wired/avail.html?highlight=fetch_rooms_values#fetch_rooms_values

        return request.make_response('200 OK', [('Content-Type', 'text/plain')])