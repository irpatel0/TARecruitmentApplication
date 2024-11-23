# Project Group Report - 1

## Team: `Alpha`

List team members and their GitHub usernames

* `Sai Teja Sunku`,`ssunku6`
* `Achintya Sanjay`,`asanjay3`
* `Ishaan Patel`,`irpatel0`
* `Jake Grier`,`JDGrier`

---
**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

----
## 1. Schedule

 Monday, Wednesday, Thursday at 5PM and meeting lasts until required

----
## 2. Iteration 1 - Summary

#### Summary of Iteration1
- Implemented the registration and login/logout for students and instructors
- Implemented restrictions for pages that students and instructors could access
- Created models for the following: User, Student, Instructor, Course, Course Section, and Position
- Used inheritance between User and Student/Instructor
- Created an association table between student and course, for courses that the student has taught for
- Displayed open positions on the student page
- Made a create course section form for instructors
- Made a create position form for instructors
- Displayed courses sections on the instructor page

#### Completed User Stories
1. As a Student, I want to be able to login to the site so that I can use the site [Email & Password] - Sai Teja Sunku, Achintya Sanjay
2. As a Professor, I want to be able to login to the site so that I can use the site [Email & Password] - Sai Teja Sunku, Achintya Sanjay
3. As a Professor, I want to create course sections so that students can view the course information - Ishaan Patel, Jake Grier
4. As a Professor, I want to create SA positions for a particular course so that students can apply for a particular course - Ishaan Patel, Jake Grier




----
## 3. Iteration 1 - Sprint Retrospective

 The scrum retrospective meetings were efficient and allowed us to effectively communicate what was going well and what needed improvement on the project. Typically in our scrum retrospective meetings, we delegate the work amongst team members for the upcoming scrum, and create subgroups if necessary. We also discussed any bugs that needed to be resolved and any improvements to be made to the project. During the scrum meetings, we also discuss strategies to implement complex tasks, such as creating databases, models, and relationships. 
 Going forward, we want to utilize GitHub issues to track and report issues that need to be resolved, and any use cases or tasks that have been completed. This will help us to better understand where the team and the project is currently at and what needs improvement.
 
----
## 4. Product Backlog refinement

 No, we did not make any changes to the product backlog during iteration1.

----
## 5. Iteration 2 - Sprint Backlog

#### User Stories
1. As a Student, I want to view all the details of every open SA position so that I know if I can meet the qualifications - Sai Teja Sunku, Achintya Sanjay
2. As a Student, I want to apply for the open SA positions - Ishaan Patel, Jake Grier
3. As a Professor, I want to view all students applied for a SA position - Sai Teja Sunku, Achintya Sanjay

#### Smaller Stories
1. [Database Model] Implement the Application model - Ishaan Patel, Jake Grier
2. [Database Model] Create One-to-Many relationship between "Student" model and "Application" model - Ishaan Patel, Jake Grier
3. [Database Model] Create One-to-Many relationship between Application and Position - Ishaan Patel, Jake Grier
4. [Database Model] Update Student model to have an "assigned" boolean field - Sai Teja Sunku, Achintya Sanjay
5. [Implementation] Develop a form to apply for the selected open SA position - Ishaan Patel
6. [Implementation] Develop a route to view all students applied for each SA position created - Sai Teja Sunku, Achintya Sanjay
7. [Implementation] Develop a route and a view to see details of every open SA position - Sai Teja Sunku, Achintya Sanjay
8. [Testing] Create unit tests for routes - Sai Teja Sunku, Achintya Sanjay
9. [Testing] Create unit tests for new models - Sai Teja Sunku, Achintya Sanjay

