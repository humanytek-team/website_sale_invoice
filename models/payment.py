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

import logging
from openerp import SUPERUSER_ID
from openerp.osv import orm, fields
from openerp.tools import float_compare
_logger = logging.getLogger(__name__)


class PaymentTransaction(orm.Model):
    _inherit = 'payment.transaction'

    _columns = {
        # link with the sale order
        'sale_order_id': fields.many2one('sale.order', 'Sale Order'),
    }

    def form_feedback(self, cr, uid, data, acquirer_name, context=None):
        """ Override to confirm the sale order, if defined, and if the transaction
        is done. """
        tx = None
        res = super(PaymentTransaction, self).form_feedback(cr, uid, data, acquirer_name, context=context)

        # fetch the tx, check its state, confirm the potential SO
        try:
            tx_find_method_name = '_%s_form_get_tx_from_data' % acquirer_name
            if hasattr(self, tx_find_method_name):
                tx = getattr(self, tx_find_method_name)(cr, uid, data, context=context)
            _logger.info('<%s> transaction processed: tx ref:%s, tx amount: %s', acquirer_name, tx.reference if tx else 'n/a', tx.amount if tx else 'n/a')

            if tx and tx.sale_order_id and tx.sale_order_id.state in ['draft', 'sent']:
                # verify SO/TX match, excluding tx.fees which are currently not included in SO
                amount_matches = float_compare(tx.amount, tx.sale_order_id.amount_total, 2) == 0
                if amount_matches or tx.sale_order_id.apply_refund_invoice:
                    if tx.state == 'done' and tx.acquirer_id.auto_confirm == 'at_pay_confirm':
                        _logger.info('<%s> transaction completed, auto-confirming order %s (ID %s)', acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
                        self.pool['sale.order'].action_confirm(cr, SUPERUSER_ID, [tx.sale_order_id.id], context=dict(context, send_email=True))
                    elif tx.state not in ['cancel', 'error'] and tx.sale_order_id.state == 'draft':
                        _logger.info('<%s> transaction pending/to confirm manually, sending quote email for order %s (ID %s)', acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
                        self.pool['sale.order'].force_quotation_send(cr, SUPERUSER_ID, [tx.sale_order_id.id], context=context)
                else:
                    _logger.warning('<%s> transaction MISMATCH for order %s (ID %s)', acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)
        except Exception:
            _logger.exception('Fail to confirm the order or send the confirmation email%s', tx and ' for the transaction %s' % tx.reference or '')

        return res