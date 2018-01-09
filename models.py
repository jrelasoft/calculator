from openerp import fields, api, models


# class brokerage_calc(models.Model):
# 	_name="brokerage.config"
# 	_inherit = "res.config.settings"

# 	int_gst_config=fields.Float('GST Change')
# 	int_brok_config=fields.Float('Brokerage Change')
# 	int_stt_config=fields.Float('STT Change')
# 	int_trans_config=fields.Float('Trasaction Change of BSE')
# 	int_sebi_config=fields.Float('SEBI Change')
# 	int_nse=fields.Float('Trasaction Change of NSE')

# 	del_gst_config=fields.Float('GST Change')
# 	del_brok_config=fields.Float('Brokerage Change')
# 	del_stt_config=fields.Float('STT Change')
# 	del_trans_config=fields.Float('Trasaction Change')
# 	del_sebi_config=fields.Float('SEBI Change')
# 	del_nse=fields.Float('Trasaction Change of NSE')

# 	fut_gst_config=fields.Float('GST Change')
# 	fut_brok_config=fields.Float('Brokerage Change')
# 	fut_stt_config=fields.Float('STT Change')
# 	fut_trans_config=fields.Float('Trasaction Change')
# 	fut_sebi_config=fields.Float('SEBI Change')
# 	fut_nse=fields.Float('Trasaction Change of NSE')

# 	opt_gst_config=fields.Float('GST Change')
# 	opt_brok_config=fields.Float('Brokerage Change')
# 	opt_stt_config=fields.Float('STT Change')
# 	opt_trans_config=fields.Float('Trasaction Change')
# 	opt_sebi_config=fields.Float('SEBI Change')
# 	opt_nse=fields.Float('Trasaction Change of NSE')

# 	@api.multi
# 	def set_equity_intraday(self):
# 		config_param_env = self.env['ir.config_parameter']

# 		equity_intraday = {
# 		'int_gst_config': self.int_gst_config or 0.00, 
# 		'int_brok_config': self.int_brok_config or 0.00,
# 		'int_stt_config': self.int_stt_config or 0.00,
# 		'int_trans_config': self.int_trans_config or 0.00,
# 		'int_sebi_config': self.int_sebi_config or 0.00,
# 		'int_nse': self.int_nse or 0.00,
# 		}
# 		config_param_env.set_param('equity_intraday', equity_intraday)


# 	@api.multi
# 	def get_default_equity_intraday(self):
# 		config_param_env = self.env['ir.config_parameter']

# 		equity_intraday = {}

# 		equity_intraday_str = config_param_env.get_param('equity_intraday')

# 		if equity_intraday_str:
# 			equity_intraday = eval(equity_intraday_str)

# 		return equity_intraday

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
        # print '\n---',self, buy_to, sell_to, to,'---\n'

        if self.select_mode == 'intraday':
            intraday = eval(config_param_env.get_param('equity_intraday') or '{}')
            int_brokerage = intraday.get('int_brokerage') or 0.00
            raw_int_brokerage = to * int_brokerage / 100
            self.brokerage = raw_int_brokerage if raw_int_brokerage < 20 else 20
            print '\n---', self.brokerage, '---\n'

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

# @api.onchange('select_mode','buy','quantity','sell','tax_select',)
# def calc_turnover_x(self):
# 	change = self.env['brokerage.config'].search([])
# 	if self.select_mode=='intraday':
# 		if self.buy:
# 			d1=self.buy*self.quantity
# 			d2=self.sell*self.quantity
# 			a=d1+d2
# 			self.turnover=a
# 		#function for Brokerage
# 			d3=d1 * 0.01/100 if change.int_brok_config==0.0 else d1 * change.int_brok_config/100
# 			d4=d2 * 0.01/100 if change.int_brok_config==0.0 else d2 * change.int_brok_config/100
# 			b=d3+d4
# 			self.brokerage=float(str(round(b, 2)))
# 		#function for STT Toatl
# 			c=d2*0.025/100 if change.int_stt_config==0.0 else d2 * change.int_stt_config/100
# 			self.stt_total=float(str(round(c, 2)))
# 		#fucntion for total transaction charge
# 			if self.tax_select=='nse':
# 				d5=d1*0.00325/100 if change.int_nse==0.0 else d1 * change.int_nse/100
# 				d6=d2*0.00325/100 if change.int_nse==0.0 else d2 * change.int_nse/100
# 				d=d5+d6
# 				self.total_txn_charge=float(str(round(d, 2)))
# 			if self.tax_select=='bse':
# 				d5=1.5 if change.int_trans_config==0.0 else change.int_trans_config
# 				d6=1.5 if change.int_trans_config==0.0 else change.int_trans_config
# 				d=d5+d6
# 				self.total_txn_charge=float(str(round(d, 2)))
# 		#function for GST
# 			d7=b+d
# 			e=d7 * 18/100 if change.int_gst_config==0.0 else d7 * change.int_gst_config/100
# 			self.gst=float(str(round(e, 2)))
# 		#function for SEBI
# 			print '\n--',a,'---\n'
# 			f=15.0/10000000 * a if change.int_sebi_config==0.0 else change.int_sebi_config/10000000 * a
# 			self.sebi_charges=float(str(round(f, 2)))
# 		#fucntion for total TAX
# 			g=b+c+d+e+f
# 			self.total_tax_and_charges=float(str(round(g, 2)))
# 		#function for Net Profit
# 			h=d1-g
# 			self.net_profit=float(str(round(h, 2)))

# 	elif self.select_mode=='delivery':
# 		if self.buy:
# 			d1=self.buy*self.quantity
# 			d2=self.sell*self.quantity
# 			a=d1+d2
# 			self.turnover=a
# 		#function for STT Toatl
# 			d3=d1 * 0.1/100 if change.del_stt_config==0.0 else d2 * change.del_stt_config/100
# 			d4=d2 * 0.1/100 if change.del_stt_config==0.0 else d2 * change.del_stt_config/100
# 			c=d3+d4
# 			self.stt_total=float(str(round(c, 2)))
# 		#fucntion for total transaction charge
# 			if self.tax_select=='nse':
# 				d5=d1*0.00325/100 if change.del_nse==0.0 else d1 * change.del_nse/100
# 				d6=d2*0.00325/100 if change.del_nse==0.0 else d2 * change.del_nse/100
# 				d=d5+d6
# 				self.total_txn_charge=float(str(round(d, 2)))
# 			if self.tax_select=='bse':
# 				d5=1.5 if change.del_trans_config==0.0 else change.del_trans_config
# 				d6=1.5 if change.del_trans_config==0.0 else change.del_trans_config
# 				d=d5+d6
# 				self.total_txn_charge=float(str(round(d, 2)))
# 		#function for GST
# 			e=d * 18/100 if change.del_gst_config==0.0 else d * change.del_gst_config/100
# 			self.gst=float(str(round(e, 2)))
# 		#function for SEBI
# 			f=15.0/10000000 * a if change.del_sebi_config==0.0 else change.del_sebi_config/10000000 * a
# 			self.sebi_charges=float(str(round(f, 2)))
# 		#fucntion for total TAX
# 			g=c+d+e+f
# 			self.total_tax_and_charges=float(str(round(g, 2)))
# 		#function for Net Profit
# 			h=d1-g
# 			self.net_profit=float(str(round(h, 2)))

# 	elif self.select_mode=='futures':
# 		if self.buy:
# 			d1=self.buy*self.quantity
# 			d2=self.sell*self.quantity
# 			a=d1+d2
# 			self.turnover=a
# 		#function for Brokerage
# 			d3=d1 * 0.01/100 if change.fut_brok_config==0.0 else d1 * change.fut_brok_config/100
# 			d4=d2 * 0.01/100 if change.fut_brok_config==0.0 else d2 * change.fut_brok_config/100
# 			b=d3+d4
# 			self.brokerage=float(str(round(b, 2)))
# 		#function for STT Toatl
# 			c=d2 * 0.01/100 if change.fut_stt_config==0.0 else d2 * change.fut_stt_config/100
# 			self.stt_total=float(str(round(c, 2)))
# 		#fucntion for total transaction charge
# 			if self.tax_select=='nse':
# 				d5=d1*0.0021/100 if change.fut_nse==0.0 else d1 * change.fut_nse/100
# 				d6=d2*0.0021/100 if change.fut_nse==0.0 else d2 * change.fut_nse/100
# 				d=d5+d6
# 				self.total_txn_charge=float(str(round(d, 2)))
# 			if self.tax_select=='bse':
# 				d5=1.5 if change.fut_trans_config==0.0 else change.fut_trans_config
# 				d6=1.5 if change.fut_trans_config==0.0 else change.fut_trans_config
# 				d=d5+d6
# 				self.total_txn_charge=float(str(round(d, 2)))
# 		#function for GST
# 			d7=b+d
# 			e=d7*18/100 if change.fut_gst_config==0.0 else d7 * change.fut_gst_config/100
# 			self.gst=float(str(round(e, 2)))
# 		#function for SEBI
# 			f=15.0/10000000 * a if change.fut_sebi_config==0.0 else change.fut_sebi_config/10000000 * a
# 			self.sebi_charges=float(str(round(f, 2)))
# 		#fucntion for total TAX
# 			g=b+c+d+e+f
# 			self.total_tax_and_charges=float(str(round(g, 2)))
# 		#function for Net Profit
# 			h=d1-g
# 			self.net_profit=float(str(round(h, 2)))

# 	elif self.select_mode=='options':
# 		if self.buy:
# 			d1=self.buy*self.quantity
# 			d2=self.sell*self.quantity
# 			a=d1+d2
# 			self.turnover=a
# 		#function for Brokerage
# 			d3=20 if change.opt_brok_config==0.0 else change.opt_brok_config
# 			d4=20 if change.opt_brok_config==0.0 else change.opt_brok_config
# 			b=d3+d4
# 			self.brokerage=float(str(round(b, 2)))
# 		#function for STT Toatl
# 			c=d2 * 0.05/100 if change.opt_stt_config==0.0 else d2 * change.opt_stt_config/100
# 			self.stt_total=float(str(round(c, 2)))
# 		#fucntion for total transaction charge
# 			if self.tax_select=='nse':
# 				d5=d1*0.053/100 if change.opt_nse==0.0 else d1 * change.opt_nse/100
# 				d6=d2*0.053/100 if change.opt_nse==0.0 else d2 * change.opt_nse/100
# 				d=d5+d6
# 				self.total_txn_charge=float(str(round(d, 2)))
# 			if self.tax_select=='bse':
# 				d5=1.5 if change.opt_trans_config==0.0 else change.opt_trans_config
# 				d6=1.5 if change.opt_trans_config==0.0 else change.opt_trans_config
# 				d=d5+d6
# 				self.total_txn_charge=float(str(round(d, 2)))
# 		#function for GST
# 			d7=b+d
# 			e=d7*18/100 if change.opt_gst_config==0.0 else d7 * change.opt_gst_config/100
# 			self.gst=float(str(round(e, 2)))
# 		#function for SEBI
# 			f=15.0/10000000 * a if change.opt_sebi_config==0.0 else change.opt_sebi_config/10000000 * a
# 			self.sebi_charges=float(str(round(f, 2)))
# 		#fucntion for total TAX
# 			g=b+c+d+e+f
# 			self.total_tax_and_charges=float(str(round(g, 2)))
# 		#function for Net Profit
# 			h=d1-g
# 			self.net_profit=float(str(round(h, 0)))
