from django.apps import apps


def check_and_make_transaction(offer_obj):
    LenmeVariables = apps.get_model("loans", "LenmeVariables")

    lenme_fee = LenmeVariables.objects.last().lenmefee
    investor = offer_obj.investor
    borrower = offer_obj.loan.borrower
    loan_amount = offer_obj.loan.loan_amount

    if investor.userbalance >= (loan_amount+lenme_fee):
        #deduct total loan amount from investor balance
        investor.userbalance -= loan_amount+lenme_fee
        investor.save()

        #add loan amount to borrower balance
        borrower.userbalance += loan_amount
        borrower.save()

        #change loan status to funded
        offer_obj.loan.loan_status = 'funded'
        offer_obj.loan.save()

    ### send notification/email to both investor and borrower wheather it is successfully funded or not

def is_loan_payment_completed(loan):
    payment_status = loan.payment_status()
    if payment_status['remain_monthes'] or payment_status['remain_amount']:
        return False 
    else:
        setattr(loan, 'loan_status', 'completed')
        loan.save()
        return True


def schedule_payment(loan):
    borrower = loan.borrower
    investor = loan.investor
    monthly_payment = loan.monthly_payment
    LoanPayments = apps.get_model("loans", "LoanPayments")

    #check if borrower balance is sufficient to pay monthly payment
    if borrower.userbalance >= monthly_payment and loan.loan_status != 'completed':
        # deduct monthly payment amount from borrower's balance
        borrower.userbalance -= monthly_payment
        borrower.save()

        # add monthly payment to investor's balance
        investor.userbalance += monthly_payment
        investor.save()

        # save this payment transaction
        LoanPayments.objects.create(loan=loan, paid_amount=monthly_payment)

        return is_loan_payment_completed(loan)


    ### send notification/email to both investor and borrower wheather monthly payment is successful or not
    
