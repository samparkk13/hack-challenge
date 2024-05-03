# OpenAPI Specification
## Overview of App

***

This backend application is modeled after a to-do list of tasks, which helps us keep track of different items we need to do / check off. For the backend, we separate to-do tasks by their categories (such as education, sports, etc), and we implement 4 routes in order to either get all categories, create a category, delete a category, and add a task (to-do) to a category. 
Our database models include a Todo model and a Category model, and there is a one-to-many relationship between the category model and the todo model, since a category can be linked to multiple Todo tasks and a Todo task can only be linked to one category. 

## **Get all categories**
 **GET** api/categories/

###### Response
 ```yaml
 {
     "id": <ID>,
     "title": <USER INPUT FOR CATEGORY NAME>,
     "todo": {
         "id": <ID>,
         "title": <USER INPUT FOR TODO TITLE>,
         "dueDate": <USER INPUT FOR DUE DATE>,
     }
 }
```

## **Create a category**
 **POST** /api/categories/
 ###### Request
 ```yaml
 {
     "title": <USER INPUT>    
 }
```
###### Response
 ```yaml
 {
     "id": <ID>,
     "title": <USER INPUT FOR CATEGORY NAME>,
     "todo": {
         "id": [],
         "title": [],
         "dueDate": [],
     }
 }
```

## **Delete a specific category**
 **DELETE** /api/categories/{id}/
###### Response
 ```yaml
 {
     "id": <ID>,
     "title": <USER INPUT FOR CATEGORY NAME>,
     "todo": {
         "id": [],
         "title": [],
         "dueDate": [],
     }
 }
```

## **Create a Todo task for a Category**
 **POST** /api/todos/{id}/create/
  ###### Request
```yaml
 {
     "title": <USER INPUT FOR TITLE>,
     "due_date": <USER INPUT FOR due_date>,
 }
```
 ###### Response
 ```yaml
 {
     "id": <ID>,
     "title": <USER INPUT FOR TITLE>,
     "due_date": <USER INPUT FOR DUE DATE>,
     "category": <USER INPUT FOR CATEGORY BASED OFF OF ID>,
 }
```