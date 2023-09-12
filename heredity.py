import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage 
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}") 


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

# a helper function for calculating the probability for any parent: 
def probability_for_parent(parent_name, one_gene, two_genes):
    if parent_name in two_genes: 
        # if the parents have two genes: 
        prob_from_parent = 1 - PROBS["mutation"] 
    elif parent_name in one_gene:
        # if the parents have one gene:
        prob_from_parent = 0.5
    else: 
        # probability of child getting it if parents have no genes 
        prob_from_parent = PROBS["mutation"]
    return prob_from_parent 

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability. 

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait. 
    """

    # the accumulator for the probability for the person for each case: 
    prob = 1

    for person in people.keys(): 
        trait_exists = person in have_trait 
        if person in one_gene: 
            if people[person]["mother"] != None and people[person]["father"] != None: 
                # gets from mother and not father or gets from father and not mother 
                prob_from_mom = probability_for_parent(people[person]["mother"], one_gene, two_genes)
                # same procedure as the mother but with the father 
                prob_from_dad = probability_for_parent(people[person]["father"], one_gene, two_genes)
                # the probability of the person acquiring the gene if they have one gene: 
                prob_for_person = (prob_from_mom * (1-prob_from_dad)) + (prob_from_dad * (1-prob_from_mom)) 
            else: 
                # if parents unkown: 
                prob_for_person = PROBS["gene"][1] 
            # if the person has traits, the deciding on True or False 
            prob *= (prob_for_person * PROBS["trait"][1][trait_exists]) 

        # if the person has two genes: 
        elif person in two_genes: 
            # checking for if parents are known: 
            if people[person]["mother"] != None and people[person]["father"] != None: 
                # gets from mother and not father or gets from father and not mother 
                prob_from_mom = probability_for_parent(people[person]["mother"], one_gene, two_genes)
                # same procedure as the mother but with the father 
                prob_from_dad = probability_for_parent(people[person]["father"], one_gene, two_genes)
                # probability of person acquiring gene 
                prob_for_person = prob_from_mom * prob_from_dad
            # if no parents: 
            else: 
                prob_for_person = PROBS["gene"][2]  
            prob *= (prob_for_person * PROBS["trait"][2][trait_exists]) 
        # if person has zero genes: 
        else: 
            if people[person]["mother"] != None and people[person]["father"] != None: 
                # gets from mother and not father or gets from father and not mother 
                prob_from_mom = probability_for_parent(people[person]["mother"], one_gene, two_genes)
                # same procedure as the mother but with the father 
                prob_from_dad = probability_for_parent(people[person]["father"], one_gene, two_genes)
                prob_for_person = (1 - prob_from_mom )* (1 - prob_from_dad )
            else: 
                prob_for_person = PROBS["gene"][0] 
            prob *= (prob_for_person * PROBS["trait"][0][trait_exists]) 

    # return the final joint probability at the end: 
    return prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """ 
    for person in probabilities.keys():
        if person in one_gene:
            # adding p to the part of the dictionary with the appropriate number of genes for each case 
            probabilities[person]['gene'][1] += p
        elif person in two_genes: 
            probabilities[person]['gene'][2] += p 
        else: 
            probabilities[person]['gene'][0] += p 
        # adding p to the part of the dictionary depending on whether the person exhibits traits or not
        if person in have_trait: 
            probabilities[person]['trait'][True] += p 
        else: 
            probabilities[person]['trait'][False] += p 

def normalize(probabilities): 
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """ 
    for person in probabilities.keys(): 
        total = 0 # accumulator 
        # normalizing the probability distribution for genes by dividing the element by the total 
        for elem in probabilities[person]['gene'].keys(): 
            total += probabilities[person]['gene'][elem] # calculating the total 
        for elem in probabilities[person]['gene'].keys():
            probabilities[person]['gene'][elem] /= total # dividing the element by the total 
        
        total = 0 # accumulator 
        # normalizing the probability distrubution for traits by dividing the element by the total 
        for elem in probabilities[person]['trait'].keys():
            total += probabilities[person]['trait'][elem] # calculating the total 
        for elem in probabilities[person]['trait'].keys(): 
            probabilities[person]['trait'][elem] /= total # dividing the element by the total 

if __name__ == "__main__":
    main() 