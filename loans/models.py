from django.db import models
from loans.utils import check_and_make_transaction

class Loans(models.Model):
    loan_statuses = [('pending', 'PENDING'), ('funded', 'FUNDED'), ('completed', 'COMPLETED')]

    borrower = models.ForeignKey("users.LenmeUser", related_name="borrower", on_delete=models.CASCADE)
    loan_amount = models.PositiveIntegerField()
    loan_period_in_month = models.PositiveSmallIntegerField()
    loan_status = models.CharField(choices=loan_statuses, default="pending", max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loan_status

    @property
    def investor(self):
        return self.loanoffers.get(accepted=True).investor

    def get_annual_interest_rate(self):
        return self.loanoffers.get(accepted=True).annual_interest_rate

    @property
    def amount_winterest(self):
        interest_amount = self.loan_amount*(self.get_annual_interest_rate()/100)*(self.loan_period_in_month/12)
        return self.loan_amount+interest_amount

    @property
    def monthly_payment(self):
        return self.amount_winterest/self.loan_period_in_month

    def payment_status(self):
        paid_amount = self.loanpayment.all().aggregate(total=models.Sum('paid_amount'))['total'] or 0
        paid_monthes = self.loanpayment.count()
        remain_amount = self.amount_winterest - paid_amount
        remain_monthes = self.loan_period_in_month - paid_monthes
        return {
            "paid_amount":paid_amount,
            "paid_monthes":paid_monthes,
            "remain_amount":remain_amount,
            "remain_monthes":remain_monthes
        }

class LoanOffers(models.Model):
    loan = models.ForeignKey("loans.Loans", related_name="loanoffers", on_delete=models.CASCADE)
    investor = models.ForeignKey("users.LenmeUser", related_name="loanoffers", on_delete=models.CASCADE)
    annual_interest_rate = models.FloatField()
    accepted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.accepted:
            check_and_make_transaction(self)

class LoanPayments(models.Model):
    loan = models.ForeignKey("loans.Loans", related_name="loanpayment", on_delete=models.CASCADE)
    paid_amount = models.FloatField()
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class LenmeVariables(models.Model):
    lenmefee = models.FloatField()