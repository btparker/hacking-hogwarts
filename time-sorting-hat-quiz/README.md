# Time - The Ultimate Harry Potter Quiz: Find Out Which House You Truly Belong In

[http://time.com/4809884/harry-potter-house-sorting-hat-quiz/](http://time.com/4809884/harry-potter-house-sorting-hat-quiz/)

## Plan of action

- [ ] Research sources for the 21 question quiz
- [ ] Develop a scraper for the quiz
- [ ] Brute force scrape ALL possible results (21 * 7 = 147)
- [ ] Using Tensorflow and a subset of the data, see if an accurate model can be created
- [ ] Using scikit and a subset of the data, create a Generalized Linear Model through traditional means
- [ ] Evaluate
- [ ] Document


## Notes

#### From the main page:

To accomplish this, we worked with the researchers to develop a 21-question quiz compiled from <mark>several well-established scientific personality surveys</mark>, choosing questions that related to prevalent themes in the books. Over the past several weeks, we recruited hundreds of Harry Potter fans to take this survey on behalf of 20 different characters from the books, five from each House. The tens of thousands of data points we gathered gave us a detailed portrait of how different personality traits correspond to the personalities of members of each of the four Houses.


The 21 questions in the Harry Potter personality quiz are drawn from both the Big Five test and a handful of other well-studied personality inventories that measure other traits that are commonly seen in the Harry Potter novels, like "courage" and "humility." The survey was assembled by <mark>Cambridge psychologists Friedrich Götz and Joe Scott</mark> in collaboration with TIME.


When you take this quiz, we analyze your responses and compare them to how closely they match each of the four Houses, using a [standard statistical model](https://en.wikipedia.org/wiki/Generalized_linear_model) (ed note: the Generalized Linear Model) designed to measure the relationship between datasets. <mark>Your affinity for each House is measured independently</mark>, so it's very possible that your personality closely matches two different Houses — a phenomenon that the Sorting Hat itself is well familiar with, given its history of waffling between two Houses when a character's personality isn't an obvious match for one. 


#### From the results page:

"Thank you for having completed the questionnaire. You have greatly helped to advance our research."

"The present investigation seeks to analyze the geographical distribution of an array of personality traits (e.g., courage, Machiavellianism, in-group loyalty) across the United States. Moreover, we are interested whether these personality traits, when averaged across all residents of a certain area, relate to indicators of economic performance, such as state-level average income or start-up rates. This is part of a rather young field of research in geographical psychology."

"Traditionally, psychologists have compared samples across countries without looking at the diversity within those countries. Geographical psychology aims to bridge the gap by examining intra-cultural differences across regions. Next, the consequences of these differences on more visible levels, such as regional economic performance, are explored. The current study advances this line of research by looking at new concepts (such as courage) that have not been studied in geographical psychology before and thus foster a more in-depth understanding of the relevant dimensions of regional differences."

"If you have any further questions regarding our research, please do not hesitate to contact us at <a href="mailto:pottercam.research@googlemail.com">pottercam.research@googlemail.com</a> or visit the <a href="http://www.psychol.cam.ac.uk">website of the Department of Psychology at the University of Cambridge</a>."


## Hacking

Found the unminified script at [http://time-static-shared.s3-website-us-east-1.amazonaws.com/interactives/harry_potter_house/script.js](http://time-static-shared.s3-website-us-east-1.amazonaws.com/interactives/harry_potter_house/script.js)

