from __future__ import division
import re
import threading
import time

class SummaryTool(object):

    # splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    # splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        if (len(s1) == 0  or len(s2)) == 0:
            return 0

        # normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # remove all non-alphbetic chars from the sentence
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_senteces_ranks(self, content):

        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):
	global summary
        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        threads = [None] * len(paragraphs)
        for i in range (len(threads)):
        	threads[i] = threading.Thread(target = self.get_best_sen_parallel,args = (paragraphs[i], sentences_dic))
        	threads[i].start()
        	
        for i in range(len(threads)):
    		threads[i].join()
        
        return ("\n").join(summary)
        
    def get_best_sen_parallel(self,p, sentences_dic):
    	sentence = self.get_best_sentence(p, sentences_dic).strip()
    	if sentence:
    		summary.append(sentence)
    		
def main():

    title = """
    Swayy is a beautiful new dashboard for discovering and curating online content [Invites]
    """

    content = """
    BA was designed by Schneier at the Cambridge Security Workshop in December 1993 to replace the Data Encryption Standard (DES). It has been widely analyzed and gradually accepted as a good and powerful encryption algorithm offering several advantages among which is its suitability and efficiency for implementing hardware. It is also unpatented and therefore does not require any license. The elementary operators of BA algorithm comprise table lookup, addition, and XOR with the table being made up of four S-boxes and a P-array. Based on Feistel rounds, BA is a cipher with the F-function design being a simplified version of the principles employed in DES to provide similar security, faster speed and higher efficiency in software [1]-[4].
Information security remains a challenge. As such, ciphers appropriate for the security of specific applications need to be developed. Algorithms and performance security of a given algorithm is dependent on various parameters including size of key and block, diffusion, and confusion properties [5].
The current cipher design is still guided by the principles of confusion and diffusion. Confusion is designed to hide the relationship between the plaintext and ciphertext. This will discourage the attacker who attempts to locate the key using ISBN: 978-1-4673-5256-7/13/$31.00 ©2013 IEEE cipher text. On the other hand, diffusion is supposed to disseminate the plaintext statistics through the ciphertext in order to discourage the attacker attempting to locate the plaintext using the ciphertext statistics. If a cipher has a good diffusion property, then flipping one bit of the input changes every bit of the output with a probability close to 1⁄2 [6]- [11].
In this paper we present the results of the analysis on the BA in terms of avalanche effect and correlation coefficient. Applying avalanche effect analysis on the BA helps to identify that it satisfies Shannon’s diffusion property, while applying correlation coefficient statistical analysis on the BA is to identify that it satisfies Shannon’s confusion property.
This paper is organized as follows: section II describes BA; section III describes the security analysis that includes avalanche effect and correlation as well as providing an explanation of the data type that used in this analysis, and section IV provides Results of Analysis; finally, section V provides the conclusion and makes recommendations for future studies.
Data encryption commences with a 64-bit block element of plaintext morphing into a 64-bit ciphertext. First, the 64-bit segment is split into two equal segments that form the base of the BA. The next step is the implementation of the exclusive- or-operation (XOR) that is carried out between the first segment of the 32-bit block (L) and the first P-array. The 32-bit data obtained from step 2 is moved to the F function which permutes the data into a 32-bit block segment, which is XOR'ed with the second segment of the 32-bit block (R) of the 64-bit plaintext split. Upon completion of the XOR operation, the 32-bit segments, L and R, are exchanged for future iterations of the BA. Fig. I illustrates the architecture of the BA with 16 rounds. The input is an element of 64-bit data; X, which is divided into two 32-bit halves: XL and XR. Data Decryption is similar to Encryption data, but P1, P2... P18 are used in the reverse order.
BA was designed by Schneier at the Cambridge Security Workshop in December 1993 to replace the Data Encryption Standard (DES). It has been widely analyzed and gradually accepted as a good and powerful encryption algorithm offering several advantages among which is its suitability and efficiency for implementing hardware. It is also unpatented and therefore does not require any license. The elementary operators of BA algorithm comprise table lookup, addition, and XOR with the table being made up of four S-boxes and a P-array. Based on Feistel rounds, BA is a cipher with the F-function design being a simplified version of the principles employed in DES to provide similar security, faster speed and higher efficiency in software [1]-[4].
Information security remains a challenge. As such, ciphers appropriate for the security of specific applications need to be developed. Algorithms and performance security of a given algorithm is dependent on various parameters including size of key and block, diffusion, and confusion properties [5].
The current cipher design is still guided by the principles of confusion and diffusion. Confusion is designed to hide the relationship between the plaintext and ciphertext. This will discourage the attacker who attempts to locate the key using ISBN: 978-1-4673-5256-7/13/$31.00 ©2013 IEEE cipher text. On the other hand, diffusion is supposed to disseminate the plaintext statistics through the ciphertext in order to discourage the attacker attempting to locate the plaintext using the ciphertext statistics. If a cipher has a good diffusion property, then flipping one bit of the input changes every bit of the output with a probability close to 1⁄2 [6]- [11].
In this paper we present the results of the analysis on the BA in terms of avalanche effect and correlation coefficient. Applying avalanche effect analysis on the BA helps to identify that it satisfies Shannon’s diffusion property, while applying correlation coefficient statistical analysis on the BA is to identify that it satisfies Shannon’s confusion property.
This paper is organized as follows: section II describes BA; section III describes the security analysis that includes avalanche effect and correlation as well as providing an explanation of the data type that used in this analysis, and section IV provides Results of Analysis; finally, section V provides the conclusion and makes recommendations for future studies.
Data encryption commences with a 64-bit block element of plaintext morphing into a 64-bit ciphertext. First, the 64-bit segment is split into two equal segments that form the base of the BA. The next step is the implementation of the exclusive- or-operation (XOR) that is carried out between the first segment of the 32-bit block (L) and the first P-array. The 32-bit data obtained from step 2 is moved to the F function which permutes the data into a 32-bit block segment, which is XOR'ed with the second segment of the 32-bit block (R) of the 64-bit plaintext split. Upon completion of the XOR operation, the 32-bit segments, L and R, are exchanged for future iterations of the BA. Fig. I illustrates the architecture of the BA with 16 rounds. The input is an element of 64-bit data; X, which is divided into two 32-bit halves: XL and XR. Data Decryption is similar to Encryption data, but P1, P2... P18 are used in the reverse order.
Lior Degani, the Co-Founder and head of Marketing of Swayy, pinged me last week when I was in California to tell me about his startup and give me beta access. I heard his pitch and was skeptical. I was also tired, cranky and missing my kids – so my frame of mind wasn’t the most positive.
    Lior Degani, the Co-Founder and head of Marketing of Swayy, pinged me last week when I was in California to tell me about his startup and give me beta access. I heard his pitch and was skeptical. I was also tired, cranky and missing my kids – so my frame of mind wasn’t the most positive.
    I went into Swayy to check it out, and when it asked for access to my Twitter and permission to tweet from my account, all I could think was, “If this thing spams my Twitter account I am going to bitch-slap him all over the Internet.” Fortunately that thought stayed in my head, and not out of my mouth.
    One week later, I’m totally addicted to Swayy and glad I said nothing about the spam (it doesn’t send out spam tweets but I liked the line too much to not use it for this article). I pinged Lior on Facebook with a request for a beta access code for TNW readers. I also asked how soon can I write about it. It’s that good. Seriously. I use every content curation service online. It really is That Good.
    What is Swayy? It’s like Percolate and LinkedIn recommended articles, mixed with trending keywords for the topics you find interesting, combined with an analytics dashboard that shows the trends of what you do and how people react to it. I like it for the simplicity and accuracy of the content curation. Everything I’m actually interested in reading is in one place – I don’t have to skip from another major tech blog over to Harvard Business Review then hop over to another major tech or business blog. It’s all in there. And it has saved me So Much Time
    After I decided that I trusted the service, I added my Facebook and LinkedIn accounts. The content just got That Much Better. I can share from the service itself, but I generally prefer reading the actual post first – so I end up sharing it from the main link, using Swayy more as a service for discovery.
    I’m also finding myself checking out trending keywords more often (more often than never, which is how often I do it on Twitter.com).
    The analytics side isn’t as interesting for me right now, but that could be due to the fact that I’ve barely been online since I came back from the US last weekend. The graphs also haven’t given me any particularly special insights as I can’t see which post got the actual feedback on the graph side (however there are numbers on the Timeline side.) This is a Beta though, and new features are being added and improved daily. I’m sure this is on the list. As they say, if you aren’t launching with something you’re embarrassed by, you’ve waited too long to launch.
    It was the suggested content that impressed me the most. The articles really are spot on – which is why I pinged Lior again to ask a few questions:
    How do you choose the articles listed on the site? Is there an algorithm involved? And is there any IP?
    Yes, we’re in the process of filing a patent for it. But basically the system works with a Natural Language Processing Engine. Actually, there are several parts for the content matching, but besides analyzing what topics the articles are talking about, we have machine learning algorithms that match you to the relevant suggested stuff. For example, if you shared an article about Zuck that got a good reaction from your followers, we might offer you another one about Kevin Systrom (just a simple example).
    Who came up with the idea for Swayy, and why? And what’s your business model?
    Our business model is a subscription model for extra social accounts (extra Facebook / Twitter, etc) and team collaboration.
    The idea was born from our day-to-day need to be active on social media, look for the best content to share with our followers, grow them, and measure what content works best.
    Who is on the team?
    Ohad Frankfurt is the CEO, Shlomi Babluki is the CTO and Oz Katz does Product and Engineering, and I [Lior Degani] do Marketing. The four of us are the founders. Oz and I were in 8200 [an elite Israeli army unit] together. Emily Engelson does Community Management and Graphic Design.
    If you use Percolate or read LinkedIn’s recommended posts I think you’ll love Swayy.
    ➤ Want to try Swayy out without having to wait? Go to this secret URL and enter the promotion code thenextweb . The first 300 people to use the code will get access.
    Image credit: Thinkstock
    """

    # Create a SummaryTool object
    st = SummaryTool()

    # Build the sentences dictionary
    sentences_dic = st.get_senteces_ranks(content)

    # Build the summary with the sentences dictionary
    summary = st.get_summary(title, content, sentences_dic)

    # Print the summary
    print summary

    # Print the ratio between the summary length and the original length
    print ""
    print "Original Length %s" % (len(title) + len(content))
    print "Summary Length %s" % len(summary)
    print "Summary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(content)))))


if __name__ == '__main__':
    s=time.time()
    main()
    e = time.time()
    print e-s

