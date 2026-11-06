## Claim



- **Claim_Identifier**: Unique identifier for a claim.

- **Catastrophe_Identifier**: Identifier of the catastrophe associated with this claim (if any).

- **Claim_Description**: Description of the claim event or incident.

- **Claims_Made_Date**: Date when the claim was made by the policyholder.

- **Company_Claim_Number**: Internal company-assigned number for tracking the claim.

- **Company_Subclaim_Number**: Sub-number used to identify a sub-claim under the main claim (if any).

- **Insurable_Object_Identifier**: Identifier of the insured object or property involved in the claim.

- **Occurrence_Identifier**: Identifier of the occurrence that led to the claim (if applicable).

- **Entry_Into_Claims_Made_Program_Date**: Date when the claim was entered into the claims-made program (if any).

- **Claim_Open_Date**: Date when the claim was officially opened or reported by the company.

- **Claim_Close_Date**: Date when the claim was closed, indicating resolution of the claim event.

- **Claim_Reopen_Date**: Date when a previously closed claim was reopened for further investigation or processing.

- **Claim_Status_Code**: Code representing the current status of the claim (e.g., open, closed, pending, etc.).

- **Claim_Reported_Date**: Date when the claim was reported to the company by the policyholder or third party.



## Claim_Amount



- **Claim_Amount_Identifier**: Unique identifier for a specific amount associated with a claim.

- **Claim_Identifier**: Identifier of the claim that this amount is related to.

- **Claim_Offer_Identifier**: Identifier of any offer made in relation to this claim (if applicable).

- **Amount_Type_Code**: Code indicating the type of amount, such as loss, expense, premium, etc. (e.g., "Loss" or "Expense").

- **Event_Date**: Date when the amount was recorded or associated with an event (e.g., a payment date or incident date).

- **Claim_Amount**: The actual monetary value of the claim amount (e.g., $1000, $2500, etc.).

- **Insurance_Type_Code**: Code indicating the type of insurance coverage that applies to this amount (e.g., property, liability, etc.).



## Loss_Payment



- **Claim_Amount_Identifier**: Identifier of the claim amount associated with a loss payment.



## Loss_Reserve



- **Claim_Amount_Identifier**: Identifier of the claim amount associated with a loss reserve.



## Expense_Payment



- **Claim_Amount_Identifier**: Identifier of the claim amount associated with an expense payment.



## Expense_Reserve



- **Claim_Amount_Identifier**: Identifier of the claim amount associated with an expense reserve.



## Claim_Coverage



- **Claim_Identifier**: Identifier of the claim that this coverage applies to.

- **Effective_Date**: Date when the coverage becomes active or effective for the claim.

- **Policy_Coverage_Detail_Identifier**: Unique identifier for a specific policy coverage detail that applies to this claim.



## Policy_Coverage_Detail



- **Effective_Date**: Date when the coverage becomes active or effective under the policy.

- **Policy_Coverage_Detail_Identifier**: Unique identifier for a specific coverage detail within the policy.

- **Coverage_Identifier**: Identifier of the general type of coverage (e.g., property, liability) covered by this detail (if applicable).

- **Insurable_Object_Identifier**: Identifier of the insured object or property that is covered under this policy detail.

- **Policy_Identifier**: Unique identifier for the insurance policy to which this coverage detail belongs.

- **Coverage_Part_Code**: Code indicating a specific part or section of the coverage (e.g., "Part A", "Part B").

- **Coverage_Description**: Description of what the coverage includes or covers (if available).

- **Expiration_Date**: Date when the coverage becomes inactive or expires under this policy detail.

- **Coverage_Inclusion_Exclusion_Code**: Code indicating whether the coverage is inclusive or exclusive for specific items or conditions (e.g., "I" for inclusion, "E" for exclusion).



## Policy



- **Policy_Identifier**: Unique identifier for an insurance policy.

- **Effective_Date**: Date when the policy becomes active and begins to provide coverage.

- **Expiration_Date**: Date when the policy ends and no longer provides coverage (if applicable).

- **Policy_Number**: Internal or external number assigned by the company to identify the policy.

- **Status_Code**: Code indicating the current status of the policy (e.g., "Active", "Inactive", "Pending").

- **Geographic_Location_Identifier**: Identifier for the geographic location where the policy applies (if applicable).



## Policy_Amount



- **Policy_Amount_Identifier**: Unique identifier for a specific amount associated with a policy.

- **Geographic_Location_Identifier**: Identifier of the geographic area covered by this policy amount (if applicable).

- **Policy_Identifier**: Identifier of the insurance policy to which this amount belongs.

- **Effective_Date**: Date when the policy amount becomes active or effective under the policy.

- **Amount_Type_Code**: Code indicating the type of amount, such as premium, loss, expense, etc. (e.g., "Premium" or "Loss").

- **Earning_Begin_Date**: Start date for earning or accruing this amount (if applicable).

- **Earning_End_Date**: End date for earning or accruing this amount (if applicable).

- **Policy_Coverage_Detail_Identifier**: Identifier of the policy coverage detail that applies to this amount.

- **Policy_Amount**: The actual monetary value of the policy amount (e.g., $1000, $2500, etc.).

- **Insurable_Object_Identifier**: Identifier of the insured object or property covered by this policy amount.

- **Insurance_Type_Code**: Code indicating the type of insurance coverage that applies to this amount (e.g., property, liability, etc.).



## Agreement_Party_Role



- **Agreement_Identifier**: Unique identifier for an agreement between parties (e.g., a contract or policy agreement).

- **Party_Identifier**: Identifier of the party involved in the agreement.

- **Party_Role_Code**: Code indicating the role that the party plays in the agreement (e.g., "PH" for Policyholder, "AG" for Agent).

- **Effective_Date**: Date when the party's role becomes active or effective under the agreement.

- **Expiration_Date**: Date when the party's role ends or expires under the agreement.



## Premium



- **Policy_Amount_Identifier**: Identifier of the policy amount associated with a premium payment.