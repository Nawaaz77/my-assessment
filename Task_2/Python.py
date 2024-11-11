import os

import numpy as np
import pandas as pd

"""
To answer the following questions, make use of datasets: 
    'scheduled_loan_repayments.csv'
    'actual_loan_repayments.csv'
These files are located in the 'data' folder. 

'scheduled_loan_repayments.csv' contains the expected monthly payments for each loan. These values are constant regardless of what is actually paid.
'actual_loan_repayments.csv' contains the actual amount paid to each loan for each month.

All loans have a loan term of 2 years with an annual interest rate of 10%. Repayments are scheduled monthly.
A type 1 default occurs on a loan when any scheduled monthly repayment is not met in full.
A type 2 default occurs on a loan when more than 15% of the expected total payments are unpaid for the year.

Note: Do not round any final answers.

"""


def calculate_df_balances(df_scheduled, df_actual):
    """
    This is a utility function that creates a merged dataframe that will be used in the following questions.
    This function will not be graded, do not make changes to it.

    Args:
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
        df_actual (DataFrame): Dataframe created from the 'actual_loan_repayments.csv' dataset

    Returns:
        DataFrame: A merged Dataframe with additional calculated columns to help with the following questions.

    """

    df_merged = pd.merge(df_actual, df_scheduled)

    def calculate_balance(group):
        r_monthly = 0.1 / 12
        group = group.sort_values("Month")
        balances = []
        interest_payments = []
        loan_start_balances = []
        for index, row in group.iterrows():
            if balances:
                interest_payment = balances[-1] * r_monthly
                balance_with_interest = balances[-1] + interest_payment
            else:
                interest_payment = row["LoanAmount"] * r_monthly
                balance_with_interest = row["LoanAmount"] + interest_payment
                loan_start_balances.append(row["LoanAmount"])

            new_balance = balance_with_interest - row["ActualRepayment"]
            interest_payments.append(interest_payment)

            new_balance = max(0, new_balance)
            balances.append(new_balance)

        loan_start_balances.extend(balances)
        loan_start_balances.pop()
        group["LoanBalanceStart"] = loan_start_balances
        group["LoanBalanceEnd"] = balances
        group["InterestPayment"] = interest_payments
        return group

    df_balances = (
        df_merged.groupby("LoanID", as_index=False)
        .apply(calculate_balance)
        .reset_index(drop=True)
    )

    df_balances["LoanBalanceEnd"] = df_balances["LoanBalanceEnd"].round(2)
    df_balances["InterestPayment"] = df_balances["InterestPayment"].round(2)
    df_balances["LoanBalanceStart"] = df_balances["LoanBalanceStart"].round(2)

    return df_balances


# Do not edit these directories
root = os.getcwd()

if "Task_2" in root:
    df_scheduled = pd.read_csv("data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("data/actual_loan_repayments.csv")
else:
    df_scheduled = pd.read_csv("Task_2/data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("Task_2/data/actual_loan_repayments.csv")

df_balances = calculate_df_balances(df_scheduled, df_actual)


def question_1(df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 1 default definition.

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The percentage of type 1 defaulted loans (ie 50.0 not 0.5)

    """
    #Get the number of total loans 
    totalLoans = df_balances["LoanID"].nunique()
    loanTracker = []
    numDefaults1 = 0
    
    for index, row in df_balances.iterrows():
        if(row["ActualRepayment"] < row["ScheduledRepayment"]): #Check condition to see if a type 1 default occurs
            if(row["LoanID"] not in loanTracker):               #Since a loan is a default if any single payment is missed, there is no need to check further after it has been flagged
                numDefaults1 += 1
                loanTracker.append(row["LoanID"])

    default_rate_percent = (numDefaults1 / (totalLoans * 1.0)) * 100
        
    return default_rate_percent


def question_2(df_scheduled, df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 2 default definition

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset

    Returns:
        float: The percentage of type 2 defaulted loans (ie 50.0 not 0.5)

    """
    totalLoans = df_balances["LoanID"].nunique()
    loanTracker = 0
    sumPaid = 0
    sumOwed = 0
    
    
    final_df = df_balances.sort_values(by=['LoanID'], ascending=False)
    #get list of unique loan ID's to loop through
    loans = df_balances["LoanID"].unique()
    
    for l in loans:
        sumPaid = df_balances.loc[df_balances['LoanID'] == l, 'ActualRepayment'].sum()
        sumOwed = df_balances.loc[df_balances['LoanID'] == l, 'ScheduledRepayment'].sum()
    
        #Check to see if what was paid is 15% less than what was expected
        # loanTracker is used to count how many loans meet this type 2 condition
        if((sumPaid / (sumOwed * 1.0)) < 0.85):
            loanTracker += 1
    
        sumPaid = 0
        sumOwed = 0
    
    default_rate_percent = ((loanTracker) / totalLoans * 1.0) * 100
    return default_rate_percent


def question_3(df_balances):
    """
    Calculate the anualized portfolio CPR (As a %) from the geometric mean SMM.
    SMM is calculated as: (Unscheduled Principal)/(Start of Month Loan Balance)
    SMM_mean is calculated as (∏(1+SMM))^(1/12) - 1
    CPR is calcualted as: 1 - (1- SMM_mean)^12

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The anualized CPR of the loan portfolio as a percent.

    """
    SMM = []
    SMM_GMean = 0
    CPR = 0
    months = df_balances["Month"].unique()

    #filter the df_balances table to only data that is applicable - where principal payments were made
    principalPayments = df_balances[df_balances['ActualRepayment'] > df_balances['ScheduledRepayment']]
    
    #Get SMM's for each individual month
    for m in months:
        principalAmount = principalPayments.loc[principalPayments['Month'] == m, 'ActualRepayment'].sum() - principalPayments.loc[principalPayments['Month'] == m, 'ScheduledRepayment'].sum()
    
        sumBalance = principalPayments.loc[principalPayments['Month'] == m, 'LoanBalanceStart'].sum()
        SMM.append(principalAmount / sumBalance)
    
    tot = 1
    for i in SMM:
        tot = tot * (1 + i)
    
    SMM_GMean = (tot ** (1/12) ) - 1
    
    
    CPR = 1 - (1 - SMM_GMean) ** 12
    
    cpr_percent = CPR * 100
                     

    return cpr_percent


def question_4(df_balances):
    """
    Calculate the predicted total loss for the second year in the loan term.
    Use the equation: probability_of_default * total_loan_balance * (1 - recovery_rate).
    The probability_of_default value must be taken from either your question_1 or question_2 answer.
    Decide between the two answers based on which default definition you believe to be the more useful metric.
    Assume a recovery rate of 80%

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The predicted total loss for the second year in the loan term.

    """

    #Get the total loan balance for the new year
    loanBalance  = df_balances['LoanBalanceEnd'].sum()

    # Question2's value is used as it is a more accurate representation of what is likely to not be paid at at the end of the year
    # A person can miss a monthly payment but it is possible they make up for it over the next few months

    predictedLoss = (question_2(df_scheduled, df_balances)/100) * loanBalance * (1-0.8)

    total_loss = predictedLoss

    return total_loss






