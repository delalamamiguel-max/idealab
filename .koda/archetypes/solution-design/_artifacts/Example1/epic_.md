Epic 1441472 BST-WLS: MC1.7 - BR-1871703 -1560 - Stolen In Transit - UFD-5260
Azure Boards
Epic 1441472: BST-WLS: MC1.7 - BR-1871703 -1560 - Stolen In Transit - UFD-5260
Review | VEDULA, DEEPIKA KRISHNA

Improved customer experience by allowing the customer to upgrade to a new connected device and finance a new loan before the end of their current loan tenure.

## Capabilities 
1865397 - C-001 - Enroll/ De-Enroll in Next Up Anytime
1865401 - C-002 - UPG w/ Turn-In && w/o Pay-up
1865407 - C-003 - UPG w/ Turn-In && w/ Pay-up for NUA promo
1904916 - C-004 - Pay-off IP w/ NUA
1865408 - C-005 - Pay-off IP w/o NUA
1904922 - C-006 - Reverse Upgrade
1904925 - C-007 - Upgrade - Chargeback & Reversal of Chargeback/Reverse
1909509 - C-008 - Reverse Pay-Up/ Pay-Off by voiding the payments

## Change requests
Decision points from WLS lock-down - 10/20:
CR 683 - Move OUT - ACC scope into 1544
CR 664 - Move OUT - legacy NextUp from MC1.5 to 1753
CR 630 - Move OUT - Digital Scope into 1159

==========================================================================================================================================
 
Refer Scope Tracker for capability mapping - https://wiki.web.att.com/pages/viewpage.action?pageId=2435811925
Business Requirements for 924 scope:
==========================================================================================================================================
 
 
 ## Sub-business requirements From SRT	 	 	 	 	 	 	 	 	 	 
924-BS001-Business Specification 01 – Enforce Next Up Anytime Turn in Eligibility Requirements and Pay to Upgrade	N/A	 	 	 	 	 	 	 	 	 

			924-BS001-Description	This capability addresses the Next Up Anytime feature and what is required to meet and enforce the eligibility criteria.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-Customer POV	As a customer, I want the ability to upgrade my device when I meet the eligibility criteria and I’m paying for the Next Up Anytime feature, so that I can receive the newest device available.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-Product Mgr POV	As a BSSe Product Manager, I want to provide the ability for customers to upgrade their device when they’ve met the eligibility criteria and they’re paying for the Next Up Anytime feature, so that they can have the newest device when it becomes available.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC10	Given that customers will want to upgrade their device to the newest available when they’re paying for the Next Up Anytime feature, then ensure that for loans residing in ILS, loan payment information is returned to the Front-end systems such that eligibility
 for Upgrade to a new device can be determined.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC20a	Include the ability for the customer to pay off a configurable number of payments, or a certain outstanding balance to meet eligibility requirements for upgrade.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC20b	Include the ability for velocity checks to ensure the customer has not met max upgrades within a certain time period.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC20c	Include the ability to suppress upgrade eligibility for BYOD customers who have been with us less than a configurable length of time (6 months).	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC30	Given that a customer wants to know when they are eligible to upgrade their device when they are on the Next Up Anytime program, then ensure that what is needed to meet the upgrade requirements are displayed to the customer.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC60	Given that a customer may have a lock on their phone when they’re processing a Next Up Anytime upgrade, then require that any locks be removed prior to processing the upgrade.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC60a	If it is found the locks are turned on, then the order is stopped until the customer turns it off.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC70	Given that a customer meets all the eligibility criteria, when they request an upgrade, then execute the upgrade seamlessly and streamline eligibility verification.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC70a	Once the CTN line is determined eligible, make a call at the account level to determine if a down-payment is necessary.

Note: Today we use credit class value, which is static in TLG. 	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC80	Given that a customer may need to meet certain conditions to qualify for an upgrade, when they’re requesting an upgrade, then ensure that eligibility is assessed by special profile.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC80a	Include the ability to advise the customer that eligibility will require an assessment and approval in the channel the customer is requesting the upgrade.	 	 	 	 	 	 	 	 	 
 	 	 	1544_924-BS001-C1AC100	Given that Device Turn-In Terms and Conditions need to be accepted when a Next Up Anytime Turn-In Upgrade is requested, then ensure that the device turn in T&Cs are presented in the channel where the upgrade request is being made.	 	 	 	 	 	 	 	 	 
 	 	 	1544_924-BS001-C1AC110	Given that Device Turn-In Terms and Conditions need to be accepted when a Next Up Anytime Turn-In upgrade is requested, then ensure that the customer acknowledges and agrees to the Device Turn-In T&Cs by providing their signature and the date of acceptance. 	 	 	 	 	 	 	 	 	 
 	 	 	924-BS001-C1AC110a	Include the ability to record the acceptance with the version accepted to Loan systems and customer records.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-Business Specification 02 – Create RMA and Process Returned Equipment	N/A	 	 	 	 	 	 	 	 	 
924-BS002-Description	When the customer has met the eligibility criteria for a Next Up Anytime Upgrade, we need the ability to process the Turn In device.  	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-Customer POV	As a customer, I want the ability to turn in my old device when I’ve met the criteria to upgrade, so that I can receive the newest device available.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-Product Mgr POV	As a BSSe Product Manager, I want to allow a customer to turn in their old device when they have met the criteria for upgrade, so that AT&T can ensure the customer receives the newest device available.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10	Given that a customer needs to turn in their old device when they’re eligible for an upgrade, then for Turn-in returns outside of “in-person”, ensure that ILS receives both the request for upgrade and the RMA information to turn in the old device.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10a	Notify ILS with the RMA information created for the old device attached to the old loan.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10b	ILS will create a new loan for the new device to be shipped.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10c	Ensure that systems notify Supply Chain of the outstanding balance for the old loan.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10d	If the order is cancelled before the old device is receipted to warehouse, then continue billing the old loan as usual.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10d1	Include reversing the upgrade and cancelling the pending IP for the upgraded device.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10e	If the order is cancelled before the old device is receipted to warehouse, then ILS should be notified and cancel/remove/close the new loan for the new device that’s in pending status.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10e1	Immediately notify Supply Chain to cancel the shipment of the upgraded device and reverse the upgrade.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10e2	An order can only be cancelled up to Supply Chain PONR (drop to warehouse), otherwise the order will not be allowed to be cancelled.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10e3	Include a hard stop after drop to warehouse, where the shipment cannot be recalled or cancelled, and the order cannot be cancelled without initiating BRE transaction.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC10f	Include the ability to create new reason codes for Next Up Anytime upgrades to drive the handling rules.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC20	Given that the new device shipped could be returned undelivered, when the carrier is unsuccessful, then ensure that the Upgrade Turn-In transaction is cancelled with undelivered reason.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC20a	Loan systems will reinstate the original IP and create the necessary GL entries to re-establish balances booked on the upgraded IP.	 	 	 	 	 	 	 	 	 
 	 	 	C4AC20b	Create and close RTO (Return only) order for the undelivered new device received.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC30	Given that the old loan is still active during the Turn In process when processing the Turn in return, then ensure for the installment plan loan for the device being “turned-in”, ILS sends a billing credit for any installment plan and Next Up Anytime charge(s)
 and a promotional debit (if applicable) sent to the biller by ILS that has not yet been billed (i.e. in Pending charge status) or has been billed and not paid.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC35a	Include the ability to reject the Turn in as not eligible when the device does not meet the conditions set forth.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC40	Given that the customer is held accountable for the Turn in when they choose to mail it in, then ensure communication takes place between ILS and Supply Chain for the outstanding balance.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC40a	Validate that the correct amount is sent from ILS to upstream systems to create the RMA.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC40b	Stop billing the customer for the old device when the Next Up Anytime Upgrade order is submitted.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC40c	Trigger the reason for return with the outstanding balance as the NRF if device is not received within a configurable time period.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC40d	Validate that the correct amount is sent from ILS to upstream systems to create the RMA.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC45	Given that most customers will choose to return their device when they’re eligible for an upgrade and mailing their device into AT&T, then ensure the systems can process the return and update the loan as received.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC45a	When the device is received, Supply Chain will process the return of the device and receive into inventory.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC45aa	Oracle Inventory performs the following financial transaction upon device receipt:

DR     Inventory

CR  Installment Plan (Old equipment on the Next plan) Revenue	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC45ab	When the device is received, Supply Chain will evaluate the condition of the device and calculate the difference between the outstanding balance and any damage dues.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC45aba	The value of the device for the customer will be reassessed based on the conditional assessment and applied to the customer balance.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC45abb	Include the ability to charge the Customer based on the conditional assessment at receipt to RL. 	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC45abc	Create a charge code for Next Up Anytime damaged device return	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC45b	Ensure when notified of turn in of the old device for an upgrade, ILS closes the loan and reverses the remaining note & imputed interest balances due to turn-in. ILS entry to write off the remaining balances as follows:

  DR Installment Plan Revenue

CR Market.1200.xx  Device IP Notes receivable (short and long term, if applicable)	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC60	Given that customers need to be held accountable when they do not return their Turn In device for upgrade, then ensure that for non-returned devices ILS is notified that the turn-in device was never returned within the initial expected time window for upgrade
 turn-in returns related to device financing (currently 60 days).	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC60a	Ensure upon notification of the non-receipt of the turn-in device (when notified by Oracle SCM after 60-day RMA auto close), ILS writes off (reverses) the remaining note and imputed interest balances. 

ILS entry to write off the remaining balances as follows:

DR Installment Plan Revenue

CR Market.1200.xx  Device IP Notes receivable

(short and long term, if applicable)	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC60b	Ensure for non-returned devices, upon SCM RMA auto-close and sends RMA Claim Amount to the biller to charge the customer as follows:

Debit:  Customer AR

Credit:  Installment Plan Revenue	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC60c	Create a charge code for non-return devices when the RMA claim is autoclosed for the amount sent to the biller to charge the customer.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC80	Given that customers can return their Turn in device after the turn in period but within the grace period, then ensure the system has the ability to automatically credit the NRC charge that was sent to the biller.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC80a	Include the ability for the customer care team to credit the full charge that was sent to the biller when the automatic refund fails.  	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC90	Given that the business wants to track the number of eligible Turn ins when returns are expected, then ensure an RMA Aging reporting is available for loans with an open RMA that includes loan balances, status and loan acceleration charges (if applicable).	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC100	Given that a customer should not be able to process more than one Turn in upgrade at a time when they’re eligible, then ensure that the solution prevents a customer from starting a new turn-in upgrade if their previous turn-in upgrade has not completed
 yet.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC110	Given that a customer will choose to Turn In their old device when they’re eligible for an upgrade, then ensure that system notify ILS of the successful return and ILS closes the loan.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS004-C4AC20b	ILS will mark the loan as “Finished due to Turn in / Upgrade” or equivalent.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC120	Given that charges may have already been sent to the biller when a customer initiates an eligible Turn In request, then ensure that ILS sends credits to the billers for any pending (not billed or paid) charges when the old device is received.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC120a	Include the ability to consider both pending and billed charges with the amount required to meet upgrade eligibility in the display.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC120b	If the customer initiates a transaction to pay to upgrade, notify ILS and then provide an immediate receipt for the payment.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC120c	If it is found that the customer has overpaid, then provide a credit on the next bill.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS002-C2AC150	Given that Turn In devices need to be properly accounted for when they’re returned, then ensure that ILS performs the necessary accounting functions related to the old loan as a result of a successful turn-in, including remaining balance reversals due to
 turn-in.  	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-Business Specification 03 – Process Device Upgrade	N/A	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-Description	Once the turn in has been processed, we need to process the device upgrade and start the new loan for the customer.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-Customer POV	As a Customer, I want to receive my upgraded device when I’ve processed a turn in, so that I can close out my upgrade transaction and use my new device.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-Product Mgr POV	As a BSSe Product Manager, I want the ability to establish a new loan with an upgraded connected device when customers have processed their Turn in, so that they can receive their new upgraded device and start using the service.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-C3AC10	Given that a customer may want to keep using their old device for a time when they’re upgrading to a new device, then setup the upgrade and mark the new loan as pending; so that the customer can still use the service until they’re ready to activate their
 new device.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-C3AC10a	Include the ability to ship the new device cold, activate the new loan, and start billing when the new device ships.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-C3AC10b	Include the ability for the customer to take the old device home and return the old device at a later date.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-C3AC10c	The RMA (RTO) will be created automatically, when the customer intends to take the old device home.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-C3AC20	Given that a customer wants to use their new device after they’ve sent in their old device return, then ensure that the carrier is able to notify supply chain systems when the old device is received at the carrier.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS003-C3AC100	Upon successful upgrade processing, ensure the process allows establishment of a new SmartPhone loan for the upgraded SmartPhone line of service 	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-Business Specification 07 – Reconciliation and Pay to Upgrade	N/A	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-Description	This capability addresses the need to reconcile installment pay to upgrade clearing accounts monthly.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-Product Mgr POV	As a BSSe Product Manager, I want the ability to collect, validate, and integrate CIPID transaction details from ILS and CAPM / CFM when customers pay to upgrade while on Next Up Anytime, so that I can reconcile Installment pay to upgrade clearing accounts.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-C7AC10	Given that the business must ensure the accuracy and consistency of their financial records when handling device financing, then ensure CIPID transaction sales details are collected from ILS and CAPM/CFM.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-C7AC20	Given that the business must ensure the accuracy and consistency of their financial records when handling device financing, ensure Collected data is sent to the AT&T reconciliation tool for processing and analysis.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-C7AC30	Given that we need to ensure the accuracy and completeness of transactions across systems when reconciling financial clearing account transactions, then ensure all required data fields (CIPID, TRANSACTION DATE, SKU, CTN, Clearing Acct Number, and Amount)
 are present and correctly formatted.  	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-C7AC40	Given that the business needs all the transactions from across the various systems when reconciling financial clearing accounts, then ensure data from all production Channels on BSSe are integrated into the reconciliation process.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-C7AC50	Given that we need to ensure the accuracy and completeness of transactions across systems when reconciling financial clearing account transactions, then ensure data from ILS and CAPM/CFM is correctly mapped to the AT&T reconciliation tool.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-C7AC60	Given that the business needs to reconcile financial clearing account transactions when reviewing all financial and transaction data, then ensure monthly reconciliation reports are generated for each system.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS007-C7AC70	Given that the business needs to understand the data when reconciling financial clearing account transactions, then ensure reports include all necessary data elements for reconciliation and are easily accessible and understandable for financial analysts
 and stakeholders.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS008-Business Specification 08 – Eliminate Multiple Installment Charges Following an Early Turn-In Upgrade Without Pay to Upgrade	N/A	 	 	 	 	 	 	 	 	 
 	 	 	924-BS008-Description	This capability addresses the need to eliminate / reverse the last pending installment charge for the previous installment plan following a turn in upgrade.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS008-Product Mgr POV	As a BSSe Product Manager, I want the ability to eliminate/ reverse the last pending installment charge from the previous installment plan following a Turn In Upgrade, so that customers do not get double charged for two installment charges on the same line
 on the subsequent bill.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS008-C8AC10	Given that a Next Up Anytime Upgrade necessitates the creation of a new Installment Plan for the new device when the old device is being turned in on the old installment plan, then ensure for early turn-in upgrade scenarios, the system will not bill the
 pending old IP charges when we have two IP billing charges for both the old and new devices until the old device is received in warehouse, so that only one monthly charge (i.e. the New Device IP charges) is reflected on the customer's bill for a given month. 	 	 	 	 	 	 	 	 	 
 	 	 	924-BS008-C8AC20	Given that the old device needs to be returned and scanned as received before the old pending charges can be reversed, then ensure for early turn-in upgrade scenarios, the system will reverse the pending old Next up anytime charges associated with the monthly
 installment charges being reversed on the old Installment Plan.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS008-C8AC40	Given that a customer can choose to pay up for Next Up Anytime Turn in upgrade as well as upgrade within the same month, then ensure the system does not reverse any pay up charges	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-Business Specification 09 – Communication	Business Specification 09 –  Communication	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-Description	N/A	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-Customer POV	As a customer, I want the ability to track my return or exchange, so that I know the status and can take any required actions necessary. 	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-Product Mgr POV	As a BSSe Product Manager, I want BSSe systems to send any required FCC Privacy / CPNI and transactional notifications to customers, so that AT&T complies with all laws and keeps our customers informed.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-C9AC10	[COMM] Given that the customer has submitted an order when intending to process a Next Up Anytime Turn in / Upgrade, then ensure that an order confirmation is sent that includes the confirmation for the Next Up Anytime transaction.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-C9AC30	[COMM] Given that customers may choose to mail in their old device when upgrading to a new device, then ensure that the customer receives reminder notifications to return their device within the 30 day return period.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-C9AC30a	[COMM] Communications reminders will trigger on day 3, 7, and 14 after the upgrade order is submitted.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-C9AC40	[COMM] Given that customers may choose to not return their old device within the 30 day return period when processing their Turn in / Upgrade, then ensure that non return communication is triggered on day 31, including, but not limited to:

• Information about the old device that needs to be returned

o Example: Make, Model, IMEI, SN

• The application of the non-return fee (NRF) to their account with the date and the amount that will be charged.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-C9AC40a	[COMM] The communications listed above will have the following information as appropriate: Customers name, account number/ BAN, date of old order, ship date of the upgrade device, picture and / or description of old device being returned, last 4 of CTN
 loan will be financed against, expected ship date (if order partially shipped, link to OM Hub to check order status, static link on how to back up and transfer info, myAT&T app module, and semi-authenticated link to track shipment.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-C9AC50	[COMM] All communications will be sent via the customers preferred communication method.  If no preferred method is noted, the communication will be sent via email.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-C9AC60	[COMM] If email bounces / fails, communication will be sent via SMS.	 	 	 	 	 	 	 	 	 
 	 	 	924-BS009-C9AC70	[COMMS]: Reporting on all comms, including but not limited to:
