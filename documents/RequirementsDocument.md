# Software Requirements and Use Cases

## Your Project Title
--------
Prepared by:

* `<author1>`,`<organization>`
* `<author1>`,`<organization>`
* `<author1>`,`<organization>`
* `<author1>`,`<organization>`

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

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-11-07 |Initial draft | 1.0        |
|      |      |         |         |
|      |      |         |         |

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

----
## 2.2 User Stories
This section will include the user stories you identified for your project. Make sure to write your user stories in the form : 
"As a **[Role]**, I want **[Feature]** so that **[Reason/Benefit]** "

1. As a Student, I want to be able to login to the site so that I can use the site
2. As a Professor, I want to be able to login to the site so that I can use the site
3. As a Student, I want to be able to create my profile so that I can be recommended best courses and the professor can see if my profile matches the requirement
4. As a Professor, I want to be able to create my profile so that the student can see my information
5. As a Student, I want to view all open SA positions so that I decide which ones I am interested in
6. As a Student, I want to view all the details of every open SA position so that I know if I can meet the qualifications
7. As a Student, I want to be recommended SA positions that match my profile 
8. As a Student, I want to apply for the open SA positions
9. As a Professor, I want to create course sections so that students can view the course information
10. As a Professor, I want to create SA positions for a particular course so that students can apply for a particular course
11. As a Professor, I want to view all students applied for a SA position so that I know if the student took the course and if he/she got an A, to determine if good fit
12. As a Professor, I want to add a student to the SA position so that I can register students who haven't applied for the position
13. As a Student, I want to check status of my applications so that I know which applications are approved, rejected or still pending
14. As a Student, I want to withdraw my pending applications so that I'm not in the system for positions as I'm no longer interested in

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

| Use case # 1      |   |
| ------------------ |--|
| Name              | "enter your reponse here"  |
| Participating actor  | "enter your reponse here"  |
| Entry condition(s)     | "enter your reponse here"  |
| Exit condition(s)           | "enter your reponse here"  |
| Flow of events | "enter your reponse here"  |
| Alternative flow of events    | "enter your reponse here"  |
| Iteration #         | "enter your reponse here"  |

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


