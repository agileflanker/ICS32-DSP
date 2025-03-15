# Andrew Ngo
# azngo@uci.edu
# 63263981
'''
GUI for the ICS32 DSP.
Users can send and receive messages from valid users in the DSP server by first
joining a server and entering a username and password. If an existing profile
is associated with the username and password entered saved in a DSU File, the
user's information such as contacts and all messages will be loaded.
A user can only send and receive messages and add new contacts if they are
connected to a DSU server, otherwise they will only be able to view saved
conversations.
'''
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ds_messenger as dm
from dsu_profile import Profile, DsuFileError


class Body(tk.Frame):
    '''
    Creates the main body of the GUI with a Treeview object for all contacts,
    a Text object to display conversations, and an Entry object to collect user
    input.
    '''
    def __init__(self, root, recipient_selected_callback: callable = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        '''
        Updates the recipient attribute of the MainApp with the name of a
        selected contact.
        '''
        if event.widget.selection():
            index = int(event.widget.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)

    def clear_contacts(self):
        '''
        Clears the Treeview of all contacts
        '''
        if self._contacts or len(self.posts_tree.get_children()) != 0:
            self._contacts = []
            for item in self.posts_tree.get_children():
                self.posts_tree.delete(item)

    def insert_contact(self, contact: str):
        '''
        Adds a new contact to the Treeview if the contact's username isn't
        found in the contacts list.
        '''
        if not contact:
            messagebox.showerror("Invalid Contact", "Invalid contact entered!")
        elif contact not in self._contacts:
            self._contacts.append(contact)
            contact_id = len(self._contacts) - 1
            self._insert_contact_tree(contact_id, contact)

    def _insert_contact_tree(self, contact_id: int, contact: str):
        if len(contact) > 25:
            contact = contact[:24] + "..."
        contact_id = self.posts_tree.insert('',
                                            contact_id,
                                            contact_id,
                                            text=contact)

    def insert_user_message(self, message: str):
        '''
        Inserts a message sent by the user to the right-side of
        the conversation box.
        '''
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        '''
        Inserts a message received by the user to the left-side of
        the conversation box.
        '''
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def clear_messages(self):
        '''
        Clears the conversation box of all messages
        '''
        self.entry_editor.delete(1.0, tk.END)

    def get_text_entry(self) -> str:
        '''
        Returns a string of the current message entered by the user in the
        entry box.
        '''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        '''
        Clears the entry box of all messages, then sets it to the specified
        value.
        '''
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    '''
    Configures the layout of the Send button for sending user messages and
    displays the status of the DSP program in the bottom-left.
    '''
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        '''
        Calls the function notifying that the Send button was clicked.
        '''
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20,
                                command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(simpledialog.Dialog):
    '''
    Creates a pop-out window when the user logs in to the program by cliking
    Settings -> Configure DS Server in the Menu bar.
    Prompts the user for an IP address, username, and password.
    '''
    def __init__(self, root, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, "Configure Account")

    def body(self, master):
        '''
        Configures the layout of the pop-out window.
        '''
        server_label = tk.Label(master, width=30, text="DS Server Address")
        server_label.pack()
        self.server_entry = tk.Entry(master, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        username_label = tk.Label(master, width=30, text="Username")
        username_label.pack()
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        password_label = tk.Label(master, width=30, text="Password")
        password_label.pack()
        self.password_entry = tk.Entry(master, width=30)
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry['show'] = '*'
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    '''
    Initializes and configures functionality for the main window of the GUI.
    '''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.direct_messenger = ''

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def send_message(self):
        '''
        If connected to a DSU server and a contact is selected, sends a
        non-empty message to the contact. Otherwise, creates a pop-up menu
        displaying an error message if unable to send.
        '''
        msg = self.body.get_text_entry()
        if not self.direct_messenger:
            messagebox.showerror("Disconnected", "Not connnected to a server!")
        elif not self.recipient:
            messagebox.showerror("No Recipient", "No recipient selected!")
        elif not msg:
            messagebox.showerror("Empty Message", "Invalid message!")
        else:
            self.direct_messenger.send(msg, self.recipient)
            self.body.insert_user_message(msg)
            all_dms = self.direct_messenger.retrieve_all()
            all_msgs = []
            for dmsg in all_dms:
                if isinstance(dmsg, dm.DirectMessage):
                    new_msg = dmsg.to_dict()
                    all_msgs.append(new_msg)

            self.profile.save_messages([all_msgs.pop()])
            self.profile.save_profile(f'{self.username}.dsu')

            self.body.set_text_entry('')

    def add_contact(self):
        '''
        If connected to a DSU server, creates a pop-up window to add a user
        to contacts.
        '''
        if not self.direct_messenger:
            messagebox.showerror("Disconnected", "Not connnected to a server!")
        else:
            username = simpledialog.askstring('Add Contact', 'Username...')
            if username == self.username:
                messagebox.showerror("Invalid Contact",
                                     "Can't add yourself as a contact!")
                return
            self.body.insert_contact(username)
            self.profile.save_friends(username)
            self.profile.save_profile(f'{self.username}.dsu')
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list

    def display_recipient_messages(self):
        '''
        Displays all saved messages for the currently selected recipient,
        both sent and received, in the conversation box.
        '''
        all_msgs = self.profile.get_messages()
        for msg in all_msgs:
            if 'recipient' in msg and msg['recipient'] == self.recipient:
                self.body.insert_user_message(msg['message'])
            elif 'from' in msg and msg['from'] == self.recipient:
                self.body.insert_contact_message(msg['message'])

    def recipient_selected(self, recipient):
        '''
        Updates the currently selected recipient when the user clicks a contact
        in the contacts list.
        '''
        self.recipient = recipient
        self.body.clear_messages()
        self.display_recipient_messages()

    def configure_server(self):
        '''
        Creates a pop-up menu prompting the user to log in to a profile.
        If the username/password is associated with a saved DSU file, loads the
        saved profile. Otherwise, creates a new profile and associating DSU
        storage file.
        Attempts to connect to the DSU server provided.
        '''
        ud = NewContactDialog(self.root,
                              self.username, self.password, self.server)
        if not ud.user or not ud.pwd:
            messagebox.showerror("No User or Password",
                                 "No username or password!")
            return
        if ud.user == self.username and (ud.pwd == self.password
                                         and ud.server == self.server):
            messagebox.showerror("Logged In Already",
                                 f"Already logged in as {self.username}!")
            return

        self.body.clear_contacts()
        self.body.clear_messages()
        self.recipient = ''

        self.username = ud.user
        self.password = ud.pwd

        self.profile = Profile(self.server,
                               self.username,
                               self.password)
        try:
            self.profile.load_profile(f'{self.username}.dsu')
        except DsuFileError:
            self.profile.save_profile(f'{self.username}.dsu')

        if not (self.profile.username == self.username
                and self.profile.password == self.password):
            messagebox.showerror("Invalid User or Password",
                                 "Invalid username or password!")
            return

        friends = self.profile.get_friends()
        for friend in friends:
            self.body.insert_contact(friend)

        if ud.server and ud.server != self.server:
            self.direct_messenger = dm.DirectMessenger(ud.server,
                                                       self.username,
                                                       self.password)
            if not self.direct_messenger:
                return
            self.server = ud.server

            all_dms = self.direct_messenger.retrieve_all()
            all_msgs = []
            for dmsg in all_dms:
                if isinstance(dmsg, dm.DirectMessage):
                    msg = dmsg.to_dict()
                    all_msgs.append(msg)
            self.profile.overwrite_messages(all_msgs)
            self.profile.save_profile(f'{self.username}.dsu')
            self.after(2000, self.check_new)

    def check_new(self):
        '''
        The program continuously checks for new messages sent to the user every
        2 seconds. If the user receives a message from a contact not already in
        the contacts list, the new contact is saved to the user's list of
        friends and inserted into the contacts list. If the user receives a
        message from the currently selected contact, displays the new message.
        '''
        if self.direct_messenger:
            all_new = self.direct_messenger.retrieve_new()
            if all_new:
                all_new_msgs = []
                for new in all_new:
                    if isinstance(new, dm.DirectMessage):
                        new = new.to_dict()
                        all_new_msgs.append(new)
                        self.body.insert_contact(new['from'])
                        if new['from'] == self.recipient:
                            self.body.insert_contact_message(new['message'])
                        self.profile.save_messages(all_new_msgs)
                        self.profile.save_profile(f'{self.username}.dsu')
            self.after(2000, self.check_new)

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    app_id = main.after(2000, app.check_new)
    print(app_id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
