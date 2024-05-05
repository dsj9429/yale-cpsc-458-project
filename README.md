# What is Entertainment Guru?

Entertainment Guru is a website designed to provide personalized recommendations for various types of media content, including TV shows, movies, educational material, sporting events, and more. Its goal is to help users make more informed decisions about what to watch or engage with by offering customized suggestions based on their preferences and moods.

# What does it do?

Entertainment Guru delivers customized recommendations to users based on how important the genre is and what genres they want to watch, how popular the movies are and what languages they want to watch it in. Users can decide which filters they want to apply and then get the name, year and the official poster for the movie that features the cast and the director. 

# How does one run Entertainment Guru?

Double clicking the HTML file should be sufficient to run the project. 

# What is interesting about it?

It gives the user a comprehensive list of movie to look forward to, spanning decades, languages and genres as they see fit. It uses The Movie Database (TMDB) API to get this list and this list is updated quite frequently.

# How is the decision explained?

The decision takes into account how popular the movies are, what languages the user wants to watch it in, how important the genre is to the user and the genres themselves. The user can decide which metrics they want to apply and which decision matters most to them. We thought of adding the importance filter for genres as it is a more important filter in the first place. 

# Constraints

Some constraints exist, e.g. the TV Movie filter for genres produces no output and is beyond our contrl in terms of manipulating via code as it is directly from the database itself, implying there are no such movies that fit the bill. 