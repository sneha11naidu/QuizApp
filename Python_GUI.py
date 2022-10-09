from tkinter import *
from functools import partial
import DBLayer

from tkinter import ttk
#



# It also creates a toplevel window, known as the root window, which serves as the main window of the application.
root = Tk()
# set the title
root.title('Quiz App')
# set the background color
root['bg'] = 'light blue'
root.geometry("1000x800")
# assume userID is 1
userID = 1
# Store the module ID and questions as global variables
selected_module_ID = 0
allQuestionsList = []
# A counter variable to show the question screen multiple times
counter = 0


# ====================================START=================================
class Python_GUI ()
    def save_selected_option(selected_ans_tuple):
    """ userID: The user identifier (primary key)
        moduleID: the selected module id
        questionID: for which question are we storing the selected ans
        selected_answerID: out of 4 options, which one was selected
        isCorrect: was the selected ans correct???"""

        local_user_id = userID
        local_module_id = selected_module_ID
        local_question_id = selected_ans_tuple[2]
        local_selected_answer_id = selected_ans_tuple[0]
        local_is_correct = selected_ans_tuple[3]

        str_show_selection = "You have selected option : " + str(selected_ans_tuple[1])
        label_show_selection = Label(root, text=str_show_selection, font=('Arial', 25), bg='light blue')
        label_show_selection.place(x=600, y=150)

        # finally call the DBLayer method that will save to database
        DBLayer.save_selected_answer(local_user_id, local_module_id, local_question_id, local_selected_answer_id,
                                     local_is_correct)


# ====================================end=================================


# ====================================START=================================
def show_final_score():
    print(" We need to show the final score")
    clear_main_page()

    # Get the results from DB layer
    results_tuple = DBLayer.calculate_score(userID, selected_module_ID)
    results_str_1 = "Your score is: " + str(results_tuple[0]) + " / " + str(results_tuple[1])
    label_results = Label(root, text=results_str_1, font=('Arial', 30), bg='light blue')
    label_results.place(x=300, y=50)

    percentage = (results_tuple[0]/results_tuple[1]) * 100
    percentage = round(percentage, 2)
    results_str_2 = "Your percentage is: " + str(percentage) + "%"
    label_percentage = Label(root, text=results_str_2, font=('Arial', 30), bg='light blue')
    label_percentage.place(x=300, y=100)

# ===========================================


def show_question():
    clear_main_page()
    # gets the list of questions for the selected moduleID
    global allQuestionsList
    global counter
    # stop if 5 questions have been shown
    if counter > 4:
        print("5 questions have been shown. Time to stop ")
        show_final_score()
        return

    if counter >= len(allQuestionsList):
        show_final_score()
        return

    counter = counter + 1  # increase the counter

    question_1_tuple = allQuestionsList[counter - 1]
    # Get answer options for question 1
    all_answer_options_list = DBLayer.get_potential_answers(question_1_tuple[0])
    ans_option_1_tuple = all_answer_options_list[0]
    ans_option_2_tuple = all_answer_options_list[1]
    ans_option_3_tuple = all_answer_options_list[2]
    ans_option_4_tuple = all_answer_options_list[3]

    # show the question as a label widget
    counter_str = str(counter) + ")."
    label_counter = Label(root, text=counter_str, font=('Arial', 30), bg='light blue')
    label_t = Label(root, text=question_1_tuple[1], font=('Arial', 30), bg='light blue')
    # position the label
    label_t.place(x=300, y=50)
    label_counter.place(x=200, y=50)

    #     show the four answer options as button widgets
    button1 = Button(root, text=ans_option_1_tuple[1], font=('Arial', 30),
                     command=partial(save_selected_option, ans_option_1_tuple))
    button1.place(x=600, y=300)
    button2 = Button(root, text=ans_option_2_tuple[1], font=('Arial', 30),
                     command=partial(save_selected_option, ans_option_2_tuple))
    button2.place(x=600, y=400)
    button3 = Button(root, text=ans_option_3_tuple[1], font=('Arial', 30),
                     command=partial(save_selected_option, ans_option_3_tuple))
    button3.place(x=600, y=500)
    button4 = Button(root, text=ans_option_4_tuple[1], font=('Arial', 30),
                     command=partial(save_selected_option, ans_option_4_tuple))
    button4.place(x=600, y=600)

    button_next = Button(root, text='Next', font=('Arial', 30), command=show_question)
    button_next.place(x=800, y=800)

    button_submit = Button(root, text='Submit', font=('Arial', 30), command=show_question)
    button_submit.place(x=1000, y=800)


# ====================================END=================================

def save_selected_module(module_tuple):
    # set the global
    global selected_module_ID
    selected_module_ID = module_tuple[0]  # Get the ID from the tuple
    print("selected module is :" + str(selected_module_ID))
    global allQuestionsList
    allQuestionsList = DBLayer.getQuestions(selected_module_ID)


# ====================================START=================================

def show_module_list():
    # destroy_login_screen()
    clear_main_page()
    module_list = DBLayer.getListOfModules()
    i = 0
    for module in module_list:
        module_tuple = module_list[i];
        button = Button(root, text=module_tuple, font=('Arial', 30),
                        activebackground='red', command=partial(save_selected_module, module_tuple))
        button.pack()

        i = i + 1

        button1 = Button(root, text='Next', font=('Arial', 30), command=show_question)
        button1.place(x=600, y=350)


# ====================================end=================================


# ====================================START=================================
def Opening_Screen():
    # global root, label_t, label1, entry1

    # we are creating a label widget under the parent 'root'
    label_t = Label(root, text='Quiz', font=('Arial', 50), bg='light blue')
    # position the label
    label_t.place(x=600, y=50)
    label1 = Label(root, text='Username', font=('Arial', 40), bg='light blue')
    label1.place(x=190, y=250)
    # Add a entry widget..which is a text box
    entry1 = Entry(root, font=('Arial', 30))
    entry1.place(x=500, y=250)
    label2 = Label(root, text='Password', font=('Arial', 40), bg='light blue')
    label2.place(x=190, y=350)
    entry2 = Entry(root, font=('Arial', 30))
    entry2.place(x=500, y=350)

    button1 = Button(root, text='SUBMIT', font=('Arial', 30), command=show_module_list)
    button1.place(x=600, y=450)


# ====================================end=================================

def clear_main_page():
    for widgets in root.winfo_children():
        widgets.destroy()


Opening_Screen()

# starts the GUI
root.mainloop()
