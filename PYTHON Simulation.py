
# Hospital Appointment & Patient Records Simulation Project
# Tools: Pandas, Faker, Seaborn, Matplotlib, xlsxwriter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker
import random

# ----------------------------
# 1. Data Simulation
# ----------------------------
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

departments = ['Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 'General Medicine']
department_df = pd.DataFrame({
    'Department_ID': range(1, len(departments) + 1),
    'Department_Name': departments
})

doctor_df = pd.DataFrame({
    'Doctor_ID': range(1, 11),
    'Name': [fake.name() for _ in range(10)],
    'Department': [random.choice(departments) for _ in range(10)],
    'Specialty': [fake.job() for _ in range(10)],
    'Years_Experience': [random.randint(1, 30) for _ in range(10)]
})

patient_df = pd.DataFrame({
    'Patient_ID': range(1, 51),
    'Name': [fake.name() for _ in range(50)],
    'Age': [random.randint(1, 90) for _ in range(50)],
    'Gender': [random.choice(['Male', 'Female']) for _ in range(50)],
    'Contact': [fake.phone_number() for _ in range(50)],
    'Date_Registered': [fake.date_between(start_date='-2y', end_date='today') for _ in range(50)]
})

appointment_df = pd.DataFrame({
    'Appointment_ID': range(1, 101),
    'Patient_ID': [random.choice(patient_df['Patient_ID']) for _ in range(100)],
    'Doctor_ID': [random.choice(doctor_df['Doctor_ID']) for _ in range(100)],
    'Date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)],
    'Time': [fake.time() for _ in range(100)],
    'Status': [random.choice(['Completed', 'Cancelled', 'No-show']) for _ in range(100)],
    'Mode': [random.choice(['Physical', 'Virtual']) for _ in range(100)]
})

visit_df = pd.DataFrame({
    'Visit_ID': range(1, 81),
    'Appointment_ID': random.sample(list(appointment_df['Appointment_ID']), 80),
    'Diagnosis': [random.choice(['Flu', 'Asthma', 'Diabetes', 'Hypertension', 'Fracture', 'Migraine']) for _ in range(80)],
    'Prescription': [random.choice(['Paracetamol', 'Ibuprofen', 'Insulin', 'Amoxicillin', 'Rest', 'Physiotherapy']) for _ in range(80)],
    'Notes': [fake.sentence() for _ in range(80)]
})

billing_df = pd.DataFrame({
    'Bill_ID': range(1, 91),
    'Appointment_ID': random.sample(list(appointment_df['Appointment_ID']), 90),
    'Amount': [round(random.uniform(500, 5000), 2) for _ in range(90)],
    'Payment_Status': [random.choice(['Paid', 'Unpaid', 'Pending']) for _ in range(90)],
    'Insurance_Used': [random.choice(['Yes', 'No']) for _ in range(90)]
})

# ----------------------------
# 2. KPIs & Insights
# ----------------------------
kpis = {
    'Total Patients': patient_df['Patient_ID'].nunique(),
    'Total Doctors': doctor_df['Doctor_ID'].nunique(),
    'Total Appointments': appointment_df['Appointment_ID'].nunique(),
    'Total Departments': department_df['Department_ID'].nunique(),
    'Appointment Status Counts': appointment_df['Status'].value_counts().to_dict(),
    'Total Billed Amount': billing_df['Amount'].sum(),
    'Average Bill Amount': billing_df['Amount'].mean(),
    'Insurance Usage': billing_df['Insurance_Used'].value_counts(normalize=True).round(2).to_dict(),
    'Top Diagnoses': visit_df['Diagnosis'].value_counts().head(3).to_dict()
}

# ----------------------------
# 3. Visualizations
# ----------------------------
sns.set(style="whitegrid")

plt.figure(figsize=(6, 4))
sns.countplot(data=appointment_df, x='Status', palette='pastel')
plt.title('Appointment Status')
plt.savefig('appointment_status.png')
plt.close()

plt.figure(figsize=(5, 5))
billing_df['Insurance_Used'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#66c2a5', '#fc8d62'])
plt.title('Insurance Usage')
plt.ylabel('')
plt.savefig('insurance_usage.png')
plt.close()

plt.figure(figsize=(6, 4))
visit_df['Diagnosis'].value_counts().head(5).plot(kind='barh', color='skyblue')
plt.title('Top Diagnoses')
plt.xlabel('Cases')
plt.savefig('top_diagnoses.png')
plt.close()

plt.figure(figsize=(6, 4))
sns.histplot(billing_df['Amount'], bins=15, kde=True, color='gray')
plt.title('Billing Amount Distribution')
plt.xlabel('Amount')
plt.savefig('billing_distribution.png')
plt.close()

# ----------------------------
# 4. Relational Insights (Pandas SQL-like joins)
# ----------------------------
doctor_appointment_counts = appointment_df.merge(doctor_df, on='Doctor_ID') \
                                          .groupby(['Doctor_ID', 'Name'])['Appointment_ID'] \
                                          .count().reset_index(name='Total_Appointments')

revenue_per_department = appointment_df.merge(billing_df, on='Appointment_ID') \
                                       .merge(doctor_df[['Doctor_ID', 'Department']], on='Doctor_ID') \
                                       .groupby('Department')['Amount'].sum().reset_index(name='Total_Revenue')

diagnosis_by_doctor = visit_df.merge(appointment_df[['Appointment_ID', 'Doctor_ID']], on='Appointment_ID') \
                              .merge(doctor_df[['Doctor_ID', 'Name']], on='Doctor_ID') \
                              .groupby(['Name', 'Diagnosis']) \
                              .size().reset_index(name='Diagnosis_Count')

# ----------------------------
# 5. Excel Dashboard Export
# ----------------------------
with pd.ExcelWriter('hospital_dashboard.xlsx', engine='xlsxwriter') as writer:
    # Export tables
    patient_df.to_excel(writer, sheet_name='Patients', index=False)
    doctor_df.to_excel(writer, sheet_name='Doctors', index=False)
    department_df.to_excel(writer, sheet_name='Departments', index=False)
    appointment_df.to_excel(writer, sheet_name='Appointments', index=False)
    visit_df.to_excel(writer, sheet_name='Visits', index=False)
    billing_df.to_excel(writer, sheet_name='Billing', index=False)

    # Export insights
    doctor_appointment_counts.to_excel(writer, sheet_name='Doctor_Appointments', index=False)
    revenue_per_department.to_excel(writer, sheet_name='Revenue_By_Department', index=False)
    diagnosis_by_doctor.to_excel(writer, sheet_name='Diagnosis_By_Doctor', index=False)

    # KPI Summary
    kpi_df = pd.DataFrame([
        ['Total Patients', kpis['Total Patients']],
        ['Total Doctors', kpis['Total Doctors']],
        ['Total Appointments', kpis['Total Appointments']],
        ['Total Departments', kpis['Total Departments']],
        ['Total Billed Amount', round(kpis['Total Billed Amount'], 2)],
        ['Average Bill Amount', round(kpis['Average Bill Amount'], 2)],
        ['Insurance Yes (%)', kpis['Insurance Usage'].get('Yes', 0) * 100],
        ['Insurance No (%)', kpis['Insurance Usage'].get('No', 0) * 100],
        ['Top Diagnosis', list(kpis['Top Diagnoses'].keys())[0]]
    ], columns=['Metric', 'Value'])

    kpi_df.to_excel(writer, sheet_name='KPI_Summary', index=False)

    # Insert charts into KPI_Summary
    worksheet = writer.sheets['KPI_Summary']
    worksheet.insert_image('D2', 'appointment_status.png')
    worksheet.insert_image('D20', 'insurance_usage.png')
    worksheet.insert_image('J2', 'top_diagnoses.png')
    worksheet.insert_image('J20', 'billing_distribution.png')
