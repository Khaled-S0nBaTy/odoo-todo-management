from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class ToDoManagement(models.Model):
    _name = 'todo_management'
    _description = 'ToDo Management'

    task_name = fields.Char(string='Task Name')
    description = fields.Char(string='Description')
    due_date = fields.Date(string='Due Date', default=fields.Date.today())
    is_late = fields.Boolean()
    estimated_time = fields.Float()
    active = fields.Boolean(default=True)
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),

    ], default='new')

    assign_to_id = fields.Many2one('res.users', string='Assign To')
    task_line_ids = fields.One2many('todo.line', 'task_id')

    # def check_due_date_if_late(self):
    #     tasks_ids = self.search([])
    #     for rec in tasks_ids:
    #         if (rec.due_date and rec.due_date < fields.Date.today() and
    #                 ( rec.status == 'new' or rec.status == 'in progress')):
    #             rec.is_late = True
    #         else:
    #             rec.is_late = False

    def late_task(self):
        late_todo = self.search([])
        for rec in late_todo:
            if rec.status == 'new' or rec.status == 'in_progress':
                if rec.due_date and rec.due_date < fields.date.today():
                    rec.is_late = True
                else:
                    rec.is_late = False

    @api.constrains('estimated_time', 'todo_line_ids.time')
    def time_diff(self):
        for rec in self:
            total_time = 0
            for lop in rec.task_line_ids:
                total_time += lop.time
            if total_time > rec.estimated_time:
                raise ValidationError("Total time exceeds estimated time")

    def action_new(self):
        for rec in self:
            rec.status = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.status = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.status = 'completed'

    def action_close(self):
        for rec in self:
            rec.status = 'closed'

    class TodoLine(models.Model):
        _name = 'todo.line'

        description = fields.Char()
        time = fields.Float()
        date = fields.Date()
        task_id = fields.Many2one('todo_management')
