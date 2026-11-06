## Claim Table



- **Claim_Identifier**: Unique identifier for each claim. This is the primary key of the table.

- **Catastrophe_Identifier**: Identifies the catastrophe that caused the claim.

- **Claim_Description**: A detailed description of the claim. This could include information about the event that led to the claim, the nature of the loss, and other relevant details.

- **Claims_Made_Date**: The date when the claim was made. This is important for tracking when a claim was submitted.

- **Company_Claim_Number**: A number assigned by the company to identify this specific claim within their system. This helps in tracking claims across different companies or departments.

- **Company_Subclaim_Number**: A subclaim number that identifies a specific part of a larger claim. This is useful for breaking down complex claims into smaller, manageable parts.

- **Insurable_Object_Identifier**: Identifies the insurable object (such as property, person, or event) that was affected by the catastrophe. This helps in determining which assets are covered under this claim.

- **Occurrence_Identifier**: A unique identifier for the occurrence (event) that led to the claim.

- **Entry_Into_Claims_Made_Program_Date**: The date when the claim was officially recorded in the claims made program. This helps track when a claim was processed and added to the system.

- **Claim_Open_Date**: The date when the claim became open for processing or review. This is important for determining when a claim can be reviewed by insurance providers.

- **Claim_Close_Date**: The date when the claim was closed, meaning it's no longer being processed or reviewed.

- **Claim_Reopen_Date**: The date when the claim was reopened after being closed. This might happen if new information becomes available or if there are changes to the claim that require reevaluation.

- **Claim_Status_Code**: A code indicating the current status of the claim.

- **Claim_Reported_Date**: The date when the claim was reported to the insurance company or relevant authority. This is used for documentation and record-keeping purposes.



## Claim_Amount Table



- **Claim_Amount_Identifier**: Unique identifier for each amount associated with a claim. This is the primary key of the table.

- **Claim_Identifier**: The claim that this amount is related to.

- **Claim_Offer_Identifier**: Identifies the offer that was made for this claim. This could be a payment offer from an insurance provider, which might be rejected or accepted.

- **Amount_Type_Code**: A code indicating the type of amount stored in the table. Possible values include "None," "Payment," "Reserve," etc., depending on the system's configuration.

- **Event_Date**: The date when the event that caused this amount was recorded. This is important for tracking when an amount was created or updated.

- **Claim_Amount**: The actual monetary value of the claim amount. This could be a payment, reserve, or other financial figure associated with the claim.

- **Insurance_Type_Code**: A code indicating the type of insurance that applies to this amount.



## Loss_Payment Table



- **Claim_Amount_Identifier**: Unique identifier for each payment related to a claim. This is the primary key of the table.

- **Loss_Payment** contains information about payments made to cover losses related to a claim. This is used for tracking when and how much was paid out in relation to specific claims.



## Loss_Reserve Table



- **Claim_Amount_Identifier**: Unique identifier for each reserve related to a claim. This is the primary key of the table.

- **Loss_Reserve** contains information about reserves set aside to cover potential future losses related to a claim. This is used for tracking when and how much was reserved in relation to specific claims.



## Expense_Payment Table



- **Claim_Amount_Identifier**: Unique identifier for each payment related to a claim. This is the primary key of the table.

- **Expense_Payment** contains information about payments made for expenses related to a claim. This is used for tracking when and how much was paid out in relation to specific claims.



## Expense_Reserve Table



- **Claim_Amount_Identifier**: Unique identifier for each reserve related to a claim. This is the primary key of the table.

- **Expense_Reserve** contains information about reserves set aside for expenses related to a claim. This is used for tracking when and how much was reserved in relation to specific claims.


## Claim_Coverage Table



- **Claim_Identifier**: Unique identifier for each claim.

- **Effective_Date**: The date when the coverage becomes effective for this claim. This helps determine when the coverage starts applying to the claim.

- **Policy_Coverage_Detail_Identifier**: A unique identifier for the policy coverage detail that applies to this claim.

- **Claim_Identifier**, **Effective_Date**, and **Policy_Coverage_Detail_Identifier** are combined into a composite primary key to ensure that each combination of these three fields is unique. This ensures that each claim has its own set of coverage details at a specific date.



## Policy_Coverage_Detail Table



- **Effective_Date**: The date when the coverage becomes effective for this detail. This helps determine when the coverage starts applying to the policy.

- **Policy_Coverage_Detail_Identifier**: A unique identifier for this coverage detail.

- **Coverage_Identifier**: Identifies the type of coverage (e.g., property, liability, etc.) that applies to this detail. This helps determine what kind of coverage is included in the policy.

- **Insurable_Object_Identifier**: Identifies the insurable object (such as property, person, or event) that is covered by this detail. This helps determine which assets are protected under this coverage.

- **Policy_Identifier**: The identifier for the policy that includes this coverage detail.

- **Coverage_Part_Code**: A code that identifies the specific part of the coverage (e.g., "None," "Property," "Liability"). This helps categorize different types of coverage within a policy.

- **Coverage_Description**: A description of the coverage details. This provides context about what kind of coverage is included in this detail.

- **Expiration_Date**: The date when the coverage becomes invalid for this detail. This helps determine when the coverage no longer applies to the insurable object.

- **Coverage_Inclusion_Exclusion_Code**: A code that indicates whether the coverage is included or excluded from the policy. This helps determine if certain types of claims are covered under specific conditions.



## Policy Table



- **Policy_Identifier**: Unique identifier for each insurance policy. This is the primary key of the table.

- **Effective_Date**: The date when the policy becomes effective. This helps determine when the coverage starts applying to the insured party.

- **Expiration_Date**: The date when the policy expires. This helps determine when the coverage stops being valid.

- **Policy_Number**: A unique number assigned to each insurance policy. This is used for identification and record-keeping purposes.

- **Status_Code**: A code indicating the current status of the policy (e.g., active, expired, canceled). This helps track whether the policy is still in effect or has been terminated.

- **Geographic_Location_Identifier**: Identifies the geographic location where the policy applies. This helps determine which regions are covered by this policy.



## Policy_Amount Table



- **Policy_Amount_Identifier**: Unique identifier for each amount associated with a policy. This is the primary key of the table.

- **Geographic_Location_Identifier**: Identifies the geographic location where this amount applies. This helps determine which regions are covered by this policy.

- **Policy_Identifier**: The identifier for the insurance policy that includes this amount.

- **Effective_Date**: The date when the coverage becomes effective. This helps determine when the amount starts applying to the insured party.

- **Amount_Type_Code**: A code indicating the type of amount stored in the table.

- **Earning_Begin_Date**: The date when earnings for this amount start. This is important for tracking when payments or reserves are calculated based on earnings.

- **Earning_End_Date**: The date when earnings for this amount end. This helps determine when the amount is valid for calculation purposes.

- **Policy_Coverage_Detail_Identifier**: A unique identifier for the coverage detail that applies to this amount.

- **Policy_Amount**: The actual monetary value of the policy amount. This could be a payment, reserve, or other financial figure associated with the policy.

- **Insurable_Object_Identifier**: Identifies the insurable object (such as property, person, or event) that is covered by this amount. This helps determine which assets are protected under this coverage.

- **Insurance_Type_Code**: A code indicating the type of insurance that applies to this amount.



## Agreement_Party_Role Table



- **Agreement_Identifier**: Identifier for each agreement party role.

- **Party_Identifier**: The identifier for the party (e.g., insurance company, insured entity) that holds this role in the agreement.

- **Party_Role_Code**: A code indicating the type of role held by the party (e.g., "AG" for agent, "PH" for policyholder). This helps determine who is responsible for what in the agreement.

- **Effective_Date**: The date when the role becomes effective. This helps determine when the role starts applying to the party.

- **Expiration_Date**: The date when the role expires. This helps determine when the role stops being valid for the party.



## Premium Table



- **Policy_Amount_Identifier**: Unique identifier for each premium associated with a policy. This is the primary key of the table.

- **Premium** contains information about the premiums paid for a policy. This is used for tracking when and how much was paid in relation to specific policies.
