# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
VibeMatch 1.0
Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---
VibeMatch 1.0 is a content-based music recommender designed to suggest songs from a small catalog based on a user's preferred genre, mood, and energy level. It assumes the user can describe their taste in terms of their favorite genre, current mood, and how high-energy they want the music to feel. The system is built for classroom exploration, not real users, and works best when the user's preferences closely match songs already in the catalog.


## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song in the catalog carries a set of attributes — genre, mood, energy, clarity, acousticness, loudness, and duration — and every user has a taste profile that describes what they're looking for. To find the best matches, the system compares each song's attributes to the user's preferences and awards points: the most points go to mood alignment, followed by how close the song's energy feels to what the user wants, then clarity (how bright or clean the song sounds), genre match, and a small bonus for acoustic songs. Loudness and duration are loaded from the catalog but not currently used in scoring. Each song gets a total score, and the top results are returned in order from best match to worst. Compared to the starter logic, the main addition was a weighted scoring system that can be tuned — mood, energy, genre, and clarity each have their own adjustable weight — so the same user profile can produce different rankings depending on which feature the system prioritizes most.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains 18 songs spanning 13 genres including pop, lofi, rock, jazz, hip-hop, blues, classical, country, reggae, r&b, soul, electronic, and synthwave. Moods represented include happy, chill, intense, relaxed, focused, moody, dark, confident, nostalgic, melancholic, peaceful, uplifting, romantic, and soulful. Eight songs were added to the original 10-song starter dataset to improve genre and mood diversity. However, most genres have only one song each, so users outside of pop or lofi will rarely see a genre bonus in their results. Moods like nostalgic, melancholic, and soulful have no matching user profile in the current system, meaning those songs can never earn a mood bonus.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for users with strong, clear preferences — particularly pop and lofi listeners, since those genres have multiple songs in the catalog and real competition for the top spots. Two patterns emerge clearly in the scoring: energy closeness consistently separates good matches from weak ones even when mood or genre don't align, and category stacking — when a song hits mood, genre, and energy bonuses all at once — pulls it far ahead of partial matches, which is exactly the behavior a recommender should have. The Deep Intense Rock profile was the clearest win — Storm Runner ranked #1 across all three weight experiments because it stacked every major bonus simultaneously, matching intuition exactly. In general, the system is most trustworthy when the user's profile overlaps with several songs at once rather than relying on a single feature to carry the score.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One weakness of the algorithm is how the clarity score structurally penalizes low-energy users, regardless of how well a song matches their other preferences. Because the catalog's highest-clarity songs are all high-energy, loud tracks, a Chill Lofi user who perfectly matches on mood, genre, and energy will still lose points on clarity to songs they would never want. This creates a hidden bias where "bright-sounding" is quietly treated as "better," nudging every user toward high-energy songs no matter what their profile says. A fairer design would make clarity relative to the user's energy target, so quiet songs score high on clarity for users who prefer them.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected.

Prompts:

Which user profiles you tested
What you looked for in the recommendations
What surprised you
Any simple tests or comparisons you ran
No need for numeric metrics unless you created some.

Three user profiles were tested — High-Energy Pop, Chill Lofi, and Deep Intense Rock — and results were checked by reading the score breakdowns printed next to each recommendation. The system behaved as expected for strong matches like Storm Runner under Deep Intense Rock, which hit mood, genre, energy, and clarity simultaneously and dominated every weight configuration. The most surprising finding was that swapping weights between mood, energy, and genre produced no score change for perfectly-matched songs, because the points just shifted between buckets without changing the total — weight experiments only matter when songs are partial matches. Three weight configurations were compared side by side: Default (where mood is weighted highest at 3.0, making emotional feel the strongest signal), Energy-First, and Genre-Dominance — and the only profile where rankings visibly shifted was High-Energy Pop, where Genre-Dominance pushed Gym Hero above Rooftop Lights by rewarding its pop genre match more heavily.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- Make clarity relative to the user's energy target instead of treating high clarity as universally better, which would fix the bias against low-energy listeners.
- Add tempo and danceability as scoreable preferences so users can express a fuller picture of their taste.
- Group similar moods together ("chill," "relaxed," "peaceful") instead of exact-match only, so the system is less brittle when a user's mood doesn't match a catalog label exactly.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this made me realize that recommender systems are not neutral. Every weight and every feature choice quietly favors certain users over others, even when that is not the intention. The most unexpected thing I found was that changing the weights between experiments produced no score difference for perfectly matched songs, which showed me that weight tuning only matters when songs are partial matches. It also changed how I think about apps like Spotify. What feels like a personalized recommendation is really just a scoring function running over a catalog, and the biases baked into that function shape what music people ever get exposed to.