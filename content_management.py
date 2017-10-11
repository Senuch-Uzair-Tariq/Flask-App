##// CURRENT:
##// list of topics by {TOPIC:[["TITLE", "URL"]]}
##
##// FUTURE:
##////list of topics by {TOPIC:[["TITLE", "URL", "TAGS"],
##////                          ["TITLE", "URL", "TAGS"]]}

def Content():
    ##    //             Suggest Branches for next steps
    ##    //             If liked: Matplotlib, link to data analysis or Pandas maybe
    ##    //             If liked: GUI stuff: Kivy, PyGame, Tkinter
    ##    //             if liked: Text and word-based: NLTK


    # MAIN : [TITLE, URL, BODY_TEXT (LIST), HINTS(LIST)]
    TOPIC_DICT = {
        "Basics": [["Python Introduction", "/introduction-to-python-programming/", [""]],
                             ["Print Function and Strings", "/python-tutorial-print-function-strings/",
                              ["The Print function outputs text to the console (black area). Let's try it out!",
                               "print() is a function, which does something with parameters, and parameters go inside the parenthesis.",
                               "See if you can use the print function to output 'Hello!' to the console!"]],
                             ["Sockets with Python Intro", "/python-sockets/"],
                             ["Simple Port Scanner with Sockets", "/python-port-scanner-sockets/"],
                             ["Threaded Port Scanner", "/python-threaded-port-scanner/"],
                             ["Binding and Listening with Sockets", "/python-binding-listening-sockets/"],
                             ["Client Server System with Sockets", "/client-server-python-sockets/"],
                             ["Python 2to3 for Converting Python 2 scripts to Python 3",
                              "/converting-python2-to-python3-2to3/"]]
                  }

    return TOPIC_DICT


if __name__ == "__main__":
    x = Content()

    print(x["Basics"])

    for each in x["Basics"]:
        print(each[1])
