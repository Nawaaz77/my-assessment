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
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""

#AVG function is used to calculate the average income. Additioanlly, a DISTINCT is used to account for duplicated customers. 
def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    qry = """Select cr.CustomerClass, 
            AVG(cd.Income) as AverageIncome FROM (SELECT Distinct(CustomerID), CustomerClass FROM credit) cr
            JOIN customers cd ON cr.CustomerID = cd.CustomerID 
            GROUP BY cr.CustomerClass"""

    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

    qry = """Select n.Region, 
    Count(CASE WHEN n.ApprovalStatus = 'Rejected' THEN 1 END) FROM (SELECT c.CustomerID, c.Region, l.ApprovalStatus FROM customers c JOIN loans l ON l.CustomerID = c.CustomerID) n 
    GROUP BY     
    CASE
        WHEN n.Region IN ('Mpumalanga', 'MP') THEN 'Mpumalanga'
        WHEN n.Region IN ('WesternCape', 'WC') THEN 'Western Cape'
        WHEN n.Region IN ('EasternCape', 'EC') THEN 'Eastern Cape'
        WHEN n.Region IN ('Gauteng', 'GT') THEN 'Gauteng'
        WHEN n.Region IN ('KwaZulu-Natal', 'KZN') THEN 'KwaZulu-Natal'
        ELSE n.Region
    END
    
    ;"""

    return qry


def question_3():
    """
    Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    qry = """CREATE TABLE financing (
            CustomerID int PRIMARY KEY,
            Income float,
            LoanAmount float,
            InterestRate float,
            ApprovalStatus varchar(8),
            CreditScore int
            )"""

    return qry


# Question 4 and 5 are linked

#HOUR function is used to extract the time from the DateTime column and 2 hours are added onto those times to account for LONDON time
def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time.
    Null values to be filled with 0.

    Hint: there should be 12x CustomerID = 1.
    """

    qry ="""
    
    CREATE TABLE timeline AS
        SELECT 
        r.CustomerID,
        m.MonthName AS MonthName,
        COUNT(r.RepaymentID) AS NumberOfRepayments,
        COALESCE(SUM(r.Amount), 0) AS AmountTotal
        
        FROM repayments r
        CROSS JOIN months m
    
        WHERE Month(r.RepaymentDate) = m.MonthID 
        AND
        HOUR(r.RepaymentDate) >= 8 and HOUR(r.RepaymentDate) <= 20
    
        GROUP BY
        r.CustomerID, m.MonthName
    
        ORDER BY
    
        r.CustomerID, m.MonthName
        
        """

    return qry

#COALESCE is used to avoid null values for cases when there is no data. 
def question_5():
    """
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """

    qry = """SELECT 
    CustomerID,

    COALESCE(SUM(CASE WHEN MonthName = 'January' THEN NumberOfRepayments END) , 0) AS JanuaryRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'January' THEN AmountTotal END),0 ) AS JanuaryTotal,
    
    COALESCE(SUM(CASE WHEN MonthName = 'February' THEN NumberOfRepayments END) , 0) AS FebruaryRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'February' THEN AmountTotal END),0 ) AS FebruaryTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'March' THEN NumberOfRepayments END) , 0) AS MarchRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'March' THEN AmountTotal END),0 ) AS MarchTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'April' THEN NumberOfRepayments END) , 0) AS AprilRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'April' THEN AmountTotal END),0 ) AS AprilTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'May' THEN NumberOfRepayments END) , 0) AS MayRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'May' THEN AmountTotal END),0 ) AS MayTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'June' THEN NumberOfRepayments END) , 0) AS JuneRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'June' THEN AmountTotal END),0 ) AS JuneTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'July' THEN NumberOfRepayments END) , 0) AS JulyRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'July' THEN AmountTotal END),0 ) AS JuluTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'August' THEN NumberOfRepayments END) , 0) AS AugustRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'August' THEN AmountTotal END),0 ) AS AugustTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'September' THEN NumberOfRepayments END) , 0) AS SeptemberRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'September' THEN AmountTotal END),0 ) AS SeptemberTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'October' THEN NumberOfRepayments END) , 0) AS OctoberRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'October' THEN AmountTotal END),0 ) AS OctoberTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'November' THEN NumberOfRepayments END) , 0) AS NovemberRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'November' THEN AmountTotal END),0 ) AS NovemberTotal,
        
    COALESCE(SUM(CASE WHEN MonthName = 'December' THEN NumberOfRepayments END) , 0) AS DecemberRepayments,
    COALESCE(SUM(CASE WHEN MonthName = 'December' THEN AmountTotal END),0 ) AS DecemberTotal
    

    FROM 
        timeline
    GROUP BY 
        CustomerID;
    
"""

    return qry


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these question.

#LAG function is used to shift the customer table accordingly. 0 is the defaulted age given for overflow.
def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """

    qry = """CREATE TABLE corrected_customers AS
            SELECT CustomerID, 
            Age, 
            LAG(Age, 2, 0) OVER (PARTITION BY Gender ORDER BY CustomerID) AS CorrectedAge, 
            Gender

            FROM customers;
            
            SELECT * FROM corrected_customers ; """

    return qry


def question_7():
    """
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`
    """

    qry = """ALTER TABLE corrected_customers 
            ADD COLUMN AgeCategory VARCHAR(20);

            UPDATE corrected_customers
            SET AgeCategory = CASE
            WHEN CorrectedAge < 20 THEN 'Teen'
            WHEN CorrectedAge >= 20 AND CorrectedAge < 30 THEN 'Young Adult'
            WHEN CorrectedAge >= 30 AND CorrectedAge < 60 THEN 'Adult'
            WHEN CorrectedAge >= 60 THEN 'Pensioner'
            END;
            
    """

    return qry
