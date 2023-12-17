import OpenAIClient
import datetime
from tfidf_query_v2 import *

##########################################################################
# Run the TF-IDF Retrieval system
##########################################################################

test_queries = [
    "I'm in the mood for a gripping novel that combines mystery and historical elements, can you recommend a book that has a similar blend of intrigue, history, and maybe a touch of the mysterious?",
    "I'm on the lookout for a new book to dive into, can you recommend perhaps something with a mix of magical realism, post-apocalyptic settings, or gripping survival stories?",
    "I'm an avid reader who loves immersive fantasy worlds, can you suggest a book that transports me to a richly detailed fantasy realm with complex characters and epic storytelling?",
    "I'm in the mood for a thought-provoking science fiction novel, can you recommend a book with intricate world-building and mind-bending concepts?",
    "I love historical fiction with a strong focus on characters and vivid settings, any recommendations for a compelling historical novel?",
    "As a fan of fast-paced thrillers I'm looking for my next gripping read. Any suggestions for a psychological thriller or mystery that keeps you on the edge of your seat?",
    "I'm in the mood for a heartwarming coming-of-age story, any recommendations for a novel with a memorable protagonist navigating the challenges of growing up?",
    "I enjoy exploring different cultures through literature, can you recommend a book that provides a rich cultural experience and deep insights into a particular society?",
    "I'm a fan of dystopian fiction, any recommendations for a thought-provoking dystopian novel that offers a unique take on a possible future?",
    "I love a good laugh and science fiction, any recommendations for a witty and humorous novel that will keep me entertained?",
    "I'm looking for a captivating non-fiction book can you suggest a compelling non-fiction work that combines research with a compelling narrative?",
    "I'm a sucker for romance novels that are both heartwarming and smart, any suggestions for a romance novel that balances emotion and intellect?",
    "I have a fascination with mysteries set in unique locations, can you recommend a mystery novel with a distinctive setting and a compelling detective?",
    "I'm a science enthusiast and loved books by Stephen Hawking, can you recommend a book that explores complex scientific concepts in an accessible and engaging way?",
    "I enjoy epic adventures with strong female protagonists, any recommendations for a fantasy or science fiction novel with a compelling heroine and a thrilling plot?",
    "I'm a history buff who's been engrossed in books like 'The Guns of August,' and 'The Rise and Fall of the Third Reich.' Can you suggest a meticulously researched historical account or narrative that provides deep insights into a specific period?",
    "I love exploring the intricacies of the mind through literature. 'One Flew Over the Cuckoo's Nest,' and 'The Catcher in the Rye' were thought-provoking. Any recommendations for a novel that delves into the complexities of mental health and identity?",
    "I'm a fan of classic literature, having enjoyed 'Jane Eyre,' and 'Crime and Punishment,' can you recommend a lesser-known classic novel that offers profound insights and timeless themes?",
    "I'm interested in exploring cultural diversity through contemporary fiction. Books like'The Namesake,' and 'The Joy Luck Club' have resonated with me. Any suggestions for a novel that explores cultural intersections in a modern context?",
    "I'm in the mood for a riveting space opera. 'Leviathan Wakes,' and 'Starship Troopers' are among my favorites. Can you recommend a science fiction novel set in space with a captivating storyline and well-developed characters?",
    "I enjoy political thrillers that are both intelligent and suspenseful. 'All the President's Men,' and 'The Manchurian Candidate' were gripping. Any recommendations for a political thriller with a contemporary or historical setting?",
    "I love exploring the natural world through literature. 'The Sea Around Us,' and 'The Sixth Extinction' have been fascinating reads. Can you suggest a book that combines nature writing with scientific exploration and environmental themes?",
    "I'm a fan of short stories that pack a punch. 'Dubliners,' and 'The Things They Carried' are some of my favorites. Any recommendations for a collection of short stories that are both diverse and impactful?",
    "I'm on the hunt for a new book and wondered if you could help. I'm in the mood for a captivating historical fiction novel with a strong sense of place and well-developed characters. Think 'The Nightingale' or 'All the Light We Cannot See.' Any recommendations that fit the bill?",
    ]

def testCollection():
    print('Initializing...')
    with open('tfidf_dict_4_200.json', 'r') as file:
        data = json.load(file)
    print("Loaded", len(data['book dict']), "books")

    stemmer = PorterStemmer()
    vocab = np.array(data['vocabulary'])
    table_idf = np.array(data['IDFs'])
    table_tfidf = reverse_lists(data['TFIDFs'])
    book_dict = data['book dict']
    titles = list(book_dict.keys())
    print('Finished Loading!')

    i = 0
    for query in test_queries:
        try:
            relevance_results = comp_relevance(query, vocab, table_idf, table_tfidf, stemmer)
            if relevance_results == False:
                for _ in range(10):
                    print("asis_TF-IDF", i, False, datetime.datetime.now(), "TF-IDF", "No Result", sep="\t")
            else:
                results = rel_results(relevance_results, titles, book_dict)
                for book in results:
                    # Ask OpenAI to verify this as a hit or not
                    chat_completion = OpenAIClient.checkRecomendation(book['title'], "author", query, book['content'])
                    print("asis_TF-IDF", i, chat_completion.choices[0].message.content.lower().find("yes") > -1, datetime.datetime.now(), "TF-IDF", book['title'], sep="\t")
        except Exception as e:
            print(e)
        i += 1

def main():
    testCollection()

if __name__ == '__main__':
    main()
