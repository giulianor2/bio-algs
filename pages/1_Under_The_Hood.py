import streamlit as st

st.set_page_config(
    page_title="Under the Hood",
    page_icon=":gear:"
    )

st.title('Genetic Sudoku Solver')
st.header('Technical and Methodological Details on the Solver Components')

st.subheader('Divide and Rule')
st.markdown(
    f"""
    As you might already know, the number of potential solutions (i.e. valid Sudoku) is by all practical means unlimited
    ([6.7e+21](https://www.technologyreview.com/2012/01/06/188520/mathematicians-solve-minimum-sudoku-problem/)). The total number of 
    combinations, i.e. 9 to the power of 81 is even greater (**{9**81:.1e}**). That makes the problem in its pure form 
    impractical for a Genetic Algorithm, as you'd either need huge populations (equals heavy computational cost) or many generations (equals long run-times) to 
    have any chance of solving the problem. None of these proved practical in initial trial runs.  
      
    The question was therefore 
    > ***Can we reduce solution candidates to a manageable number?***

    The way I chose to address this was by
    - Reducing the options per field by running the problem through a greedy algorithm first
    - Feeding only valid rows into the algorithm, i.e. excluding solution candidates with repetitive numbers in a row  
      
    For easier problems the greedy algorithm will already solve the Sudoku. To avoid trying several examples to find one
    hard enough, just try Example 1 from the dropdown menu. This is one of the hardest Sudoku from a puzzle book
    I encountered in the trial runs. It ends up with 6.7e21 potential combinations for 
    the possible numbers in each field after the greedy algorithm, giving you some room to play
    with the GA parameters.
    """
    )

tabs_upper = st.tabs(['The Greedy Algorithm', 'The Genetic Algorithm'])
with tabs_upper[0]:
    st.subheader('The Greedy Algorithm')
    st.markdown(
        """
        While there are several solution approaches out there, I have just implemented two basic algorithms to reduce the solution
        options per field. A field is deemed as solved if there is just one number left as an option. So for each field not yet solved:
        - Start with the initial set of numbers (1 to 9) and reduce this list for all already solved fields in the same row, same column or same
        sector (3x3 square). If the number of options is reduced to one, this field is set to solved.
        - For each field reduce the remaining options by all options of the fields in the same row, same column or same sector. This
        checks, whether there is one single option that is unique to this field. If so, this field is set to solved.  
        
        The algorithm iterates over all fields while it is still able to solve at least one field in a complete run. It then terminates and returns
        the options it found. Though simple and easy to implement, this approach already solves most Sudoku problems you throw at it.  
        
        In human terms, only those Sudoku remain, where you have to "guess" a number among several options at some point and try if it works. This is
        where the Genetic Algorithm takes over.
        """
        )
with tabs_upper[1]:
    st.subheader('The Genetic Algorithm')
    st.markdown(
        """
        If you are not yet familiar with the basics of Genetic Algorithms, I recommend spending some time on this extremely 
        [well written book](https://github.com/PacktPublishing/Hands-On-Genetic-Algorithms-with-Python). For the following passages I 
        assume that you already have some knowledge on the topic.
        """
    )

    tabs_ga = st.tabs(['Gene Encoding', 'GA Operators', 'Shock Events'])
    with tabs_ga[0]:
        st.markdown("""#### From Number to Gene""")
        st.markdown(
            f"""
            The most crucial part in applying Genetic Algorithms is in how you encode the problem. While there are many variants out there
            (for reference check the examples in [this book](https://github.com/PacktPublishing/Hands-On-Genetic-Algorithms-with-Python)), 
            each new problem will most probably ask for a different approach.  
            
            My initial idea was to define the gene as a list of length 81, where each element represented a field in the 9x9 Sudoku 
            (i.e. number of 1 to 9 per field). This proved extremely difficult to manage, as it required cumbersome slicing operations 
            to validate results as well as highly customized mating and mutation functions.  
            
            For the solution presented here I resorted to a different approach. I generate an array of length 9, where each element holds all
            possible and valid rows that can be built from the options returned by the Greedy Algorithm. In practical terms I take the
            cross-product of all field options per row and eliminate all rows with repeated elements. The gene is finally an array of length
            9 where each element is an index of the former array (i.e. gene[0] with value 3 refers to the fourth option of first Sudoku row). 
            You thus get a gene where each point on this gene has a different number of elements.  
              
            While this process might sound complicated, it allows the usage of standard mating and mutation functions provided by the 
            [deap library](https://github.com/DEAP/deap) as well as quick validation of a given generation.  
              
            At the same time this encoding significantly reduces the number of potential individuals. To put some numbers to it, the greedy 
            algorithm reduces the number of solution candidates for Example 1 from **{9**61:.1e}** to **5.5e+26** and the encoding process whittles 
            this down further to **5.4e+11** candidates. Still a lot (which proves the power of Genetic Algorithms) but by a significant
            number of degrees better.              
            """
        )  
    with tabs_ga[1]:
        st.markdown("""#### Selection, Mutation and Mating""")
        st.markdown(
            """
            The base unit i.e. "individual" in our case represents a completely filled Sudoku as defined by the specific expression of its gene. 
            Multiple individuals form a "population" which is specific to a "generation". As with every basic Genetic Algorithm we run through the 
            same procedure for each round (= generation):
            - select individuals based on their fitness (e.g. value of penalty function)
            - crossover/mate the selected individuals to build a new generation from their offspring
            - mutate the genes of some of the offspring
            - evaluate the fitness of the resulting population
            - terminate if either the optimal solution has been found or the defined number of generations has been reached, else repeat 
            
            ###### Selection :microscope::
            A parent population is built tournament-style by sampling repeatedly two individuals from the previous generation
            and selecting the fittest. While tournament selection allows for larger samples, the low sampling rate contributes
            to variety in the population by giving less fit individuals a fighting chance to procreate.

            ###### Crossover/Mating :woman-kiss-man::
            For crossover/mating the two parent individuals are split at the same random point and recombined (single point crossover). 
            This results in two offspring that replace their parents in the population. Based on the mating probability, not all
            individuals will produce offspring, some remain unchanged.

            ###### Mutation :smile_cat::
            The resulting offspring may be mutated based on the mutation probability. For mutation a row is selected at random. In this row 
            the current solution option is replaced by a different random one of the same row. This brings new variants into the population.

            ###### Hall of Fame :medal::
            To ensure that the fittest individuals are not lost time and again to mating and mutation, these are collected in a Hall of Fame and
            re-injected to the next population without changes ("elitism"). As the Hall of Fame fills up, less fit individuals
            are replaced by fitter individuals from the new round.

            ###### Evaluation :dart::
            For evaluation a validation function counts how often a solution candidate breaks the Sudoku Rules, i.e. has doubles in rows,
            columns or 3x3 sectors. The best fitness (and termination condition) is zero.
            """
            )
    with tabs_ga[2]:
        st.markdown("""#### Selected Catastrophies""")
        st.markdown(
            """
            Unfortunately none of the classic algorithms for selection, mutation and mating was able to provide a high enough
            probability that the algorithm wouldn't get stuck in local minima (often a fitness of 2). Therefore I developed two
            "Shock Events" that throw everything in the air if a GA run is stuck in a rut for too long.
            
            ###### Radiation Leak :radioactive_sign::
            As the name might suggest, we increase mutation probability significantly (i.e to 50%) for several rounds. As this doesn't affect
            the Hall of Fame members, we secure our progress already made while we increase the chance of stumbling on fitter individuals
            in the remaining population.

            ###### Comet Strike :comet::
            In analogy to the comet that wiped out the dinosaurs but created a new playing field for mammals, we wipe out the complete
            population apart from the Hall of Fame. We generate the remainder of the population randomly and clear the Hall of Fame.
            Thus previous Hall of Fame members are now part of the same selection, mutation and mating process again as the rest of the fold.  
              
            In most cases the Radiation Leak proved to be the more successful option.
            """
            )