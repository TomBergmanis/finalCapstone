# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"
current_date = datetime.now().date()


# ========= create tasks.txt =========
# Creates tasks.txt if it doesn't exist

if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


# ========= create list of tasks ========= 
    
task_list = [] 

for t_str in task_data:
    curr_t = {} # dictionary created to store the values below. 

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = task_components[5]
    task_list.append(curr_t)

#  ========= Login Section ========= 
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
# Creates user.txt if it doesnt exist
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#  ========= Menu Section / Main Code ========= 

# function reg_user register a new user  when 'r' is chosen 

def reg_user(username_password):
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")

    while new_username in username_password.keys(): # uses a while loop to repeatedly ask the user to enter a new username 
        print("Username taken, please enter a unique username\n")
        new_username = input("New Username: ")
    # once the user has entered a valid username the program will then prompt the user to to enter a password
    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
    
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

# function add_task adds a new task to a username  when 'a' is chosen 
        
def add_task(task_list, username_password):
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")
 
    # Then get the current date.
    curr_date = date.today()
    
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": "No",
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                t['completed'], 
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


# function view_all shows all tasks assigned when 'va' is chosen 
# task_counter = 0


def view_all(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Task Complete: \t {t['completed']}\n"
        print(disp_str)

# function view_mine shows the specific tasks assigned to the username inputted when 'vm' is chosen 

def view_mine(task_list, curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling)
    '''

    while True:
        # gets the task infromation for the current user 
        user_tasks = [t for t in task_list if t['username'] == curr_user] 

        for i, task in enumerate(user_tasks, start=1):
            disp_str = f"Task: \t\t {task['title']}\n"
            disp_str += f"Task Number: \t {i}\n"
            disp_str += f"Assigned to: \t {task['username']}\n"
            disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {task['description']}\n"
            disp_str += f"Task Complete: \t {task['completed']}\n"
            print(disp_str)

# when the user selects a number it will print that task ... 
        try:
            select = int(input("Enter the number of the task you want to select/view (-1 to exit): ")) 
# currently numbers the task(s) corresponding to the position in the list created each time the vm is entered. 
            if select == -1: # if -1 is entered by the user, it will exit to the main menu. 
                break
            elif 1 <= select <= len(user_tasks): 
                selected_task = user_tasks[select - 1]
                print(f"\nSelected Task {select} Details:")
                print(f"  Title: {selected_task['title']}")
                print(f"  Assigned to: {selected_task['username']}")
                print(f"  Date Assigned: {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
                print(f"  Due Date: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
                print(f"  Task Description: {selected_task['description']}\n")
                print(f" Task Complete: {selected_task['completed']}\n")
                
             
                task_complete = input(f" Task Complete: Yes/ No? ").lower()

                selected_task['completed'] = "No" # defaults to "No" 

                # once the task has been selected, it will display that task in the terminal. 
                # below is the logic for the task complete feature in the program. 
                # if the task_complete = yes then marks it as complete
                if task_complete == "yes":
                    selected_task['completed'] = "Yes" # this will display if the user chooses to mark the task as complete. 

                    print(f"\ntask {select} has been marked as complete.")
                else: # if the task_complete = no then it marks it as incomplete and follows with a prompt to edit the task
                    selected_task['completed'] = "No" # the default for the task complete is "No" the user can also choose to mark it as not complete with "No".
                    if selected_task['completed'] == "No": # if the task is marked as not complete then the user can edit the task else the user cannot edit the task. 
                        edit_task = input(f"Do you want to edit this task? (Yes/No) ").lower()
                        if edit_task == "yes":
                            # Add logic to edit task details enables the user to reassign tasks and change the due date
                            new_username = input("Reassign the task to a new username: ")
                            new_due_date_time = input("Enter a new due date (YYYY-MM-DD): ")
                            selected_task['username'] = new_username
                            selected_task['due_date'] = datetime.strptime(new_due_date_time, DATETIME_STRING_FORMAT)
                            print(f"Task {select} has been edited.")
                        else:
                            print(f"Task {select} is not complete and has not been edited.")
                    else: # not sure if this is necassary as if the complete == "Yes" means it doesnt let you edit it. 
                        print(f"Task {select} is marked as complete and cannot be edited.") # potentially there to catch the possibility of getting through to edit a task if it is marked as complete.
            else:
                print("Invalid selection. Please enter a valid task number assigned to you.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# function generate_reports generates a report when 'gr' is chosen 
           
def generate_reports(task_list, current_date, username_password):
# when the user choose generate reports 'gr' => generate task_overview.txt and user_overview.txt.
    user_generated = input("Do you want to generate a report? (Yes/No): ").lower() # gets the user input for creating a report

    # place holders for the different statistics 
    overdue_tasks = 0 # number of overdue tasks
    completed_tasks = 0 # number of completed tasks
    incomplete_tasks = 0 # number of incomplete tasks 

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Task Complete: \t {t['completed']}\n"
        print(disp_str)

    # loops through the task_list to find if t['completed] == "Yes". this adds to the total of complete or incomplete tasks
    for t in task_list:
        if t['completed'] == "Yes":
            completed_tasks += 1
        else:
            incomplete_tasks += 1

    # converting the current date to match the t['due_date] format so it can compare.
    current_datetime = datetime.combine(current_date, datetime.min.time())

    for t in task_list:
        if current_datetime > t['due_date'] and t['completed'] == "No":
            """ this checks if the due date has expired and...
              also if the task has been marked as complete or not
            """
            overdue_tasks += 1
    # no need for an else statement as there is nothing to do if the if statement returns False. 

    total_tasks = len(task_list) # gets the total number of tasks created. 

    # if "" > 0 else 0 statement added to all percentage calculations to avoid division by zero errors. 
    incomplete_precentage = round((incomplete_tasks / len(task_list)) * 100, 2) if incomplete_tasks > 0 else 0 # percentage of incomplete tasks. 
    overdue_percentage = round((overdue_tasks / len(task_list)) * 100, 2) if overdue_tasks > 0 else 0 # percentage of overdue and incomplete tasks. 

    report_tasks = "---------- \t Task Overview Report \t ----------\n"
    report_tasks += f"\n|| \tTotal number of tasks: {(total_tasks)}" # gets the total number of tasks added to this program. 
    report_tasks += f"\n|| \tTotal completed tasks: {completed_tasks} " 
    report_tasks += f"\n|| \tTotal incomplete tasks: {incomplete_tasks}" 
    report_tasks += f"\n|| \tTotal overdue tasks: {overdue_tasks}"
    report_tasks += f"\n|| \tIncomplete tasks: {incomplete_precentage}%"
    report_tasks += f"\n|| \tOverdue tasks: {overdue_percentage}%"
    report_tasks += f"\n\nReport generated on: {datetime.now().date()}\n" # gets the date the report is due
    report_tasks += "-------------------------------------------------"

    total_users = len(user_data)
    
    user_task_counts = {}
    user_completed_task_counts = {}
    user_incomplete_task_counts = {}
    user_overdue_task = {}

    for t in task_list:
        assigned_user = t['username']
        if assigned_user not in user_task_counts: # this loop checks to see if the username is already in the user_task_counts dictionary. 
            # if the user is not already in the dictionary that means this is the first task assigned to that user. 
            user_task_counts[assigned_user] = 1 # initialises the count to 1 for the current task.
            # initialises the count for all the different counts below: 
            user_completed_task_counts[assigned_user] = 0 
            user_incomplete_task_counts[assigned_user] = 0
            user_overdue_task[assigned_user] = 0
        else:
            user_task_counts[assigned_user] += 1
        if t['completed'] == 'Yes': # checks to see if the current task has been marked as "Yes" i.e. complete. 
            user_completed_task_counts[assigned_user] += 1
        else:
            user_incomplete_task_counts[assigned_user] += 1

        if t['completed'] == "No" and current_datetime > t['due_date']:
            user_overdue_task[assigned_user] += 1

    
    user_report = "---------- \t User Overview Report \t ----------\n"
    user_report += f"\n Total number of users registered: {(total_users)}" # gets the total number of tasks added to this program. 
    user_report += f"\n Total number of tasks: {(total_tasks)}\n" # gets the total number of tasks added to this program. 
    # for each user:
    user_report += "\n============================================================\n"
    # the for loop below iterates over the task_list and finds the username, creating the list below. 
    for username, task_count in user_task_counts.items(): 
        # assigning variables to the dictionaries created outside the for loop. 
        completed_task_count = user_completed_task_counts[username]
        incompleted_task_count = user_incomplete_task_counts[username]
        user_overdue_task_count = user_overdue_task[username] 

        user_report += f"\n\n User: {username}" 
        user_report += f"\n Assigned Tasks: {task_count}" # total number of tasks assigned to the user
        user_percentage = round((task_count / total_tasks) * 100, 2) 
        user_report += f"\n Percentage of tasks assigned to user: {user_percentage}%" # percentage of total number of tasks assigned to the user 
        user_completed = round((completed_task_count / task_count) * 100, 2)
        user_report += f"\n Percentage of completed tasks: {user_completed}%"
       
        try:
            user_incomplete = round((incompleted_task_count / task_count) * 100, 2) if task_count > 0 else 0 
            # the if statement avoids an error warning if the user tries to generate a report when there are no tasks.
            user_report += f"\n Percentage of incomplete tasks: {user_incomplete}%" 
            overdue_user_percentage = round(user_overdue_task_count / (incompleted_task_count) * 100, 2) if incompleted_task_count > 0 else 0
            # the if statement avoids an error warning if the user tries to generate a report when there are no incompleted tasks.
            user_report += f"\n Percentage of incomplete and overdue tasks: {overdue_user_percentage}%"
        except ZeroDivisionError: # needed incase there is a 0, which would cause a zero division error to occur. 
            user_incomplete = None # if there is no overdue or incomplete tasks it will not appear in the report. 
            overdue_user_percentage = None   
        
        user_report += "\n\n============================================================\n\n" 
    # the below is taken out of the loop so that it only appears at the end of the reports generated. 
    user_report += f"\n\nReport generated on: {datetime.now().date()}\n" # gets the date the report is due
    user_report += "-------------------------------------------------"

# generates the report if the user inputs yes 
    if user_generated == 'yes':
            with open("task_overview.txt", "w") as task_overview_file:
                task_overview_file.writelines(report_tasks) # change variable from test to something else maybe task_report?   
            with open("user_overview.txt", "w") as user_overview_file:
                user_overview_file.writelines(user_report)
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

    print("Reports successfully generated.") # confirms to the user that the .txt files have been successfully created. 

# function display_statistics, displays all statistics when 'ds' is chosen 

def display_statistics(username_password, task_list, curr_user):
    ''' If the user is an admin they can display statistics about number of users
        and tasks.
        if user selects 'ds' the reports generated are read from task.txt and user.txt and displayed in the terminal.
        
    '''
    if curr_user == 'admin':
    # at the top of the program the user.txt file and task.txt file are both created if there is not one already in existance.
    # (within the directory).
        try:
            with open("tasks.txt", "r") as task_statistics:
                task_content = task_statistics.readlines()
            print("\n\nTask Statistics:\n")
            print(f"Total Number of tasks: {len(task_list)}\n")
            print("\n----------------------------------------\n")
            
            for line in task_content:
                line_parts = line.strip().split(';')
                # Print each part with appropriate formatting
                print("Name:", line_parts[0])
                print("Test:", line_parts[1])
                print("Description:", line_parts[2])
                print("Start Date:", line_parts[3])
                print("End Date:", line_parts[4])
                print("Completed:", line_parts[5])
                print("\n\n----------------------------------------\n")
                print("\n")  # Add a newline for better separation between entries

        except FileNotFoundError:
            print("The file does not exist.")
# seperate try and except loop incase user.txt exists but task.txt does not and vice versa. 
        count = 0
        try:
            with open("user.txt", "r") as user_statistics:
                user_content = user_statistics.readlines()

            print("User Statistics:\n")
            print(f"Number of users: {len(username_password.keys())}\t\t")
            print("\n----------------------------------------\n")
            for line in user_content:
                line_parts = line.strip().split(';')
                # Print each part with appropriate formatting
                count += 1 
                print(f"User Number: {count}")
                print("Username:", line_parts[0])
                print("Password:", line_parts[1])
                print("\n----------------------------------------")
                print("\n")  # Add a newline for better separation between entries

        except FileNotFoundError:
            print("The file does not exist.")
            # num_users = len(username_password.keys()) # total number of users
        # num_tasks = len(task_list) # gives the total number of tasks 
        # print("-----------------------------------")
        # print(f"Number of users: \t\t {num_users}")
        # print(f"Number of tasks: \t\t {num_tasks}")
        # print("-----------------------------------")    
    else: 
         print("You are not an admin")
            
# ======== ======== While Loop and if elif else statement ======== ========
    """ While loop kept the same but the if elif else statement changed to call each of the following functions when the user selects:
        'reg_user', 'add_task', 'view_all' and 'view_mine' the original statements were copied into functions that are called in the while loop below
    """

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()
    
# changed if elif else to call functions instead 
    if menu == 'r':
        reg_user(username_password)
    elif menu == 'a':
        add_task(task_list, username_password)
    elif menu == 'va':
        view_all(task_list)
    elif menu == 'vm':
        view_mine(task_list, curr_user = input("What is your username? : ")) # figure out a way to see your own individual tasks 
    # gr added to generate .txt files tasK_overview.txt and user.overview.txt
    elif menu == 'gr': 
        generate_reports(task_list, current_date, username_password)
# extra function created for displaying the statistics 
    elif menu == 'ds':
        display_statistics(username_password, task_list, curr_user = input("What is your username? : "))
# exits the menu
    elif menu == 'e':  
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")  
     
    
