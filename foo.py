import json
cache = []

def read_cache():
    """Read cache into memory"""
    global cache
    
    with open("cache.txt") as file:
        for line in file:
            node = json.loads(line)
            cache.append(node)


def check_cache(word):
    """Search cache for the word, return rhymes if in cache"""
    global cache
  
    for node in cache:
        if node["word"] == word:
            return node["rhymes"]
    return False


def add_to_cache(word, rhymes):
    """Store a node consisting of a word and its rhymes in the cache"""
    global cache

    node = {"word": word, "rhymes": rhymes}
    cache.append(node)


def write_cache():
    """Write cache back to file"""
    global cache

    with open("foo.txt", "w") as file:
        for node in cache:
            json.dump(node, file)
            file.write("\n")


def main():
    # print(cache)
    # read_cache()
    # print(cache)
    # print("done")
    # print(check_cache("ear"))
    # print(check_cache("orange"))
    # for _ in range(10):
    #     print("\n")
    # add_to_cache("foo", ["bar", "baz"])
    # print(cache)
    read_cache()
    write_cache()


main()