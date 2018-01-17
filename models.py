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

    def get_charges(self, buy, sell, qty, slct_md):
        record = self.create({'buy': buy, 'sell': sell, 'quantity': qty, 'select_mode':slct_md})
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
            # STT Function
            int_stt = intraday.get('int_stt') or 0.00
            self.stt_total = sell_to * int_stt / 100
            # Transaction Charge
            int_bse_transaction = intraday.get('int_bse_transaction') or 0.00
            int_nse_transaction = intraday.get('int_nse_transaction') or 0.00
            if self.tax_select == 'bse':
                self.total_txn_charge = (int_bse_transaction if buy_to else 0.0) + (
                int_bse_transaction if sell_to else 0.0)
            elif self.tax_select == 'nse':
                self.total_txn_charge = to * (int_nse_transaction / 100)

            # gst fucntion
            int_gst = intraday.get('int_gst') or 0.00
            self.gst =(self.brokerage + self.total_txn_charge) * int_gst / 100
            # SEBI Charge
            int_sebi_charges = intraday.get('int_sebi') or 0.00
            self.sebi_charges = (buy_to + sell_to) * (int_sebi_charges / 10000000)
            # Total TAX And Charges
            self.total_tax_and_charges = self.brokerage + self.stt_total + self.total_txn_charge + self.gst + self.sebi_charges
            # Net Profit
            self.net_profit = sell_to - buy_to - self.total_tax_and_charges


        if self.select_mode == 'delivery':
            intraday = eval(config_param_env.get_param('equity_delivery') or '{}')
            del_brokerage = intraday.get('del_brokerage') or 0.00
            raw_del_brokerage = to * del_brokerage / 100
            self.brokerage = raw_del_brokerage if raw_del_brokerage < 20 else 20
            # STT Function
            del_stt = intraday.get('del_stt') or 0.00
            self.stt_total = to * del_stt / 100
            # Transaction Charge
            del_bse_transaction = intraday.get('del_bse_transaction') or 0.00
            del_nse_transaction = intraday.get('del_nse_transaction') or 0.00
            if self.tax_select == 'bse':
                self.total_txn_charge = (del_bse_transaction if buy_to else 0.0) + (del_bse_transaction if sell_to else 0.0)
            elif self.tax_select == 'nse':
                self.total_txn_charge = to * (del_nse_transaction / 100)

            # gst fucntion
            del_gst = intraday.get('del_gst') or 0.00
            self.gst = (del_brokerage + self.total_txn_charge) * del_gst / 100
            # SEBI Charge
            del_sebi_charges = intraday.get('del_sebi') or 0.00
            self.sebi_charges = (buy_to + sell_to) * (del_sebi_charges / 10000000)
            # Total TAX And Charges
            self.total_tax_and_charges =self.stt_total + self.total_txn_charge + self.gst + self.sebi_charges
            # Net Profit
            self.net_profit = sell_to - buy_to - self.total_tax_and_charges


        if self.select_mode == 'futures':
            intraday = eval(config_param_env.get_param('equity_future') or '{}')
            fut_brokerage = intraday.get('fut_brokerage') or 0.00
            raw_fut_brokerage = to * fut_brokerage / 100
            self.brokerage = raw_fut_brokerage if raw_fut_brokerage < 20 else 20

            # STT Function
            fut_stt = intraday.get('fut_stt') or 0.00
            self.stt_total = sell_to * fut_stt / 100
            # Transaction Charge
            fut_bse_transaction = intraday.get('fut_bse_transaction') or 0.00
            fut_nse_transaction = intraday.get('fut_nse_transaction') or 0.00
            if self.tax_select == 'bse':
                self.total_txn_charge = (fut_bse_transaction if buy_to else 0.0) + (
                fut_bse_transaction if sell_to else 0.0)
            elif self.tax_select == 'nse':
                self.total_txn_charge = to * (fut_nse_transaction / 100)

            # gst fucntion
            fut_gst = intraday.get('fut_gst') or 0.00
            self.gst = (self.brokerage + self.total_txn_charge) * fut_gst / 100
            # SEBI Charge
            fut_sebi_charges = intraday.get('fut_sebi') or 0.00
            self.sebi_charges = (buy_to + sell_to) * (fut_sebi_charges / 10000000)
            # Total TAX And Charges
            self.total_tax_and_charges = self.brokerage + self.stt_total + self.total_txn_charge + self.gst + self.sebi_charges
            # Net Profit
            self.net_profit = sell_to - buy_to - self.total_tax_and_charges



        if self.select_mode == 'options':
            intraday = eval(config_param_env.get_param('equity_option') or '{}')
            opt_brokerage = intraday.get('opt_brokerage') or 0.00
            self.brokerage = (opt_brokerage if buy_to else 0.00) + (opt_brokerage if sell_to else 0.0)

            # STT Function
            opt_stt = intraday.get('opt_stt') or 0.00
            self.stt_total = sell_to * opt_stt / 100
            # Transaction Charge
            opt_bse_transaction = intraday.get('opt_bse_transaction') or 0.00
            opt_nse_transaction = intraday.get('opt_nse_transaction') or 0.00
            if self.tax_select == 'bse':
                self.total_txn_charge = (opt_bse_transaction if buy_to else 0.0) + (
                opt_bse_transaction if sell_to else 0.0)
            elif self.tax_select == 'nse':
                self.total_txn_charge = to * (opt_nse_transaction / 100)

            # gst fucntion
            opt_gst = intraday.get('opt_gst') or 0.00
            self.gst = (self.brokerage + self.total_txn_charge) * opt_gst / 100
            # SEBI Charge
            opt_sebi_charges = intraday.get('opt_sebi') or 0.00
            self.sebi_charges = (buy_to + sell_to) * (opt_sebi_charges / 10000000)
            # Total TAX And Charges
            self.total_tax_and_charges = self.brokerage + self.stt_total + self.total_txn_charge + self.gst + self.sebi_charges
            # Net Profit
            self.net_profit = sell_to - buy_to - self.total_tax_and_charges
