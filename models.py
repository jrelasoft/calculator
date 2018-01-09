from openerp import fields, api, models



class brokerage_calc(models.Model):
    _name = "brokerage.calc"

    VALUES = [('intraday', 'Equity Intraday'), ('delivery', 'Equity Delivery'), ('futures', 'F&O Futures'),
              ('options', 'F&O Options')]
    select_mode = fields.Selection(VALUES, default="intraday")
    turnover = fields.Float('Turnover')
    brokerage = fields.Float('Brokerage')
    stt_total = fields.Float('STT total')
    total_txn_charge = fields.Float('Total txn charge')
    gst = fields.Float('GST')
    sebi_charges = fields.Float('SEBI charges')
    total_tax_and_charges = fields.Float('Total tax and charges')
    Poins_to_breakeven = fields.Float('Points to breakeven')
    net_profit = fields.Float('Net profit')
    tax_select = fields.Selection([('nse', 'NSE'), ('bse', 'BSE')], default="nse")
    # input values fields
    buy = fields.Float('Buy')
    sell = fields.Float('Sell')
    quantity = fields.Integer('Quantity')

    def get_charges(self, buy, sell, qty):
        record = self.create({'buy': buy, 'sell': sell, 'quantity': qty})
        print '\n---', self, buy, sell, qty, '---\n'
        record.calc_turnover_x()
        return record.total_tax_and_charges, record.net_profit

    @api.onchange('select_mode', 'buy', 'quantity', 'sell', 'tax_select', )
    def calc_turnover_x(self):
        config_param_env = self.env['ir.config_parameter']

        buy_to = (self.buy or 0.00) * (self.quantity or 0.00)
        sell_to = (self.sell or 0.00) * (self.quantity or 0.00)
        to = buy_to + sell_to

        self.turnover = to

        if self.select_mode == 'intraday':
            intraday = eval(config_param_env.get_param('equity_intraday') or '{}')
            int_brokerage = intraday.get('int_brokerage') or 0.00
            raw_int_brokerage = to * int_brokerage / 100
            self.brokerage = raw_int_brokerage if raw_int_brokerage < 20 else 20
            print '\n---', self.brokerage, '---brokerage\n'

            # STT Function
            int_stt = intraday.get('int_stt') or 0.00
            self.stt_total = sell_to * int_stt / 100
            print '\n---', self.stt_total, '---stt_total\n'
            # Transaction Charge
            int_bse_transaction = intraday.get('int_bse_transaction') or 0.00
            int_nse_transaction = intraday.get('int_nse_transaction') or 0.00
            if self.tax_select == 'bse':
                self.total_txn_charge = (int_bse_transaction if buy_to else 0.0) + (
                int_bse_transaction if sell_to else 0.0)
            elif self.tax_select == 'nse':
                self.total_txn_charge = to * (int_nse_transaction / 100)
            print '\n---', self.total_txn_charge, '---total_txn_charge\n'

            # gst fucntion
            int_gst = intraday.get('int_gst') or 0.00
            self.gst = (self.brokerage + self.total_txn_charge) * int_gst / 100
            print '\n---', self.gst, '---gst\n'
            # SEBI Charge
            int_sebi_charges = intraday.get('int_sebi') or 0.00
            self.sebi_charges = (buy_to + sell_to) * (int_sebi_charges / 10000000)
            print '\n---', self.sebi_charges, '---sebi_charges\n'
            # Total TAX And Charges
            self.total_tax_and_charges = self.brokerage + self.stt_total + self.total_txn_charge + self.gst + self.sebi_charges
            print '\n---', self.total_tax_and_charges, '---total_tax_and_charges\n'
            # Net Profit
            self.net_profit = sell_to - buy_to - self.total_tax_and_charges
            print '\n---', self.net_profit, '---net_profit\n'
