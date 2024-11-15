# Project Design Document

## Your Project Title: CSAssist
--------
Prepared by:

* `Sai Teja Sunku`,`WPI`
* `Achintya Sanjay`,`WPI`
* `Ishaan Patel`,`WPI`
* `Jake Grier`,`WPI`
---

**Course** : CS 3733 - Software Engineering 

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Software Design](#2-software-design)
    - [2.1 Database Model](#21-model)
    - [2.2 Subsystems and Interfaces](#22-subsystems-and-interfaces)
    - [2.2.1 Overview](#221-overview)
    - [2.2.2 Interfaces](#222-interfaces)
    - [2.3 User Interface Design](#23-view-and-user-interface-design)
- [3. References](#3-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

### Document Revision History

| Name       | Date       | Changes                                          | Version |
|------------|------------|--------------------------------------------------|---------|
| Revision 1 | 2024-11-12 | Initial draft for section 1, 2.1, 2.2, 2.3       | 1.0     |
| Revision 2 | 2024-11-13 | Added information to section 2.2                 | 2.0     |
| Revision 3 | 2024-11-14 | Revised section 2.2 and added additional details | 3.0     |
| Revision 4 | 2024-11-15 | Added UML design for section 2.1                 | 4.0     |


# 1. Introduction

Explain the purpose of this document. If this is a revision of an earlier document, please make sure to summarize what changes have been made during the revision (keep this discussion brief). 

This Design Document aims to explain software design of CSAssist web application. The software design includes:
1. Database Model
2. Subsystems and Interfaces
3. Subsystem Routes
4. User Interfaces
The database model provide information about the tables involved, fields in each table, foreign and primary keys, any association table, and multiplicity and interactions between tables.
The subsystem and interfaces provide information on how the web application is divided into different components and any dependencies between components. The subsystem is designed to have low coupling and high cohesion.
The subsystem routes gives information about the routes, decorator functions and their purpose. The user interfaces provide high level overview of how the web application looks and features present for user to interact with.

# 2. Software Design

(**Note**: For all subsections of Section-2: You should describe the design for the end product (completed application) - not only your iteration1 version. You will revise this document and add more details later.)

## 2.1 Database Model
1. Student
    *   This database model will maintain information about students, and will maintain information about past SA roles.
    * Student will have a relationship with Course, to show prior courses that the Student has been an SA for
    * Student will have a relationship with Position, to show courses that the student has applied to be an SA for
    * Student will have a relationship with Position to show courses that the student is currently assigned to be an SA for
2. Professor
    * This database model will maintain information about professors.
    * Professor will have a relationship with Course, to show courses that the Professor is teaching
3. Course
    * This database model will maintain information about Course sections and will maintain information about the professor teaching the course.
    * Course will have a relationship with Teacher, to show the professor teaching that course
    * Courses will have a relationship with Position, to show open SA positions for the course
4. Position
    * This database model will maintain information about the SA positions of a course. It will maintain information about the course it is assigned to, the SA applicants, and the current SAs of the course.
    * Position will have a relatinoship with Course, to show the course that the postion is associated with


<kbd>      
      <img src="images/UML.png">
  </kbd>

## 2.2 Subsystems and Interfaces

### 2.2.1 Overview

#### Subsystem Overview
The subsystems involved in this web application are:
1. Main - handles homepage/index page for both the user roles: Student and Instructor
2. Auth - handles the login, logout, and authentication logic for both users roles Student and Instructor and redirects accordingly. 
3. Errors - displays error templates when some part of the app fails.
4. Student - handles all the operations for a Student user like applying for SA position, viewing open positions, registering profile, providing recommendations, and application management. 
5. Instructor - handles all the operations for a Instructor user like creating course section and SA position, registering profile, application management, and viewing student.
All the subsystems fit together as the flow starts from Auth for logging-in, then Main for homepage, then Student or Instructor subsystem to handle main parts of the web app, finally Auth again manages logout. All the subsystems can throw errors through Error subsystem.

#### UML Component Diagram
<kbd>
      <img src="images/CS3733_Subsystems_Diagram.drawio.png"  border="2">
</kbd>

### 2.2.2 Interfaces

#### 2.2.2.1 Student Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. |view_positions()   |/student/viewpositions |  Student can view open positions for SA                    
|2. |view_recommend()   | /student/viewrecommend           |  Students can view recommended positions to apply for based on their credentials            |
|3. |view_SA_details()  |  /student/viewsadetails          |   Students can check the details of each SA position           |
|4. |check_app_status() |  /student/checkappstatus          |  Students can check status of submitted SA application(s)            |
|5. | withdraw_app()    |  /student/withdrawapp          |  Students can withdraw existing submitted applications            |
|6. |   student_register()                |   /student/studentregister         |  Students can create student profiles to access SA positions information and application pages            |

#### 2.2.2.2 Main Routes

|   | Methods           | URL Path   | Description                         |
|:--|:------------------|:-----------|:------------------------------------|
|1. | index()           |  /index    | Home Page for Instructor or Student |

#### 2.2.2.3 Auth Routes

|    | Methods     | URL Path       | Description                                                                                                                                                                                                                       |
|:---|:------------|:---------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. | login()     | /user/login    | Authenticates the user based on username and password and redirects to homepage according to their role on success. If the validation fails because of wrong credentials or user does not exist, then error message is displayed. |
| 2. | logout()    | /user/logout   | Logs out the user from the session and redirect back to the login page.                                                                                                                                                           |
| 3. | login_sso() | /user/loginsso | Allows user to login using Azure SSO instead of email and password.                                                                                                                                                               |

#### 2.2.2.4 Instructor Routes

|   | Methods                  | URL Path                             | Description                                                                                                                                                                                           |
|:--|:-------------------------|:-------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1. | add_student(student_id)  | /instructor/<student_id>/addstudent  | Adds the selected student to the open SA position only if the student is unassigned, else throws an error. Saves the student for that position and mark as assigned.                                  |
|2. | view_student(student_id) | /instructor/<student_id>/viewstudent | Displays the student information and qualifications for the positions.                                                                                                                                |
|3. | view_allstudents()       | /instructor/viewallstudents          | Displays all the students who applied for every SA position that the instructor created.                                                                                                              |
|4. | create_position()        | /instructor/createposition           | Create a SA position for the course that the instructor created and save the data in database. SA position form includes course section, number of SAs, and qualifications information.               |
|5. | create_course()          | /instructor/createcourse             | Create course section by selecting course from course catalog, course section, and the term. After submitting the course is saved into database.                                                      |
|6. | instructor_register()    | /instructor/register                 | Create instructor profile with username, password, name, WPI ID, email, and phone number. After submitting the data is stored into database and the username and password can be used for logging-in. |

#### 2.2.2.5 Error Routes

|    | Methods           | URL Path       | Description                                                         |
|:---|:------------------|:---------------|:--------------------------------------------------------------------|
| 1. | not_found_error() | 404            | Displays 404 error template                                         |
| 2. | internal_error()  | 500            | Displays 500 error template                                         |



### 2.3 User Interface Design 

Provide a list of the page templates you plan to create and supplement your description with UI sketches or screenshots. Make sure to mention which user-stories in your “Requirements and Use Cases" document will utilize these interfaces for user interaction. 

1. Student sign in page<br>This page includes a form for students to sign into their account, a button to switch to instructor sign in, and a button to register.<br>
User story: 1
  <kbd>      
      <img src="images/StudentSignIn1.png">
  </kbd>

2. Instructor sign in page<br>This page includes a form for instructors to sign in, a button to switch to student sign in page, and a button to register.<br>
User story: 2
  <kbd>      
      <img src="images/InstructorSignIn1.png">
  </kbd>

3. Student create account page<br>This page includes a form for a student to create an account and register, and a button to switch to the sign in page.<br>
User story: 3
  <kbd>      
      <img src="images/CreateStudent1.png">
  </kbd>

4. Instructor create account page<br>This page includes a form for a professor to create an account and register, and a button to switch to the sign in page.<br>
User story: 4
  <kbd>      
      <img src="images/CreateInstructor1.png">
  </kbd>

5. Add course section pages<br>This page includes a form for professors to add course sections, and a logout button.<br>
User Story: 9
  <kbd>      
      <img src="images/AddCourseSections.png">
  </kbd>

6. View Open SA Positions page<br>This page includes three secions to display the three recomended levels for the open sa positions. It also has a logout button.<br>
User Story: 5, 6, 7
  <kbd>      
      <img src="images/CS3733_TeamProject1_3and4student.png">
  </kbd>

7. Apply for SA Position page<br> This page includes a form for students to submit their application to open sa positions. It also has a logout button<br>
User Story: 8
  <kbd>      
      <img src="images/ApplyForSAPosition.png">
  </kbd>

8. View application status page<br> This page allows students to view the status of all their applications and gives the option to withdraw. It also includes a logout button.<br>
User Story: 13, 14
  <kbd>      
      <img src="images/CS3733_TeamProject1_6%267student.png">
  </kbd>

9. Create SA Position page<br>This page includes a form for instructors to create sa positions.<br>
User Story: 10, 12
  <kbd>      
      <img src="images/CS3733_TeamProject1_5instructor.png">
  </kbd>

10. View Student Qualifications<br> This page displays a selected students qualifications to an instructor<br>
User Story: 11
  <kbd>      
      <img src="images/ViewStudentQualifications.png">
  </kbd>


# 3. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

----
# Appendix: Grading Rubric
(Please remove this part in your final submission)

 * You will first  submit a draft version of this document:
    * "Project 3 : Project Design Document - draft" (5pts). 
* We will provide feedback on your document and you will revise and update it.
    * "Project 5 : Project Design Document - final" (80pts) 

Below is the grading rubric that we will use to evaluate the final version of your document. 

|**MaxPoints**| **Design** |
|:---------:|:-------------------------------------------------------------------------|
|           | Are all parts of the document in agreement with the product requirements? |
| 8         | Is the architecture of the system ([2.2.1 Overview](#221-overview)) described well, with the major components and their interfaces?         
| 8        | Is the database model (i.e., [2.1 Database Model](#21-database-model)) explained well with sufficient detail? Do the team clearly explain the purpose of each table included in the model?| 
|          | Is the document making good use of semi-formal notation (i.e., UML diagrams)? Does the document provide a clear UML class diagram visualizing the DB model of the system? |
| 18        | Is the UML class diagram complete? Does it include all classes (tables) and does it clearly mark the PK and FKs for each table? Does it clearly show the associations between them? Are the multiplicities of the associations shown correctly? ([2.1 Database Model](#21-database-model)) |
| 25        | Are all major interfaces (i.e., the routes) listed? Are the routes explained in sufficient detail? ([2.2.2 Interfaces](#222-interfaces)) |
| 13        | Is the view and the user interfaces explained well? Did the team provide the screenshots of the interfaces they built so far.  ([2.3 User Interface Design](#23-user-interface-design)) |
|           | **Clarity** |
|           | Is the solution at a fairly consistent and appropriate level of detail? Is the solution clear enough to be turned over to an independent group for implementation and still be understood? |
| 5         | Is the document carefully written, without typos and grammatical errors?  |
| 3         | Is the document well formatted? (Make sure to check your document on GitHub. You will loose points if there are formatting issues in your document.  )  |
|           |  |
| 80         | **Total** |
|           |  |