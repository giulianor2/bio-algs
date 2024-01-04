import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon=":information_source:"
    )

st.title('Genetic Sudoku Solver')
st.header('About this App')

st.subheader('A Perfect Nonsense Machine?')
st.markdown(
    """
    Why bother with a Sudoku Solver? Why use a machine to solve a puzzle whose very intent it
    is to tickle your brain? Surely this is nothing but a complex [Nonsense Machine](https://en.wikipedia.org/wiki/Rube_Goldberg_machine).  
      
    While there is some truth to this, the search for an algorithm that solves a puzzle is a brain-teaser in and of itself. Even more,
    you may be able to transfer your learnings to other fields and applications.  
      
    To such an end Sudoku presents a very good research object. The rules of the game are extremely easy. At the same time the problem
    complexity can be scaled deliberately and to a high degree by the number and combination of pre-defined fields.  
      
    Also, the number of potential solutions (i.e. valid Sudoku) is by all practical means unlimited
    ([6.7e21](https://www.technologyreview.com/2012/01/06/188520/mathematicians-solve-minimum-sudoku-problem/)). That is more than the
    number of stars in the known universe and precludes run-of-the-mill brute force methods.
    """
    )

st.subheader('But Why A Genetic Algorithm?')
st.markdown(
    """
    Genetic algorithms have a proven track-record on a [wide range of optimization problems](https://en.wikipedia.org/wiki/List_of_genetic_algorithm_applications). 
    Not only can the cope with greatly differing problem domains, they can also easily incorporate hard and soft constraints and find very good if
    not always optimal solutions.  
      
    And that is exactly the point I wanted to test. There is (mostly) only one correct solution for a Sudoku Problem. If we measure 
    the "wrongness" of a solution by the number of incorrect fields though, there is  a huge number of solution candidates with only two 
    or three fields off - and still totally wrong.  
      
    So the question was: ***Can we build a genetic algorithm in such a way, that it avoids getting stuck in the wide range of "good" local
    optima and instead reaches the global optimum of zero errors?***
    """
    )

st.subheader("And Then There's the UI Part ...")
st.markdown(
    """
    One of the hardest lessons of the last few years for me was, that all your skills as a Data Scientist or Data Analyst come
    to naught if you're not able to expose your results to users in an easily accessible way. So outside of the world of 
    "simple" Business Intelligence applications I am constantly on the lookout for tools that provide an easy to build and easy
    to use Frontend package, allowing the quick implementation of impactful POC and MVP.  

    I have tried out Jupyter Notebooks, tkinter, Svelte (plus FastAPI) in the past and none of these was really well suited.
    They were either not really approachable for Business Users (Jupyter) or hard to work with for data applications (esp. tkinter).
    Up and above standard frontend tools require significant knowledge and application of CSS, HTML and Java, which takes
    valuable time away from working on the actual Data Science problems.

    **And then along came [streamlit](https://streamlit.io).** This newish library not only allows you to build the complete frontend in 
    Python and thus seamlessly integrates with your backend-oriented data work. A constantly growing number of functions and 
    users-built components provides an ever wider range of possibilities to improve your user-facing work. While I heard some 
    good things about streamlit recently, I hadn't tried it out for myself though.  
      
    So this Genetic Sudoku Solver problem seemed like the perfect opportunity to learn and to try out the possibilities this 
    library offers. I've thrown everything at it, user inputs, forms, multi-page setup, plotting, multi-interaction, optical sugar, ...
    and it held up perfectly. It is easy to use, quick to learn and requires a minimum of coding to get really good results. 
    And I sincerely hope it provides a good user experience to you as well :smiley:.  
    """
    )

st.subheader("Credits")
st.markdown(
    """
    For the Genetic Algorithm part I rely heavily on ["Hands-On Genetic Algorithms with Python"](https://github.com/PacktPublishing/Hands-On-Genetic-Algorithms-with-Python)
    by Eyal Wirsansky, which not only provides a great learning source. Eyal has also developed a great code base
    that builds on the DEAP libraries and provides some useful additional classes and functions.

    As for the frontend part, I'd like to thank the streamlit for providing not only a perfect library but also a very concise and comprehensive documentation.
    I'd also like to thank the streamlit community for the loads of content and solution approaches to even the most particular of problems.
    """
    )