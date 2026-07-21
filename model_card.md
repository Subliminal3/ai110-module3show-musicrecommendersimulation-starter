# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **SongScraper V0.0000003**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
This recommender generates songs based on the users listen history. Giving them recommendations based on the attributes they most listen to.
- What assumptions does it make about the user  
This program makes assumptions that the user wants to stay within their comfort zone. Only recommending songs similar to what they have listened to in the past
- Is this for real users or classroom exploration  
I would say this is more for classroom exploration. It is too narrow and there are way too many factors to consider for real user to find it useful.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.) 
All attributes of the song are considered. The most common attribute gets more weight. 
- What user preferences are considered  
The algorithm takes into account the preferences from the users listening history. Only recommedning songs based on what they like to listen to.
- How does the model turn those into a score  
It checks which attribute the user listens to most often and gives songs with that attribute more weight.
- What changes did you make from the starter logic  
I had the AI implement an entropy-based scoring algorithm that changes weights based on common attributes.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
There was only 20 songs in my catalog. A small dataset
- What genres or moods are represented  
A variety of genres and moods are represented from pop to jazz to lowfi. The songs vary in valence, tempo, and energy
- Did you add or remove data  
I used the AI to double the dataset
- Are there parts of musical taste missing in the dataset  
It would be extremely difficult to include every genre in a dataset. Thats why I think songs with no genre are often classified as Indie or Folk.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
The most reasonable results came from the users that like a specific genre. The pop user was recommended high energy pop songs and the lofi user was recommended low tempo chill songs.
- Any patterns you think your scoring captures correctly  
Tempo is often a good indicator of preference and the system is able to match the tempos correctly. That being said it may put too much weight into tempo.
- Cases where the recommendations matched your intuition  
The obvious or easy user recommendations didnt surprise me. A pop lover is recommended pop songs. A rock lover is recommended rock songs.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The system prioritized exact categorical matches. Mood/genre only score if they match exactly. A user who likes Rock doesnt get any points for Metal.

No negative weighing. If a user doesnt like a certain type of music it doestn take that into account and might recommend a song with those attributes.

Small dataset. The program was only tested on a dataset of 20 songs. If a genre takes up most of that dataset then it will be biased toward that genre. 

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Using the user_extreme_values profile I was surprised to see the algorithm averaged out those values and recommended songs in the middle of the extreme values.

Prompts:  

- Which user profiles you tested  
user_extreme_values
  This user was reccommended the midpoint between their extreme attribute values
user_high_energy_sad
  This user was recommended songs with simmilar tempo, energy, and Valence. Tempo was prioritized most since it was high energy
user_high_energy_pop
  Similar to high energy sad this user was recommended songs based on tempo, energy, and valence.It had some similar songs but also some different once since the tempo was lower
user_chill_lofi
  This user was recommended all lowfi songs. Slow tempo and low energy
user_deep_intense_rock
  This user was recommended a wide variety of songs. The tempo recommendation was wide so it gave songs from different categories.


No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
Broaden the scoring system. Find a more accurate way to weigh each attribute. Maybe test it on real songs so its easier to understand. Also a larger dataset helps
- Better ways to explain recommendations  
I had to limit the explination the AI created for me since it becomes unreadable if it displays all the weights. There is probably a better format that explains the reasons each weight was given in plain english.
- Improving diversity among the top results  
Tempo, energy, and valence took too much priority in my Algorithm. I could revise my methods to spread the preferences. Also a larger dataset
- Handling more complex user tastes
The best way I can think of is focusing on what a majority of the songs have in common and recommending songs based on that. Or take the average of the attributes and make recommendations that way.  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
They work kind of how I expected them to, but i didnt realize there were so many attributes for each song, I dont even know what valence is.
- Something unexpected or interesting you discovered 
The complexity of a good song recommending algorith like Spotify's. I know theirs is heavily influenced by the users "liked songs".
- How this changed the way you think about music recommendation apps 
It was interesing to see behind the curtain and it explains why some song recommendation algorithms are so much better than others. The more factors that are accounted for the better the results. 
