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
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class website_sale(openerp.addons.website_sale.controllers.main.website_sale):

    @http.route(['/shop/payment_invoice_refund'], type='http',
                auth="public", website=True)
    def set_invoice_refund(self, **post):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        sale_order_orm = registry.get('sale.order')

        order = sale_order_orm.browse(cr, SUPERUSER_ID,
                            request.session['sale_order_id'], context)
        value = False
        if order:
            if post.get('apply_refund_invoice'):
                value = True
            order.set_apply_refund_invoice(value)

        return request.redirect("/shop/payment")

    @http.route(['/shop/payment/transaction/<int:acquirer_id>'], type='json',
                auth="public", website=True)
    def payment_transaction(self, acquirer_id):
        """ Json method that creates a payment.transaction, used to create a
        transaction when the user clicks on 'pay now' button. After having
        created the transaction, the event continues and the user is redirected
        to the acquirer website.

        :param int acquirer_id: id of a payment.acquirer record. If not set the
                                user is redirected to the checkout page
        """
        cr, uid, context = request.cr, request.uid, request.context
        payment_obj = request.registry.get('payment.acquirer')
        transaction_obj = request.registry.get('payment.transaction')
        order = request.website.sale_get_order(context=context)
        res_partner_orm = request.registry.get('res.partner')
        account_invoice_orm = request.registry.get('account.invoice')
        if not order or not order.order_line or acquirer_id is None:
            return request.redirect("/shop/checkout")

        assert order.partner_id.id != request.website.partner_id.id

        # find an already existing transaction
        tx = request.website.sale_get_transaction()
        amount = order.amount_total
        if order.apply_refund_invoice:
            _logger.info(res_partner_orm._compute_amount2(order.partner_id.id,
                    request.registry, cr, SUPERUSER_ID, context))
            amount = order.amount_total - res_partner_orm._compute_amount2(
                    order.partner_id.id,
                    request.registry, cr, SUPERUSER_ID, context)
            _logger.info(amount)
        if tx:
            tx_id = tx.id
            if tx.sale_order_id.id != order.id or tx.state in ['error', 'cancel'] or tx.acquirer_id.id != acquirer_id:
                tx = False
                tx_id = False
            elif tx.state == 'draft':  # button cliked but no more info -> rewrite on tx or create a new one ?
                tx.write(dict(transaction_obj.on_change_partner_id(cr, SUPERUSER_ID, None, order.partner_id.id, context=context).get('value', {}), amount=amount))
        if not tx:
            tx_id = transaction_obj.create(cr, SUPERUSER_ID, {
                'acquirer_id': acquirer_id,
                'type': 'form',
                'amount': amount,
                'currency_id': order.pricelist_id.currency_id.id,
                'partner_id': order.partner_id.id,
                'partner_country_id': order.partner_id.country_id.id,
                'reference': request.env['payment.transaction'].get_next_reference(order.name),
                'sale_order_id': order.id,
            }, context=context)
            request.session['sale_transaction_id'] = tx_id
            tx = transaction_obj.browse(cr, SUPERUSER_ID, tx_id, context=context)

        # update quotation
        request.registry['sale.order'].write(
            cr, SUPERUSER_ID, [order.id], {
                'payment_acquirer_id': acquirer_id,
                'payment_tx_id': request.session['sale_transaction_id']
            }, context=context)

        # confirm the quotation
        if tx.acquirer_id.auto_confirm == 'at_pay_now':
            request.registry['sale.order'].action_confirm(cr, SUPERUSER_ID,
                            [order.id], context=dict(request.context,
                            send_email=True))
        return payment_obj.render(
            request.cr, SUPERUSER_ID, tx.acquirer_id.id,
            tx.reference,
            amount,
            order.pricelist_id.currency_id.id,
            values={
                'return_url': '/shop/payment/validate',
                'partner_id': order.partner_shipping_id.id or order.partner_invoice_id.id,
                'billing_partner_id': order.partner_invoice_id.id,
            },
            context=dict(context, submit_class='btn btn-primary',
                        submit_txt=_('Pay Now')))

