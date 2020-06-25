import pymongo
import os
import sys
import re
from pprint import pprint

import inquirer
from inquirer import errors

sys.path.append(os.path.realpath('.'))


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]

mycol = db["students"] 



# for x in mycol.find({},{ "_id": 0, "name": 1, "surname": 1 }):
#     print(x)

operations = [
    inquirer.List('operation',
                  message="You have to perform operations on 'students' table. Which operation?",
                  choices=['Insert', 'Select', 'Update', 'Delete','Close'],
              ),
]

operation = inquirer.prompt(operations)

while operation.get('operation') != 'Close':
    
    if operation.get('operation') == 'Insert':
        table_fields = [
            inquirer.Text('name',
                        message="Input student's name"),
            inquirer.Text('surname',
                        message="Input student's surname "),
        ]

        answers = inquirer.prompt(table_fields)
        x = mycol.insert_one(answers)

    elif operation.get('operation') == 'Select':
        question = [
            inquirer.List('operation',
                        message="What do you want to get from database? ",
                        choices=['First student', 'All students', 'Filter'],
                    ),
        ]

        select_operation = inquirer.prompt(question)

        if select_operation.get('operation') == 'First student':
            x = mycol.find_one()
            print(x)

        elif select_operation.get('operation') == 'All students':
            for x in mycol.find({},{ "_id": 0, "name": 1, "surname": 1 }):
                print(x)

        elif select_operation.get('operation') == 'Filter':
            question = [
                inquirer.List('filter',
                            message="Filter by",
                            choices=['Student name', 'Student surname'],
                        ),
            ]

            filter_by = inquirer.prompt(question)

            if filter_by.get('filter') == 'Student name':
                print('work')
                questions = [
                    inquirer.Text('name',
                                message="Input student's name for filtering"),
                ]

                answers = inquirer.prompt(questions)
                mydoc = mycol.find(answers)
                for x in mydoc:
                    print(x)
            else:
                questions = [
                    inquirer.Text('surname',
                                message="Input student's surname for to filter"),
                ]

                answers = inquirer.prompt(questions)
                mydoc = mycol.find(answers)
                for x in mydoc:
                    print(x)

    elif operation.get('operation') == 'Delete':
        question = [
                inquirer.List('operation',
                            message="Select delete option : ",
                            choices=['Delete one', 'Delete all'],
                        ),
            ]

        delete_operation = inquirer.prompt(question)

        if delete_operation.get('operation') == 'Delete one':
            question = [
                inquirer.List('delete',
                            message="Delete by",
                            choices=['Student name', 'Student surname'],
                        ),
            ]
            
            delete_by = inquirer.prompt(question)

            if delete_by.get('delete') == 'Student name':
                questions = [
                    inquirer.Text('name',
                                message="Input student's name for deleting"),
                ]

                answers = inquirer.prompt(questions)
                mycol.delete_one(answers)
            
            else:
                questions = [
                    inquirer.Text('name',
                                message="Input student's surname for deleting"),
                ]

                answers = inquirer.prompt(questions)
                mycol.delete_one(answers)
        
        elif delete_operation.get('operation') == 'Delete all':
            x = mycol.delete_many({})
            print(x.deleted_count, " documents deleted.")

    elif operation.get('operation') == 'Update':
        question = [
                inquirer.List('operation',
                            message="Select update option : ",
                            choices=['Update only one student', 'Update many students '],
                        ),
            ]

        update_operation = inquirer.prompt(question)

        if update_operation.get('operation') == 'Update only one student':
            question = [
                inquirer.List('update',
                            message="Input student's name or surname for updating",
                            choices=['Student name', 'Student surname'],
                        ),
            ]
            
            update_by = inquirer.prompt(question)

            if update_by.get('update') == 'Student name':
                questions = [
                    inquirer.Text('name',
                                message="Input student's name for updating"),
                ]

                old_student = inquirer.prompt(questions)

                questions = [
                    inquirer.Text('name',
                                message="Input student's new name"),
                ]

                new_student = inquirer.prompt(questions)
                newvalues = { "$set": new_student }
                mycol.update_one(old_student, newvalues)
            
            else:
                questions = [
                    inquirer.Text('surname',
                                message="Input student's surname for updating"),
                ]

                old_student = inquirer.prompt(questions)

                questions = [
                    inquirer.Text('name',
                                message="Input student's new surname"),
                ]

                new_student = inquirer.prompt(questions)
                newvalues = { "$set": new_student }
                mycol.update_one(old_student, newvalues)

    operations = [
        inquirer.List('operation',
                    message="Do you want to continue to perform operations on 'students' table. Which operation?",
                    choices=['Insert', 'Select', 'Update', 'Delete','Close'],
                ),
    ]

    operation = inquirer.prompt(operations)
