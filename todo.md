## Challenges faced ##

- Visiting links and scraping data 
- Since data was paginated it only got links of images from index.shtml 
- Found the pattern of pagination and asked chatgpt for list of urls 
- Found ascii images end with .txt
- Content structure was plain text representation of ASCII art, rather than structured HTML.
    - Given this format, tried a different approach to extract ASCII art data:
    1. Direct Parsing: Since the content is not HTML but plain text, you should directly process the text to extract ASCII art and any associated metadata.
    2. Regex Matching: Use regular expressions to identify and extract ASCII art patterns from the text.