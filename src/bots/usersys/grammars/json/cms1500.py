# -*- coding: utf-8 -*-

from bots.botsconfig import *

syntax = {
    "indented": True,
    "indentation": 2,
}

structure = [
    {
        ID: "CMS1500",
        MIN: 1,
        MAX: 1,
        LEVEL: [
            # Billing Provider Information
            {ID: "Billing_Provider_Name", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_NPI", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_Address_Line1", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_Address_Line2", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_City", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_State", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_Zip", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_Phone", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_Taxonomy", MIN: 0, MAX: 1},
            {ID: "Billing_Provider_Taxonomy_Qualifier", MIN: 0, MAX: 1},
            # Pay-to Provider Information (Box 33) if different from Billing Provider
            {ID: "Pay_To_Provider_Name", MIN: 0, MAX: 1},
            {ID: "Pay_To_Provider_NPI", MIN: 0, MAX: 1},
            {ID: "Pay_To_Provider_Address_Line1", MIN: 0, MAX: 1},
            {ID: "Pay_To_Provider_Address_Line2", MIN: 0, MAX: 1},
            {ID: "Pay_To_Provider_City", MIN: 0, MAX: 1},
            {ID: "Pay_To_Provider_State", MIN: 0, MAX: 1},
            {ID: "Pay_To_Provider_Zip", MIN: 0, MAX: 1},
            # Service Facility Location Information (Box 32)
            {ID: "Service_Facility_Name", MIN: 0, MAX: 1},
            {ID: "Service_Facility_NPI", MIN: 0, MAX: 1},
            {ID: "Service_Facility_Address_Line1", MIN: 0, MAX: 1},
            {ID: "Service_Facility_Address_Line2", MIN: 0, MAX: 1},
            {ID: "Service_Facility_City", MIN: 0, MAX: 1},
            {ID: "Service_Facility_State", MIN: 0, MAX: 1},
            {ID: "Service_Facility_Zip", MIN: 0, MAX: 1},
            # Referring Provider Information (Box 17)
            {ID: "Referring_Provider_Name", MIN: 0, MAX: 1},
            {ID: "Referring_Provider_NPI", MIN: 0, MAX: 1},
            {
                ID: "Referring_Provider_Qualifier",
                MIN: 0,
                MAX: 1,
            },  # DN=Referring Provider, DK=Ordering Provider, DQ=Supervising Provider
            # Patient Information (Box 2)
            {ID: "Patient_Last_Name", MIN: 0, MAX: 1},
            {ID: "Patient_First_Name", MIN: 0, MAX: 1},
            {ID: "Patient_Middle_Initial", MIN: 0, MAX: 1},
            {ID: "Patient_DOB", MIN: 0, MAX: 1},
            {ID: "Patient_Gender", MIN: 0, MAX: 1},
            {ID: "Patient_Address_Line1", MIN: 0, MAX: 1},
            {ID: "Patient_Address_Line2", MIN: 0, MAX: 1},
            {ID: "Patient_City", MIN: 0, MAX: 1},
            {ID: "Patient_State", MIN: 0, MAX: 1},
            {ID: "Patient_Zip", MIN: 0, MAX: 1},
            {ID: "Patient_Phone", MIN: 0, MAX: 1},
            {
                ID: "Patient_Relationship",
                MIN: 0,
                MAX: 1,
            },  # Maps to PAT01 (SELF, SPOUSE, CHILD, OTHER)
            {ID: "Patient_Account_Number", MIN: 0, MAX: 1},  # Box 26, maps to CLM01
            {ID: "Patient_Signature_On_File", MIN: 0, MAX: 1},  # Box 12 - Yes/No
            {ID: "Patient_Signature_Date", MIN: 0, MAX: 1},  # Box 12
            # Insurance Information
            {
                ID: "Insurance_Type",
                MIN: 0,
                MAX: 1,
            },  # Maps to SBR01 (P=Primary, S=Secondary, T=Tertiary)
            {ID: "Insurance_Name", MIN: 0, MAX: 1},  # Box 4
            {ID: "Insurance_ID", MIN: 0, MAX: 1},  # Payer ID
            {ID: "Insured_ID", MIN: 0, MAX: 1},  # Box 1a - Member ID
            {ID: "Insured_Group", MIN: 0, MAX: 1},  # Box 11 - Insurance Group Number
            {ID: "Insured_Group_Name", MIN: 0, MAX: 1},  # Name of the group
            # Insured Information (if different from patient)
            {ID: "Insured_Last_Name", MIN: 0, MAX: 1},  # Box 4
            {ID: "Insured_First_Name", MIN: 0, MAX: 1},  # Box 4
            {ID: "Insured_Middle_Initial", MIN: 0, MAX: 1},  # Box 4
            {ID: "Insured_Address_Line1", MIN: 0, MAX: 1},  # Box 7
            {ID: "Insured_Address_Line2", MIN: 0, MAX: 1},
            {ID: "Insured_City", MIN: 0, MAX: 1},  # Box 7
            {ID: "Insured_State", MIN: 0, MAX: 1},  # Box 7
            {ID: "Insured_Zip", MIN: 0, MAX: 1},  # Box 7
            {ID: "Insured_Phone", MIN: 0, MAX: 1},  # Box 7
            {ID: "Insured_DOB", MIN: 0, MAX: 1},  # Box 11a
            {ID: "Insured_Gender", MIN: 0, MAX: 1},  # Box 11a
            {ID: "Insured_Employer_Name", MIN: 0, MAX: 1},  # Box 11b
            {ID: "Insured_Employer_Address", MIN: 0, MAX: 1},
            # Claim Information
            {ID: "Claim_Number", MIN: 0, MAX: 1},  # Box 26 - Patient Account Number
            {ID: "Accept_Assignment", MIN: 0, MAX: 1},  # Box 27 - Accept Assignment Y/N
            {ID: "Total_Charge", MIN: 0, MAX: 1},  # Box 28 - Total Charges
            {ID: "Amount_Paid", MIN: 0, MAX: 1},  # Box 29 - Amount Paid
            {ID: "Balance_Due", MIN: 0, MAX: 1},  # Box 30 - Balance Due
            {ID: "Provider_Signature", MIN: 0, MAX: 1},  # Box 31 - Y/N
            {ID: "Provider_Signature_Date", MIN: 0, MAX: 1},  # Box 31
            # Additional Claim Information
            {ID: "Place_Of_Service", MIN: 0, MAX: 1},  # Box 24B - Place of Service Code
            {ID: "Claim_Type", MIN: 0, MAX: 1},
            {ID: "EMG", MIN: 0, MAX: 1},  # Box 24C - EMG (Emergency) indicator
            {ID: "EPSDT", MIN: 0, MAX: 1},  # Box 24H - EPSDT indicator
            {ID: "Family_Planning", MIN: 0, MAX: 1},  # Box 24H - Family Planning indicator
            # Date Information
            {ID: "Service_Date_From", MIN: 0, MAX: 1},  # Box 24A - From Date
            {ID: "Service_Date_To", MIN: 0, MAX: 1},  # Box 24A - To Date
            {ID: "Admission_Date", MIN: 0, MAX: 1},  # Box 18 - Hospitalization Dates From
            {ID: "Discharge_Date", MIN: 0, MAX: 1},  # Box 18 - Hospitalization Dates To
            {ID: "Current_Illness_Date", MIN: 0, MAX: 1},  # Box 14 - Date of Current Illness
            {ID: "Similar_Illness_Date", MIN: 0, MAX: 1},  # Box 15 - Date of Similar Illness
            {
                ID: "Unable_To_Work_From_Date",
                MIN: 0,
                MAX: 1,
            },  # Box 16 - Dates Patient Unable to Work - From
            {
                ID: "Unable_To_Work_To_Date",
                MIN: 0,
                MAX: 1,
            },  # Box 16 - Dates Patient Unable to Work - To
            # Diagnosis Information (Box 21)
            {ID: "Diagnosis_Code_1", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_2", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_3", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_4", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_5", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_6", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_7", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_8", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_9", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_10", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_11", MIN: 0, MAX: 1},
            {ID: "Diagnosis_Code_12", MIN: 0, MAX: 1},
            # Additional Claim Information
            {ID: "Prior_Authorization_Number", MIN: 0, MAX: 1},  # Box 23
            {ID: "Referring_Provider_Number", MIN: 0, MAX: 1},  # Box 17a
            {ID: "Medicaid_Resubmission_Code", MIN: 0, MAX: 1},  # Box 22
            {ID: "Medicaid_Original_Reference", MIN: 0, MAX: 1},  # Box 22
            {ID: "Mammography_Certification_Number", MIN: 0, MAX: 1},  # Box 23
            {ID: "Investigational_Device_Exemption", MIN: 0, MAX: 1},  # Box 23
            {ID: "CLIA_Number", MIN: 0, MAX: 1},  # Box 23
            # Procedure Information (up to 6 lines) - Box 24
            {ID: "Procedure_Code_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Description_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_1_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_1_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_1_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_1_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Amount_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Units_1", MIN: 0, MAX: 1},
            {
                ID: "Procedure_Pointer_1",
                MIN: 0,
                MAX: 1,
            },  # Reference to the diagnosis code (e.g., "1,2,3")
            {ID: "Procedure_EMG_1", MIN: 0, MAX: 1},
            {ID: "Procedure_EPSDT_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Family_Planning_1", MIN: 0, MAX: 1},
            {ID: "Procedure_COB_1", MIN: 0, MAX: 1},
            {ID: "Rendering_Provider_NPI_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Code_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Description_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_2_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_2_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_2_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_2_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Amount_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Units_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Pointer_2", MIN: 0, MAX: 1},
            {ID: "Procedure_EMG_2", MIN: 0, MAX: 1},
            {ID: "Procedure_EPSDT_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Family_Planning_2", MIN: 0, MAX: 1},
            {ID: "Procedure_COB_2", MIN: 0, MAX: 1},
            {ID: "Rendering_Provider_NPI_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Code_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Description_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_3_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_3_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_3_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_3_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Amount_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Units_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Pointer_3", MIN: 0, MAX: 1},
            {ID: "Procedure_EMG_3", MIN: 0, MAX: 1},
            {ID: "Procedure_EPSDT_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Family_Planning_3", MIN: 0, MAX: 1},
            {ID: "Procedure_COB_3", MIN: 0, MAX: 1},
            {ID: "Rendering_Provider_NPI_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Code_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Description_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_4_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_4_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_4_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_4_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Amount_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Units_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Pointer_4", MIN: 0, MAX: 1},
            {ID: "Procedure_EMG_4", MIN: 0, MAX: 1},
            {ID: "Procedure_EPSDT_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Family_Planning_4", MIN: 0, MAX: 1},
            {ID: "Procedure_COB_4", MIN: 0, MAX: 1},
            {ID: "Rendering_Provider_NPI_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Code_5", MIN: 0, MAX: 1},
            {ID: "Procedure_Description_5", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_5_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_5_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_5_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_5_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Amount_5", MIN: 0, MAX: 1},
            {ID: "Procedure_Units_5", MIN: 0, MAX: 1},
            {ID: "Procedure_Pointer_5", MIN: 0, MAX: 1},
            {ID: "Procedure_EMG_5", MIN: 0, MAX: 1},
            {ID: "Procedure_EPSDT_5", MIN: 0, MAX: 1},
            {ID: "Procedure_Family_Planning_5", MIN: 0, MAX: 1},
            {ID: "Procedure_COB_5", MIN: 0, MAX: 1},
            {ID: "Rendering_Provider_NPI_5", MIN: 0, MAX: 1},
            {ID: "Procedure_Code_6", MIN: 0, MAX: 1},
            {ID: "Procedure_Description_6", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_6_1", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_6_2", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_6_3", MIN: 0, MAX: 1},
            {ID: "Procedure_Modifier_6_4", MIN: 0, MAX: 1},
            {ID: "Procedure_Amount_6", MIN: 0, MAX: 1},
            {ID: "Procedure_Units_6", MIN: 0, MAX: 1},
            {ID: "Procedure_Pointer_6", MIN: 0, MAX: 1},
            {ID: "Procedure_EMG_6", MIN: 0, MAX: 1},
            {ID: "Procedure_EPSDT_6", MIN: 0, MAX: 1},
            {ID: "Procedure_Family_Planning_6", MIN: 0, MAX: 1},
            {ID: "Procedure_COB_6", MIN: 0, MAX: 1},
            {ID: "Rendering_Provider_NPI_6", MIN: 0, MAX: 1},
        ],
    }
]

recorddefs = {
    "CMS1500": [
        ["BOTSID", "M", 7, "AN"],
        # Billing Provider Information
        ["Billing_Provider_Name", "C", 60, "AN"],
        ["Billing_Provider_NPI", "C", 10, "AN"],
        ["Billing_Provider_Address_Line1", "C", 55, "AN"],
        ["Billing_Provider_Address_Line2", "C", 55, "AN"],
        ["Billing_Provider_City", "C", 30, "AN"],
        ["Billing_Provider_State", "C", 2, "AN"],
        ["Billing_Provider_Zip", "C", 12, "AN"],
        ["Billing_Provider_Phone", "C", 12, "AN"],
        ["Billing_Provider_Taxonomy", "C", 10, "AN"],
        ["Billing_Provider_Taxonomy_Qualifier", "C", 2, "AN"],
        # Pay-to Provider Information
        ["Pay_To_Provider_Name", "C", 60, "AN"],
        ["Pay_To_Provider_NPI", "C", 10, "AN"],
        ["Pay_To_Provider_Address_Line1", "C", 55, "AN"],
        ["Pay_To_Provider_Address_Line2", "C", 55, "AN"],
        ["Pay_To_Provider_City", "C", 30, "AN"],
        ["Pay_To_Provider_State", "C", 2, "AN"],
        ["Pay_To_Provider_Zip", "C", 12, "AN"],
        # Service Facility Location Information
        ["Service_Facility_Name", "C", 60, "AN"],
        ["Service_Facility_NPI", "C", 10, "AN"],
        ["Service_Facility_Address_Line1", "C", 55, "AN"],
        ["Service_Facility_Address_Line2", "C", 55, "AN"],
        ["Service_Facility_City", "C", 30, "AN"],
        ["Service_Facility_State", "C", 2, "AN"],
        ["Service_Facility_Zip", "C", 12, "AN"],
        # Referring Provider Information
        ["Referring_Provider_Name", "C", 60, "AN"],
        ["Referring_Provider_NPI", "C", 10, "AN"],
        ["Referring_Provider_Qualifier", "C", 2, "AN"],
        # Patient Information
        ["Patient_Last_Name", "C", 60, "AN"],
        ["Patient_First_Name", "C", 35, "AN"],
        ["Patient_Middle_Initial", "C", 1, "AN"],
        ["Patient_DOB", "C", 10, "AN"],
        ["Patient_Gender", "C", 1, "AN"],
        ["Patient_Address_Line1", "C", 55, "AN"],
        ["Patient_Address_Line2", "C", 55, "AN"],
        ["Patient_City", "C", 30, "AN"],
        ["Patient_State", "C", 2, "AN"],
        ["Patient_Zip", "C", 12, "AN"],
        ["Patient_Phone", "C", 12, "AN"],
        ["Patient_Relationship", "C", 10, "AN"],
        ["Patient_Account_Number", "C", 30, "AN"],
        ["Patient_Signature_On_File", "C", 1, "AN"],
        ["Patient_Signature_Date", "C", 10, "AN"],
        # Insurance Information
        ["Insurance_Type", "C", 1, "AN"],
        ["Insurance_Name", "C", 60, "AN"],
        ["Insurance_ID", "C", 30, "AN"],
        ["Insured_ID", "C", 30, "AN"],
        ["Insured_Group", "C", 30, "AN"],
        ["Insured_Group_Name", "C", 60, "AN"],
        # Insured Information (if different from patient)
        ["Insured_Last_Name", "C", 60, "AN"],
        ["Insured_First_Name", "C", 35, "AN"],
        ["Insured_Middle_Initial", "C", 1, "AN"],
        ["Insured_Address_Line1", "C", 55, "AN"],
        ["Insured_Address_Line2", "C", 55, "AN"],
        ["Insured_City", "C", 30, "AN"],
        ["Insured_State", "C", 2, "AN"],
        ["Insured_Zip", "C", 12, "AN"],
        ["Insured_Phone", "C", 12, "AN"],
        ["Insured_DOB", "C", 10, "AN"],
        ["Insured_Gender", "C", 1, "AN"],
        ["Insured_Employer_Name", "C", 60, "AN"],
        ["Insured_Employer_Address", "C", 60, "AN"],
        # Claim Information
        ["Claim_Number", "C", 30, "AN"],
        ["Accept_Assignment", "C", 1, "AN"],
        ["Total_Charge", "C", 10, "AN"],
        ["Amount_Paid", "C", 10, "AN"],
        ["Balance_Due", "C", 10, "AN"],
        ["Provider_Signature", "C", 1, "AN"],
        ["Provider_Signature_Date", "C", 10, "AN"],
        # Additional Claim Information
        ["Place_Of_Service", "C", 2, "AN"],
        ["Claim_Type", "C", 1, "AN"],
        ["EMG", "C", 1, "AN"],
        ["EPSDT", "C", 1, "AN"],
        ["Family_Planning", "C", 1, "AN"],
        # Date Information
        ["Service_Date_From", "C", 10, "AN"],
        ["Service_Date_To", "C", 10, "AN"],
        ["Admission_Date", "C", 10, "AN"],
        ["Discharge_Date", "C", 10, "AN"],
        ["Current_Illness_Date", "C", 10, "AN"],
        ["Similar_Illness_Date", "C", 10, "AN"],
        ["Unable_To_Work_From_Date", "C", 10, "AN"],
        ["Unable_To_Work_To_Date", "C", 10, "AN"],
        # Diagnosis Information
        ["Diagnosis_Code_1", "C", 10, "AN"],
        ["Diagnosis_Code_2", "C", 10, "AN"],
        ["Diagnosis_Code_3", "C", 10, "AN"],
        ["Diagnosis_Code_4", "C", 10, "AN"],
        ["Diagnosis_Code_5", "C", 10, "AN"],
        ["Diagnosis_Code_6", "C", 10, "AN"],
        ["Diagnosis_Code_7", "C", 10, "AN"],
        ["Diagnosis_Code_8", "C", 10, "AN"],
        ["Diagnosis_Code_9", "C", 10, "AN"],
        ["Diagnosis_Code_10", "C", 10, "AN"],
        ["Diagnosis_Code_11", "C", 10, "AN"],
        ["Diagnosis_Code_12", "C", 10, "AN"],
        # Additional Claim Information
        ["Prior_Authorization_Number", "C", 30, "AN"],
        ["Referring_Provider_Number", "C", 30, "AN"],
        ["Medicaid_Resubmission_Code", "C", 10, "AN"],
        ["Medicaid_Original_Reference", "C", 30, "AN"],
        ["Mammography_Certification_Number", "C", 30, "AN"],
        ["Investigational_Device_Exemption", "C", 30, "AN"],
        ["CLIA_Number", "C", 30, "AN"],
        # Procedure Information (up to 6 lines)
        ["Procedure_Code_1", "C", 10, "AN"],
        ["Procedure_Description_1", "C", 80, "AN"],
        ["Procedure_Modifier_1_1", "C", 2, "AN"],
        ["Procedure_Modifier_1_2", "C", 2, "AN"],
        ["Procedure_Modifier_1_3", "C", 2, "AN"],
        ["Procedure_Modifier_1_4", "C", 2, "AN"],
        ["Procedure_Amount_1", "C", 10, "AN"],
        ["Procedure_Units_1", "C", 5, "AN"],
        ["Procedure_Pointer_1", "C", 10, "AN"],
        ["Procedure_EMG_1", "C", 1, "AN"],
        ["Procedure_EPSDT_1", "C", 1, "AN"],
        ["Procedure_Family_Planning_1", "C", 1, "AN"],
        ["Procedure_COB_1", "C", 1, "AN"],
        ["Rendering_Provider_NPI_1", "C", 10, "AN"],
        ["Procedure_Code_2", "C", 10, "AN"],
        ["Procedure_Description_2", "C", 80, "AN"],
        ["Procedure_Modifier_2_1", "C", 2, "AN"],
        ["Procedure_Modifier_2_2", "C", 2, "AN"],
        ["Procedure_Modifier_2_3", "C", 2, "AN"],
        ["Procedure_Modifier_2_4", "C", 2, "AN"],
        ["Procedure_Amount_2", "C", 10, "AN"],
        ["Procedure_Units_2", "C", 5, "AN"],
        ["Procedure_Pointer_2", "C", 10, "AN"],
        ["Procedure_EMG_2", "C", 1, "AN"],
        ["Procedure_EPSDT_2", "C", 1, "AN"],
        ["Procedure_Family_Planning_2", "C", 1, "AN"],
        ["Procedure_COB_2", "C", 1, "AN"],
        ["Rendering_Provider_NPI_2", "C", 10, "AN"],
        ["Procedure_Code_3", "C", 10, "AN"],
        ["Procedure_Description_3", "C", 80, "AN"],
        ["Procedure_Modifier_3_1", "C", 2, "AN"],
        ["Procedure_Modifier_3_2", "C", 2, "AN"],
        ["Procedure_Modifier_3_3", "C", 2, "AN"],
        ["Procedure_Modifier_3_4", "C", 2, "AN"],
        ["Procedure_Amount_3", "C", 10, "AN"],
        ["Procedure_Units_3", "C", 5, "AN"],
        ["Procedure_Pointer_3", "C", 10, "AN"],
        ["Procedure_EMG_3", "C", 1, "AN"],
        ["Procedure_EPSDT_3", "C", 1, "AN"],
        ["Procedure_Family_Planning_3", "C", 1, "AN"],
        ["Procedure_COB_3", "C", 1, "AN"],
        ["Rendering_Provider_NPI_3", "C", 10, "AN"],
        ["Procedure_Code_4", "C", 10, "AN"],
        ["Procedure_Description_4", "C", 80, "AN"],
        ["Procedure_Modifier_4_1", "C", 2, "AN"],
        ["Procedure_Modifier_4_2", "C", 2, "AN"],
        ["Procedure_Modifier_4_3", "C", 2, "AN"],
        ["Procedure_Modifier_4_4", "C", 2, "AN"],
        ["Procedure_Amount_4", "C", 10, "AN"],
        ["Procedure_Units_4", "C", 5, "AN"],
        ["Procedure_Pointer_4", "C", 10, "AN"],
        ["Procedure_EMG_4", "C", 1, "AN"],
        ["Procedure_EPSDT_4", "C", 1, "AN"],
        ["Procedure_Family_Planning_4", "C", 1, "AN"],
        ["Procedure_COB_4", "C", 1, "AN"],
        ["Rendering_Provider_NPI_4", "C", 10, "AN"],
        ["Procedure_Code_5", "C", 10, "AN"],
        ["Procedure_Description_5", "C", 80, "AN"],
        ["Procedure_Modifier_5_1", "C", 2, "AN"],
        ["Procedure_Modifier_5_2", "C", 2, "AN"],
        ["Procedure_Modifier_5_3", "C", 2, "AN"],
        ["Procedure_Modifier_5_4", "C", 2, "AN"],
        ["Procedure_Amount_5", "C", 10, "AN"],
        ["Procedure_Units_5", "C", 5, "AN"],
        ["Procedure_Pointer_5", "C", 10, "AN"],
        ["Procedure_EMG_5", "C", 1, "AN"],
        ["Procedure_EPSDT_5", "C", 1, "AN"],
        ["Procedure_Family_Planning_5", "C", 1, "AN"],
        ["Procedure_COB_5", "C", 1, "AN"],
        ["Rendering_Provider_NPI_5", "C", 10, "AN"],
        ["Procedure_Code_6", "C", 10, "AN"],
        ["Procedure_Description_6", "C", 80, "AN"],
        ["Procedure_Modifier_6_1", "C", 2, "AN"],
        ["Procedure_Modifier_6_2", "C", 2, "AN"],
        ["Procedure_Modifier_6_3", "C", 2, "AN"],
        ["Procedure_Modifier_6_4", "C", 2, "AN"],
        ["Procedure_Amount_6", "C", 10, "AN"],
        ["Procedure_Units_6", "C", 5, "AN"],
        ["Procedure_Pointer_6", "C", 10, "AN"],
        ["Procedure_EMG_6", "C", 1, "AN"],
        ["Procedure_EPSDT_6", "C", 1, "AN"],
        ["Procedure_Family_Planning_6", "C", 1, "AN"],
        ["Procedure_COB_6", "C", 1, "AN"],
        ["Rendering_Provider_NPI_6", "C", 10, "AN"],
    ],
}
