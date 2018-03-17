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

from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.osv import osv
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _

import logging
import pprint

_logger = logging.getLogger(__name__)


class TransferPaymentTransaction(osv.Model):
    _inherit = 'payment.transaction'

    def _transfer_form_get_invalid_parameters(self, cr, uid, tx, data, context=None):
        invalid_parameters = []

        if data.get('amount'):
            if float_compare(float(data.get('amount', '0.0')), tx.amount, 2) != 0:
                invalid_parameters.append(('amount', data.get('amount'), '%.2f' % tx.amount))

        if data.get('currency'):
            if data.get('currency') != tx.currency_id.name:
                invalid_parameters.append(('currency', data.get('currency'), tx.currency_id.name))

        return invalid_parameters