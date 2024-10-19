Title: Responses to walking a very large poodle
Date: 2024-10-24 21:00
Category: Blog

<style>
figcaption {
  text-align: center;
}

video {
  display: block;
  margin: 0 auto;
}

img {
  display: block;
  margin: 0 auto;
}
</style>

*Shameless plug: [Archie is on Instagram](https://www.instagram.com/poky_poodle_puppy/).*

I was inspired by a recent [article posted on HN](https://news.ycombinator.com/item?id=39103142) about how people responded to seeing a man unicycling, to do a similar analysis of the way people responded to seeing me walking my partner's very large standard poodle. Over a two month period from 2024/7/13 to 2024/9/17, I recorded every verbal comment that I overheard about our dog Archie while walking him twice daily around Manhattan, as well as basic demographic information about the comment-giver. I excluded comments from conversations that I initiated, as well as any comments from people I knew. This is an analysis of the kinds of unprompted comments that New Yorkers make about our dog.

<figure>
  <img src="/images/poodle-walks/poodle/metro-north.jpg" alt="A poodle lays down across three seats on a Metro North commuter train."/>
  <figcaption><em>So majestic.</em></figcaption>
</figure>

Archie is the largest poodle that I have ever seen. He has a wonderful, calm, friendly temperament and is great with kids. He's the kind of dog that attracts a lot of positive attention, and he charms everyone he meets. My partner did a wonderful job training him. We joke that wherever Archie goes, he inspires people to get poodles of their own, and we know of several cases where that has happened for sure!

<figure>
  <video autoplay loop muted playsinline width=70%>
    <source src="/images/poodle-walks/poodle/wag.mp4" type="video/mp4">
  </video>
  <figcaption><em>He deserves everything he wants.</em></figcaption>
</figure>

Before meeting Archie, I didn't have much of an idea what poodles were like. The stereotype about poodles is that they are snooty and feminine. People did tend to assume that Archie was a girl at first, although I didn't record data on how often that happened. But what I've learned is that poodles are wonderful companion dogs. They are attentive, loyal, good-natured, and affectionate. They play in a very distinctive way, with lots of spinning. It's very cute. You should get a poodle.

<figure>
  <img src="/images/poodle-walks/poodle/helmets.jpg" alt="Two matching ebike helmet with decals of a poodle and the text: I have Standards."/>
  <figcaption><em>We're not crazy poodle people. Pay no attention to the matching helmets.</em></figcaption>
</figure>

Anyway, I made a bunch of graphs. Graphs are great.

# Demographics

I divided people by gender into Male / Female, and by age into Kid (18 or under), College (19-24), Adult (25-64), and Older (65+). This was based on my own judgment and is probably not perfectly accurate. I did not collect information on race or ethnicity, but the population was diverse. If I were unsure of which category to put someone, then I excluded that comment from the category breakdown.

In retrospect, I wish that I had divided Adult into more categories. Most of the comment-givers fell into Adult.

![](/images/poodle-walks/graphs/comments_by_age.png)
![](/images/poodle-walks/graphs/comments_by_gender.png)

I did not collect a base rate for how common each group was, so the data doesn't tell us if an individual from any particular group is more likely to comment then an individual from any other group. In other words, the way to interpret the charts is `P(Group=X | Comment)`, and I don't have `P(Group=X)`, so we can't calculate `P(Comment | Group=X)`.

Here is an example comment from each group:

| Gender | Age     | Comment                                                           |
|--------|---------|-------------------------------------------------------------------|
| M      | Kid     | Look Mommy, that doggy has a leaf on his head!                    |
| M      | College | I've never seen a dog like that, that's pretty cool man.          |
| M      | Adult   | How much for a haircut? Is he working for that?                   |
| M      | Older   | What a showdog. I hope you win!                                   |
| F      | Kid     | I've never seen a real poodle before!                             |
| F      | College | Can I take a picture? This is my fashion inspo for the day.       |
| F      | Adult   | I love poodles, he looks so fancy and he knows it.                |
| F      | Older   | Beautiful! Take this dollar and buy him something nice, I insist. |

# Topics

I grouped comments by topic. Name and Age were common topics but I rarely wrote down whether they asked, so I unfortunately don't have good data on those and have excluded them.

I mostly kept Archie's appearance constant while walking him: his haircut stayed the same over the entire period, and he always wore the same collar. However, about halfway through we did paint his toenails green, and starting around the same time he started sometimes wearing a tie. It is not meaningful to directly compare the frequencies of those topics with the others.

<figure>
  <img src="/images/poodle-walks/poodle/subway-tie.jpg" style="width: 70%;" alt="A man and a poodle on a subway platform. The poodle is wearing a necktie."/>
  <figcaption><em>He looks good in a tie.</em></figcaption>
</figure>

On one occasion, a large leaf fell down and landed on his head, becoming stuck there for some time. It was very cute. All of the leaf comments come from that one walk.

<figure>
  <img src="/images/poodle-walks/poodle/leaf-dog.jpg" style="width: 70%;" alt="A poodle with a leaf on his head walks outside."/>
  <figcaption><em>It's called fashion.</em></figcaption>
</figure>

![](/images/poodle-walks/graphs/topics.png)

These graphs are intuitive but a little tricky to explain. They show the Bayesian posterior probability distribution of group assuming a uniform prior distribution:

1) assume that `P(Group=X | Comment, Any Topic)` is equal for all `Group`, 2) observe `This Topic`, 3) the bar shows `P(Group=X | Comment, Any Topic, This Topic)` after applying Bayes' rule. In other words, these graphs show how much you should believe that a comment on a specific topic came from a certain group, if you initially assumed that a comment on any topic was equally likely to be from each group.

![](/images/poodle-walks/graphs/topics_by_age.png)

Kids were likely to remark on his size or his painted toenails. That makes sense because he was often bigger than they were, and they are closer to his feet then adults. All age groups were about equally likely to mention him being a poodle. College students were by far the most likely to ask for a photo. Adults were the most concerned about the cost and time spent grooming him (I can relate!). Older people were likely to compare him to an animal or ask if he was a showdog.

![](/images/poodle-walks/graphs/topics_by_gender.png)

*There is one fewer observation for toenails by gender than by age, because that comment was by a boy and girl and I didn't record which kid commented on his nails.*

Most topics were pretty balanced between genders. Only women commented on his painted toenails. Men were more concerned with his haircut and the cost of grooming and more likely to ask if he was a showdog. I do intuitively consider those to be more masculine topics.

Here is an example comment from each topic:

| Topic              | Comment                                         |
|--------------------|-------------------------------------------------|
| Compliment         | That is the best dog I've ever seen.            |
| Breed              | Poodle right? Standard?                         |
| Size               | *(to child)* That dog is bigger than you!       |
| Comparison         | That's a horse, can I ride it?                  |
| Photo              | Mind if I take a photo with your beautiful dog? |
| Haircut            | Sickest haircut I've ever seen.                 |
| Grooming Cost      | Grooming bills must be high!                    |
| Grooming Frequency | How often do you get him trimmed?               |
| Showdog            | Wow! A showdog.                                 |
| Toenails           | Oooh, he has painted toenails!                  |
| Tie                | Love your dogs tie.                             |
| Leaf               | Excuse me, your dog has a leaf on his head.     |

# Breed Terminology

I recorded the most specific breed that people used to describe Archie. There are three types of poodle in the AKC classification: Toy Poodle, Miniature Poodle, and Standard Poodle. Archie is a large Standard Poodle.

![](/images/poodle-walks/graphs/breed_by_age.png)

As age increases, people are (probably) more likely to use "Standard Poodle".

*We don't have enough data for significant results. A Fisher's exact test produces p=0.3443 for the null hypothesis that all four samples are from the same distribution.*

![](/images/poodle-walks/graphs/breed_by_gender.png)

Woman are (probably) more likely to use "Standard Poodle". There is (probably) no difference is how often men and women use "Poodle". I think that people generally know what a poodle is but mostly just say "dog". I personally tend to say "dog" when complimenting other dogs because I am bad at recognizing breeds and don't want to offend.

*Again, we don't have enough data for significant results. A Fisher's exact test produces p=0.2606 for the null hypothesis that both samples are from the same distribution.*

It was pretty common for people to think he was a poodle mix. I didn't collect data on what they thought he was mixed with, but the most common guess seemed to be Great Dane.

We often call Archie a "Royal Standard Poodle", which is not an official AKC breed, but is colloquially a thing that very big poodles can be called. No one else ever called him a royal standard poodle. Although in fairness, we haven't seen any other royal standard poodles in Manhattan.

# Compliments

I recorded what compliment words people used when commenting on Archie.

![](/images/poodle-walks/graphs/compliments.png)

*As I wrote this, we read him the list of compliments in order of descending frequency. He enjoyed it greatly.*

Because there was a long tail of compliments, I restricted these graphs to only popular compliment words. The interpretation is similar to the topic graphs; these are Bayesian posterior probability distributions. `P(Group=X | Comment, Any Compliment)` includes the rare compliments that are not included in the graph.

To restate, these graphs show how much you should believe that a comment with a specific compliment came from a certain group, if you initially assumed that a comment with any compliment was equally likely to be from each group.

![](/images/poodle-walks/graphs/compliments_by_age.png)

Kids were very likely to call him "big". College students favored "cute", "pretty", and "tall". Adults liked "gorgeous" and "nice". Older people went with "beautiful", "fancy", and "handsome". All of these are great words to describe Archie.

![](/images/poodle-walks/graphs/compliments_by_gender.png)

I'm not surprised that "gorgeous", "cute", "pretty", and "fancy" predicted women, but I can't get over how strongly "nice" predicted men.

# Comparisons

Archie is a very large poodle, and he did not have a traditional poodle haircut during the comment period. People often compared him to another animal, or more generally said that he was like something else.

![](/images/poodle-walks/graphs/comparisons_grouped.png)

*Similar comparisons have been grouped together.*

We were going for horse--he has a mane--but the opinions are delightfully varied! I have a feeling that this will vary based on haircut and season, but this is what we got for his current haircut during the summer.

The unique comparisons were a lot of fun to hear as well.

The person who said Na'vi actually said "Avatar", because no one remembers anything about Avatar besides the title.

<figure>
  <img src="/images/poodle-walks/poodle/navi.png" alt="Two images side-by-side. The left is a poodle wearing a bandana that says Let's Sniff Butts. The right is Jake Sully from the movie Avatar."/>
  <figcaption><em>They're the same picture.</em></figcaption>
</figure>

We were confused by "Pokemon" until we learned about Furfrou, the poodle Pokemon. Possible Halloween costume for Archie? We just have to choose [which trim](https://bulbapedia.bulbagarden.net/wiki/Furfrou_(Pok%C3%A9mon)#:~:text=Forms-,Furfrou%20has%20ten%20different%20forms,-named%20after%20the).

<figure>
  <img src="/images/poodle-walks/poodle/furfrou-trims.png" alt="The 10 different haircuts for Furfrou, the poodle pokemon."/>
  <figcaption><em>I think that Archie could pull off the Dandy trim.</em></figcaption>
</figure>

# Comment Rate

I tracked how long I walked Archie each day, which lets me calculate the rate that he got comments.

![](/images/poodle-walks/graphs/comments_rate_hist.png)

I unfortunately did not track time-of-day. I didn't walk Archie at very consistent times and that probably accounts for some of the variation in comment rate. But there is an interesting effect for day-of-week:

![](/images/poodle-walks/graphs/comments_rate.png)

The reason that Saturdays are so much higher is that that's when we take him with us to the grocery store and the farmers market. People absolutely love him at the farmers market. I think that it's an environment where people are already curious, social, and relaxed, and so we get a lot of comments.

# Conclusion

That's about it! Thank you for reading this silly post about our poodle.

<figure>
  <img src="/images/poodle-walks/poodle/nap-time.jpg" alt="A poodle napping on the couch with his head resting on a pillow."/>
  <figcaption><em>All tuckered out.</em></figcaption>
</figure>
    
*Thank you to Veronica Lopez for many things, including providing feedback on drafts of this post. All mistakes are my own.*
