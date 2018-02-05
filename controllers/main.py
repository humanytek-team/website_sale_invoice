# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import openerp
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
import openerp.addons.website_sale.controllers.main
import logging
_logger = logging.getLogger(__name__)


class website_sale(openerp.addons.website_sale.controllers.main.website_sale):

    @http.route(['/shop/payment_invoice_refund'], type='http',
                auth="public", website=True)
    def set_invoice_refund(self, **post):
        _logger.info('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        _logger.info(self)
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        _logger.info(post)
        _logger.info(post.get('apply_refund_invoice'))
        _logger.info(request.website)
        sale_order_orm = registry.get('sale.order')
        order = sale_order_orm.browse(cr, SUPERUSER_ID,
                            request.session['sale_order_id'], context)
        _logger.info(request.session['sale_order_id'])
        #order = request.website.sale_get_order(context=context)
        value = False
        if order:
            if post.get('apply_refund_invoice'):
                value = True
            _logger.info('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
                #values = self.checkout_values(post)
                #_logger.info(order.apply_refund_invoice)
            _logger.info(value)
            order.set_apply_refund_invoice(value)
            #return request.redirect("/shop")

        #redirection = self.checkout_redirection(order)
        #if redirection:
            #return redirection

        #values = self.checkout_values(post)

        #values["error"], values["error_message"] = self.checkout_form_validate(values["checkout"])
        #if values["error"]:
            #return request.website.render("website_sale.checkout", values)

        #self.checkout_form_save(values["checkout"])

        #order.onchange_partner_shipping_id()
        #order.order_line._compute_tax_id()

        #request.session['sale_last_order_id'] = order.id

        #request.website.sale_get_order(update_pricelist=True, context=context)

        #extra_step = registry['ir.model.data'].xmlid_to_object(cr, uid, 'website_sale.extra_info_option', raise_if_not_found=True)
        #if extra_step.active:
            #return request.redirect("/shop/extra_info")

        return request.redirect("/shop/payment")