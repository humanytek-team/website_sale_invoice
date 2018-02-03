# -*- coding: utf-8 -*-
from openerp import api, fields, models
#import random
#import openerp

#from openerp import SUPERUSER_ID, tools
#import openerp.addons.decimal_precision as dp
#from openerp.osv import osv, orm, fields
#from openerp.addons.web.http import request
#from openerp.tools.translate import _
#from openerp.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    def _compute_amount(self, partner_id):
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