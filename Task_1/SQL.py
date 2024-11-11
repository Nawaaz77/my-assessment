"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)


NOTE:
Each question in this section is isolated, for example, you do not need to consider how Q5 may affect Q4.
Remember to clean your data.

"""

#A COUNT function is used to count occurences of customers that are duplicated
def question_1():
    """
    Find the name, surname and customer ids for all the duplicated customer ids in the customers dataset.
    Return the `Name`, `Surname` and `CustomerID`
    """

    qry = """Select Name, 
                    Surname, 
                    CustomerID  
                    FROM customers 
                    GROUP BY CustomerID, Name, Surname Having COUNT(CustomerID) > 1"""

    return qry

#Order By clause is used to get the correct ordering. DESC is specified as the ORDER BY clause is ASC by default
def question_2():
    """
    Return the `Name`, `Surname` and `Income` of all female customers in the dataset in descending order of income
    """

    qry = """SELECT Name, Surname, Income 
    FROM customers 
    WHERE Gender ='Female' ORDER BY Income DESC"""

    return qry

#CASE statement used to accomplish count of approved loans. No else is added as only the true condition should be accounted for
def question_3():
    """
    Calculate the percentage of approved loans by LoanTerm, with the result displayed as a percentage out of 100.
    ie 50 not 0.5
    There is only 1 loan per customer ID.
    """

    qry = """Select LoanTerm, 
            (Count(CASE WHEN ApprovalStatus = 'Approved' THEN 1 END)/Count(LoanTerm)) * 100.0 AS PercentageApproved 
            FROM loans GROUP BY LoanTerm"""

    return qry

#DISTINCT is used to account for duplicated customers. 
def question_4():
    """
    Return a breakdown of the number of customers per CustomerClass in the credit data
    Return columns `CustomerClass` and `Count`
    """

    qry = """Select CustomerClass, 
            Count(DISTINCT(CustomerID)) AS Count 
            FROM credit GROUP BY CustomerClass 
            ORDER BY CustomerClass"""

    return qry


def question_5():
    """
    Make use of the UPDATE function to amend/fix the following: Customers with a CreditScore between and including 600 to 650 must be classified as CustomerClass C.
    """

    qry = """Update credit SET CustomerClass = 'C' WHERE CreditScore >=600 and CreditScore <=650"""

    return qry
