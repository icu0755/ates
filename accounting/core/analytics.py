from collections import defaultdict
from datetime import date


class Analytics:
    def __init__(self):
        self.top_management_income = 0
        self.negative_balance_count = 0
        self.most_expensive_tasks = defaultdict(int)

    def task_assigned(self, account, assign_cost):
        self.top_management_income += assign_cost
        old_balance = account.balance + assign_cost

        if account.balance < 0 <= old_balance:
            self.negative_balance_count += 1

    def task_completed(self, account, complete_cost):
        self.top_management_income -= complete_cost
        old_balance = account.balance - complete_cost

        if old_balance < 0 <= account.balance:
            self.negative_balance_count -= 1

        today = date.today()
        self.most_expensive_tasks[today] = max(
            self.most_expensive_tasks[today], complete_cost
        )

    def close_billing_cycle(self):
        self.top_management_income = 0
        self.negative_balance_count = 0

    def get_top_management_income(self):
        return self.top_management_income

    def get_negative_balance_count(self):
        return self.negative_balance_count

    def get_most_expensive_task_for_period(self, start, end):
        most_expensive = 0
        for task_date, complete_cost in self.most_expensive_tasks.items():
            if task_date < start:
                continue
            if task_date > end:
                continue
            most_expensive = max(most_expensive, complete_cost)
        return most_expensive


analytics = Analytics()
