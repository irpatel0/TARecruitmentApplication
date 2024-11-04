# Software Requirements and Use Cases

## Your Project Title
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
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 User Stories](#22-user-stories)
  - [2.3 Use Cases](#23-use-cases)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

## Document Revision History

| Name | Date       | Changes | Version |
| ------ |------------| --------- | --------- |
|Revision 1 | 2024-11-03 |Initial draft | 1.0        |
|      |            |         |         |
|      |            |         |         |

----
# 1. Introduction

Provide a short description of the software being specified. Describe its purpose, including relevant benefits, objectives, and goals.

The software being developed is a web application for Computer Science department to recruit undergraduate student assistants (SAs) for the
introductory level courses and lab sections. This product aims to eliminate the manual process of applying and processing for an SA position.
In this web application students who are interested in SA positions will create accounts and enter their contact
information as well as their course preferences for student assistantships. In addition, instructors will be able to choose their student assistants among the students who are
interested in their courses. The web application can be accessed from anywhere at anytime using any device. The application's benefits include:  
- Secured login system
- Look at open SA positions
- Students can apply for open SA positions
- Display information for each SA position
- Identify students that match the position
- Recommend SA positions to students
- View application status
- Withdraw pending applications if necessary for students

The application can simplify the process for students and professors.

----
# 2. Requirements Specification

This section specifies the software product's requirements. Specify all of the software requirements to a level of detail sufficient to enable designers to design a software system to satisfy those requirements, and to enable testers to test that the software system satisfies those requirements.

## 2.1 Customer, Users, and Stakeholders

A brief description of the customer, stakeholders, and users of your software.

- The customer for this product are the undergraduate students who are interested in being an SA for a course.

- The stakeholder is the Computer Science department at WPI, who want to make the process for recruiting student assistants easier 

- The users of the software are the students who are interested in being a student assistant, and the instructor that want to create applications for their courses, and accept students to be a student assistant

----
## 2.2 User Stories
This section will include the user stories you identified for your project. Make sure to write your user stories in the form : 
"As a **[Role]**, I want **[Feature]** so that **[Reason/Benefit]** "

1. **Student Login:** As a Student, I want to be able to login to the site so that I can use the site
2. **Professor Login:** As a Professor, I want to be able to login to the site so that I can use the site
3. **Student Profile:** As a Student, I want to be able to create my profile so that I can be recommended best courses and the professor can see if my profile matches the requirement
4. **Professor Profile:** As a Professor, I want to be able to create my profile so that the student can see my information
5. **View Open SA Positions:** As a Student, I want to view all open SA positions so that I decide which ones I am interested in
6. **View SA Position Details:** As a Student, I want to view all the details of every open SA position so that I know if I can meet the qualifications
7. **View SA Position Recommendations:** As a Student, I want to be recommended SA positions that match my profile 
8. **Apply For SA Position:** As a Student, I want to apply for the open SA positions
9. **Create Course:** As a Professor, I want to create course sections so that students can view the course information
10. **Create SA Positions:** As a Professor, I want to create SA positions for a particular course so that students can apply for a particular course
11. **View Student Applications:** As a Professor, I want to view all students applied for a SA position so that I know if the student took the course and if he/she got an A, to determine if good fit
12. **Add Student To A Position:** As a Professor, I want to add a student to the SA position so that I can register students who haven't been assigned a position
13. **Check Application Status:** As a Student, I want to check status of my applications so that I know which applications are approved, rejected or still pending
14. **Withdraw Application:** As a Student, I want to withdraw my pending applications so that I'm not in the system for positions as I'm no longer interested in

----
## 2.3 Use Cases

This section will include the specification for your project in the form of use cases. 

Group the related user stories and provide a use case for each user story group. You don't need to draw the use-case diagram for the use cases; you will only provide the textual descriptions.  **Also, you don't need to include the use cases for "registration" and "login" use cases for both student and faculty users.**

  * First, provide a short description of the actors involved (e.g., regular user, administrator, etc.) and then follow with a list of the use cases.
  * Then, for each use case, include the following:

    * Name,
    * Participating actors,
    * Entry condition(s) (in what system state is this use case applicable),
    * Exit condition(s) (what is the system state after the use case is done),
    * Flow of events (how will the user interact with the system; list the user actions and the system responses to those),
    * Alternative flow of events (what are the exceptional cases in the flow of events and they will be handles)
    * Iteration # (which sprint do you plan to work on this use case) 

Each use case should also have a field called "Iteration" where you specify in which iteration you plan to implement this feature.

You may use the following table template for your use cases. Copy-paste this table for each use case you will include in your document.

<!------------------------------------------------------------------------>
Use Case 5
Name: View open SA Positions,
Participating actors: Students,
Entry condition(s): Student has created an account and is logged in,
Exit condition(s): The web applications displays a list of open SA Positons,
Flow of events:
  1. The student logs in to their account
  2. The student selects the button "View Open SA Positions
  3. The System gets the open SA Position from the database
  4. The System displays a list of open SA positions,
Alternative flow of events:
  1. The Student is not logged in to an account: They will be redirected to the sign in page and a message will flash saying "Please log in to access this page"
  2. No SA Positions are open: A message will flash saying "No open positions found"
  3. There is an error fetching the data from the db: A message will flash saying "Error gathering information, please try again"
Iteration # TBD
<!------------------------------------------------------------------------->
Use Case 6
Name: View Details of SA Positon,
Participating actors: Students,
Entry condition(s): Student has created an account and is logged in,
Exit condition(s): The web applications displays the details of the selected position,
Flow of events:
  1. The student logs in to their account
  2. The student selects to view all open SA Positions
  3. The system gets all open sa positions from the DB
  4. The system displays a list of all open SA Positions
  5. The Student selects "View Details" on one of the SA Positions
  6. The system gets the data from that position in the db
  7. The system displays the details of that position to the student. 
Alternative flow of events:
  1. The Student is not logged in to an account: They will be redirected to the sign in page and a message will flash saying "Please log in to access this page"
  2. No SA Positions are open: A message will flash saying "No open positions found"
  3. There is an error fetching the data from the db: A message will flash saying "Error gathering information, please try again"
  4. The student selects to view the details of a positon but it is no longer found in the db: Flash error saying "Position not found"
Iteration # TBD
<!------------------------------------------------------------------------->
Use Case 7
Name: View Recommended positions,
Participating actors: Students,
Entry condition(s): Student has created an account and is logged in,
Exit condition(s): The web applications displays a list of open positions ranked on the recomendation algorithm,
Flow of events:
  1. The student logs in to their account
  2. The student selects to view all open SA Positions
  3. The system gets all open sa positions from the DB
  4. The system displays a list of all open SA Positions
  5. The student selects the button "Filter by recommendned"
  6. The web application reorders the list of open sa Positions using the recommendation algorithm
  7. The web application displays the reordered list of positions.
Alternative flow of events:
  1. The Student is not logged in to an account: They will be redirected to the sign in page and a message will flash saying "Please log in to access this page"
  2. No SA Positions are open: A message will flash saying "No open positions found"
  3. There is an error fetching the data from the db: A message will flash saying "Error gathering information, please try again"
  4. The student is not recommeneded for any positions, flash message saying "No positions found" 
Iteration # TBD
<!------------------------------------------------------------------------->
Use Case 8
Name: Apply for SA Positions,
Participating actors: Students,
Entry condition(s): Student has created an account and is logged in,
Exit condition(s): The system adds the students application to the db,
Flow of events:
  1. The student logs in to their account
  2. The student selects to view all open SA Positions
  3. The system gets all open sa positions from the DB
  4. The system displays a list of all open SA Positions
  5. The student selects the "Apply" button on the selected position
  6. The system displays the applicaton form for the selected position.
  7. The student enters the grade they earned in the course.
  8. The student enters the year and term they took the course.
  9. The student enters the year and term they are applying for.
  10. The student selects Submit.
  11. The system adds the application to the db.
Alternative flow of events:
  1. The Student is not logged in to an account: They will be redirected to the sign in page and a message will flash saying "Please log in to access this page"
  2. No SA Positions are open: A message will flash saying "No open positions found"
  3. There is an error fetching the data from the db: A message will flash saying "Error gathering information, please try again"
  4. The student does not enter all fields: Flash message saying "Please complete all fields before submitting."
Iteration # TBD
<!------------------------------------------------------------------------->
| Use case # 9               |                                                                                                                                                                                                                                                                                                                  |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name                       | Create Course                                                                                                                                                                                                                                                                                                    |
| Participating actor        | Professor                                                                                                                                                                                                                                                                                                        |
| Entry condition(s)         | The user is logged in to the application and opened the create course page.                                                                                                                                                                                                                                      |
| Exit condition(s)          | The new created course is displayed correctly with all the information entered by professor.                                                                                                                                                                                                                     |
| Flow of events             | 1. The user chooses the create course option.<br/> 2. The system prompts the user to choose course number, section, and term from the pre-created list of courses.<br/> 3. The user submits the chosen course number, section, and term.<br/> 4. The system adds the course and displays the new course created. |
| Alternative flow of events | 1. In step 2, if the desired course for the professor to add does not exist, they can manually enter the course number and choose the section and term they are going to offer that course.<br/> 2. The user can abort creating the course at any time during steps 2 or 3.                                      |
| Iteration #                | TBD                                                                                                                                                                                                                                                                                                              |

| Use case # 10              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name                       | Create SA Positions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Participating actor        | Professor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Entry condition(s)         | The user is logged in to the application and opened the create SA positions page.                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Exit condition(s)          | The SA position is successfully added to a specific course with all the correct information of the qualifications entered by the professor.                                                                                                                                                                                                                                                                                                                                                                      |
| Flow of events             | 1. The user chooses the create SA position option.<br/> 2. The system prompts the user to enter course section<br/> 3. The professor enters the course section for which SAships needs to be added.<br/> 4. The system prompts the user to enter number of SAs and qualifications needed for that particular position.<br/> 5. The user fills out all the SA position information and submits.<br/> 6. The system displays a success message by adding the SA position to the course specified by the professor. |
| Alternative flow of events | 1. In step 2, the user can create SA positions only for the courses created by them. If the user chooses a section that was not created by them, then the system throws an error and does not allow to add SAships.<br/> 2. In step 4, the user can enter as many additional qualifications they want but min GPA, grade earned for the course, prior SA experience are required information.<br/> 3. The user can create multiple SA positions for multiple course sections that were created by the same user. |
| Iteration #                | TBD                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

| Use case # 11              |                                                                                                                                                                                                                                                                                                                                                                                                               |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name                       | View Student Applications                                                                                                                                                                                                                                                                                                                                                                                     |
| Participating actor        | Professor                                                                                                                                                                                                                                                                                                                                                                                                     |
| Entry condition(s)         | The user is logged in to the application and opened view student applications page.                                                                                                                                                                                                                                                                                                                           |
| Exit condition(s)          | Display of all the student applications with student's profile information who applied for the SA position for that particular professor.                                                                                                                                                                                                                                                                     |
| Flow of events             | 1. The user chooses view student applications option.<br/> 2. The system displays all the student applications for all the course sections handled by that specific user and also shows if a student applicant is already assigned to different course.<br/> 3. The user can select a particular student to view student's profile.<br/> 4. The system displays student's profile with all their information. |
| Alternative flow of events | 1. In step 2, the system only displays student applications that are pending for approval from the professor.                                                                                                                                                                                                                                                                                                 |
| Iteration #                | TBD                                                                                                                                                                                                                                                                                                                                                                                                           |


| Use case # 12      |                                                                                                                                                                              |
| ------------------ |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name              | Add Student To A Position                                                                                                                                              |
| Participating actor  | "Professor"                                                                                                                                                                  |
| Entry condition(s)     | Faculty user logged in and is on the page listing students that applied.                                                                                                     |
| Exit condition(s)           | Prompt the screen that student was successfully added to course                                                                                                              |
| Flow of events | 1. Faculty user views list of students that applied for SA positions.<br/> 2. Faculty user views qualifications of candidate.<br/> 3. Faculty user clicks on a student to add to a course |
| Alternative flow of events    | 1. Faculty reverts to the previous page<br/> 2. The user can only choose the student who has not been yet assigned to any SAship position for any course.                    |
| Iteration #         | TBD                                                                                                                                                                          |

| Use case # 13      |                                                                                                                                   |
| ------------------ |-----------------------------------------------------------------------------------------------------------------------------------|
| Name              | Check Application Status                                                                                                          |
| Participating actor  | "Student"                                                                                                                         |
| Entry condition(s)     | User logs in with username and password and then selects application page                                                         |
| Exit condition(s)           | User clicks on another page (such as withdraw application)                                                                        |
| Flow of events | 1. User scrolls down to each application                                                                                          |
| Alternative flow of events   | 1. Each application displays individual status<br/> 2. User submits new application, which will newly show as pending application |
| Iteration #         | TBD                                                                                                                               |

| Use case # 14      |                                                                                                                                                                                                                                                                                                                   |
| ------------------ |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name              | Withdraw Application                                                                                                                                                                                                                                                                                              |
| Participating actor  | "Student"                                                                                                                                                                                                                                                                                                         |
| Entry condition(s)     | User logs in with username and password and clicks on applications page                                                                                                                                                                                                                                           |
| Exit condition(s)           | User is redirected to applications page showing remaining applications status                                                                                                                                                                                                                                     |
| Flow of events | 1. User is on the application page<br/> 2. User scrolls down to part of the page displaying submitted pending applications<br/> 3. User selects option to withdraw<br/> 4. System prompts to confirm withdrawal<br/> 5. User selects confirm option<br/> 6. User is prompted successful withdrawal of application |
| Alternative flow of events    | 1. User selects cancel on withdrawal confirmation prompt<br/> 2. User is prompted application withdrawal cancelled                                                                                                                                                                                                     |
| Iteration #         | TBD                                                                                                                                                                                                                                                                                                               |

----
# 3. User Interface

Here you should include the sketches or mockups for the main parts of the interface.
You may use Figma to design your interface:

  Example image. The image file is in the `./images` directory.
  <kbd>
      <img src="images/figma.jpg"  border="2">
  </kbd>
  
----
# 4. Product Backlog

Here you should include a link to your GitHub repo issues page, i.e., your product backlog. Make sure to create an issue for each user story.  

----
# 5. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

----
----
# Appendix: Grading Rubric
(Please remove this part in your final submission)

These is the grading rubric that we will use to evaluate your document. 

| Max Points  | **Content** |
| ----------- | ------- |
| 4          | Do the requirements clearly state the customers’ needs? |
| 2          | Do the requirements avoid specifying a design (note: customer-specified design elements are allowed)? |
| | |  
|    | **Completeness** |
| 14 | Are user stories complete? Are all major user stories included in the document?  |
| 5 | Are user stories written in correct form? | 
| 14 |  Are all major use cases (except registeration and login) included in the document? |
| 15 | Are use cases written in sufficient detail to allow for design and planning? Are the "flow of events" in use case descriptions written in the form of "user actions and system responses to those"? Are alternate flow of events provided (when applicable)? | 
| 6 |  Are the User Interface Requirements given with some detail? Are there some sketches, mockups?  |
| | |  
|   | **Clarity** |
| 5 | Is the document carefully written, without typos and grammatical errors? <br> Is each part of the document in agreement with all other parts? <br> Are all items clear and not ambiguous? |
| | |
|**65**|**TOTAL**|


