# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

From what I understand two ways software like Spotify recommends songs is based on listening history, matching commonly
  liked music with eachother. And suggesting songs based on the attributes of the songs themselves. 

For my project I will assign weights using entropy based scoring. The algorithm will check the users listening history and
  determine which rules like 'genre, mood, energy, and tempo' to determine which rule each song has most in common.
  from there, the scoring will put more weight into the rules that are more common. It will then recommend songs that 
  match the different rules based on priority. 

Some prompts to answer:

- What features does each `Song` use in your system
  - it will store and rank songs based on genre, mood, energy, tempo, valence, accousticness, and dancibility
- What information does your `UserProfile` store
    User profile will store the rank of importance for each user based on their history.
- How does your `Recommender` compute a score for each song
    Using entropy-based scoring it will determine which attribute is most common in the users song history and give it higher priority
- How do you choose which songs to recommend
    Pick songs based on which attribute the user favors

A potential bias is that the user wont experience new music outside of their prefered attributes.

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

py src/main.py
Loaded 20 songs from data/songs.csv

Top recommendations:

Sunrise City - Score: 9.90
Because: Genre 'pop' matches (weight: 3.0); Mood 'happy' matches (weight: 2.0); energy: 0.82 vs 0.80 (weight: 5.0)

Gym Hero - Score: 7.35
Because: Genre 'pop' matches (weight: 3.0); energy: 0.93 vs 0.80 (weight: 5.0)

Rooftop Lights - Score: 6.80
Because: Mood 'happy' matches (weight: 2.0); energy: 0.76 vs 0.80 (weight: 5.0)

Funk It Up - Score: 4.95
Because: energy: 0.81 vs 0.80 (weight: 5.0)

Night Drive Loop - Score: 4.75
Because: energy: 0.75 vs 0.80 (weight: 5.0)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:


Building this recommender taught me that turning listning data and user history into song predictions is about identifying patters and weighing what attributes matter most. I knew that songs could be classified into genres and artists but I now know how many different attributes are in each song. By analyzing the users listening history and searching the database you are able to match songs based on patterns. The difficult part is determining how to balance these patterns and avoid biases. 

This system definitely has many biases and pittfalls but with more time you could iron them out and create a more detailed, complex recommendation algorithm.


