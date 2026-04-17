The User 
We need to create a complete solution design document. That starts with the summary of the business requirements and capabilities. 

We need to design the high level solution design that can be passed to the technical team to build their design documents.

Create a solution design document.

Include an application summary table. Perform an impact analaysis on the given requirements and capabilities. the analaysis should include impacted applications, impact type, and level of effort (LOE). 

We need a product team summary table with MOTS ID, Application, LOE.

Create and interface summary table and should include the source application, target application, impact type, interface type, and data exchange details between source and destination applications.

Hard stops
- Never make up MOTS IDs 
- Never make up application names
- Never 

Mandatory
- Use the templates in the _artifacts/templates folder

Preferred
- Refer to ITAP for application names and MOTS IDs and discriptions

## SI analysis
- Use past SI's
- look for close relations to or foundational to the business requirements provided
- look for named applicaiton names in the business requirements and related impacted applications
- look into the discussed dependecies of past SI's and if not in the provided past SI's, make it known to the user
- Based on the requirements and capabilities, deliver on the application for each requirement


1st Pass of IA - Scaffold: all applications for each capability
2nd Pass of IA - Refactor: for all applications, what is the impact on the application to deliver the capability
3rd Pass of SI - do one more pass on impacted applications and classify on high/medium/low confidence vs level of impact

Gaps:
- The SA's have most of the knowledge in their heads.


IA - Impact Analysis
round 1 - all applications for each capability
    - All SI's
    - ITAP
round 2 - for all applications, what is the impact on the application to deliver the capability
    - Wiki's
round 3 - all capabilities by microservices



--------- V1 Prompt
/solution-document 

We need to create a complete solution design document. That starts with the summary of the business requirements and capabilities. 

We need to design the high level solution design that can be passed to the technical team to build their design documents.

Create a solution design document.

Include an application summary table. Perform an impact analaysis on the given requirements and capabilities. the analaysis should include impacted applications, impact type, and level of effort (LOE).  use desciptions @SI_Table_Documentation.md to help fill in the required values

We need a product team summary table with MOTS ID, Application, LOE.

Create and interface summary table and should include the source application, target application, impact type, interface type, and data exchange details between source and destination applications. use desciptions @SI_Table_Documentation.md 

Undestand the requirements and capabilities.

1) Get business requirements, provided here @epic_.md 
2) Look at prior SI documents for reference, predecessor documents, or related epics. reference SI repository or ADO. @past_solution_intents 
3) then create a new solution intent document and follow the @2026 SI Template Example.docx 