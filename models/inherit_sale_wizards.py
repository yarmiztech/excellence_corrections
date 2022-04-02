from odoo import models,fields,api
from odoo.exceptions import ValidationError, UserError



class SaleWizard(models.Model):
    _inherit = 'sale.wizards'


    def create_sale_order(self):
        task_list = self.env['project.task'].search([('project_id', '=', self.project_id.id)])
        tax_id = self.env['account.tax'].search([('name', '=', 'Vat 15%'), ('type_tax_use', '=', 'sale')])
        sale_id = None
        order_list = []
        all_timesheet = []
        counter = 0
        total_hours = 0
        total_amount = 0
        for task in task_list:
            if task.unit == 'Hour':
                timesheets = self.env['account.analytic.line'].search(
                    [('date', '>=', self.from_date), ('date', '<=', self.to_date), ('sostatus', '=', 'unpaid'),
                     ('project_id', '=', self.project_id.id), ('task_id', '=', task.id)])
                if len(timesheets) > 0:
                    counter += 1
                for time in timesheets:
                    # total_hours += time.unit_amount + time.overtime_amt
                    total_hours += time.unit_amount
                    total_amount = task.payment_amt
                    all_timesheet.append(time.id)
                order_line = (0, 0, {
                    'product_id': task.product_id.product_variant_id.id,
                    # 'product_uom_qty': time.unit_amount,
                    'product_uom_qty': total_hours,
                    'price_unit': total_amount,
                    'name': 'Wage For(' + time.employee_id.name + ')',
                    'product_uom': (self.env['uom.uom'].search([('name', '=', 'Hours')])).id,
                    'tax_id': [(6, 0, tax_id.ids)],
                    'project_id': self.project_id.id,
                    'employee_id': time.employee_id.id,
                    'po_number': task.crm_id.po_number,
                })
                order_list.append(order_line)

                    # time.order_id = line_id.id
                    # time.sale_id = sale_id.id
                    # line.sostatus = 'paid'
            if task.unit == 'Monthly':
                timesheets = self.env['account.analytic.line'].search(
                    [('date', '>=', self.from_date), ('date', '<=', self.to_date), ('sostatus', '=', 'unpaid'),
                     ('project_id', '=', self.project_id.id), ('task_id', '=', task.id)])
                over_timesheets = self.env['account.analytic.line'].search(
                    [('date', '>=', self.from_date), ('date', '<=', self.to_date), ('sostatus', '=', 'unpaid'),
                     ('project_id', '=', self.project_id.id), ('task_id', '=', task.id), ('extra_time', '=', True)])
                # all_timesheet = all_timesheet + timesheets
                # all_timesheet = all_timesheet  + over_timesheets
                employees = timesheets.mapped('employee_id')
                all_timesheet.append(timesheets.mapped('id'))
                if len(timesheets) > 0 or len(over_timesheets) > 0:
                    counter += 1
                for emp in employees:
                    order_line = (0, 0, {
                        'product_id': task.product_id.product_variant_id.id,
                        'product_uom_qty': 1,
                        'price_unit': task.payment_amt,
                        'name': 'Wage For(' + emp.name + ')',
                        'product_uom': (self.env['uom.uom'].search([('name', '=', 'Month')])).id,
                        'tax_id': [(6, 0, tax_id.ids)],
                        'project_id': self.project_id.id,
                        'employee_id': emp.id,
                        'po_number': task.crm_id.po_number,
                    })
                    order_list.append(order_line)
                for over in over_timesheets:
                    all_timesheet.append(over.id)
                    order_line = (0, 0, {
                        'product_id': task.product_id.product_variant_id.id,
                        'product_uom_qty': over.unit_amount,
                        'price_unit': task.hour_charge,
                        'name': 'Wage For(' + over.employee_id.name + ')',
                        'product_uom': (self.env['uom.uom'].search([('name', '=', 'Hours')])).id,
                        'tax_id': [(6, 0, tax_id.ids)],
                        'project_id': self.project_id.id,
                        'employee_id': over.employee_id.id,
                        'po_number': task.crm_id.po_number,
                    })
                    order_list.append(order_line)
            if task.unit == 'Daily':
                # timesheets = self.env['account.analytic.line'].search(
                #     [('date', '>=', self.from_date), ('date', '<=', self.to_date), ('sostatus', '=', 'unpaid'),
                #      ('project_id', '=', self.project_id.id), ('task_id', '=', task.id)])
                timesheets = self.env['account.analytic.line'].search(
                    [('date', '>=', self.from_date), ('date', '<=', self.to_date), ('sostatus', '=', 'unpaid'),
                     ('project_id', '=', self.project_id.id), ('task_id', '=', task.id)])
                # over_timesheets = self.env['account.analytic.line'].search(
                #     [('date', '>=', self.from_date), ('date', '<=', self.to_date), ('sostatus', '=', 'unpaid'),
                #      ('project_id', '=', self.project_id.id), ('task_id', '=', task.id), ('extra_time', '=', True)])
                employees = timesheets.mapped('employee_id')
                all_timesheet.append(timesheets.mapped('id'))
                if len(timesheets) > 0:
                    counter += 1
                for emp in employees:
                    timesheets = self.env['account.analytic.line'].search(
                        [('date', '>=', self.from_date), ('date', '<=', self.to_date), ('sostatus', '=', 'unpaid'),
                         ('project_id', '=', self.project_id.id), ('task_id', '=', task.id),('employee_id','=',emp.id)])
                    order_line = (0, 0, {
                        'product_id': task.product_id.product_variant_id.id,
                        'product_uom_qty': len(timesheets),
                        'price_unit': task.payment_amt,
                        'name': 'Wage For(' + emp.name + ')',
                        'product_uom': (self.env['uom.uom'].search([('name', '=', 'Days')])).id,
                        'tax_id': [(6, 0, tax_id.ids)],
                        'project_id': self.project_id.id,
                        'employee_id': emp.id,
                        'po_number': task.crm_id.po_number,
                    })
                    order_list.append(order_line)

                # for emp in employees:
                #     timesheets = self.env['account.analytic.line'].search(
                #             [('date', '>=', self.from_date), ('date', '<=', self.to_date), ('sostatus', '=', 'unpaid'),
                #              ('project_id', '=', self.project_id.id), ('task_id', '=', task.id),
                #              ('employee_id', '=', emp.id)])
                #     if len(timesheets) > 0:
                #         counter += 1
                #     for time in timesheets:
                #         total_hours += time.overtime_amt
                #         total_amount = task.payment_amt
                #     if time.overtime_amt > 0:
                #         order_line = (0, 0, {
                #             'product_id': task.product_id.product_variant_id.id,
                #             # 'product_uom_qty': time.overtime_amt,
                #             'product_uom_qty': total_hours,
                #             # 'price_unit': task.hour_charge,
                #             'price_unit': task.hour_charge,
                #             'name': 'Wage For(' + time.employee_id.name + ')',
                #             'product_uom': (self.env['uom.uom'].search([('name', '=', 'Hours')])).id,
                #             'tax_id': [(6, 0, tax_id.ids)],
                #             'project_id': self.project_id.id,
                #             'employee_id': time.employee_id.id,
                #             'po_number': task.crm_id.po_number,
                #         })
                #         order_list.append(order_line)
                #         hours = self.env['sale.order.line'].search([('product_uom','=','Hours')])
                #         hours.unlink()


        if len(order_list) > 0:
            sale_id = self.env['sale.order'].create({
                'partner_id': self.project_id.partner_id.id,
                'analytic_account_id': self.project_id.analytic_account_id.id,
                'team_id': self.project_id.crm_id.team_id.id,
                'campaign_id': self.project_id.crm_id.campaign_id.id,
                'medium_id': self.project_id.crm_id.medium_id.id,
                'source_id': self.project_id.crm_id.source_id.id,
                'origin': 'Wage For ' + self.project_id.name,
                'from_date': self.from_date,
                'to_date': self.to_date,
                'opportunity_id': self.project_id.crm_id.id,
                'order_line': order_list,
                'po_number': self.project_id.crm_id.po_number,
            })
        if not sale_id:
            expenses = self.env['hr.expense'].search(
                [('analytic_account_id', '=', self.project_id.analytic_account_id.id), ('added', '=', 'no'),
                 ('add_in_invoice', '=', True), ('state', 'in', ('done', 'approved'))])
            if len(expenses) > 0:
                sale_id = self.env['sale.order'].create({
                    'partner_id': self.project_id.partner_id.id,
                    'analytic_account_id': self.project_id.analytic_account_id.id,
                    'team_id': self.project_id.crm_id.team_id.id,
                    'campaign_id': self.project_id.crm_id.campaign_id.id,
                    'medium_id': self.project_id.crm_id.medium_id.id,
                    'source_id': self.project_id.crm_id.source_id.id,
                    'origin': 'Wage For ' + self.project_id.name,
                    'from_date': self.from_date,
                    'to_date': self.to_date,
                    'opportunity_id': self.project_id.crm_id.id,
                    'po_number': self.project_id.crm_id.po_number,
                })

        if sale_id:
            self.project_id.allow_billable = True
            sale_id.project_id = self.project_id.id
            sale_id.project_ids = [(6, 0, self.project_id.ids)]
            sale_id.analytic_account_id = self.project_id.analytic_account_id.id
            expenses = self.env['hr.expense'].search(
                [('analytic_account_id', '=', self.project_id.analytic_account_id.id), ('added', '=', 'no'),
                 ('add_in_invoice', '=', True), ('state', 'in', ('done', 'approved'))])
            for ex_line in expenses:
                sale_line_id = self.env['sale.order.line'].create({
                    'order_id': sale_id.id,
                    'product_id': ex_line.product_id.id,
                    'product_uom_qty': ex_line.quantity,
                    'price_unit': ex_line.unit_amount,
                    'name': ex_line.name,
                    'product_uom': ex_line.product_id.uom_id.id,
                    'tax_id': ex_line.tax_ids,
                    'project_id': self.project_id.id,
                })
                ex_line.order_id = sale_line_id.id
                ex_line.sale_id = sale_id.id
                ex_line.added = 'yes'
        if counter > 0:
            for all_time in all_timesheet:
                times = self.env['account.analytic.line'].search([('id','=',all_time)])
                times.sale_id = sale_id.id
                times.sostatus = 'paid'
        else:
            raise UserError('Please Update the Timsheet')
        # if timesheets:
        #     sale_id = self.env['sale.order'].create({
        #         'partner_id': self.project_id.partner_id.id,
        #         'analytic_account_id': self.project_id.analytic_account_id.id,
        #         'team_id': self.project_id.crm_id.team_id.id,
        #         'campaign_id': self.project_id.crm_id.campaign_id.id,
        #         'medium_id': self.project_id.crm_id.medium_id.id,
        #         'source_id': self.project_id.crm_id.source_id.id,
        #         'origin': 'Wage For '+self.project_id.name,
        #         'from_date':self.from_date,
        #         'to_date':self.to_date,
        #         # 'payment_term_id': self.payment_terms_id.id,
        #         'opportunity_id': self.project_id.crm_id.id,
        #         # 'order_line': product_list,
        #         # 'timesheet_lines': timesheet_list,
        #         # 'so_month': month,
        #         # 'so_year': year,
        #         'po_number': self.project_id.crm_id.po_number,
        #     })
        #     if sale_id:
        #         self.project_id.allow_billable = True
        #         sale_id.project_id = self.project_id.id
        #         sale_id.project_ids = [(6, 0, self.project_id.ids)]
        #         sale_id.analytic_account_id = self.project_id.analytic_account_id.id
        #     # product_id = self.env['product.template'].search([('name','=','Man Power Service')])[0]
        #     tax_id = self.env['account.tax'].search([('name', '=', 'Vat 15%'), ('type_tax_use', '=', 'sale')])
        #     # print(tax_id)
        #     for line in timesheets:
        #         line_id = self.env['sale.order.line'].create({
        #             'order_id':sale_id.id,
        #             'product_id': line.task_id.product_id.product_variant_id.id,
        #             'product_uom_qty': line.unit_amount,
        #             'price_unit': line.task_id.payment_amt,
        #             'name': 'Wage For(' + line.employee_id.name + ')',
        #             'product_uom': (self.env['uom.uom'].search([('name', '=', 'Hours')])).id,
        #             'tax_id': [(6,0,tax_id.ids)],
        #             'project_id': self.project_id.id,
        #         })
        #         line.order_id = line_id.id
        #         line.sale_id = sale_id.id
        #         line.sostatus = 'paid'
        #     for ex_line in expenses:
        #         sale_line_id = self.env['sale.order.line'].create({
        #             'order_id': sale_id.id,
        #             'product_id': ex_line.product_id.id,
        #             'product_uom_qty': ex_line.quantity,
        #             'price_unit': ex_line.unit_amount,
        #             'name': ex_line.name,
        #             'product_uom': ex_line.product_id.uom_id.id,
        #             'tax_id': ex_line.tax_ids,
        #             'project_id': self.project_id.id,
        #         })
        #         ex_line.order_id = sale_line_id.id
        #         ex_line.sale_id = sale_id.id
        #         ex_line.added = 'yes'
        # else:
        #     raise UserError('Please Update the Timsheet')
