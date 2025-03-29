# --- OOP Email Simulator --- #
from typing import List, Optional

# --- Email Class --- #
class Email:
    email_id_tracking = 1000

# Initialise the instance variables for each email.
    def __init__(self, email_address = "", subject_line = "", email_content = ""):
        self.__email_address = email_address
        self.__subject_line = subject_line
        self.__email_content = email_content
        self.__has_been_read = False
    # Putting a unique ID for each email
        self.__email_id = self.email_id_generator()

    def get_email_address(self) -> str:
        return self.__email_address
    def set_email_address(self, email_address = "") -> None:
        self.__email_address = email_address
    def get_subject_line(self) -> str:
        return self.__subject_line
    def set_subject_line(self, subject_line = "") -> None:
        self.__subject_line = subject_line
    def get_email_content(self) -> str:
        return self.__email_content
    def set_email_content(self, email_content = "") -> None:
        self.__email_content = email_content
    def get_email_has_been_read(self) -> bool:
        return self.__has_been_read
    def get_email_id(self) -> int:
        return self.__email_id
    
 
# Change email has_been_read to True.
    def mark_as_read(self) -> None:
        print(f"\nEmail id :{self.__email_id} marked as read")
        self.__has_been_read = True


# Handling Email Id
    @classmethod
    def email_id_generator(cls) -> int:
        cls.email_id_tracking += 1
        return cls.email_id_tracking

# --- Functions --- #
# Build out the required functions for your program.


def populate_inbox(inbox_list : List["Email"]) -> List["Email"]:
    # Create 3 sample emails and add them to the inbox list.
    if inbox_list is None:
        inbox_list = []
    
    inbox_list.append( Email("no1@111.com", "Subject 1", "Hi, if you are seeing this, you are at part 1"))
    inbox_list.append( Email("no2@222.com", "Subject 2", "Nice you see you 2"))
    inbox_list.append( Email("no3@333.com", "Subject 3", "Good things come in 3"))
    return inbox_list

# List out email in inbox_list with email ID (index)
def list_emails(inbox_list : List["Email"], empty_message = "There is no email") -> None:
    if inbox_list is None:
        return
    elif len(inbox_list) == 0:
        print(empty_message)
    else :
        print("List of email:")
        for i in range (0, len(inbox_list)):
            print(f"{inbox_list[i].get_email_id()} | {inbox_list[i].get_subject_line()}")


# Displaying email with selected email_id
def read_email(inbox_list: List["Email"], email_id = 0) -> None:
    if inbox_list is None:
        return 
    else:
        selected_email = None
        for email in inbox_list:
            if(email.get_email_id() == email_id):
                selected_email = email
        if selected_email is None:
            print(f"Sorry, there is no email with id: {email_id}")
            return
        selected_email.mark_as_read()
        print(f"\nEmail address: {selected_email.get_email_address()}")
        print(f"Subject: {selected_email.get_subject_line()}")
        print(f"Content: {selected_email.get_email_content()}")


# Filtering unread email
def unread_emails_filter(email : "Email") -> Optional["Email"]:
    if (not email.get_email_has_been_read()):
        return email
    else:
        return None


# Displaying unread email
def view_unread_emails(inbox_list: List["Email"]) -> Optional[int]:
    if inbox_list is None:
        print("if")
    else:
        unread_list = list(filter(unread_emails_filter, inbox_list))
        list_emails(unread_list, "There is no unread email")
        return len(unread_list)


# --- Lists --- #
# Initialise an empty list outside the class to store the email objects.
inbox_list : List["Email"] = []

# --- Email Program --- #

#Populate the inbox 
populate_inbox(inbox_list)

# Display the menu options for each iteration of the loop.
while True:
    user_choice = int(
        input(
            """\nWould you like to:
    1. Read an email
    2. View unread emails
    3. Quit application

    Enter selection: """
        )
    )

    if user_choice == 1:
        # Add logic here to read an email
        print("Here is your inbox:")
        list_emails(inbox_list, "Your inbox is empty")

        # Getting email_id from user.
        email_id = int(input("Enter email id (e.g. 1001) to read email or input 0 to back to menu : "))
        if (email_id != 0 ):
            read_email(inbox_list, email_id)

    elif user_choice == 2:
        # Add logic here to view unread emails
        unread_number = view_unread_emails(inbox_list)
        
        if unread_number is not None and unread_number > 0:
            email_id = int(input("Enter email id (e.g. 1001) to read or input 0 to back to menu : "))
            if (email_id != 0 ):
                read_email(inbox_list, email_id)

    elif user_choice == 3:
        break

    else:
        print("Oops - incorrect input.")

print ("Thank you for using our email service")