import sqlite3, datetime, bcrypt, getpass, csv
from index import user_profile,get_comp_info, get_assess_info, get_assr_info, gen_update
from utility import print_compass_ids, get_edit_input, print_user_select, print_assr_ids

connection = sqlite3.connect("capstone.db")
cursor = connection.cursor()
dt = datetime.datetime.now().replace(microsecond=0)

class User:
    def __init__(self, email, password, first_name, last_name, phone, hire_date, date_created, user_type):
        self.phone = phone
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_type = user_type
        self.hire_date = hire_date
        self.date_created = date_created

    def user_menu(id, email, first_name, last_name, cursor):
        while True:
            nav = input('\n[1] View Competency Report\n[2] View Assessment Data\n[3] Edit Your Profile\n[Q] Logout\n>>> ')
            if nav.lower() == 'q':
                logout_user()
                break
            elif int(nav) == 1:
                user_competency(id, email, first_name, last_name, cursor)
            elif int(nav) == 2:
                user_assessments(id, email, first_name, last_name, cursor)
            elif int(nav) == 3:
                edit_user_info(id)
            else:
                print("Invalid input, try again.")

class Manager(User):
    def __init__(self, email, password, first_name, last_name, phone, hire_date, date_created):
        super().__init__(email, password, first_name, last_name, phone, hire_date, date_created, 'manager')
        
    def manager_menu():
        while True:
            nav = input('\n--- MAIN MENU ---\n\n[1] Access User Terminal\n[2] Manage Competencies & Assessments\n[Q] Logout\n>>> ')
            if nav.lower() == 'q':
                logout_user()
                break
            elif int(nav) == 1:
                user_terminal()
            elif int(nav) == 2:
                compass()
            else:
                print("Invalid input, try again.")
    
def hash_password(password):
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return password               
def check_password(password,stored_hash):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

def user_terminal():
    while True:
        nav = input('\n--- USER TERMINAL ---\n\n[1] View Users\n[2] Add New User\n[3] Edit User Info\n[Q] Quit\n>>> ')
        if nav.lower() == 'q':
            break
        elif int(nav) == 1:
            check = input("\nSearch for a particular user? (Y/N)\n>>> ")
            if check.lower() == 'y':
                search_user()
            else:
                view_all = cursor.execute("SELECT user_id, email, first_name, last_name FROM Users").fetchall()
                ids = print_user_select(view_all)
                view_users(ids)
        elif int(nav) == 2:
            register_user()
        elif int(nav) == 3:
            view_all = cursor.execute("SELECT user_id, email, first_name, last_name FROM Users").fetchall()
            ids = print_user_select(view_all)
            while True:
                id = int(input("Enter Valid User ID: "))
                if id in ids:
                    edit_user_info(id)
                    break
                print("Invalid input, try again.")
        else:
            print("Invalid input, try again.")

def compass():
    while True:
        nav = input("\n--- COMPETENCY & ASSESSMENT MENU ---\n\n[1] Manage Competency Reports\n[2] Manage Assessments\n[3] Gradebook\n[Q] Quit\n>>> ")
        if nav.lower() == 'q':
            break
        elif int(nav) == 1:
            while True:
                nav = input("\n--- COMPETENCY MENU ---\n\n[1] Add Competency\n[2] Edit Competency\n[3] View Universal Competency Report\n[Q] Quit\n>>> ")
                if nav.lower() == 'q':
                    break
                elif int(nav) == 1:
                    add_comp()
                elif int(nav) == 2:
                    edit_comp()
                elif int(nav) == 3:
                    uni_comp_report()
                else:
                    print("Invalid input, try again.")
        elif int(nav) == 2:
            while True:
                nav = input("\n--- ASSESSMENT MENU ---\n\n[1] Add Assessment\n[2] Edit Assessment\n[Q] Quit\n>>> ")
                if nav.lower() == 'q':
                    break
                elif int(nav) == 1:
                    add_assess()
                elif int(nav) == 2:
                    edit_assess()
                else:
                    print("Invalid input, try again.")
        elif int(nav) == 3:
            while True:
                user_info = cursor.execute('SELECT user_id, email, first_name, last_name FROM Users').fetchall()
                nav = input("\n--- GRADEBOOK ---\n\n[1] Add Assessment Result\n[2] Edit Assessment Result\n[3] Delete Assessment Result\n[4] Import Results from CSV\n[Q] Quit\n>>> ")
                if nav.lower() == 'q':
                    break
                ids = print_user_select(user_info)
                nav_id = int(input("Select which User ID's Results to affect: "))
                try:
                    if nav_id in ids:
                        if int(nav) == 1:
                            add_assr(nav_id)
                        elif int(nav) == 2:
                            edit_assr(nav_id)
                        elif int(nav) == 3:
                            del_assr(nav_id)
                        elif int(nav) == 4:
                            file = input("Enter the CSV file name to import from: ")
                            import_assr(file)
                        else:
                            print("Invalid input.")
                except Exception as e:
                    print(f'An error occurred: {e}')
                    return None

def user_assessments(id, email, first_name, last_name, cursor):
    headers = ["result_id", "title", "score", "date_taken"]
    try:
        query = "SELECT ar.result_id, a.title, ar.score, ar.date_taken FROM Assessment_Results ar JOIN Assessments a ON ar.assessment_id = a.assessment_id WHERE user_id = ?"
        rows = cursor.execute(query, (id,)).fetchall()
        ids = []
        name = " ".join([first_name, last_name])
        print(f'\n{"---- ASSESSMENT SUMMARY ----":>37}\n\nName:  {name}\nEmail: {email}\nAssessments Taken:')
        print(f'{"ID":<4} {"Title":<30} {"Score":<5} {"Date Taken"}')
        for row in rows:
            ids.append(row[0])
            print(f'{row[0]:<4} {row[1]:<30} {row[2]:<5} {row[3]}')
        report = input("Would you like to export this report to a CSV? (Y/N): ")
        if report.lower() == 'y':
            try:
                file = input("Enter the CSV file name to export to: ")
                export_report(headers, rows, file)
            except Exception as e:
                print(f'An error occurred: {e}')
                return None
        
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def user_competency(id, email, first_name, last_name, cursor):
    headers = ["competency_id", "name", "max_score", "avg_score"]
    try:
        comp_query = '''SELECT c.competency_id, c.name, COALESCE(MAX(ar.score), 0) AS max_score, AVG(COALESCE(ar.score, 0)) AS avg_score 
                        FROM Competencies c 
                        LEFT JOIN Assessments a ON c.competency_id = a.competency_id
                        LEFT JOIN Assessment_Results ar ON a.assessment_id = ar.assessment_id AND ar.user_id = ?
                        GROUP BY c.competency_id, c.name;
                        '''
        rows = cursor.execute(comp_query, (id,)).fetchall()
        name = " ".join([first_name, last_name])
        print(f'\n{"---- COMPETENCY SUMMARY ----":>37}\n')
        print(f'Name:  {name}\nEmail: {email}')
        print(f"\n{'ID':<4} {'Competency Name':<35} {'Score'}")
        total_score = []
        count = 0
        for row in rows:
            count += 1
            total_score.append(int(row[2]))
            print(f'{row[0]:<4} {row[1]:<39} {row[2]}')
        if count >0:    
            avg_comp_score = sum(total_score)/count
            print(f"\n{first_name}'s average competency score: {avg_comp_score}")
            report = input("Would you like to export this report to a CSV? (Y/N): ")
            if report.lower() == 'y':
                try:
                    file = input("Enter the CSV file name to export to: ")
                    export_report(headers, rows, file)
                except Exception as e:
                    print(f'An error occurred: {e}')
                    return None
        else:
            print(f"It appears {first_name} has not earned any competencies so far.")
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def search_user():
    while True:
        try:
            query = input("Search for user: ")
            search_query = '%'+ query +'%'
            searches = (search_query, search_query)
            print('\n--- USERS ---')
            query = "SELECT user_id, email, first_name, last_name FROM Users WHERE first_name LIKE ? or last_name LIKE ?"
            rows = cursor.execute(query, searches).fetchall();
            search_ids = print_user_select(rows)
            view_users(search_ids)
            break
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

def view_users(ids):
    while True:
        nav = input("\n[1] View Individual User Competency Summary\n[2] View Individual User Assessment Results\n[Q] Quit\n>>> ")
        if nav.lower() == 'q':
            break
        id = int(input("Enter Valid User ID: "))
        if id in ids:
            if int(nav) == 1:
                handle_return_reports(id,1)
                break
            elif int(nav) == 2:
                handle_return_reports(id,2)
                break
            print("Invalid input, try again.")
        print("Invalid input, try again.")

def uni_comp_report():
    while True:
        comps = cursor.execute("SELECT competency_id, name FROM Competencies").fetchall()
        ids = print_compass_ids(comps, "Competency")
        nav = input("\nEnter Competency ID to generate report: ")
        if int(nav) in ids:
            name = cursor.execute("SELECT name FROM Competencies WHERE competency_id = ?", (nav,)).fetchone()
            name = name[0]
            generate_uni_comp_report(nav, name)
            break
        print("Invalid input.")

def register_user():
    print('\n--- NEW USER ---\n')
    email = input(f"{'Email (Login)':<10}: ")
    password = input(f"{'Password':<10}: ")
    password = hash_password(password)
    first_name = input(f"{'First Name':<10}: ")
    last_name = input(f"{'Last Name':<10}: ")
    phone = input(f"{'Phone':<10}: ")
    hire_date = input(f"{'Date of Hire':<10}: ")
    user_type = input(f"{'Manager [Y/N]':<10}: ")
    if user_type.lower() == 'n':
        user = User(email, password, first_name, last_name, phone, hire_date, dt, 'user')
    elif user_type.lower() == 'y':
        user = Manager(email, password, first_name, last_name, phone, hire_date, dt)
    try:
        query = 'INSERT INTO Users (email, password, first_name, last_name, phone, hire_date, date_created, user_type) VALUES (?,?,?,?,?,?,?,?)'
        vals = (user.email, user.password, user.first_name, user.last_name, user.phone, user.hire_date, user.date_created, user.user_type)
        cursor.execute(query, vals)
        connection.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("User already exists.")

def add_comp():
    name = input("\nCompetency Name: ")
    description = input("Description: ")
    vals = (name, description)
    cursor.execute("INSERT INTO Competencies (name, description) VALUES (?,?)", vals)
    connection.commit()
    print("Competency successfully added!")

def add_assess():
    title = input("Assessment Title: ")
    comps = cursor.execute("SELECT competency_id, name FROM Competencies").fetchall()
    ids = print_compass_ids(comps, "Competency")
    add_to_comp = input("Select the Competency ID to attach this assessment to: ")
    vals = (title, int(add_to_comp), dt)
    try:
        if int(add_to_comp) in ids:
            cursor.execute('INSERT INTO Assessments (title, competency_id, date_created) VALUES (?,?,?)', vals)
            connection.commit()
        else:
            print("Sorry, that was an invalid Competency ID.")
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def add_assr(stud_id):
    while True:
        assess = cursor.execute("SELECT assessment_id, title FROM Assessments").fetchall()
        user = cursor.execute("SELECT first_name FROM Users WHERE user_id = ?", (stud_id,)).fetchone()
        name = user[0]
        get_ids = print_compass_ids(assess, "Assessment")
        nav = int(input("Select the Assessment ID to attach this score to: "))
        score = int(input(f"Enter {name}'s score (0-4): "))
        while score > 4 or score < 0:
            score = int(input(f"Invalid score. Please enter {name}'s score (0-4): "))
        manager = input(f"Was this assessment proctored? (Y/N): ")
        if nav in get_ids:
            handle_new_assr(stud_id, nav, manager, score)
            break
        print("Input was invalid, try again.")

def edit_user_info(id):
    while True:
        user_profile(id)
        edit = input("Which field would you like to change?\nOr [Q] to Quit\n>>> ")
        try:
            if edit.lower() == 'q':
                break
            elif int(edit) == 1:
                vals = get_edit_input(id, "Enter first name:")
                gen_update("Users", "first_name", "user_id", vals)
            elif int(edit) == 2:
                vals = get_edit_input(id, "Enter last name:")
                gen_update("Users", "last_name", "user_id", vals)
            elif int(edit) == 3:
                vals = get_edit_input(id, "Enter new email:")
                gen_update("Users", "email", "user_id", vals)
            elif int(edit) == 4:
                password = input("Enter new password: ")
                hashed = hash_password(password)
                vals = (hashed, id)
                gen_update("Users", "password", "user_id", vals)
            elif int(edit) == 5:
                vals = get_edit_input(id, "Enter new phone:")
                gen_update("Users", "phone", "user_id", vals)
            else:
                print("Invalid input.")
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

def edit_comp():
    while True:
        get_info = cursor.execute("SELECT competency_id, name FROM Competencies").fetchall()
        ids = print_compass_ids(get_info, "Competency")
        nav = input("\nEnter the ID of the Competency to edit\n[Q] Quit\n>>> ")
        if nav.lower() == 'q':
            break
        if int(nav) in ids:
            handle_comp_edits(nav)
            break
        print("Input was invalid, try again.")

def edit_assess():
    while True:
        get_info = cursor.execute("SELECT assessment_id, title FROM Assessments").fetchall()
        ids = print_compass_ids(get_info, "Assessment")
        nav = input("\nEnter the ID of the Assessment to edit\n[Q] Quit\n>>> ")
        if nav.lower() == 'q':
            break
        if int(nav) in ids:
            handle_assess_edits(nav)
            break    
        print("Invalid input, try again.")

def edit_assr(stud_id):
    while True:
        assr = cursor.execute("SELECT ar.result_id, a.title, ar.score, ar.date_taken FROM Assessment_Results ar JOIN Assessments a ON ar.assessment_id = a.assessment_id WHERE user_id = ?", (stud_id,)).fetchall()
        ids = print_assr_ids(assr)
        nav = input("\nEnter the Result ID of the Assessment Result you'd like to edit\nOr [Q] to Return to Gradebook\n>>> ")
        if nav.lower() == 'q':
            break
        if int(nav) in ids:
            handle_assr_edits(nav)
            break
        print("Input was invalid, try again.")

def del_assr(stud_id):
    while True:
        assr = cursor.execute("SELECT ar.result_id, a.title, ar.score, ar.date_taken FROM Assessment_Results ar JOIN Assessments a ON ar.assessment_id = a.assessment_id WHERE user_id = ?", (stud_id,)).fetchall()
        ids = print_assr_ids(assr)
        nav = input("Enter the Result ID of the Assessment Result you'd like to Delete\nOr [Q] to Return to Gradebookn\n>>> ")
        if nav.lower() == 'q':
            break
        if int(nav) in ids:
            check = input("\nWARNING: This will permanently remove this record from the database. Are you sure you want to proceed? (Y/N)\n>>> ")
            if check == 'y':
                cursor.execute("DELETE FROM Assessment_Results WHERE result_id = ?", (nav,))
                connection.commit()
                print("Success! This Assessment Result has been successfully removed from the database.")
                break
            else:
                print("Record not removed. Returning to the Gradebook Menu.")
                break

def handle_return_reports(id, report_num):
    try:
        user_info = cursor.execute("SELECT email, first_name, last_name FROM Users WHERE user_id = ?",(id,)).fetchone()
        email = user_info[0]
        first_name = user_info[1]
        last_name = user_info[2]
        if report_num == 1:
            user_competency(id, email, first_name, last_name, cursor)
        elif report_num == 2:
            user_assessments(id, email, first_name, last_name, cursor)
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def handle_new_assr(stud_id, nav, manager, score):
    try:
        if manager.lower() == 'y':
            val = 'manager'
            query = cursor.execute("SELECT user_id, email, first_name, last_name FROM Users WHERE user_type = ?", (val,))
            proc_ids = print_user_select(query)
            proctor = input("Select Proctor ID: ")
            if int(proctor) in proc_ids:
                vals = (stud_id, nav, score, dt, int(proctor))
                cursor.execute('INSERT INTO Assessment_Results (user_id, assessment_id, score, date_taken, manager_id) VALUES (?,?,?,?,?)', vals)
                connection.commit()
            else:
                print("Sorry, that was an invalid Proctor ID.")
        elif manager.lower() == 'n':
            vals = (stud_id, nav, score, dt)
            cursor.execute('INSERT INTO Assessment_Results (user_id, assessment_id, score, date_taken) VALUES (?,?,?,?)', vals)
            connection.commit()
        else:
            print("Sorry, that was an invalid input.")
    
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def handle_comp_edits(nav):
    get_comp_info(nav)
    edit = int(input("Which field would you like to change?\n>>> "))
    try:
        if edit == 1:
            vals = get_edit_input(nav, "Enter new name:")
            gen_update("Competencies", "name", "competency_id", vals)
        elif edit == 2:
            vals = get_edit_input(nav, "Enter new description:")
            gen_update("Competencies", "description", "competency_id", vals)
        else:
            print("Invalid input.")
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def handle_assess_edits(nav):
    get_assess_info(nav)
    edit = int(input("Which field would you like to change?\n>>> "))
    try:
        if edit == 1:
            vals = get_edit_input(nav, "Enter new title:")
            gen_update("Assessments", "title", "assessment_id", vals)
        elif edit == 2:
            comps = cursor.execute("SELECT competency_id, name FROM Competencies").fetchall()
            print_compass_ids(comps, "Competency")
            hold = get_edit_input(nav, "Select the Competency ID to attach this assessment to:")
            vals = (int(hold[0]), nav)
            gen_update("Assessments", "competency_id", "assessment_id", vals)
        else:
            print("Invalid input.")
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def handle_assr_edits(nav):
    get_assr_info(nav)
    edit = input("Would you like to change the score? (Y/N)\n>>> ").lower().strip()
    try:
        if edit == 'y':
            vals = get_edit_input(nav, "Enter new score:")
            gen_update("Assessment_Results", "score", "result_id", vals)
        elif edit == 'n':
            print("\nReturning to Gradebook Menu.")
        else:
            print("Invalid input.")
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def generate_uni_comp_report(nav, name):
    taken_query = '''SELECT u.user_id, u.first_name, u.last_name,
                    COALESCE(MAX(CASE WHEN a.competency_id = ? THEN ar.score ELSE NULL END), 0) AS max_score,  
                    COALESCE(MAX(CASE WHEN a.competency_id = ? THEN ar.date_taken ELSE NULL END), 'Not Taken') AS date_taken,
                    COALESCE(MAX(CASE WHEN a.competency_id = ? THEN a.title ELSE NULL END), 'No Assessment') AS assessment_title
                    FROM Users u
                    LEFT JOIN Assessment_Results ar ON u.user_id = ar.user_id
                    LEFT JOIN Assessments a ON ar.assessment_id = a.assessment_id
                    GROUP BY u.user_id, u.first_name, u.last_name
                    ORDER BY u.user_id;
                    '''
    vals = (nav, nav, nav)
    rows = cursor.execute(taken_query, vals).fetchall()
    print(rows)
    print(f'\n{"---- UNIVERSAL COMPETENCY REPORT ----":>60}\n\nCompetency: {name}\n{"User ID":<8} {"Name":<24} {"Assessment":<30} {"Score":<5} {"Date Taken"}')
    total_score = []
    count = 0
    for row in rows:
        count += 1
        total_score.append(int(row[3]))
        print(f'{row[0]:>7}  {row[1]:<9} {row[2]:<14} {row[5]:<30} {row[3]:<5} {row[4]}')
    try:
        if count >0:    
            avg_comp_score = sum(total_score)/count
            print(f"\nAVG Competency Score across All Users: {avg_comp_score}")
    except Exception as e:
        print(f"An error occured: {e}")
        return None

def import_assr(file):
    with open(f'{file}','r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        results = []
        for lines in csvfile:
            results.append(lines.strip().split(','))
    for item in results:
        try:
            vals = (item[0], item[1], item[2], item[3])
            cursor.execute("INSERT INTO Assessment_Results (user_id, assessment_id, score, date_taken) VALUES (?,?,?,?)", vals)
            connection.commit()
        except Exception as e:
            print(f'An error occured: {e}')
            return None

def export_report(headers, result_set, file):
    with open(f'{file}', 'w', newline = '') as outfile:
        wrt = csv.writer(outfile)
        wrt.writerow(headers)
        for row in result_set:
            cleaned_row = [str(field).strip() for field in row]
            wrt.writerow(cleaned_row)

def login_user(email, password):
    try:
        cursor.execute('SELECT user_id, first_name, last_name, password, user_type FROM Users WHERE email = ?', (email,))
        result = cursor.fetchone()
        if result:
            stored_password = result[3]
            id = result[0]
            first_name = result[1]
            last_name = result[2]
            if check_password(password, stored_password):
                print("Login successful!")
                if result[4] == 'manager':
                    Manager.manager_menu()
                else:
                    User.user_menu(id, email, first_name, last_name, cursor)
                return User
            else:
                print("Invalid password.")
                return None
        else:
            print("Username not found.")
            return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def logout_user():
    print("User logged out successfully!")

def main():
    while True:
        print("\n---- COMPETENCY TRACKING DATABASE ----\n")
        action = input("\n[1] Login\n[Q] Quit\n>>> ").strip()

        if action.lower() == 'q':
            print("Exiting the application.")
            break
        elif int(action) == 1:
            username = input("Enter email to login: ")
            password = getpass.getpass("Enter password: ")
            login_user(username, password)
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()

