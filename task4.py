paragraph = input("Enter a paragraph: ")

words = paragraph.split()
unique_words = set(words)
longest_word = max(words, key=len)
shortest_word = min(words, key=len)

print("\n Words in the paragraph:")
print(words)
print("\n Total number of words:", len(words))
print("Number of unique words:",unique_words)

print("Longest word:", longest_word)

print("Shortest word:", shortest_word)
duplicate_words = []
for word in unique_words:
    if words.count(word) > 1:
        duplicate_words.append(word)
print("Words more than once:", duplicate_words)
alphabetical_words = sorted(words)
print("Words in alphabetical order:",alphabetical_words)
