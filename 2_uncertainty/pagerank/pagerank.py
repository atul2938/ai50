import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Holds probability of each state given current state
    probabilityDistribution = dict()
    # Holds all possible states
    domain = corpus.keys() 
    # Domain range for current state (links from the active webpage)
    domain_range = corpus.get(page) # page = current state
    
    for state in domain:
        if domain_range == None:
            probability = 1/len(domain)
            probabilityDistribution[state] = round(probability, 4)
        else:
            if state not in domain_range:
                probability = (1.00 - damping_factor)/len(domain)
                probabilityDistribution[state] = round(probability, 4)
            else:
                probability = damping_factor/len(domain_range) + (1.00 - damping_factor)/len(domain)
                probabilityDistribution[state] = round(probability, 4)
        # print("Probability for " + state + " = " + str(float(probabilityDistribution.get(state)*100)) + "%.")
    
    return probabilityDistribution
        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    random.seed()

    for page in corpus:
        pagerank[page] = 0

    sample = random.choices(list(corpus.keys()), k=1)[0] # random.choices(population, weights, k) = list()
    
    for i in range(n):
        model = transition_model(corpus, sample, damping_factor)
        pagerank[sample] += 1
        population, weights = zip(*model.items()) # zip(*model.items()) = zip(model.keys(), model.values())
        sample = random.choices(population, weights=weights, k=1)[0]

    for page in corpus:
        pagerank[page] /= n
    
    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    newrank = dict()

    # Init equal page rank
    for page in corpus:
        pagerank[page] = 1/len(corpus)
    
    repeat = True

    while repeat:
        
        for page in pagerank:
            total = float(0)

            for i in corpus:
                if page in corpus[i]:
                    total += pagerank[i]/len(corpus[i])
                if not corpus[i]:
                    total += pagerank[i] / len(corpus)

            # pagerank[page] =  (1-damping_factor)/len(corpus) + (damping_factor * total)
            newrank[page] = (1 - damping_factor) / len(corpus) + damping_factor * total

        repeat = False

        # If any of the values changes by more than the threshold, repeat process
        for page in pagerank:
            if not math.isclose(newrank[page], pagerank[page], abs_tol=0.001):
                repeat = True
            # Assign new values to current values
            pagerank[page] = newrank[page]

    return pagerank



if __name__ == "__main__":
    main()
