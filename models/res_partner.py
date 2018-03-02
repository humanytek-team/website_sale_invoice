# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
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

from openerp import models
import logging
_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    def _compute_amount(self, partner_id):
        amount = 0
        if partner_id:
            AccountInvoice = self.env['account.invoice']
            invoices = AccountInvoice.search([
                ('partner_id.id', '=', partner_id),
                ('type', '=', 'out_refund'),
                ('state', '=', 'open')])
            amount = 0
            for invoice in invoices:
                amount += invoice.residual
        return amount

    def _compute_amount2(self, partner_id, pool, cr, uid, context):
        amount = 0
        if partner_id:
            AccountInvoice = pool['account.invoice']
            invoice_ids = AccountInvoice.search(cr, uid, [
                ('partner_id.id', '=', partner_id),
                ('type', '=', 'out_refund'),
                ('state', '=', 'open')
                ], context=context)
            amount = 0
            invoices = AccountInvoice.browse(cr, uid, invoice_ids, context)
            for invoice in invoices:
                amount += invoice.residual
        return amount