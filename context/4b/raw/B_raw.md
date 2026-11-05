## Claim  
- **Claim_Identifier**: Unique identifier for a claim.  
- **Catastrophe_Identifier**: Reference to the catastrophe event associated with the claim.  
- **Claim_Description**: Description of the claim.  
- **Claims_Made_Date**: Date when the claim was made.  
- **Company_Claim_Number**: Claim number assigned by the company.  
- **Company_Subclaim_Number**: Subclaim number assigned by the company.  
- **Insurable_Object_Identifier**: Reference to the insurable object involved in the claim.  
- **Occurrence_Identifier**: Reference to the occurrence associated with the claim.  
- **Entry_Into_Claims_Made_Program_Date**: Date when the claim was entered into the claims made program.  
- **Claim_Open_Date**: Date when the claim was opened.  
- **Claim_Close_Date**: Date when the claim was closed.  
- **Claim_Reopen_Date**: Date when the claim was reopened.  
- **Claim_Status_Code**: Code indicating the status of the claim (e.g., open, closed, reopened).  
- **Claim_Reported_Date**: Date when the claim was reported.  

## Claim_Amount  
- **Claim_Amount_Identifier**: Unique identifier for a claim amount.  
- **Claim_Identifier**: Reference to the claim associated with the amount.  
- **Claim_Offer_Identifier**: Reference to the claim offer associated with the amount.  
- **Amount_Type_Code**: Code indicating the type of amount (e.g., payment, reserve).  
- **Event_Date**: Date when the event related to the amount occurred.  
- **Claim_Amount**: Amount of money involved in the claim.  
- **Insurance_Type_Code**: Code indicating the type of insurance.  

## Loss_Payment  
- **Claim_Amount_Identifier**: Reference to the claim amount associated with a payment.  

## Loss_Reserve  
- **Claim_Amount_Identifier**: Reference to the claim amount associated with a reserve.  

## Expense_Payment  
- **Claim_Amount_Identifier**: Reference to the claim amount associated with an expense payment.  

## Expense_Reserve  
- **Claim_Amount_Identifier**: Reference to the claim amount associated with an expense reserve.  

## Claim_Coverage  
- **Claim_Identifier**: Reference to the claim associated with coverage.  
- **Effective_Date**: Date when the coverage became effective.  
- **Policy_Coverage_Detail_Identifier**: Reference to the policy coverage detail associated with the claim.  

## Policy_Coverage_Detail  
- **Effective_Date**: Date when the coverage detail became effective.  
- **Policy_Coverage_Detail_Identifier**: Unique identifier for the policy coverage detail.  
- **Coverage_Identifier**: Reference to the coverage type.  
- **Insurable_Object_Identifier**: Reference to the insurable object associated with the coverage.  
- **Policy_Identifier**: Reference to the policy associated with the coverage detail.  
- **Coverage_Part_Code**: Code indicating the part of the coverage.  
- **Coverage_Description**: Description of the coverage.  
- **Expiration_Date**: Date when the coverage expires.  
- **Coverage_Inclusion_Exclusion_Code**: Code indicating whether the coverage is included or excluded.  

## Policy  
- **Policy_Identifier**: Unique identifier for a policy.  
- **Effective_Date**: Date when the policy became effective.  
- **Expiration_Date**: Date when the policy expires.  
- **Policy_Number**: Number assigned to the policy.  
- **Status_Code**: Code indicating the status of the policy (e.g., active, inactive).  
- **Geographic_Location_Identifier**: Reference to the geographic location associated with the policy.  

## Policy_Amount  
- **Policy_Amount_Identifier**: Unique identifier for a policy amount.  
- **Geographic_Location_Identifier**: Reference to the geographic location associated with the policy amount.  
- **Policy_Identifier**: Reference to the policy associated with the amount.  
- **Effective_Date**: Date when the policy amount became effective.  
- **Amount_Type_Code**: Code indicating the type of amount (e.g., payment, reserve).  
- **Earning_Begin_Date**: Date when earnings begin for the policy amount.  
- **Earning_End_Date**: Date when earnings end for the policy amount.  
- **Policy_Coverage_Detail_Identifier**: Reference to the policy coverage detail associated with the amount.  
- **Policy_Amount**: Amount of money involved in the policy.  
- **Insurable_Object_Identifier**: Reference to the insurable object associated with the policy amount.  
- **Insurance_Type_Code**: Code indicating the type of insurance.  

## Agreement_Party_Role  
- **Agreement_Identifier**: Reference to the agreement associated with the party role.  
- **Party_Identifier**: Reference to the party involved in the agreement.  
- **Party_Role_Code**: Code indicating the role of the party in the agreement.  
- **Effective_Date**: Date when the party role became effective.  
- **Expiration_Date**: Date when the party role expires.