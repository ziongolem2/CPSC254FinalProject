Part 1( What & why) : 



Part 2 (Iterations (≥3 versions, ~75–150 words each):

-- v.1 BASELINE --
Change: Thinking of this as going from 0 to 1, I implemented my main system prompts that provided the foundatiion for how the CineBot AI model will behave in the appT. My prompt implements 4 rules: Ask at least one clarifying question before recommending a movie, always include a movie title, genre, reasoning, and streaming platform in every recommendation, maintain a friendly conversational tone, and ask follow up questions instead of just dumping a list if the user doesn't like the recommendation.

Motivating example:A motivating example that led me to think v1 would be a good start place for my prompts would be a scenario where a user tells the AI: "I want to watch a hilarious movie tonight", and then the bot would just provide the user with seemingly random movie reccomendations that are not personalzied, or provide any garuantee of listed eval metrics I defined such as always including a streaming platform, follow up questions, etc. 

Delta: The metric is the baseline with no before and after comparison. However, there it has an overall score of 68.4%. Meaning 13 out of 19 test cases passed in the eval.

Conclusion: Baseline, metric is neutral and I'm unsure how good or bad the model performs. 


-- VERSION 2. --
Change: I carefully constructed and implemented an additional new rule (Rule #5) into the system prompts for both 'app.py' and 'eval.py'. This rule states "As soon as you have enough information to make a relevant recommendation (genre/mood and streaming platform), immediately provide a recommendation and avoid asking unecessary follow-up questions. 

Motivating example: Though there were serveral failing cases (5 total) that motivated this change, Test Case 03 motivated this change the most as it was the most obvious. Essentially, it was most clear that by adding this change, it would most likely fix this test case fail and likely the other failing test cases too. In tc03, we can clearly see that the user had already provided the AI chatbot with a desired genre/mood (classic romance), a streaming platform (HBO Max),and also a response to at least one clarifying follow up question,  yet the AI still asked an additional uncessary follow up question ("Just to narrow it down a bit more, are you in the mood for something more light-hearted or something a bit more dramatic?"). The AI asked this uneeded question instead of recommending a movie to the user, despite already having every metric it needed.

Delta: Metric before: 68.4% (13/19). Metric After: → 94.7% (18/19)! Huge positive improvement of 26% increase in accuracy on the evaluation!

Conclusion: After performing the system prompt changes, the metric significantly improved because 5 out of the 6 total failures were all being caused by the same core issue, in which the AI model (CineBot) would keep asking additional unecessary follow up questions despite already having the information it needed from the user to recommend a movie. By adding the new additional rule #5 to the system prompt, it pushed CineBot to immediately provide the user with a movie recommendaition as soon as it collected enough prefrence information from the user, and made it a clear stopping point expectation in the sytsem prompt. This prompt change directly fixed and turned those 5/6 failing cases into passes, as the expected output (movie recomendation with the user's preferences) was now satisified. For my next eval, I'm aiming to fix the last error, test case 013. The error appears to be caused by the AI model still asking an additional unecessary follow up question but for a different reason in this scenario.


-- VERSION 3. --
Change:
Motivating example:
Delta:
Conclusion:




Part 3 (Code walkthrough):



Part 4 (AI disclosure & safety):
