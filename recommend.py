# import random # We will use this package for testing

class Feature:
    '''Class for features to be (hopefully) addressed by a computer.'''
    # Variables to keep track of each feature instance
    count = 0    # The number of features created
    features = {}  # Dictionary to store the features

    def __init__(self, name, desirability_score=0):
        ''' 
        The constructor for an feature. It is invoked with the class name and
        the name of the feature (i.e. Feature("gaming"))
        If the feature is already in the dictionary, ignore the instance.
        Otherwise, add it to the dictionary.
        Assign a sequential count to the instance and increment the class count.
        Add the new feature in dictionary.
        '''
        self.name = name.upper()
        if self.name not in Feature.features:
            self.count = Feature.count
            Feature.count += 1
            Feature.features[self.name] = self
            self.desirability_score = desirability_score

    def __repr__(self):
        ''' Print out a representation that evaluates to this feature.'''
        return f"Feature({self.name!r})"

    def __str__(self):
        ''' Return string version of the feature with its name and count.'''
        return f"<Feature ({self.count}): {self.name}>"

    def __eq__(self, other):
        ''' Overload == operator. Two features must match feature name. '''
        return self.name == other.name
    
    def set_desirability_score(self, score):
        '''Set the desirability score for the feature.'''
        self.desirability_score = score

    def get_desirability_score(self):
        '''Get the desirability score for the feature.'''
        return self.desirability_score

class Entertainment:
    '''Class for entertainments with features.'''
    # Variables to keep track of each entertainment instance
    count = 0    # The number of entertainments created
    entertainments = []  # List to store the entertainments

    def __init__(self, name, features):
        ''' Constructor for Entertainment with name and features.'''
        self.name = name
        self.features = features  # A list of Feature instances
        self.total_desirability = self.calculate_total_desirability()
        Entertainment.entertainments.append(self)
        Entertainment.count += 1

    def __repr__(self):
        '''Prints out code that evaluates to this entertainment.'''
        return f"Entertainment({self.name!r}, {self.features!r})"

    def __str__(self):
        '''Return string version of entertainment.'''
        return f"<Entertainment: {self.name} - Features: {', '.join(feature.name for feature in self.features)}>"

    def __eq__(self, other):
        '''
        Overload == operator. Two entertainments are equal if name and features match.
        '''
        return self.name == other.name and self.features == other.features
    
    def calculate_total_desirability(self):
        '''Calculate total desirability score of all features for the entertainment.'''
        total_desirability = sum(feature.get_desirability_score() for feature in self.features)
        return total_desirability
    
    def get_total_desirability(self):
        '''Get the total desirability score for the entertainment.'''
        return self.total_desirability

class Stance:
    ''' Class for importance and side on a given feature.'''
    # Variables to keep track of each stance instance
    count = 0    # The number of stances created
    stances = []  # List to store the stances

    def __init__(self, featurename, side='pro', importance='low'):
        '''
        Constructor for stance(). If the featurename is not already an feature, 
        create a new feature.
        '''
        if featurename.upper() not in Feature.features:
            Feature(featurename)
        self.feature = Feature.features[featurename.upper()]
        self.side = side.upper()
        self.importance = importance.upper()
        self.count = Stance.count
        Stance.count += 1
        Stance.stances.append(self)

    def __repr__(self):
        ''' Print out code that evaluates to this stance.'''
        return f"Stance({self.feature.name!r}, {self.side!r}, {self.importance!r})"

    def __str__(self):
        ''' Return string version of self '''
        return f"<Stance ({self.count}): {self.feature.name} [{self.side}:{self.importance}]>"

    def __eq__(self, other):
        '''
        Overload == operator. Two stances must match feature and side, though
        not importance.
        '''
        return self.feature == other.feature and self.side == other.side
    
    def copy(self):
        '''
        Clone a stance.  New stance has same feature, side, and importance.
        '''
        return Stance(self.feature.name, self.side, self.importance)
    
    def __hash__(self):
        '''
        hash() function for stance. 
        Need this for set() to remove duplicates.   
        Note: no need to include importance. Match is on feature and side only
        '''
        return hash((self.feature.name, self.side))
    
    def __lt__(self, other):
        ''' Comparison operator < to allow sorting stances. '''
        return self.feature.name + self.side < other.feature.name + other.side

class User:
    '''Class for users who have goals.'''

    # Variables to keep track of each user instance
    count = 0  # The number of users created
    users = []  # List to store the users

    def __init__(self, name):
        ''' Constructor for user with name.'''
        self.name = name
        self.goals = []
        self.count = User.count
        User.count += 1
        User.users.append(self)

    def __repr__(self):
        ''' Print out user so that it can evaluate to itself.'''
        return f"User({self.name!r})"

    def __str__(self):
        '''Return user as a string.'''
        return f"<User name: {self.name} ({self.count})>"
    
    def add_goal(self, goal):                                                                                                 
        '''Add goals (stances) without duplicates.'''                                                                         
        if goal not in self.goals:                                                                                            
            self.goals.append(goal)

    def pp(self):                                                                                                             
        '''Pretty print user information.'''                                                                                 
        result = f"Name:\t{self.name}"                                                                                        
        if self.goals:                                                                                                        
            result += f"\nGoals:\t{self.goals}"
        return result 

    def __eq__(self, other):
        '''
        Overload == operator.  Are two users equal by name and goals?
        '''
        same_name = self.name == other.name
        same_goals = self.goals == other.goals

        return same_name and same_goals

    def copy(self):
        ''' Clone the user, including name, and goals. '''
        new_user = User(self.name)                                                                                           
        new_user.goals = self.goals[:]                                                                                        
        return new_user

def likes(user, entertainment):
    '''Determines if an user likes a entertainment based on its feature stances.'''
    proresult = []
    conresult = []
    for goal in user.goals:
        for feature in entertainment.features:
            if goal.feature == feature:
                if goal.side == 'PRO':
                    proresult.append(feature)
                else:
                    conresult.append(feature)
    if proresult and conresult:
        return ("Both", proresult, conresult)
    if proresult:
        return (True, proresult)
    if conresult:
        return (False, conresult)
    else:
        return False

def prefers(user, entertainments):
    '''
    Determines which entertainments an user prefers based on its feature stances.
    '''
    preferred_entertainments = []
    for entertainment in entertainments:
        result = likes(user, entertainment)
        if isinstance(result, tuple):
            if result[0] == "Both" or result[0]:
                preferred_entertainments.append(entertainment)
        else:
            if likes(user, entertainment):
                preferred_entertainments.append(entertainment)
    return preferred_entertainments

def recommend(user):
    '''
    Makes a recommendation based not only the user's own preferences, but also
    the program's knowledge of what the user might actually want or need,
    without knowing it.
    '''
    preferred_entertainments = prefers(user, Entertainment.entertainments)

    recommended_entertainment = max(preferred_entertainments, key=lambda entertainment: entertainment.get_total_desirability(), default=None)

    return recommended_entertainment

# def main():
#     # Initializing Features
#     # Assume that these feature and its desirability score is a result from
#     # studying the market
#     print("\nInitializing Features:")
#     features = []
#     features.append(Feature('Dedicated Graphics Card', 4))
#     features.append(Feature('High-Resolution Display', 5))
#     features.append(Feature('Long Battery Life', 10))
#     features.append(Feature('Lightweight and Portable Design', 10))
#     features.append(Feature('Privacy Features', 8))
#     features.append(Feature('Fast Processor', 10))
#     features.append(Feature('Large Storage Capacity', 7))
#     features.append(Feature('High RAM Capacity', 6))
#     features.append(Feature('Excellent Audio Output', 8))
#     features.append(Feature('macOS', 4))
#     features.append(Feature('Touchscreen Display', 5))
#     features.append(Feature('Virtual Reality (VR) Ready', 2))
#     features.append(Feature('Eco-Friendly Materials', 2))
#     features.append(Feature('Customizable RGB Lighting', 4))
#     features.append(Feature('Expandable Storage Options', 2))
#     features.append(Feature('High-Refresh-Rate Display', 5))
#     features.append(Feature('Noise-Canceling Microphone', 2))
#     features.append(Feature('Gaming Keyboard and Mouse Compatibility', 3))
#     features.append(Feature('Cheap', 10))
#     features.append(Feature('Expensive', -10))
    
#     for feature in features:
#         print(feature)

#     # Initializing Stances
#     print("\nInitializing stances:")
#     stances = []
#     for _ in range(20):
#         feature = random.choice(features)
#         side = random.choice(['pro', 'con'])
#         importance = random.choice(['low', 'medium', 'high'])
#         stance = Stance(feature.name, side, importance)
#         stances.append(stance)
    
#     for stance in stances:
#         print(stance)
    
#     # Initializing Entertainments
#     print("\nInitializing Entertainments:")
#     entertainments = []
#     entertainments.append(Entertainment('Gaming Desktop', [features[0], features[1], features[5], features[6], features[7], features[8], features[13], features[14], features[15], features[16], features[17], features[19]]))
#     entertainments.append(Entertainment('Professional Workstation', [features[1], features[2], features[5], features[6], features[7], features[9], features[15], features[19]]))
#     entertainments.append(Entertainment('Student Laptop', [features[2], features[3], features[5], features[14], features[18]]))
#     entertainments.append(Entertainment('Entertainment Tablet', [features[1], features[3], features[5], features[8], features[10], features[14], features[18]]))
#     entertainments.append(Entertainment('Eco-Friendly Ergonomic Supercomputer', [features[0], features[1], features[2], features[5], features[6], features[7], features[8], features[11], features[12], features[15], features[19]]))

#     for i in range(5):
#         entertainment_name = f"Random_Entertainment_{i}"
#         num_features = random.randint(1, len(features))
#         entertainment_features = random.sample(features, num_features)
#         entertainment = Entertainment(entertainment_name, entertainment_features)
#         entertainments.append(entertainment)
    
#     for entertainment in entertainments:
#         print(entertainment)
    
#     # Initializing users 10 users with random feature stances
#     print("\nInitializing Users:")
#     users = []
#     user_names = ["User " + str(i) for i in range(10)]
#     for name in user_names:
#         user = User(name)
#         # Randomly select stances for the user's goals
#         num_goals = random.randint(1, len(stances))
#         user_goals = random.sample(stances, num_goals)
#         for goal in user_goals:
#             user.add_goal(goal)
#         users.append(user)

#     for user in users:
#         print(user)
    
#     print("\nUser Information:")
#     for user in users:
#         print(user.pp())
    
#     # Testing if each user likes a random entertainment
#     print("\nTesting likes() function:")
#     for user in users:
#         random_entertainment = random.choice(entertainments)
#         result = likes(user, random_entertainment)
#         if isinstance(result, tuple):
#             result = result[0]
#         print(f"{user.name} likes {random_entertainment.name}: {result}")
    
#     # Testing the prefers() function for each user using all entertainments
#     print("\nTesting prefers() function:")
#     for user in users:
#         print(f"\nUser: {user.name}")
#         print("Preferred Entertainments:")
#         preferred_entertainments = prefers(user, entertainments)
#         if preferred_entertainments:
#             for entertainment in preferred_entertainments:
#                 print(f"\t{entertainment.name}")
#         else:
#             print("No entertainment preferred.")
    
#     # Test recommend() function for each user
#     print("\nTesting recommend() function:")
#     for user in users:
#         print(f"\nUser: {user.name}")
#         recommended_entertainment = recommend(user)
#         if recommended_entertainment:
#             print(f"Recommended Entertainment: {recommended_entertainment.name}")
#         else:
#             print("No entertainment recommended.")

# if __name__ == "__main__":
#     main()