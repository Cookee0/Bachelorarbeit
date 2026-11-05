Claim:
- Claim_Identifier: Unique identifier for claims.
- Catastrophe_Identifier: Reference to the catastrophe in the Catastrophe table.
- Claim_Description: Description of the claim.
- Claims_Made_Date: Date when the claim was made.
- Company_Claim_Number: Number used by the company.
- Insurable_Object_Identifier: Identifier for the insurable object.
- Occurrence_Identifier: Identifier for the occurrence of the claim.
- Entry_Into_Claims_Made_Program_Date: Date when the claim was entered into the program.
- Claim_Open_Date: Date when the claim opens.
- Claim_Close_Date: Date when the claim closes.
- Claim_Reopen_Date: Date when the claim reopens.
- Claim_Status_Code: Status code for the claim.
- Claim_Reported_Date: Date when the claim was reported.

Claim_Amount:
- Claim_Amount_Identifier: Unique identifier for the amount.
- Claim_Identifier: Identifier of the claim.
- Claim_Offer_Identifier: Identifier of the offer related to the claim.
- Amount_Type_Code: Code for the amount type.
- Event_Date: Date when the event occurred.
- Claim_Amount: Amount in decimal format.
- Insurance_Type_Code: Code for the insurance type.

Claim_Coverage:
- Claim_Identifier: Identifier for the claim.
- Effective_Date: Date when the policy coverage starts.
- Policy_Coverage_Detail_Identifier: Identifier of the policy coverage detail.
- Insurable_Object_Identifier: Identifier for the insurable object.

Expense_Payment:
- Claim_Amount_Identifier: Unique identifier for the payment.

Expense_Reserve:
- Claim_Amount_Identifier: Unique identifier for the reserve.

Loss_Payment:
- Claim_Amount_Identifier: Unique identifier for the payment.

Loss_Reserve:
- Claim_Amount_Identifier: Unique identifier for the reserve.

Policy:
- Policy_Identifier: Identifier for the policy.
- Effective_Date: Date when the policy starts.
- Expiration_Date: Date when the policy ends.
- Policy_Number: Number of the policy.
- Status_Code: Code for the status of the policy.
- Geographic_Location_Identifier: Identifier for the geographic location.

Policy_Amount:
- Policy_Amount_Identifier: Unique identifier for the amount.
- Geographic_Location_Identifier: Identifier for the location.
- Policy_Identifier: Identifier for the policy.
- Effective_Date: Date when the policy starts.
- Amount_Type_Code: Code for the amount type.
- Earning_Begin_Date: Start date of earnings.
- Earning_End_Date: End date of earnings.
- Policy_Coverage_Detail_Identifier: Identifier for the coverage detail.

Policy_Coverage_Detail:
- Effective_Date: Date when the policy covers.
- Policy_Coverage_Detail_Identifier: Identifier for the policy coverage detail.
- Coverage_Identifier: Identifier for the coverage part.
- Insurable_Object_Identifier: Identifier for the insurable object.
- Policy_Identifier: Identifier for the policy.
- Coverage_Part_Code: Code for the coverage part.
- Coverage_Description: Description of the coverage.
- Expiration_Date: Date when the coverage expires.
- Coverage_Inclusion_Exclusion_Code: Code for inclusion/exclusion.