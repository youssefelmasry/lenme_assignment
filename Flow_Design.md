# Flow Design:

### APIs:
```
	1. /user/register/ POST
		request:
			username: str
			email: str
			password: str
			usertype: str (investor/borrower)
		response:
			refresh: str(token)
			access: str(token)

	2. /user/token/obtain/ POST
		request:
			username/email: str
			password: str
		response:
			refresh: str(token)
			access: str(token)

	3. /user/token/refresh/ POST
		request:
			refresh: str(token)
		response:
			access: str(token)			

	4. /loans/submit/ POST
		request:
			user(borrower): Bearer token(Authorization header)
			loan_amount: int
			loan_period: int

		response:
			msg: "loan submitted check later for offers"

	5. /offer/submit/ POST
		request:
			user(investor): Bearer token(Authorization header)
			loan: int
			annual_interest_rate: float

	6. /offer/submit/<int:offer_id>/ PATCH
		request:
			user(borrower): Bearer token(Authorization header)
			accepted: boolean
```
### Database Models:
* Loans:
	* attributes:

	    * ***borrower:*** foriegen key(user)
	    * ***investor:*** foriegen key(user)
	    * ***loan_amount:*** positiveintegerfield(default:null)
	    * ***annual_interest_rate:*** floatfield(default:null)
	    * ***loan_period_month:*** positiveintegerfield
	    * ***loan_status:*** charfield (choises: pending(default), funded, completed)
	    * ***created_at:*** datetimefield
	    * ***updated_at:*** datetimefield

	* methods:

		* ***payment_status():*** -> {
			"paid_amount": float,
			"paid_monthes": int,
			"remain_amount":float,
			"remain_monthes":int,
		}
		* ***monthly_payment():*** -> float
		* ***amount_winterest():*** -> float
		* ***get_annual_interest_rate():*** -> flaot
		* ***investor():*** -> object

* payments:
	* ***loan:*** foriegen key(loans)
	* ***amount:*** floatfield
	* ***date:*** datetimefield

* LenmeAccount:
	* ***user:*** OneToOneField(user)
	* ***balance:*** floatfield
	* ***user_type:*** charfield (choices: borrower, investor)

* Lenme_Variabless:
	* ***Lenme_fee:*** floatfield

	*This table to make admin change the Lenme_fee anytime from admin dashboar, also to add any other fields*


*__P.S:__ In a real project I would create a table for each Investor & Borrower and link each one with User table, to give everone it's own fields*
*But in this assignment both will be in Lenme_Account with field user_type*



### utils_functions:
* ***check_and_make_transaction(object):*** -> None
* ***is_loan_payment_completed(object):*** -> boolean
* ***schedule_payment(object):*** -> boolean
