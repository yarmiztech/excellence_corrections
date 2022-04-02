from odoo import models,fields,api
from datetime import datetime,date



class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    # def compute_sheet(self):
    #     super(HrPayslip, self).compute_sheet()
    #     overtime = 0
    #     total_amount = 0
    #     print('calllll')
    #     for ovr in self.line_ids.filtered(lambda a:a.code == 'OT'):
    #             print('ovr',ovr,ovr.amount)
    #             prev_month = date.today().month - 1
    #             timesheets = self.env['account.analytic.line'].search([('employee_id', '=', self.employee_id.id)])
    #             print('timesheets', timesheets)
    #
    #             total_amount =0
    #             for time in timesheets:
    #                 if time.date < self.date_from:
    #                     timesheet = time.date.month
    #                     from_date = self.date_from.month-1
    #                     if timesheet == from_date:
    #                         overtime += time.overtime_amt
    #                         print('overtime',overtime)
    #                         print('time.overtime_amt',time.overtime_amt)
    #                     else:
    #                         overtime = 0.00
    #                         print('overtime',overtime)
    #
    #                 else:
    #                     overtime = 0.00
    #                     print('overtime', overtime)
    #
    #             project_task = self.env['project.task'].search([('timesheet_ids', '=', time.id)])
    #             print('project_task', project_task)
    #
    #             for amt in project_task:
    #                 total_amount += overtime * amt.hour_charge
    #                 print(total_amount)
    #             ovr.amount = total_amount
    #     if self.struct_id.name == 'Timesheet Salary Structure':
    #         for i in self.line_ids.filtered(lambda a: a.code == 'NET'):
    #             for timesalary in self.line_ids.filtered(lambda a: a.code == 'TS'):
    #                 for ded in self.line_ids.filtered(lambda a: a.code == 'DED'):
    #                     i.amount = timesalary.amount - ded.amount
    #                     print(i.amount)
    #
    #     # for i in self.line_ids.filtered(lambda a:a.code == 'NET'):
    #     #     if self.line_ids.filtered(lambda a: a.code == 'OT'):
    #     #         for ovr in self.line_ids.filtered(lambda a: a.code == 'OT'):
    #     #             i.amount = i.amount +ovr.amount
    #     #             print('i.amountnet',i.amount)
    #     #
    #     #             # i.total = i.total +ovr.amount
    #     #     else:
    #     #         i.amount = i.amount
    #     #         print('i.amount', i.amount)
    #     #
    #     # for i in self.line_ids.filtered(lambda a:a.code == 'NET'):
    #     #     if self.line_ids.filtered(lambda a: a.code == 'OT'):
    #     #         for ovr in self.line_ids.filtered(lambda a: a.code == 'OT'):
    #     #             i.amount = i.amount +ovr.amount
    #     #             print('i.amountnet',i.amount)
    #     #
    #     #             # i.total = i.total +ovr.amount
    #     #     else:
    #     #         i.amount = i.amount
    #     #         print('i.amount', i.amount)
    #
    #
    #             # i.total = i.total
    #         # if self.line_ids.filtered(lambda a: a.code == 'TS'):
    #         #     for timesalary in self.line_ids.filtered(lambda a: a.code == 'TS'):
    #         #
    #         #         # i.amount = i.amount +timesalary.amount
    #         #         print("nbn")
    #         #         timesheets = self.env['account.analytic.line'].search([('employee_id', '=', self.employee_id.id)])
    #         #
    #         #         for time in timesheets:
    #         #             overtime += time.overtime_amt
    #         #             total_amount += overtime * time.employee_id.timesheet_cost
    #         #             timesalary.amount = timesalary.amount - total_amount
    #         #             print("i.amount")
    #         #             # i.total = timesalary.amount - total_amount
    #         #
    #         #         # i.total = i.total +ovr.amount
    #         # else:
    #         #     i.amount = i.amount
    def compute_sheet(self):
        super(HrPayslip, self).compute_sheet()
        overtime = 0
        total_amount = 0
        print('calllll')
        if self.struct_id.name != 'Timesheet Salary Structure':
            for ovr in self.line_ids.filtered(lambda a: a.code == 'OT'):
                print('ovr', ovr, ovr.amount)
                prev_month = date.today().month - 1
                timesheets = self.env['account.analytic.line'].search([('employee_id', '=', self.employee_id.id)])
                total_amount = 0
                for time in timesheets:
                    if time.date < self.date_from:
                        timesheet = time.date.month
                        from_date = self.date_from.month - 1
                        if timesheet == from_date:
                            overtime += time.overtime_amt
                project_task = self.env['project.task'].search([('timesheet_ids', '=', time.id)])
                for amt in project_task:
                    total_amount += overtime * amt.hour_charge
                ovr.amount = total_amount
        else:
            for ovr in self.line_ids.filtered(lambda a: a.code == 'OT'):
                print('ovr', ovr, ovr.amount)
                prev_month = date.today().month - 1
                # hr.employee
                timesheets = self.env['account.analytic.line'].search([('employee_id', '=', self.employee_id.id)])
                total_amount = 0
                for time in timesheets:
                    if time.date < self.date_from:
                        timesheet = time.date.month
                        from_date = self.date_from.month - 1
                        if timesheet == from_date:
                            overtime += time.overtime_amt

                # for amt in project_task:
                total_amount += overtime * self.employee_id.timesheet_cost
                ovr.amount = total_amount
        # for i in self.line_ids.filtered(lambda a: a.code == 'NET'):
        #     if self.line_ids.filtered(lambda a: a.code == 'OT'):
        #         for ovr in self.line_ids.filtered(lambda a: a.code == 'OT'):
        #             i.amount = i.amount + ovr.amount
        #             # i.total = i.total +ovr.amount
        #     else:
        #         i.amount = i.amount
        #         # i.total = i.total
        #     # if self.line_ids.filtered(lambda a: a.code == 'TS'):
        #     #     for timesalary in self.line_ids.filtered(lambda a: a.code == 'TS'):
        #     #         i.amount = i.amount + timesalary.amount
        #     #         # i.total = i.total +ovr.amount
        #     # else:
        #     #     i.amount = i.amount
        # if self.struct_id.name == 'Timesheet Salary Structure':
            for i in self.line_ids.filtered(lambda a: a.code == 'NET'):
                for timesalary in self.line_ids.filtered(lambda a: a.code == 'TS'):
                    for ded in self.line_ids.filtered(lambda a: a.code == 'DED'):
                        i.amount = total_amount+timesalary.amount - ded.amount
                        print(i.amount)




class TimesheetIds(models.Model):
    _inherit = 'account.analytic.line'

    weekend_or_holiday = fields.Boolean('Weekend/Holiday')

