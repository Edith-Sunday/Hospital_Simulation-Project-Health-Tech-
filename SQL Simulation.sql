-- Table: Departments
CREATE TABLE Departments (
    Department_ID INT,
    Department_Name VARCHAR(255)
);
INSERT INTO Departments VALUES (1, 'Cardiology');
INSERT INTO Departments VALUES (2, 'Neurology');
INSERT INTO Departments VALUES (3, 'Pediatrics');
INSERT INTO Departments VALUES (4, 'Orthopedics');
INSERT INTO Departments VALUES (5, 'General Medicine');


-- Table: Doctors
CREATE TABLE Doctors (
    Doctor_ID INT,
    Name VARCHAR(255),
    Department VARCHAR(255),
    Specialty VARCHAR(255),
    Years_Experience INT
);
INSERT INTO Doctors VALUES (1, 'Allison Hill', 'Cardiology', 'Armed forces logistics/support/administrative officer', 14);
INSERT INTO Doctors VALUES (2, 'Noah Rhodes', 'Cardiology', 'Psychiatric nurse', 2);
INSERT INTO Doctors VALUES (3, 'Angie Henderson', 'Pediatrics', 'Software engineer', 1);
INSERT INTO Doctors VALUES (4, 'Daniel Wagner', 'Neurology', 'Company secretary', 3);
INSERT INTO Doctors VALUES (5, 'Cristian Santos', 'Neurology', 'Multimedia specialist', 7);


-- Table: Patients
CREATE TABLE Patients (
    Patient_ID INT,
    Name VARCHAR(255),
    Age INT,
    Gender VARCHAR(255),
    Contact VARCHAR(255),
    Date_Registered DATE
);
INSERT INTO Patients VALUES (1, 'Michele Williams', 26, 'Female', '(247)317-8108x01326', '2023-08-12');
INSERT INTO Patients VALUES (2, 'Dylan Miller', 84, 'Male', '736.026.0647x4687', '2023-10-01');
INSERT INTO Patients VALUES (3, 'Brian Ramirez', 90, 'Female', '(343)098-0500', '2024-01-16');
INSERT INTO Patients VALUES (4, 'Holly Wood', 70, 'Female', '001-788-208-1219', '2024-12-27');
INSERT INTO Patients VALUES (5, 'Derek Zuniga', 54, 'Male', '361-939-9091', '2025-05-02');


-- Table: Appointments
CREATE TABLE Appointments (
    Appointment_ID INT,
    Patient_ID INT,
    Doctor_ID INT,
    Date DATE,
    Time VARCHAR(255),
    Status VARCHAR(255),
    Mode VARCHAR(255)
);
INSERT INTO Appointments VALUES (1, 36, 4, '2024-08-05', '02:17:01', 'No-show', 'Physical');
INSERT INTO Appointments VALUES (2, 1, 2, '2025-01-14', '15:30:07', 'Completed', 'Virtual');
INSERT INTO Appointments VALUES (3, 44, 1, '2024-08-25', '09:59:18', 'Cancelled', 'Physical');
INSERT INTO Appointments VALUES (4, 47, 6, '2024-11-21', '01:46:12', 'No-show', 'Physical');
INSERT INTO Appointments VALUES (5, 8, 2, '2024-10-28', '21:59:36', 'No-show', 'Virtual');


-- Table: Visits
CREATE TABLE Visits (
    Visit_ID INT,
    Appointment_ID INT,
    Diagnosis VARCHAR(255),
    Prescription VARCHAR(255),
    Notes VARCHAR(255)
);
INSERT INTO Visits VALUES (1, 97, 'Hypertension', 'Paracetamol', 'Grow issue each include radio.');
INSERT INTO Visits VALUES (2, 31, 'Hypertension', 'Ibuprofen', 'Color bad that people.');
INSERT INTO Visits VALUES (3, 87, 'Diabetes', 'Ibuprofen', 'Marriage on discussion point least.');
INSERT INTO Visits VALUES (4, 40, 'Fracture', 'Paracetamol', 'Together let explain.');
INSERT INTO Visits VALUES (5, 29, 'Hypertension', 'Rest', 'Citizen kid generation onto police interesting economic.');


-- Table: Billing
CREATE TABLE Billing (
    Bill_ID INT,
    Appointment_ID INT,
    Amount FLOAT,
    Payment_Status VARCHAR(255),
    Insurance_Used VARCHAR(255)
);
INSERT INTO Billing VALUES (1, 35, 704.82, 'Paid', 'Yes');
INSERT INTO Billing VALUES (2, 42, 745.37, 'Unpaid', 'No');
INSERT INTO Billing VALUES (3, 32, 1814.61, 'Pending', 'Yes');
INSERT INTO Billing VALUES (4, 12, 4748.4, 'Pending', 'Yes');
INSERT INTO Billing VALUES (5, 36, 3370.41, 'Unpaid', 'Yes');


-- =============================
-- Relational Analysis Queries
-- =============================
-- Insight 1: Doctor Appointment Counts
SELECT 
    d.Doctor_ID,
    d.Name,
    COUNT(a.Appointment_ID) AS Total_Appointments
FROM Appointments a
JOIN Doctors d ON a.Doctor_ID = d.Doctor_ID
GROUP BY d.Doctor_ID, d.Name;
-- Insight 2: Revenue by Department
SELECT 
    d.Department,
    SUM(b.Amount) AS Total_Revenue
FROM Appointments a
JOIN Billing b ON a.Appointment_ID = b.Appointment_ID
JOIN Doctors d ON a.Doctor_ID = d.Doctor_ID
GROUP BY d.Department;
-- Insight 3: Diagnosis Frequency by Doctor
SELECT 
    doc.Name,
    v.Diagnosis,
    COUNT(*) AS Diagnosis_Count
FROM Visits v
JOIN Appointments a ON v.Appointment_ID = a.Appointment_ID
JOIN Doctors doc ON a.Doctor_ID = doc.Doctor_ID
GROUP BY doc.Name, v.Diagnosis
ORDER BY doc.Name, Diagnosis_Count DESC;