const timelineData = [
  {
    date: "2014",
    side: "left",
    title: "The Silkworm Published",
    description:
      "Rowling writes 'The Silkworm,' the second novel in the Cormoran Strike mystery series. The book includes a trans woman character who is portrayed as conspicuous, unable to pass, and is threatened with prison rape by the main character.",
  },
  {
    date: "October 2017",
    side: "right",
    title: "Likes Controversial Tweet",
    description:
      "Rowling 'likes' a tweet that links to a Medium article referring to a theoretical trans woman in a female space as 'a stranger with a penis.' The article argues that trans women are a threat to cisgender women in spaces like bathrooms.",
  },
  {
    date: "March 2018",
    side: "left",
    title: "'Men in Dresses' Tweet Liked",
    description:
      "She 'likes' and then unlikes a tweet referring to trans women as 'men in dresses' and implying trans rights are misogynistic. A spokesperson for Rowling claimed it was an accident, a 'middle-aged moment.'",
  },
  {
    date: "September 2018",
    side: "right",
    title: "Likes Tweet from Anti-Trans Feminist",
    description:
      "Rowling 'likes' a tweet by known 'trans-exclusionary radical feminist' (TERF) Janice Turner. The linked column argued that trans women are sexual predators, referring to them as 'fox[es] in a henhouse...identify[ing] as [hens].'",
  },
  {
    date: "December 2019",
    side: "left",
    title: "Support for Maya Forstater",
    description:
      "Rowling vocally supports Maya Forstater, a woman who lost her job after posting numerous anti-trans tweets. Rowling's tweet marks a shift toward openly voicing her views and brings her anti-trans sentiments to mainstream attention.",
  },
  {
    date: "June 2020",
    side: "right",
    title: "Mocks 'People Who Menstruate'",
    description:
      "In a tweet, Rowling mocks the inclusive phrase 'people who menstruate,' implying it erases the word 'women.' In follow-up tweets, she suggests trans activism is 'erasing the concept of [biological] sex' and the 'lived reality of women.'",
  },
  {
    date: "June 2020",
    side: "left",
    title: "Publishes 3,600-Word Manifesto",
    description:
      "Rowling publishes a lengthy essay on her website filled with what the article describes as myths and false transphobic stereotypes. She claims the trans rights movement offers 'cover to predators' and amplifies the debunked idea that teens are transitioning due to a 'social media trend.'",
  },
  {
    date: "August 2020",
    side: "right",
    title: "Returns Human Rights Award",
    description:
      "After the Robert F. Kennedy Human Rights organization repudiates her transphobic statements, Rowling returns the award she had received from them in 2019.",
  },
  {
    date: "September 2020",
    side: "left",
    title: "'Troubled Blood' Released",
    description:
      "Her new Cormoran Strike novel, 'Troubled Blood,' is widely criticized for featuring a villain who is a male serial killer preying on women by dressing as one, reinforcing the stereotype of trans women as deceptive predators.",
  },
  {
    date: "December 2020",
    side: "right",
    title: "Claims 90% Fan Agreement",
    description:
      "In an interview with Good Housekeeping, Rowling claims that '90 percent' of Harry Potter fans secretly agree with her anti-trans views but are afraid to speak out, stereotyping trans activists as a 'vicious mob.'",
  },
  {
    date: "July 2021",
    side: "left",
    title: "Targets Trans Twitter User",
    description:
      "Rowling tweets a screenshot of a post from a trans woman discussing her father’s death. Rowling taunts her to '[say] it to my face,' a tweet that the article notes contains an implicit threat of violence.",
  },
  {
    date: "November 2021",
    side: "right",
    title: "Promotes Gay/Lesbian Alliance Against Defamation",
    description:
      "Rowling promotes the UK-based LGB Alliance, a group accused by critics of promoting anti-trans policies under the guise of LGB advocacy. She praises a documentary on the group by comedy duo Simon Evans and Andrew Doyle.",
  },
  {
    date: "December 2021",
    side: "left",
    title: "Mobilizes Followers Against Trans Activists",
    description:
      "Rowling mobilizes her followers to dox three trans rights activists who protested outside her home, calling them the real bullies while her fanbase allegedly engages in doxxing and threats.",
  },
  {
    date: "March 2022",
    side: "right",
    title: "Insults Trans Olympic Medalist",
    description:
      "Rowling insults trans Olympic medalist Laurel Hubbard, calling her 'a man' and promoting the narrative that trans women are inherently a threat to cisgender women in sports.",
  },
  {
    date: "June 2022",
    side: "left",
    title: "Aligns with Matt Walsh",
    description:
      "Rowling aligns herself with far-right commentator Matt Walsh, who has a history of anti-trans rhetoric, praising his film about 'what is a woman.'",
  },
  {
    date: "October 2022",
    side: "right",
    title: "International Women's Day Tweets",
    description:
      "On International Women's Day, Rowling posts a series of tweets maligning gender-inclusive language, mockingly referencing Voldemort, and criticizing gender-inclusive legislation.",
  },
  {
    date: "August 2022",
    side: "left",
    title: "'The Ink Black Heart' Controversy",
    description:
      "Her latest Cormoran Strike book, 'The Ink Black Heart,' is criticized for featuring a character widely seen as a stand-in for Rowling herself: an anti-trans public figure who is 'canceled' by the internet on trumped-up charges of transphobia and is then murdered.",
  },
  {
    date: "December 2022",
    side: "right",
    title: "Funds Trans-Exclusionary Center",
    description:
      "Rowling funds a new domestic violence support center in Edinburgh that explicitly excludes trans women, framing it as offering 'women-centered and women-delivered care.'",
  },
  {
    date: "January 2023",
    side: "left",
    title: "Refers to Trans Women as Rapists",
    description:
      "Rowling posts that she is 'Deeply amused by those telling me I’ve lost their admiration due to the disrespect I show violent, duplicitous rapists,' which the article suggests is an implication that she considers all trans women to be such.",
  },
  {
    date: "March 2023",
    side: "right",
    title: "'The Witch Trials' Podcast",
    description:
      "In the podcast 'The Witch Trials of J.K. Rowling,' she calls the modern trans rights movement 'dangerous' and compares it to the Death Eaters from her books, who she says 'demonized and dehumanized those who were not like them.'",
  },
  {
    date: "February 2024",
    side: "left",
    title: "Donates to Anti-Trans Lobby",
    description:
      "Rowling donates £70,000 to For Women Scotland, an anti-trans political lobby campaigning to restrict the definition of 'women' in Scottish law to only cisgender women.",
  },
  {
    date: "March 2024",
    side: "right",
    title: "Denies Trans People in Holocaust",
    description:
      "On X (formerly Twitter), Rowling appears to deny that trans people were targeted during the Holocaust, calling the well-documented burning of books from Berlin's Institute for Sexual Research a 'fever dream.' She later attempts to separate 'trans-identifying people' from 'gay people' as victims of the Nazis.",
  },
  {
    date: "April 2024",
    side: "left",
    title: "Challenges Scottish Hate Crime Law",
    description:
      "On the day a new Scottish hate crime law takes effect, Rowling posts a thread spotlighting and misgendering several trans women, stating they 'aren’t women at all, but men,' and ends with the hashtag #ArrestMe.",
  },
  {
    date: "May 2024",
    side: "right",
    title: "Compares Trans Identity to Cultural Appropriation",
    description:
      "After deliberately misgendering a trans soccer manager, Rowling compares being transgender to racial cultural appropriation, writing, 'Do I get to be black if I like Motown and fancy myself in cornrows?'",
  },
  {
    date: "August 2024",
    side: "left",
    title: "Harasses Olympic Boxer",
    description:
      "Rowling contributes to the harassment of Olympic boxer Imane Khelif, a cisgender woman with naturally high testosterone levels, by calling her a 'male' and framing her match as a 'misogynistic assault.' Khelif later filed a lawsuit against Rowling and Elon Musk.",
  },
  {
    date: "April 2025",
    side: "right",
    title: "Celebrates Anti-Trans Court Ruling",
    description:
      "Following a UK Supreme Court ruling that denies trans women protection from discrimination—a lawsuit she helped fund—Rowling posts a picture of herself smoking a cigar with the caption, 'I love it when a plan comes together.'",
  },
  {
    date: "May 2025",
    side: "left",
    title: "Launches Anti-Trans Fund",
    description:
      "Rowling launches the J.K. Rowling Women’s Fund, an organization explicitly devoted to funding the legal challenges of 'transphobic activists and organizations under the guise of “women’s rights” activism.'",
  },
];

const timelineContainer = document.getElementById("timeline-container");
const modal = document.getElementById("timeline-modal");
const modalTitle = document.getElementById("modal-title");
const modalText = document.getElementById("modal-text");
const span = document.getElementsByClassName("close")[0];

timelineData.forEach((item) => {
  const timelineItem = document.createElement("div");
  timelineItem.className = `timeline-item ${item.side}`;

  const contentDiv = document.createElement("div");
  contentDiv.className = "content";

  const title = document.createElement("h2");
  title.textContent = item.date;

  const description = document.createElement("p");
  description.textContent = item.title;

  contentDiv.appendChild(title);
  contentDiv.appendChild(description);
  timelineItem.appendChild(contentDiv);

  timelineItem.addEventListener("click", () => {
    modalTitle.textContent = `${item.date}: ${item.title}`;
    modalText.textContent = item.description;
    modal.style.display = "block";
  });

  timelineContainer.appendChild(timelineItem);
});

span.onclick = function () {
  modal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
