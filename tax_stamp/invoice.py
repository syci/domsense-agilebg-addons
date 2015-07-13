from osv import osv, fields
from tools import config

class invoice_line(osv.osv):
    _inherit = 'account.invoice.line'
    _columns = {
        'tax_stamp': fields.boolean('Tax stamp', help='Specify whether this line should be used for comuting the taxable amount'),
        }
invoice_line()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _amount_all(self, cr, uid, ids, name, args, context=None):
#        import pdb; pdb.set_trace()
        res = {}
        for invoice in self.browse(cr,uid,ids, context=context):
            res[invoice.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0
            }
            for line in invoice.invoice_line:
                if(line.tax_stamp):
                    res[invoice.id]['amount_tax'] += line.price_subtotal
                else:
                    res[invoice.id]['amount_untaxed'] += line.price_subtotal
            for line in invoice.tax_line:
                res[invoice.id]['amount_tax'] += line.amount
            res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']
        return res

    def _get_invoice_tax(self, cr, uid, ids, context=None):
        return super(account_invoice, self)._get_invoice_tax(self, cr, uid, ids, context)

    def _get_invoice_line(self, cr, uid, ids, context=None):
        return super(account_invoice, self)._get_invoice_line(self, cr, uid, ids, context)

    _columns = {
        'amount_untaxed': fields.function(_amount_all, method=True, digits=(16, int(config['price_accuracy'])),string='Untaxed',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount'], 20),
            },
            multi='all'),
        'amount_tax': fields.function(_amount_all, method=True, digits=(16, int(config['price_accuracy'])), string='Tax',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount'], 20),
            },
            multi='all'),
        'amount_total': fields.function(_amount_all, method=True, digits=(16, int(config['price_accuracy'])), string='Total',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount'], 20),
            },
            multi='all'),
        }

account_invoice()
