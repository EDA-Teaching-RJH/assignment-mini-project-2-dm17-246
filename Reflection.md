Libraries

In Lecture 7, we learned about libraries and how to import some of the most commonly used modules. For this project, I used three different libraries. The re library was used in all of the validation and search functions. The csv library was used in the save and load functions with the DictWriter and DictReader classes to handle the headers automatically. Finally, the os library was used to check if the file already existed prior to attempting to open it. These are all library modules instead of the third-party packages which, while functional, is not as strong a feature as using a custom defined module (which would have been used if I had had time to create such a module).

File I/O

In Lecture 9, we learned about file I/O. Specifically, how to use the “with” statement to automatically close the files that were opened by the script. For the project, I have three different file functions. The save_to_file function will write every student object to a file named students.csv. The load_from_file function will read the file and construct each student object from the rows in the file, skipping any corrupt rows with a warning message. Finally, the export_report function will output the students report to a file named report.txt. Thus, I have included both the .csv and .txt file formats that were discussed in Lecture 9.

Earlier Lectures

A few of the earlier lectures also fed into this project. The get_grade function uses the exact same if/elif statements as lecture 3 regarding degree classifications. Additionally, both the main_menu function and the _validate_input function use the while True loop discussed in lecture 4. Finally, the validate_score and load_from_file functions use try and except statements as discussed in lecture 6.

Overall Reflection

Overall, I am happy with the project that I have created. The one area that I would love to improve upon, however, would have been the libraries portion of the code. Specifically, if I had time to create a separate module file to contain all of the validation functions instead of defining them directly in this project file. I would have also loved to have created a Course class to extend the object orientation of this project. Nevertheless, I believe that the project fulfills the requirements of the assignment and makes it clear how each of these lectures relate to the project.