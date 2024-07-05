# Importing the libraries
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import webbrowser
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, _tree
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageFilter

# Importing the dataset
training_dataset = pd.read_csv('Training.csv')
test_dataset = pd.read_csv('Testing.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:132].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Implementing the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols     = training_dataset.columns
cols     = cols[:-1]

# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

# Implementing the Visual Tree
from sklearn.tree import _tree

# Implementing the HyperlinkManager class
class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# Function to handle tree traversal and diagnosis
def print_disease(node):
    #print(node)
        node = node[0]
        #print(len(node))
        val  = node.nonzero() 
        #print(val)
        disease = labelencoder.inverse_transform(val[0])
        return disease

def recurse(node, depth):
    global tree_, feature_name, symptoms_present
    indent = "  " * depth
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        name = feature_name[node]
        threshold = tree_.threshold[node]
        yield name + " ?"
        
        if ans.lower() == 'yes':
            val = 1
        else:
            val = 0
        if val <= threshold:
            yield from recurse(tree_.children_left[node], depth + 1)
        else:
            symptoms_present.append(name)
            yield from recurse(tree_.children_right[node], depth + 1)
    else:
        strData=""
        present_disease = print_disease(tree_.value[node])
        strData = "You may have :" + str(print_disease(tree_.value[node]))
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        
        red_cols = dimensionality_reduction.columns
        symptoms_given = red_cols[dimensionality_reduction.loc[print_disease(tree_.value[node])].values[0].nonzero()]
        strData = "symptoms present: " + str(list(symptoms_present))
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        
        strData = "symptoms given: " + str(list(symptoms_given))
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        
        confidence_level = (1.0 * len(symptoms_present)) / len(symptoms_given)
        strData = "confidence level is: " + str(confidence_level)
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        
        strData = 'The chatbot suggests:'
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        
        row = doctors[doctors['disease'] == present_disease[0]]
        strData = 'Consult ' + str(row['name'].values)
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        
        hyperlink = HyperlinkManager(QuestionDigonosis.objRef.txtDigonosis)
        strData = 'Visit ' + str(row['link'].values[0])
        def click1():
                    webbrowser.open_new(str(row['link'].values[0]))
        QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(click1))
        yield strData

def tree_to_code(tree, feature_names):
    global tree_, feature_name, symptoms_present
    tree_ = tree.tree_
    feature_name = [feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!" for i in tree_.feature]
    symptoms_present = []

def execute_bot():
    tree_to_code(classifier, cols)
    

# This section of code to be run after scraping the data

doc_dataset = pd.read_csv('doctors_dataset.csv', names = ['Name', 'Description'])


diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = np.nan
doctors['link'] = np.nan
doctors['disease'] = np.nan

doctors['disease'] = diseases['prognosis']


doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']

record = doctors[doctors['disease'] == 'AIDS']
record['name']
record['link']



# GUI classes
class QuestionDigonosis(Frame):
    objIter = None
    objRef = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Health Care Chatbot")
        master.geometry("800x600")
        self.configure(bg="#001028")
        QuestionDigonosis.objRef = self
        self.createWidget()

    def createWidget(self):
        main_frame = Frame(self, bg="#001028", padx=20, pady=20)
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.lblQuestion = Label(main_frame, text="Question", width=12, bg="#001028", fg="white")
        self.lblQuestion.grid(row=0, column=0, padx=(0,10), pady=(0,10))

        self.txtQuestion = Text(main_frame, width=80, height=5)
        self.txtQuestion.grid(row=0, column=1, pady=(0,10))

        self.lblDigonosis = Label(main_frame, text="Diagnosis", width=12, bg="#001028", fg="white")
        self.lblDigonosis.grid(row=1, column=0, padx=(0,10), pady=(0,10))

        self.txtDigonosis = Text(main_frame, width=80, height=20)
        self.txtDigonosis.grid(row=1, column=1, pady=(0,10))

        button_frame = Frame(main_frame, bg="#001028")
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10,0))
        
        self.btnStart = Button(button_frame, text="Start", width=12, bg="#83F28F", command=self.btnStart_Click)
        self.btnStart.grid(row=0, column=3)
        
        self.btnYes = Button(button_frame, text="Yes", width=12, bg="#83F28F", command=self.btnYes_Click)
        self.btnYes.grid(row=0, column=1, padx=(0,5))

        self.btnNo = Button(button_frame, text="No", width=12, bg="#83F28F", command=self.btnNo_Click)
        self.btnNo.grid(row=0, column=0, padx=(0,5))


        self.btnClear = Button(button_frame, text="Clear", width=12, bg="#83F28F", command=self.btnClear_Click)
        self.btnClear.grid(row=0, column=2, padx=(0,5))

        
        
    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0, END)
        self.txtQuestion.delete(0.0, END)
        self.txtDigonosis.insert(END, "Please Click on Yes or No for the Above symptoms in Question")
        QuestionDigonosis.objIter = recurse(0, 1)
        str1 = QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END, str1 + "\n")
        
    def btnYes_Click(self):
        global ans
        ans = 'yes'
        self.txtDigonosis.delete(0.0, END)
        str1 = QuestionDigonosis.objIter.__next__()
        
    def btnNo_Click(self):
        global ans
        ans = 'no'
        str1 = QuestionDigonosis.objIter.__next__()
        self.txtQuestion.delete(0.0, END)
        self.txtQuestion.insert(END, str1 + "\n")


    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0, END)
        self.txtQuestion.delete(0.0, END)

    

class MainForm(Frame):
    main_Root = None

    def __init__(self, master=None):
        MainForm.main_Root = master
        super().__init__(master=master)
        master.geometry("500x600")
        master.title("Health Care Chatbot")
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#f0f5f9")
        self.createWidget()

    def createWidget(self):
        # Create a frame to act as the card
        self.card_frame = tk.Frame(self, bg="#001028", bd=0)
        self.card_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)

        # Create glass effect
        self.create_glass_effect()

        # Custom fonts
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        button_font = tkfont.Font(family="Helvetica", size=14)
        label_font = tkfont.Font(family="Helvetica", size=12)

        # Title
        self.lblMsg = tk.Label(self.card_frame, text="Health Care Chatbot", 
                               bg="#001028", fg="#ffffff", 
                               font=title_font)
        self.lblMsg.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        # Login button
        self.btnLogin = tk.Button(self.card_frame, text="Login", 
                                  command=self.lblLogin_Click,
                                  bg="#83F28F", fg="#ffffff",
                                  font=button_font, width=15, height=2,
                                  relief=tk.FLAT, activebackground="#3a7bc8")
        self.btnLogin.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Register button
        self.btnRegister = tk.Button(self.card_frame, text="Register", 
                                     command=self.btnRegister_Click,
                                     bg="#DAA520", fg="#ffffff",
                                     font=button_font, width=15, height=2,
                                     relief=tk.FLAT, activebackground="#3a7bc8")
        self.btnRegister.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Made by label
        self.lblTeam = tk.Label(self.card_frame, text="Made by:", 
                                bg="#001028", fg="#ffffff",
                                font=label_font)
        self.lblTeam.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # Name label
        self.lblName1 = tk.Label(self.card_frame, text="Akash Deep Sarkar", 
                                 bg="#001028", fg="#ffffff",
                                 font=label_font)
        self.lblName1.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    def create_glass_effect(self):
        # Create a blurred background
        bg_image = Image.new('RGB', (400, 500), color=(0, 16, 40))  # Dark blue background
        blurred_image = bg_image.filter(ImageFilter.GaussianBlur(radius=20))
        self.bg_photo = ImageTk.PhotoImage(blurred_image)

        # Create a canvas and add the blurred image
        self.canvas = tk.Canvas(self.card_frame, width=400, height=500, 
                                highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        # Add a semi-transparent overlay
        self.canvas.create_rectangle(0, 0, 400, 500, fill="#001028", 
                                     stipple="gray25", outline="")

    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()

    def lblLogin_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        login = Login(master=MainForm.main_Root)
        login.pack(fill=tk.BOTH, expand=True)

    def btnRegister_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        register = Register(master=MainForm.main_Root)
        register.pack(fill=tk.BOTH, expand=True)

class Login(Frame):
    login_Root = None

    def __init__(self, master=None):
        Login.login_Root = master
        super().__init__(master=master)
        master.geometry("500x600")
        master.title("Login")
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#f0f5f9")
        self.createWidget()

    def createWidget(self):
        # Create a frame to act as the card
        self.card_frame = tk.Frame(self, bg="#001028", bd=0)
        self.card_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)

        # Create glass effect
        self.create_glass_effect()

        # Custom fonts
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=12)
        button_font = tkfont.Font(family="Helvetica", size=14)

        # Title
        self.lblMsg = tk.Label(self.card_frame, text="Login", 
                               bg="#001028", fg="#ffffff", 
                               font=title_font)
        self.lblMsg.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Username
        self.lblUsername = tk.Label(self.card_frame, text="Username", 
                                    bg="#001028", fg="#ffffff", font=label_font)
        self.lblUsername.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.txtUsername = tk.Entry(self.card_frame, font=label_font, width=25)
        self.txtUsername.place(relx=0.5, rely=0.37, anchor=tk.CENTER)

        # Password
        self.lblPassword = tk.Label(self.card_frame, text="Password", 
                                    bg="#001028", fg="#ffffff", font=label_font)
        self.lblPassword.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.txtPassword = tk.Entry(self.card_frame, show='*', font=label_font, width=25)
        self.txtPassword.place(relx=0.5, rely=0.57, anchor=tk.CENTER)

        # Login button
        self.btnLogin = tk.Button(self.card_frame, text="Login", 
                                  command=self.btnLogin_Click,
                                  bg="#83F28F", fg="#ffffff",
                                  font=button_font, width=15, height=2,
                                  relief=tk.FLAT, activebackground="#3a7bc8")
        self.btnLogin.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        # Message label
        self.lblMsg = tk.Label(self.card_frame, text="", 
                               bg="#001028", fg="#ffffff", font=label_font)
        self.lblMsg.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def create_glass_effect(self):
        # Create a blurred background
        bg_image = Image.new('RGB', (400, 500), color=(0, 16, 40))  # Dark blue background
        blurred_image = bg_image.filter(ImageFilter.GaussianBlur(radius=20))
        self.bg_photo = ImageTk.PhotoImage(blurred_image)

        # Create a canvas and add the blurred image
        self.canvas = tk.Canvas(self.card_frame, width=400, height=500, 
                                highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        # Add a semi-transparent overlay
        self.canvas.create_rectangle(0, 0, 400, 500, fill="#001028", 
                                     stipple="gray25", outline="")

    def login_sucess(self):
        self.lblMsg.config(text="Login Success", fg="#00ff00")
        self.destroyPackWidget(Login.login_Root)
        qd = QuestionDigonosis(master=Login.login_Root)
        qd.pack(fill=tk.BOTH, expand=True)

    def password_not_recognised(self):
        self.lblMsg.config(text="Invalid Password", fg="#ff0000")

    def user_not_found(self):
        self.lblMsg.config(text="User Not Found", fg="#ff0000")

    def btnLogin_Click(self):
        username = self.txtUsername.get()
        password = self.txtPassword.get()

        if os.path.exists(username):
            with open(username, "r") as file:
                data = file.read().splitlines()
                if password in data:
                    self.login_sucess()
                else:
                    self.password_not_recognised()
        else:
            self.user_not_found()

    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()

class Register(Frame):
    register_Root = None

    def __init__(self, master=None):
        Register.register_Root = master
        super().__init__(master=master)
        master.geometry("500x600")
        master.title("Register")
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="#f0f5f9")
        self.createWidget()

    def createWidget(self):
        # Create a frame to act as the card
        self.card_frame = tk.Frame(self, bg="#001028", bd=0)
        self.card_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)

        # Create glass effect
        self.create_glass_effect()

        # Custom fonts
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=12)
        button_font = tkfont.Font(family="Helvetica", size=14)

        # Title
        self.lblMsg = tk.Label(self.card_frame, text="Register", 
                               bg="#001028", fg="#ffffff", 
                               font=title_font)
        self.lblMsg.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Username
        self.lblUsername = tk.Label(self.card_frame, text="Username *", 
                                    bg="#001028", fg="#ffffff", font=label_font)
        self.lblUsername.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.txtUsername = tk.Entry(self.card_frame, font=label_font, width=25)
        self.txtUsername.place(relx=0.5, rely=0.37, anchor=tk.CENTER)

        # Password
        self.lblPassword = tk.Label(self.card_frame, text="Password *", 
                                    bg="#001028", fg="#ffffff", font=label_font)
        self.lblPassword.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.txtPassword = tk.Entry(self.card_frame, show='*', font=label_font, width=25)
        self.txtPassword.place(relx=0.5, rely=0.57, anchor=tk.CENTER)

        # Register button
        self.btnRegister = tk.Button(self.card_frame, text="Register", 
                                     command=self.btnRegister_Click,
                                     bg="#DAA520", fg="#ffffff",
                                     font=button_font, width=15, height=2,
                                     relief=tk.FLAT, activebackground="#3a7bc8")
        self.btnRegister.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        # Message label
        self.lblMsg = tk.Label(self.card_frame, text="", 
                               bg="#001028", fg="#ffffff", font=label_font)
        self.lblMsg.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def create_glass_effect(self):
        # Create a blurred background
        bg_image = Image.new('RGB', (400, 500), color=(0, 16, 40))  # Dark blue background
        blurred_image = bg_image.filter(ImageFilter.GaussianBlur(radius=20))
        self.bg_photo = ImageTk.PhotoImage(blurred_image)

        # Create a canvas and add the blurred image
        self.canvas = tk.Canvas(self.card_frame, width=400, height=500, 
                                highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        # Add a semi-transparent overlay
        self.canvas.create_rectangle(0, 0, 400, 500, fill="#001028", 
                                     stipple="gray25", outline="")

    def registration_success(self):
        self.lblMsg.config(text="Registration Success", fg="#00ff00")
        self.destroyPackWidget(Register.register_Root)
        qd = QuestionDigonosis(master=Register.register_Root)
        qd.pack(fill=tk.BOTH, expand=True)

    def user_already_exists(self):
        self.lblMsg.config(text="User Already Exists", fg="#ff0000")

    def btnRegister_Click(self):
        username = self.txtUsername.get()
        password = self.txtPassword.get()

        if os.path.exists(username):
            self.user_already_exists()
        else:
            with open(username, "w") as file:
                file.write(f"{username}\n{password}")
            self.registration_success()

    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()

# Main code to run the application
root = Tk()
mainform = MainForm(master=root)
mainform.pack()
root.mainloop()
