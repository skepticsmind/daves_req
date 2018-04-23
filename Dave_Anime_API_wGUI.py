import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox, Entry
import time
import random


class Utility:
    @staticmethod
    def make_list_box(frame, row, column):
        """ This function is used to make a basic textbox using the frame that is passed into it as an argument in the
        space dictated by the row and column passed into it.  The frame will have both horizonal and vertical scrollbars
        added in the row+1 row and column+1 columns respectively.

        This function returns the resulting listbox
        """
        v_list_scroll = Scrollbar(frame)
        v_list_scroll.grid(row=row, column=column + 1, sticky=N + S + W, rowspan=2, )
        h_list_scroll = Scrollbar(frame, orient=HORIZONTAL)
        h_list_scroll.grid(row=row + 2, column=column, sticky=E + W)
        listbox = Listbox(frame, height=8, width=40, yscrollcommand=v_list_scroll.set,
                          xscrollcommand=h_list_scroll.set)
        listbox.grid(row=row, column=column, rowspan=2, sticky=E + W + N + S)
        v_list_scroll.config(command=listbox.yview)
        h_list_scroll.config(command=listbox.xview)
        return listbox


class MenuBar(Frame):
    # CONSTRUCTOR
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # CREATE THE MENU BAR
        menu_bar = Menu(parent)
        drop_down = Menu(menu_bar, tearoff=0)
        drop_down.add_command(label="Exit", command=parent.quit)
        menu_bar.add_cascade(label="File", menu=drop_down)
        parent.config(menu=menu_bar)


class MainApplication(Frame):
    # CONSTRUCTOR
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # CALL OTHER CLASSES
        FindUserPage(parent)
        MenuBar(parent)


class FindUserPage(Frame):

    # CONSTRUCTOR
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # CREATE A NEW FRAME
        self.user_entry = []
        self.entry_var = IntVar()
        self.new_frame = Frame(parent, width=600, height=600)
        self.new_frame.grid(row=0, column=0)
        self.label = Label(self.new_frame, text="Enter the usernames that will be compared")
        self.num_user_label = Label(self.new_frame, text="How many lists would you like to compare?")
        self.num_user_label.grid(row=0, column=0)
        self.num_user_entry = Entry(self.new_frame, textvariable=self.entry_var)
        self.num_user_entry.grid(row=0, column=1)
        self.user_num_button = Button(self.new_frame, text="Next", command=self.get_users)
        self.user_num_button.grid(row=1, column=1, sticky=E, pady=(0, 5), padx=(0, 5))

    # Called after button is clicked in the constructor
    # noinspection PyTypeChecker
    def get_users(self):
        """ Once the user enters the number of users that they wish to compare the user_num_button will be deleted and
        entry boxes will be added to the window equal to the number of users the user entered in the num_user_entry box.
         Once entered, the user will click on the submit button which will call the submit_clicked function
         """
        self.user_num_button.destroy()
        self.label.grid(row=1, column=0, columnspan=2)
        num_user = self.entry_var.get()
        for i in range(0, num_user):
            self.user_entry.append(Entry(self.new_frame))
            self.user_entry[i].grid(row=i + 2, column=0, pady=(2, 2), sticky=W)
        continue_button = Button(self.new_frame, text="Submit", command=self.submit_clicked)
        continue_button.grid(row=num_user + 3, column=1, sticky=E)

    # Called when continue is clicked in get_users function
    def submit_clicked(self):
        """ Handles the API calls with 1s between each call to minimize errors. The returned data is error checked to
        ensure there were no errors. If there were no errors the data from the api call the data is passed to the
        get_info function which returns a dictionary of sorted information parsed from the API call. The dictionaries
        are put into a list which is then passed into the MenuPage class.
        """
        user_info = []
        for w in range(0, self.entry_var.get()):
            username = self.user_entry[w].get()
            raw_data = self.api_call(username)
            time.sleep(1)
            if raw_data == -1:
                return -1
            user_info.append(self.get_info(raw_data, username))
        self.new_frame.destroy()
        MenuPage(self.parent, user_info)

    # called in submit_clicked
    # requests data from API, calls are on a 1.5 second delay and returns the xml data of the API if call was successful
    # on error it returns -1
    def api_call(self, username):
        """ Creates and executes the API call. Then error checks to ensure the API call was successful and that the
        username exists.

        The data taken from the api call is returned.
        """
        call = "https://myanimelist.net/malappinfo.php?u=" + username + "&status=all&type=anime"
        response = requests.get(call)
        if response.status_code != 200:
            self.label.config(text="ERROR API CALL FAILED")
            return -1
        elif response.status_code == 200:
            print("API CALL SUCCESFUL")
            soup = BeautifulSoup(response.text, "xml")
            if soup.find("user_id") is None:
                Label(self.new_frame, text="Invalid Username Please check usernames", fg="red", bg="white").grid(row=1,
                                                                                                                 column=0,
                                                                                                                 columnspan=2)
                return -1
            else:
                return soup

    # called in submit_clicked Parses the text that is passed to it via the soup variable and returns a dictionary
    # object with the username as well as that user's shows they have watched and plan on watching
    @staticmethod
    def get_info(soup, username):
        """ Takes the data from the API call and sorts it into various lists inside a dictionary.

         The dictionary is returned.
         """
        # DEFINE VARIABLES
        watched_shows = []
        planned_shows = []
        dropped_shows = []
        currently_watching_shows = []
        on_hold_shows = []
        switch = {
            "1": currently_watching_shows,
            "2": watched_shows,
            "3": on_hold_shows,
            "4": dropped_shows,
            "6": planned_shows,
        }

        # PARSE DATA
        shows = soup.find_all('series_title')
        watch_status = soup.find_all('my_status')

        # FORMAT DATA
        for y in range(0, len(shows)):
            shows[y] = shows[y].text
            watch_status[y] = watch_status[y].text
            switch[watch_status[y]].append(shows[y])
        watched_shows.sort()
        planned_shows.sort()
        dropped_shows.sort()
        currently_watching_shows.sort()
        on_hold_shows.sort()
        # CREATE DICTIONARY TO RETURN
        user_data = {
            "Username": username,
            "watching": currently_watching_shows,
            "watchedlist": watched_shows,
            "plannedList": planned_shows,
            "dropped": dropped_shows,
            "hold": on_hold_shows,
            "showsToWatch": [],
        }
        return user_data


class MenuPage(Frame):

    # CONSTRUCTOR
    def __init__(self, parent, user_dictionary):
        Frame.__init__(self, parent)
        self.parent = parent
        self.user_dictionary = user_dictionary
        self.combined_plan_to_watch = []
        self.frame = Frame(parent)
        self.frame.grid(row=0, column=0)
        Label(self.frame, text="SHOWS YOU CAN WATCH", font='Helvetica 14').grid(row=0, column=0, columnspan=3)
        self.results_listbox = Utility.make_list_box(self.frame, 1, 1)
        self.shows_to_watch = self.get_results()
        for x in range(0, len(self.shows_to_watch)):
            self.results_listbox.insert("end", self.shows_to_watch[x])
        self.results_listbox.configure(height=10, width=40)
        Button(self.frame, text="User Info", command=lambda: UserData(self.parent, self.user_dictionary)).grid(row=4,
                                                                                                               column=0,
                                                                                                               padx=(
                                                                                                                   5,
                                                                                                                   0),
                                                                                                               pady=(
                                                                                                                   0,
                                                                                                                   5))
        Button(self.frame, text="Detailed List", command=lambda: DetailedList(self.parent,self.user_dictionary, self.combined_plan_to_watch)).grid(row=4, column=2, padx=(0, 5),
                                                                                     pady=(0, 5))
        Button(self.frame, text="Random Show", command=self.random_show).grid(row=4, column=1, pady=(0, 5))

    def random_show(self):
        """ When the user presses the random show button this function executes. It picks a random show from the
        shows_to_watch list and adds it to the clipboard then prompts a message to the user letting them know what show
        has been chosen.
        """
        self.frame.clipboard_clear()
        self.results_listbox.selection_clear(0, "end")
        rng = random.randint(1, 1001) % len(self.shows_to_watch)
        self.results_listbox.selection_set(rng)
        messagebox.showinfo("Random Show",
                            "The random show is \n%s\nIt has been copied to the clipboard" % self.shows_to_watch[rng])
        self.frame.clipboard_append(self.shows_to_watch[rng])

    def get_results(self):
        """ Takes the list of dictionaries and compares all shows in each users plan to watch lists against each users
        other lists which indicate they have already seen the show. If a show is on each users watch list and not in any
        of the lists which indicates they have watched it already then the show is added to the combined_plan_to_watch
        list
        """
        eliminated_shows = []
        results = []
        # Compile All Lists of Shows
        for x in range(0, len(self.user_dictionary)):
            # Watched Show List
            for y in range(0, len(self.user_dictionary[x]['watchedlist'])):
                if self.user_dictionary[x]['watchedlist'][y] not in eliminated_shows:
                    eliminated_shows.append(self.user_dictionary[x]['watchedlist'][y])
            # Shows currently being watched
            for y in range(0, len(self.user_dictionary[x]['watching'])):
                if self.user_dictionary[x]['watching'][y] not in eliminated_shows:
                    eliminated_shows.append(self.user_dictionary[x]['watching'][y])
            # Dropped Shows
            for y in range(0, len(self.user_dictionary[x]['dropped'])):
                if self.user_dictionary[x]['dropped'][y] not in eliminated_shows:
                    eliminated_shows.append(self.user_dictionary[x]['dropped'][y])
            # Shows that user put on hold
            for y in range(0, len(self.user_dictionary[x]['hold'])):
                if self.user_dictionary[x]['hold'][y] not in eliminated_shows:
                    eliminated_shows.append(self.user_dictionary[x]['hold'][y])
                    eliminated_shows.sort()
            # Check if planned lists are in master watched
            for y in range(0, len(self.user_dictionary[x]['plannedList'])):
                if self.user_dictionary[x]['plannedList'][y] not in eliminated_shows:
                    self.user_dictionary[x]['showsToWatch'].append(self.user_dictionary[x]['plannedList'][y])
            # add user's shows that no1 else has watched to the master list
            for y in range(0, len(self.user_dictionary[x]['showsToWatch'])):
                self.combined_plan_to_watch.append(self.user_dictionary[x]['showsToWatch'][y])
        # if the number of times a show is on the compiled plan to watch list is equal to the number of users
        # then all users have it on their lists and it can be put into the final list.
        for x in range(0, len(self.combined_plan_to_watch)):
            if self.combined_plan_to_watch.count(self.combined_plan_to_watch[x]) == len(self.user_dictionary):
                if self.combined_plan_to_watch[x] not in results:
                    results.append(self.combined_plan_to_watch[x])
        results.sort()
        return results


class UserData(Frame):

    def __init__(self, parent, user_data):
        Frame.__init__(self, parent)
        self.parent = parent
        self.top = Toplevel()
        MenuBar(self.top)
        self.user_data = user_data

        # make a new canvas and embed a frame
        self.canvas = Canvas(self.top, width=1500, height=600)
        self.frame = Frame(self.top)
        self.canvasscroll = Scrollbar(self.top, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.canvasscroll.set)
        self.canvasscroll.grid(row=1, column=25, sticky=N + S + E, rowspan=10)
        self.canvas.grid(row=1, column=0, sticky=N + E + W + S, columnspan=9)
        self.canvas.create_window((2, 0), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.on_frame_configure)

        Label(self.frame, text="Shows Watched", font='Helvetica 18 bold').grid(row=1, column=1)
        Label(self.frame, text="Shows to Watch", font='Helvetica 18 bold').grid(row=1, column=3)
        Label(self.frame, text="Dropped Shows", font='Helvetica 18 bold').grid(row=1, column=5)
        Label(self.frame, text="Currently Watching", font='Helvetica 18 bold').grid(row=1, column=7)
        Label(self.frame, text="On Hold", font='Helvetica 18 bold').grid(row=1, column=9)
        for x in range(0, len(user_data)):
            self.display_user_info(user_data[x], x)
        Button(self.top, text="Close", command=lambda: self.top.destroy()).grid(row=len(user_data)+1, column=0, columnspan=10,
                                                                                pady=(5, 5))

    def on_frame_configure(self):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def display_user_info(self, user_data, row_num):
        """Creates five text boxes and fills each with the shows of the selected list."""
        row_num = 2 * row_num + (row_num + 2)
        Label(self.frame, text=user_data["Username"]).grid(row=row_num, column=0, rowspan=2, padx=(0, 10))
        user_watched = Utility.make_list_box(self.frame, row_num, 1)
        user_plan = Utility.make_list_box(self.frame, row_num, 3)
        user_dropped = Utility.make_list_box(self.frame, row_num, 5)
        user_watching = Utility.make_list_box(self.frame, row_num, 7)
        user_hold = Utility.make_list_box(self.frame, row_num, 9)
        for y in range(0, len(user_data["watchedlist"])):
            user_watched.insert("end", user_data["watchedlist"][y] + "\n")
        for z in range(0, len(user_data["plannedList"])):
            user_plan.insert("end", user_data["plannedList"][z] + "\n")
        for x in range(0, len(user_data["dropped"])):
            user_dropped.insert("end", user_data["dropped"][x] + "\n")
        for x in range(0, len(user_data["watching"])):
            user_watching.insert("end", user_data["watching"][x] + "\n")
        for x in range(0, len(user_data["hold"])):
            user_hold.insert("end", user_data["hold"][x] + "\n")


class DetailedList(Frame):
    def __init__(self, parent, user_data, user_plan):
        Frame.__init__(self, parent)
        self.parent = parent
        self.user_data = user_data
        self.user_plan = sorted(user_plan, key=user_plan.count, reverse=True)
        shows_placed = []
        self.top = Toplevel(self.parent)
        MenuBar(self.top)
        Label(self.top, text="Detailed List").grid(row=0, column=0, columnspan=2)
        Label(self.top, text="Show").grid(row=1, column=0)
        Label(self.top, text="Users").grid(row=1, column=1)
        self.v_list_scroll = Scrollbar(self.top)
        self.v_list_scroll.grid(row=2, column=2, sticky=N+S)
        self.show_box = Listbox(self.top, height=8, width=40, yscrollcommand=self.show_scroll)
        self.show_box.grid(row=2, column=0)
        self.user_box = Listbox(self.top, height=8, width=40, yscrollcommand=self.user_scroll)
        self.user_box.grid(row=2, column=1)
        self.v_list_scroll.config(command=self.two_text_scroll)

        for x in range(0, len(self.user_plan)):
            if self.user_plan[x] not in shows_placed:
                users_watched = []
                self.show_box.insert("end", self.user_plan[x])
                shows_placed.append(self.user_plan[x])
                for y in range(0, len(user_data)):
                    if self.user_plan[x] in user_data[y]["plannedList"]:
                        users_watched.append(user_data[y]["Username"])
                self.user_box.insert("end", users_watched)
        Button(self.top, text="Close", command=lambda: self.top.destroy()).grid(row=3, column=0, columnspan=2, pady=(5, 5))

    def show_scroll(self, *args):
        if self.user_box.yview() != self.show_box.yview():
            self.user_box.yview_moveto(args[0])
        self.v_list_scroll.set(*args)

    def user_scroll(self, *args):
        if self.show_box.yview() != self.user_box.yview():
            self.show_box.yview_moveto(args[0])
        self.v_list_scroll.set(*args)

    def two_text_scroll(self, *args):
        self.show_box.yview(*args)
        self.user_box.yview(*args)


if __name__ == "__main__":
    root = Tk()
    root.title("Anime Selection Tool")
    for x in range(1, 20):
        root.rowconfigure(x, weight=1)
        root.columnconfigure(x, weight=1)
    my_gui = MainApplication(root)
    mainloop()
