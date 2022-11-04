"""
THINKBOI TWEETER DESKTOP
GUI-V.0.1

A simple GUI Twitter desktop client,
intended for sending short one-liner tweets.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QMessageBox, QTextEdit, QLabel, \
    QVBoxLayout, QDialog
from PyQt5 import QtGui
import tweepy

all_keys = open("api_keys.txt", 'r').read().splitlines()
if all_keys[0] == "API KEY":
    print("Please enter your API keys in the text file 'api_keys.txt' to start tweeting!")
    print("You can find your API keys in your Twitter Developer account.")
    print("If you don't have a Twitter Developer account, you can create one at https://developer.twitter.com/en/apply-for-access \n")
    print("The order of the keys in the text file should be: \n"
          "API key \n"
          "Secret API key\n"
          "Access token \n"
          "Secret access token\n")
    input("Press enter to exit. Restart the program after you have entered your API keys in the correct order.")
    sys.exit()
# The order of the keys in the file ought to be as follows:
CONSUMER_KEY = all_keys[0]  # API key on the first line
CONSUMER_SECRET = all_keys[1]  # Secret API key on the second line
ACCESS_TOKEN = all_keys[2]  # Access token on the third line
ACCESS_TOKEN_SECRET = all_keys[3]  # Secret access token on the fourth line

# ADD NOTHING TO THE API KEY FILE BUT THE KEYS!


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Constructor for the main window.
        """
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('thinkboitweetlogo1.png'))

        self.text_label = QLabel(self)
        self.length_label = QLabel(self)
        self.input_tweet = QLineEdit(self)
        self.send_button = QPushButton('Send tweet', self)
        self.save_button = QPushButton('Save as a draft', self)
        self.setWindowTitle("thinkboi tweeter desktop")
        self.setGeometry(500, 500, 500, 175)

        # Set background color of the main window as light blue
        self.setStyleSheet("background-color: lightblue;")

        self.initUI()

    def initUI(self):
        """
        Initializes the GUI.
        """

        self.send_button.move(50, 80)
        self.send_button.setStyleSheet("background-color: white; color: black;")

        self.save_button.move(150, 80)
        self.save_button.setStyleSheet("background-color: white; color: black;")

        self.send_button.clicked.connect(self.send_button_on_click)
        self.save_button.clicked.connect(self.save_button_on_click)

        self.tweet_input()
        self.update_count()
        self.menu_bar_func()

        self.show()

    def send_button_on_click(self):
        """
        Sends the tweet to the Twitter API.
        When the button is clicked, a confirmation message window is displayed
        where the user can confirm the tweet before sending it.
        """

        # Twitter authentication:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth, wait_on_rate_limit=True)
        tweet = self.input_tweet.text()

        # If the user didn't enter anything, but tries to send a tweet, print an error message
        if tweet == "":
            QMessageBox.question(self, 'Error', "You didn't enter anything!", QMessageBox.Ok, QMessageBox.Ok)
        # If the user clicks yes, print the textbox value
        # If the user clicks no, pass
        else:
            confirm_send = QMessageBox.question(self, 'Confirm', "Your tweet: \n\n" + tweet +
                                                "\n\nDo you want to tweet this?",
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)
            if confirm_send == QMessageBox.Yes:
                print("Tweeting...")
                # Send the tweet
                try:
                    send_tweet = api.update_status(tweet)
                    if send_tweet:
                        QMessageBox.question(self, 'Success', "Tweet sent successfully!",
                                             QMessageBox.Ok, QMessageBox.Ok)
                except tweepy.Forbidden:
                    QMessageBox.question(self, 'Error', "You're not allowed to tweet!"
                                                        "\nPlease check your API keys"
                                                        " and the permissions given to your developer account.",
                                         QMessageBox.Ok, QMessageBox.Ok)
                    pass
            # If the user clicks no, pass
            elif confirm_send == QMessageBox.No:
                pass

    def save_button_on_click(self):
        """
        The user can save the tweet as a draft.
        The draft file is saved in the same directory as the main file,
        to a file named drafts.txt.
        """
        tweet = self.input_tweet.text()

        # If the user didn't enter anything, print an error message
        if tweet == "":
            QMessageBox.question(self, 'Error', "You didn't enter anything!", QMessageBox.Ok, QMessageBox.Ok)
        # If the user clicks yes, save the prompt value to the drafts file
        # If the user clicks no, pass
        else:
            confirm_save = QMessageBox.question(self, 'Confirm', "Your tweet: \n\n" + tweet +
                                                "\n\nDo you want to save this as a draft?",
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)
            if confirm_save == QMessageBox.Yes:

                # Save the tweet as a draft in the drafts.txt file
                # Create a new file if the file doesn't exist
                try:
                    with open("drafts.txt", "a") as f:
                        print("Saving...")
                        f.write(tweet + "\n\n")
                        QMessageBox.question(self, "Success", "Draft saved successfully!",
                                             QMessageBox.Ok, QMessageBox.Ok)

                except FileNotFoundError:
                    with open("drafts.txt", "w") as f:
                        print("Saving...")
                        f.write(tweet + "\n\n")
                        QMessageBox.question(self, "Success", "Your tweet was saved into a new file"
                                                              "entitled drafts.txt", QMessageBox.Ok,
                                             QMessageBox.Ok)
                except OSError:
                    print("Error saving draft, please try again.")
            # If the user clicks no, close the window
            if confirm_save == QMessageBox.No:
                pass

    def open_draft_file(self):
        """
        Opens the drafts.txt file, and views its contents in a QTextEdit widget.
        Though the user can edit the text in the textedit widget, the text is not saved.
        A QTextEdit widget is employed so the user can copy the text in the drafts.
        """

        print("Opening drafts.txt...")
        # Open the drafts.txt file
        # If the file doesn't exist, create it
        try:
            with open("drafts.txt", "r") as f:
                print("Drafts.txt opened successfully!")

                # Create a new text prompt with the contents of the file
                self.text_window = QTextEdit(self)
                self.text_window.setText(f.read())
                self.text_window.setWindowTitle("Your drafts")

                drafts_window = QDialog()
                drafts_window.setWindowTitle("Your drafts")
                drafts_window.setGeometry(500, 500, 500, 500)
                drafts_window.setStyleSheet("background-color: lightblue;")
                drafts_window.setWindowIcon(QtGui.QIcon('thinkboitweetlogo1.png'))
                drafts_window.setLayout(QVBoxLayout())

                drafts_window.layout().addWidget(self.text_window)
                drafts_window.exec_()
                f.close()
        except FileNotFoundError:
            with open("drafts.txt", "w") as f:
                print("Drafts.txt created successfully!")
                f.write("")
                f.close()
        except OSError:
            print("Error opening drafts.txt, please try again.")

    def clear_draft_file(self):
        """
        Clears the contents of the drafts.txt file if the user chooses 'Yes'
        """

        choice = QMessageBox.question(self, 'WARNING', "Are you sure you want to clear the drafts? "
                                                       "This action cannot be undone.",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            try:
                with open("drafts.txt", "w") as f:
                    print("Clearing...")
                    f.write("")
                    QMessageBox.question(self, "Success", "Drafts cleared successfully!",
                                         QMessageBox.Ok, QMessageBox.Ok)
            except FileNotFoundError:
                print("Drafts file doesn't exist.")
            except OSError:
                print("Error clearing drafts, please try again.")
        else:
            pass

    def tweet_input(self):
        """
        Input prompt for the tweet.
        QLineEdit widget for the first version; in later versions this will be a QTextEdit widget
        to enable longer inputs.
        """

        font = self.input_tweet.font()
        font.setPointSize(12)
        font.setStyleName("Times New Roman")

        self.input_tweet.setFont(font)
        self.input_tweet.setStyleSheet("color: black;")
        self.input_tweet.setGeometry(50, 50, 400, 30)
        self.input_tweet.setPlaceholderText("Write your tweet here...")
        self.input_tweet.textChanged.connect(self.update_count)

        if len(self.input_tweet.text()) > 140:
            self.input_tweet.setStyleSheet("color: red;")

        self.input_tweet.show()
        self.text_label.show()

    def update_count(self):
        """
        Updates the count of the characters in the text box.
        With each keystroke, the count is updated.
        """
        self.length_label.setGeometry(50, 110, 400, 30)

        # Display character count
        self.length_label.setText(str(140 - len(self.input_tweet.text())))

        # Character counter
        self.length_label.setText("Characters left: " + str(140 - len(self.input_tweet.text())))
        if len(self.input_tweet.text()) >= 140:
            self.length_label.setStyleSheet("color: red;")
            self.input_tweet.setStyleSheet("color: red;")
            self.send_button.setEnabled(False)
        else:
            self.input_tweet.setStyleSheet("color: black;")
            self.length_label.setStyleSheet("color: black;")
            self.send_button.setEnabled(True)

        self.length_label.show()

    def close_application(self):
        """
        Closes the application.
        """
        choice = QMessageBox.question(self, 'Quit', "Do you want to exit?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quitting...")
            sys.exit()
        else:
            pass

    def info_window(self):
        """
        Opens an info prompt window.
        """
        self.info_window = QMessageBox.question(self, 'Info',
                                                "thinkboi tweeter is a desktop Twitter client that allows you to "
                                                "tweet from your desktop, "
                                                "giving you the space to tweet "
                                                "without contaminating your stream of thoughts "
                                                "with the Twitter newsfeed. \n\n"
                                                "The interface displays the number of characters remaining, "
                                                "counting down from 140 to which they are limited. This is "
                                                "done to incentivize the potency and simplicity of your tweets.\n\n"
                                                "The interface also allows you to save your tweets to a draft file, "
                                                "in case you do not want to tweet them right away. \n\n"
                                                "The application is open source, and can be found at: \n"
                                                "github.com/lauriparonen/thinkboi-tweeter-desktop",
                                                QMessageBox.Ok, QMessageBox.Ok)

    def instruction_prompt(self):
        """
        Opens a prompt window with instructions on how to use the application
        """
        self.instruction_prompt = QMessageBox.question(self, 'Instructions',
                                                       "To start with tweeting, enter your API access keys in the "
                                                       "text file entitled 'api_keys.txt', "
                                                       "in the following order:\n\n"
                                                       "consumer key, \n"
                                                       "secret consumer key,\n"
                                                       "access token, \n"
                                                       "secret access token. \n\n"
                                                       "Ensure there is nothing in the text file other than "
                                                       "the keys!\n\n"
                                                       "The keys are stored in the file for your convenience: "
                                                       "you can change between accounts simply by using different "
                                                       "files, instead of needing to manually "
                                                       "enter the keys to the code each time.\n\n"
                                                       "If you want to add a new account, simply add a new text file "
                                                       "with the keys to the same directory as the program - "
                                                       "just remember to name it 'api_keys<app_name>.txt' "
                                                       "and update the line in the beginning of the code where the "
                                                       "variable 'all_keys' is initialized.\n\n",
                                                       QMessageBox.Ok, QMessageBox.Ok)

    def open_api_keys(self):
        """
        Opens a window where the user can enter their API keys.
        into the text file.

        If the text file is empty, the user can enter their keys straight
        away in the window. If the text file is not empty, the user can
        confirm that they are the correct keys.

        If the user confirms the keys, the keys are saved to the text file.
        If the user doesn't confirm the keys, the window is closed.

        If the user wants to enter their keys of a different account,
        they can do so by deleting the text file and restarting the program.
        Another way to do this is to create a different text file with
        the name "api_keys_<account_name>.txt" and put the keys in there,
        and include in the function a way to choose which text file to use.

        """
        self.api_keys_window = QTextEdit()
        self.api_keys_window.setWindowTitle("View API keys")
        self.api_keys_window.setWindowIcon(QtGui.QIcon('thinkboitweetlogo1.png'))

        self.api_keys_window.setGeometry(500, 500, 500, 175)
        self.api_keys_window.setStyleSheet("background-color: lightblue;")

        try:
            with open("api_keys.txt", "r") as f:
                self.api_keys = f.readlines()
                if self.api_keys == "":
                    self.api_keys_window.setText("No API keys found. Please enter your keys in the text file.")
                else:
                    self.api_keys_window.setText("Consumer key: " + self.api_keys[0] + "\n" +
                                                 "Secret consumer key: " + self.api_keys[1] + "\n" 
                                                 "Access token: " + self.api_keys[2] + "\n" +
                                                 "Secret access token: " + self.api_keys[3])

        except FileNotFoundError:
            self.QMessageBox = QMessageBox.question(self, 'Error',
                                                    "The file 'api_keys.txt' was not found. "
                                                    "Please make sure it is in the same directory as the program.",
                                                    QMessageBox.Ok, QMessageBox.Ok)
            self.api_keys_window.close()

        self.api_keys_window.setWhatsThis("To edit your API keys, select 'Edit API keys' from the menu!")

        self.api_keys_window.show()

    def menu_bar_func(self):
        """
        Function for the menu bar.
        """

        self.menu_bar = self.menuBar()
        self.menu = self.menu_bar.addMenu("File")
        self.about = self.menu_bar.addMenu("About")

        self.api_keys = self.menu_bar.addMenu("API keys")

        about_prompt = self.about.addAction("Info")
        about_prompt.triggered.connect(self.info_window)

        view_drafts = self.menu.addAction("View drafts")
        view_drafts.triggered.connect(self.open_draft_file)

        clear_drafts = self.menu.addAction("Clear drafts")
        clear_drafts.triggered.connect(self.clear_draft_file)

        quit_menu = self.menu.addAction("Quit")
        quit_menu.triggered.connect(self.close_application)

        instruction_prompt = self.about.addAction("Instructions")
        instruction_prompt.triggered.connect(self.instruction_prompt)

        view_api_keys_prompt = self.api_keys.addAction("View API keys")
        view_api_keys_prompt.triggered.connect(self.open_api_keys)

        self.menu_bar.show()


# Main function to run the application
def main():
    app = QApplication([])
    mw = MainWindow()
    mw.show()
    app.exec_()


if __name__ == "__main__":
    main()
