# Search Engine Python Program

## Data Structures Used

### Trie
- Each HTML file has its own trie that stores all the words from the file in the form of nodes. Each node has:
  - `is_end`: A boolean indicating whether the letter (node) is the end of a word. If it is, the value is `True`.
  - `children = {}`: A dictionary where the key is a character and the value is a node.
  - `counter`: A counter that counts the occurrences of each word within the file.
  - `index_list`: A list with the indices of the occurrences of the word within the file.

### Directed Graph
- When the parser parses an HTML file, the list of links it returns is stored in the graph. It consists of nodes and edges:
  - `node`: Each HTML file in the directory is a node.
  - `edge`: An edge is a connection between two nodes. If HTML file A links to HTML file B, they are connected by an edge where A is the source and B is the destination.

### Dictionary

## Merge Sort
Merge sort works on the principle of 'divide and conquer'. It recursively splits the list in half until it reaches the base case, where only one element remains. After that, it merges the split lists and sorts them while merging. It is used to sort files after a user performs a search.

## Ranking
Results are ranked using the formula:
`eval = round(3 * word_count + 0.03 * word_count_in_linking_file + 0.2 * link_count)`

Some HTML files, for example, in the footer, will be linked by all HTML files and will always have a high rank. To prevent these from always appearing at the top of the search results, the word count has a much higher coefficient than the number of links or the word count within the files that link to it. This way, the user will see files with a lot of searched words at the top of the list, as well as files linked by other files.

## Additional Features

### Phrase Search
It is used in the following way:
`"some phrase"`
After this input, the program will go through all the files in the directory and calculate the rank only if all the words enclosed in quotes appear consecutively. A different ranking formula is used for phrase searches:
`eval = round(10 * word_count + 0.05 * word_count_in_linking_file + 0.3 * link_count)`

The word count in this ranking has a much higher coefficient than other factors because it is much rarer for many files to have that exact combination of words.

## Usage

Upon starting the program, the user inputs a directory. After the input, the main menu opens where the user can choose to change the directory, search for a word, or close the program.

## Loading the Directory

The user’s input is validated, and if everything is correct, the program goes through all subfolders and files within the given directory. If the file is .html, it parses it, creates a list of edges to later construct the graph, and fills the trie data structure with letters from one HTML file. Each HTML file has its own trie while the graph is created only for the directory entered by the user (root dir). After all the files are loaded, the main menu opens.



