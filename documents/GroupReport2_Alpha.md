# Project Group Report - 2

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
## 1. Iteration 2 - Summary

 * Include a summary of your `Iteration-2` accomplishments. 
 * Implemented apply feature for students to apply for open positions, and they can apply for each position only once. If already applied, the status of their application is displayed.
 * Implemented viewing applications feature where instructors can view all the applications applied for the position created by them. The table also displays if the student is assigned or unassigned and assignment disables if already assigned.
 * The instructor can also view student details from the applications table.
 * The student can view the open positions and its details
 * Created the applications table with relationships to Student and Position tables
 * Extra credit - Implemented edit profile feature for students and instructors
 * List the user stories completed in `Iteration-2`. Mention who worked on those user stories. 
 * As a Professor, I want to view all students applied for a SA position - Sai Teja Sunku, Achintya Sanjay
 * As a Student, I want to apply for the open SA positions - Ishaan Patel, Jake Grier
 * As a Student, I want to view all open SA positions so that I decide which ones I am interested in - Jake Grier
 * As a Student, I want to view all the details of every open SA position so that I know if I can meet the qualifications - Sai Teja Sunku, Achintya Sanjay

----
## 2. Iteration 2 - Sprint Retrospective

 * Include the outcome of your `Iteration-2 Scrum retrospective meetings`. 
 * Mention the changes the team will be doing to improve itself as a result of the Scrum reflections.

----
## 3. Product Backlog refinement

 * Have you made any changes to your `product backlog` after `Iteration-2`? If so, please explain the changes here. 

----
## 4. Iteration 3 - Sprint Backlog

#### User Stories
1. As a Student, I want to be able to login to the site so that I can use the site(SSO) - Sai Teja Sunku, Achintya Sanjay
2. As a Professor, I want to be able to login to the site so that I can use the site(SSO) - Sai Teja Sunku, Achintya Sanjay
3. As a Student, I want to be recommended SA Positions that match my profile - Jake Grier, Ishaan Patel
4. As a Student, I want to check the status of my applications so that I know which of my applications have been approved, rejected, or are still pending. - Jake Grier, Ishaan Patel
5. As A Student, I want to withdraw pending applications so that I'm not in the system for positions I'm no longer interested in. - Jake Grier, Ishaan Patel
6. As a Professor, I want to add a student to the SA position so that I can register students who haven't been assigned a position. - Sai Teja Sunku, Achintya Sanjay
#### Tasks
1. [Implementation] Create logic to mark the course section as closed if number of SAs required if fulfilled - Sai Teja Sunku, Achintya Sanjay
2. [Implementation] Develop a route for switching the sort category - Jake Grier, Ishaan Patel
3. [Implementation] Display all assigned students on instructor page - Sai Teja Sunku, Achintya Sanjay
4. [Implementation] Develop a route for students withdrawing an application - Jake Grier, Ishaan Patel
5. [Implementation] Develop route to assign a position to a student - Sai Teja Sunku, Achintya Sanjay
6. Add notes to the course positions, so students can see criteria that they meet at a glance - Jake Grier, Ishaan Patel
7. [Implementation] Create logic to use Azure SSO for login and signup - Sai Teja Sunku, Achintya Sanjay
8. Develop an algorithm to produce a weighted score for each position, based on student information - Jake Grier, Ishaan Patel
9. [Database Model] Create One-to-Many relationship between "Student" model and "SA Position" model for assigned courses - Sai Teja Sunku, Achintya Sanjay